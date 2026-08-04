from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_buyer, get_current_user
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.db_depends import get_async_db
from app.models.reviews import Review as ReviewModel
from app.schemas import ReviewCreate, Review as ReviewSchema
from sqlalchemy import select, update, func


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.
    """
    stmt = select(ReviewModel).where(ReviewModel.is_active == True)
    reviews = (await db.scalars(stmt)).all()
    return reviews


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_buyer)):
    """
    Создаёт новый отзыв. Только для пользователей с ролью 'buyer'.
    После создания пересчитывает средний рейтинг товара.
    """
    # Проверяем, что товар существует и активен
    product = (await db.scalars(
        select(ProductModel).where(
            ProductModel.id == review.product_id,
            ProductModel.is_active == True
        )
    )).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found or inactive"
        )

    # Создаём отзыв
    db_review = ReviewModel(
        user_id=current_user.id,
        product_id=review.product_id,
        comment=review.comment,
        grade=review.grade,
    )
    db.add(db_review)
    await db.flush()

    # Пересчитываем средний рейтинг товара
    avg_rating = (await db.scalars(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == review.product_id,
            ReviewModel.is_active == True
        )
    )).first()

    await db.execute(
        update(ProductModel)
        .where(ProductModel.id == review.product_id)
        .values(rating=float(avg_rating) if avg_rating is not None else 0.0)
    )

    await db.commit()
    await db.refresh(db_review)
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Мягкое удаление отзыва. Доступ: автор отзыва или пользователь с ролью 'admin'.
    После удаления пересчитывает средний рейтинг товара.
    """
    # Ищем активный отзыв
    review = (await db.scalars(
        select(ReviewModel).where(
            ReviewModel.id == review_id,
            ReviewModel.is_active == True
        )
    )).first()

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or already inactive"
        )

    # Проверяем права: автор отзыва или admin
    if current_user.id != review.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the author or admin can delete this review"
        )

    # Мягкое удаление
    await db.execute(
        update(ReviewModel)
        .where(ReviewModel.id == review_id)
        .values(is_active=False)
    )

    # Пересчитываем средний рейтинг товара
    avg_rating = (await db.scalars(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == review.product_id,
            ReviewModel.is_active == True
        )
    )).first()

    await db.execute(
        update(ProductModel)
        .where(ProductModel.id == review.product_id)
        .values(rating=float(avg_rating) if avg_rating is not None else 0.0)
    )

    await db.commit()
    return {"message": "Review deleted"}

