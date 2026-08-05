from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_seller
from app.db_depends import get_async_db
from app.schemas import Product as ProductSchema, DeleteResponseSchema, ProductList
from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.models.users import User as UserModel
from app.models.reviews import Review as ReviewModel
from app.schemas import ProductCreate
from app.schemas import Review as ReviewSchema
from sqlalchemy import select, update, func

# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=ProductList, status_code=status.HTTP_200_OK)
async def get_all_products(
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        category_id: int | None = Query(
            None, description="ID категории для фильтрации"),
        min_price: float | None = Query(
            None, ge=0, description="Минимальная цена товара"),
        max_price: float | None = Query(
            None, ge=0, description="Максимальная цена товара"),
        in_stock: bool | None = Query(
            None, description="true — только товары в наличии, false — только без остатка"),
        seller_id: int | None = Query(
            None, description="ID продавца для фильтрации"),
        created_after: datetime | None = Query(
            None, description="Товары, созданные после этой даты (ISO 8601)"),
        created_before: datetime | None = Query(
            None, description="Товары, созданные до этой даты (ISO 8601)"),
        updated_after: datetime | None = Query(
            None, description="Товары, обновлённые после этой даты (ISO 8601)"),
        updated_before: datetime | None = Query(
            None, description="Товары, обновлённые до этой даты (ISO 8601)"),
        sort_by: str = Query(
            "id", pattern="^(id|created_at|price|rating)$",
            description="Поле для сортировки: id, created_at, price, rating"),
        order: str = Query(
            "asc", pattern="^(asc|desc)$",
            description="Направление: asc (возрастание) или desc (убывание)"),
        db: AsyncSession = Depends(get_async_db)):
        """
        Возвращает список всех активных товаров с поддержкой фильтров и сортировки.
        """
        # Проверка логики min_price <= max_price
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_price не может быть больше max_price",
            )
        # Формируем список фильтров
        filters = [ProductModel.is_active == True]

        if category_id is not None:
            filters.append(ProductModel.category_id == category_id)
        if min_price is not None:
            filters.append(ProductModel.price >= min_price)
        if max_price is not None:
            filters.append(ProductModel.price <= max_price)
        if in_stock is not None:
            filters.append(ProductModel.stock > 0 if in_stock else ProductModel.stock == 0)
        if seller_id is not None:
            filters.append(ProductModel.seller_id == seller_id)
        if created_after is not None:
            filters.append(ProductModel.created_at >= created_after)
        if created_before is not None:
            filters.append(ProductModel.created_at <= created_before)
        if updated_after is not None:
            filters.append(ProductModel.updated_at >= updated_after)
        if updated_before is not None:
            filters.append(ProductModel.updated_at <= updated_before)

        # Сортировка
        sort_column = getattr(ProductModel, sort_by)
        if order == "desc":
            sort_column = sort_column.desc()

        total_stmt = select(func.count()).select_from(ProductModel).where(*filters)
        total = await db.scalar(total_stmt) or 0

        stmt = (
            select(ProductModel)
            .where(*filters)
            .order_by(sort_column)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = (await db.scalars(stmt)).all()
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_seller)):
    """
    Создаёт новый товар, привязанный к текущему продавцу (только для 'seller').
    """
    # Проверяем, существует ли активная категория
    stmt_category = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                    CategoryModel.is_active == True)

    category = (await db.scalars(stmt_category)).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category not found or inactive")

    # Создаём товар
    db_product = ProductModel(**product.model_dump(), seller_id=current_user.id)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.get("/category/{category_id}", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == category_id,
        CategoryModel.is_active == True)
    category = (await db.scalars(category_stmt)).first()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    stmt = select(ProductModel).where(
        ProductModel.category_id == category_id,
        ProductModel.is_active == True
    )
    products = (await db.scalars(stmt)).all()
    return products



@router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    # Сначала ищем продукт без проверки is_active
    stmt_product = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    product = (await db.scalars(stmt_product)).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Проверяем, существует ли активная категория
    stmt_category = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                    CategoryModel.is_active == True)
    category = (await db.scalars(stmt_category)).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found or inactive")
    return product


@router.put("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_seller)):
    """
    Обновляет товар по его ID. Если он принадлежит текущему продавцу (только для 'seller')
    """
    # Проверяем товар
    stmt_product = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    db_product = (await db.scalars(stmt_product)).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")
    if db_product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")

    # Проверяем категорию (category_id обязателен в схеме, поэтому проверка всегда нужна)
    stmt_category = select(CategoryModel).where(CategoryModel.id == product.category_id, CategoryModel.is_active == True)
    category = (await db.scalars(stmt_category)).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or inactive")

    # Обновляем
    update_data = product.model_dump()
    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(**update_data)
    )
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", response_model=DeleteResponseSchema, status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_seller)):
    """
    Удаляет товар по его ID, если он принадлежит текущему продавцу (только для 'seller').
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    product = (await db.scalars(stmt)).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own products")
    await db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(is_active=False))
    await db.commit()
    return DeleteResponseSchema(
        status="success",
        message="Product marked as inactive"
    )


@router.get("/{product_id}/reviews/", response_model=list[ReviewSchema])
async def get_product_reviews(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список активных отзывов для указанного товара.
    """
    product = (await db.scalars(
        select(ProductModel).where(
            ProductModel.id == product_id,
            ProductModel.is_active == True
        )
    )).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    stmt = select(ReviewModel).where(
        ReviewModel.product_id == product_id,
        ReviewModel.is_active == True
    )
    reviews = (await db.scalars(stmt)).all()
    return reviews

