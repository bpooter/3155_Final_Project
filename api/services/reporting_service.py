from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.orders import Order
from ..models.reviews import Review


def get_daily_revenue(db: Session, report_date: date):
    revenue = (
        db.query(func.sum(Order.total_price))
        .filter(
            func.date(Order.order_date) == report_date
        )
        .scalar()
    )

    return revenue

def get_orders_by_date_range(db, start_date, end_date):

    return (
        db.query(Order)
        .filter(
            Order.order_date >= start_date,
            Order.order_date <= end_date
        )
        .all()
    )

def get_low_rated_reviews(db):

    return (
        db.query(Review).filter(Review.rating <= 2).all()
    )

def get_high_rated_reviews(db):
    return (
        db.query(Review).filter(Review.rating >= 4).all()
    )

def get_restaurant_average_rating(db):
    average_rating = (
        db.query(func.avg(Review.rating)).scalar()
    )

    if average_rating is None:
        return 0
    return round(float(average_rating),2)


