from datetime import date

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..services import reporting_service
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/revenue/{report_date}")
def daily_revenue(report_date:date, db:Session = Depends(get_db)):
    return reporting_service.get_daily_revenue(db, report_date)

@router.get("/orders/{start_date}/{end_date}")
def get_orders_by_date_range(start_date: date, end_date: date, db:Session = Depends(get_db)):
    return reporting_service.get_orders_by_date_range(db, start_date, end_date)

@router.get("/low_ratings")
def get_low_ratings(db:Session = Depends(get_db)):
    return reporting_service.get_low_rated_reviews(db)

@router.get("/high_ratings")
def get_high_ratings(db:Session = Depends(get_db)):
    return reporting_service.get_high_rated_reviews(db)

@router.get("/average_ratings")
def get_average_ratings(db:Session = Depends(get_db)):
    return reporting_service.get_restaurant_average_rating(db)