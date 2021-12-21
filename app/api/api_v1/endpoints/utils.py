from typing import Any
import pandas as pd
import datetime as dt
import calendar
import os
import sys
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.utils import (
    convert_date_to_utc_with_hours,
    convert_date_from_utc,
    Montel_Reader,
    Spot,
)
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


# @router.get("/schedule", response_model=schemas.Msg, status_code=201)
# def unique_itn_schedule(
#     startDate: str,
#     endDate: str,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Get unique itn from schedule for period in UTC
#     """
#     crud.schedule.get_unique_itn_schedule_for_period_utc(email_to=email_to)
#     return {"msg": "Test email sent"}


@router.get("/stp/{code}")
def excel(
    code: str,
    start_date: str = "01/12/2021",
    end_date: str = "31/12/2021",
    # type: str = 'raw',
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # path = os.path.join(os.path.join(
    #                 app.root_path, app.config[curr_path]), file.filename)
    try:
        start_date_obj = dt.datetime.strptime(start_date, "%d/%m/%Y")
        end_date_obj = dt.datetime.strptime(end_date, "%d/%m/%Y")
        end_date_obj = end_date_obj.replace(hour=23)

        start_date_utc = convert_date_to_utc_with_hours("Europe/Sofia", start_date_obj)
        end_date_utc = convert_date_to_utc_with_hours("Europe/Sofia", end_date_obj)
        # print("🚀 ~ file: utils.py ~ line 60 ~ end_date_utc", end_date_utc)

        stp_codes = settings.STP_CODES
        df = pd.read_excel(
            os.path.join(os.getcwd(), "stp2021_parts.xlsx"),
            sheet_name=code.split("_")[0],
            index_col=0,
        )
        # print(df)

        raw_df = df[
            (df["code"] == code)
            & (df.index >= start_date_utc)
            & (df.index <= end_date_utc)
        ]
        # print("🚀 ~ file: utils.py ~ line 84 ~ raw_df", raw_df)

        raw_df.reset_index(inplace=True)

        raw_df = raw_df[["utc", "value"]]
        raw_df["eet"] = raw_df["utc"].apply(
            lambda x: str(convert_date_from_utc("EET", x, False))
        )
        raw_df["utc"] = raw_df["utc"].astype(str, copy=False)

        if raw_df.empty:
            raise HTTPException(
                status_code=404,
                detail="Wrong STP code or missing data!",
            )

        # Montly
        month_start_date = start_date_obj.replace(day=1)
        month_end_date = start_date_obj.replace(
            day=calendar.monthrange(
                start_date_obj.year, month=int(start_date_obj.month)
            )[1]
        )
        month_start_date_utc = convert_date_to_utc_with_hours(
            "Europe/Sofia", month_start_date
        )
        month_end_date_utc = convert_date_to_utc_with_hours(
            "Europe/Sofia", month_end_date
        )
        monthly_df = df[
            (df["code"] == code)
            & (df.index >= month_start_date_utc)
            & (df.index <= month_end_date_utc)
        ]
        monthly_df.reset_index(inplace=True)

        monthly_df = monthly_df[["utc", "value"]]
        monthly_df["eet"] = monthly_df["utc"].apply(
            lambda x: convert_date_from_utc("EET", x, False)
        )
        monthly_df["utc"] = monthly_df["utc"].astype(str, copy=False)
        monthly_df["week_day"] = monthly_df["eet"].dt.dayofweek

        monthly_df["is_work"] = monthly_df["week_day"].apply(lambda x: x < 5)
        monthly_df["hour"] = monthly_df["eet"].dt.hour + 1
        work_df = monthly_df[monthly_df["is_work"]].groupby(["hour"]).mean()
        work_df.reset_index(inplace=True)
        work_df = work_df[["hour", "value"]]

        weekend_df = monthly_df[~monthly_df["is_work"]].groupby(["hour"]).mean()
        weekend_df.reset_index(inplace=True)
        weekend_df = weekend_df[["hour", "value"]]
        # print(f'work DF\n', work_df)
        # print(f'weekend DF\n', weekend_df)

    except:
        raise HTTPException(
            status_code=404,
            detail="Wrong query params.",
        )
    return [
        {code: raw_df.to_json(orient="index")},
        {
            f"{calendar.month_name[start_date_obj.month]}-{start_date_obj.year}": work_df.to_json(
                orient="index"
            )
        },
        {
            f"{calendar.month_name[start_date_obj.month]}-{start_date_obj.year}-WeekEnd": weekend_df.to_json(
                orient="index"
            )
        },
    ]

    # data_to_return = [{code: raw_df}, {
    #     calendar.month_name[start_date_obj.month]: work_df}]
    # json_result = json.dumps(data_to_return)
    # print("🚀 ~ file: utils.py ~ line 132 ~ json_result", json_result)
    # return {code: data_to_return.to_json(orient='index')}


@router.get("/spots")
def spots(
    # code: str,
    start_date: str = "01/12/2021",
    end_date: str = "31/12/2021",
    # type: str = 'raw',
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    try:
        print(f"from eeeeenv ---> {settings.EQ_API_KEY}")
        reader = Montel_Reader()
        #
        scraper = Spot(reader, start_date, end_date)
        data_df = scraper.get_data()
        data_df["eet"] = data_df["utc"].apply(
            lambda x: str(convert_date_from_utc("EET", x, False))
        )
        print("🚀 ~ file: utils.py ~ line 162 ~ data_df", data_df)
        return [{"data": data_df.to_json(orient="index")}]
        # scraper.update_db(data)

    except Exception as e:
        print("🚀 ~ file: utils.py ~ line 165 ~ e", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb.tb_lineno)
        raise HTTPException(status_code=500, detail="Server error !Spots not loaded !")
