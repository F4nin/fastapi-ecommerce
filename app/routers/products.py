from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.db_depends import get_db
from app.schemas import Product as ProductSchema
from app.models.products import Product as ProductModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.models.categories import Category as CategoryModel
from app.schemas import ProductCreate
from sqlalchemy.orm import Session
from sqlalchemy import select, update



# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products(db: Session = Depends(get_db)):
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    products = db.scalars(stmt).all()
    return products


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Создаёт новый товар.
    """
    # Проверяем, существует ли активная категория
    category = db.scalars(
        select(CategoryModel).where(CategoryModel.id == product.category_id,
                                    CategoryModel.is_active == True)
    ).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category not found or inactive")

    # Создаём товар
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/category/{category_id}", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == category_id,
        CategoryModel.is_active == True)
    category = db.scalars(category_stmt).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    stmt = select(ProductModel).where(
        ProductModel.category_id == category_id,
        ProductModel.is_active == True
    )
    products = db.scalars(stmt).all()
    return products



@router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    # Сначала ищем продукт без проверки is_active
    stmt_product = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    product = db.scalars(stmt_product).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Проверяем, существует ли активная категория
    stmt_category = select(CategoryModel).where(CategoryModel.id == product.category_id,
                                    CategoryModel.is_active == True)
    category = db.scalars(stmt_category).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found or inactive")

    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """
    Обновляет товар по его ID.
    """
    # Проверяем товар
    db_product = db.scalars(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    ).first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Проверяем категорию (category_id обязателен в схеме, поэтому проверка всегда нужна)
    category = db.scalars(
        select(CategoryModel).where(
            CategoryModel.id == product.category_id,
            CategoryModel.is_active == True
        )
    ).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or inactive")

    # Обновляем
    db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(**product.model_dump())
    )
    db.commit()
    db.refresh(db_product)
    return db_product




@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удаляет товар по его ID.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    product = db.scalars(stmt).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.execute(update(ProductModel).where(ProductModel.id == product_id).values(is_active=False))
    db.commit()
    return {"status": "success", "message": "Product marked as inactive"}

