# from utils import file_io as uff
from metadata import dataset as ds
from metadata import holiday as hd
from metadata import schedule as sh
from functools import lru_cache
from datetime import datetime, timedelta
from dateutil import rrule
import pandas as pd

import logging


# For testing, keep the cache size as 1.
# In production, the cycle date will change daily and so the cache should be expired.
@lru_cache(maxsize=1)
def get_cur_cycle_date() -> str:
    """
    Get the current cycle date.
    """

    # Simulate getting the cycle date from API
    # src_file_path = f"{sc.src_file_path}/cycle_date.csv"
    # logging.debug("Reading the cycle date file {src_file_path}")
    # src_file_records = uff.uf_read_delim_file_to_list_of_dict(file_path=src_file_path)
    src_file_records = [{"cycle_date": "2024-12-26"}]
    try:
        if src_file_records and len(src_file_records) == 1:
            cycle_date = src_file_records[0]["cycle_date"]
            logging.info("Cycle date: %s", cycle_date)
            if check_if_valid_date(given_date=cycle_date, date_format="%Y-%m-%d"):
                return cycle_date
        else:
            raise ValueError(
                "One and only one cycle date in the format YYYY-MM-DD is expected."
            )
    except ValueError as error:
        logging.error(error)
        raise


def check_if_cycle_date_is_holiday(
    cycle_date: str, schedule: sh.Schedule, holidays: list[hd.Holiday]
) -> bool:
    """
    Check if the given date is a holiday for the schedule.
    """

    holiday_flag = False
    for holiday in holidays:
        if isinstance(holiday, hd.Holiday) and holiday.holiday_date == cycle_date:
            for hd_group in holiday.holiday_groups:
                for sh_hd_group in schedule.holiday_groups:
                    if hd_group == sh_hd_group:
                        holiday_flag = True
                        return holiday_flag

    return holiday_flag


@lru_cache(maxsize=128)
def generate_run_calendar(
    schedule_id: str,
    calendar_start_date: str = "2024-11-28",
    calendar_end_date: str = "2024-12-31",
) -> pd.DataFrame:
    """
    Generate run calendar for the schedule.
    """

    # Simulate getting the schedule metadata from API
    logging.info("Get schedule metadata")
    schedule = sh.Schedule.from_json(schedule_id)

    # Simulate getting the holiday metadata from API
    logging.info("Get holiday metadata")
    # holiday = hd.Holiday.from_json(holiday_date=cycle_date)
    holidays = hd.get_all_holidays_from_json() + hd.get_weekend_holidays(
        start_date=calendar_start_date, end_date=calendar_end_date
    )

    run_calendar = []
    date_format = "%Y-%m-%d"
    for dt in rrule.rrule(
        rrule.DAILY,
        dtstart=datetime.strptime(calendar_start_date, date_format),
        until=datetime.strptime(calendar_end_date, date_format),
    ):

        if not check_if_cycle_date_is_holiday(
            cycle_date=dt.strftime(date_format), schedule=schedule, holidays=holidays
        ):
            rc_item = {
                "schedule_id": schedule.schedule_id,
                "calendar_date": dt.strftime(date_format),
            }
            run_calendar.append(rc_item)

    # Prepare the dataframe
    df_run_calendar = (
        pd.DataFrame.from_records(run_calendar)
        # Sort by calendar_date to ensure order
        .sort_values(by="calendar_date", ascending=True)
        # Set calendar_date as index
        .set_index("calendar_date")
    )

    return df_run_calendar


def get_eff_date_from_run_calendar(
    cycle_date: str, df_run_calendar: pd.DataFrame, offset: int
):

    eff_date = None

    try:
        if cycle_date not in df_run_calendar.index:
            raise ValueError("Cycle date is not found in the run calendar.")
        elif not isinstance(offset, int):
            raise ValueError("Run calendar offset is invalid.")
        else:
            # get_loc returns ordinal index (i.e location) of the index label (cycle_date)
            # derive the effective date index using offset
            eff_date_idx = df_run_calendar.index.get_loc(cycle_date) + offset
            # get the effective date using the derived index
            # iloc returns the df item based on ordinal index (i.e. location)
            # name returns index label (which is cycle_date as the df is indexed by cycle_date)
            eff_date = df_run_calendar.iloc[eff_date_idx].name
            logging.info("Cycle date: %s, Effective date: %s", cycle_date, eff_date)

            if check_if_valid_date(given_date=eff_date, date_format="%Y-%m-%d"):
                return eff_date
            else:
                raise ValueError(
                    "Effective date is either invalid or not in the expected YYYY-MM-DD format."
                )

    except ValueError as error:
        logging.error(error)
        raise


def check_if_valid_date(given_date: str, date_format: str):
    try:
        if given_date and isinstance(
            datetime.strptime(given_date, date_format), datetime
        ):
            return True
        else:
            raise ValueError("Given date is invalid.")
    except ValueError as error:
        logging.info(error)
        # It is intentional to not raise an exception as it is an utility function.
        return False


def get_cur_eff_date(schedule_id: str) -> str:
    # Simulate getting the cycle date from API
    # Run this from the parent app
    cycle_date = get_cur_cycle_date()

    df_run_calendar = generate_run_calendar(schedule_id=schedule_id)

    # Simulate getting the schedule metadata from API
    logging.info("Get schedule metadata")
    schedule = sh.Schedule.from_json(schedule_id)
    offset = schedule.run_calendar_offset

    eff_date = get_eff_date_from_run_calendar(
        cycle_date=cycle_date,
        df_run_calendar=df_run_calendar,
        offset=offset,
    )
    logging.info("Current effective date: %s", eff_date)
    return eff_date


def get_prior_eff_dates(
    schedule_id: str, snapshots: list[ds.DataSnapshot]
) -> list[str]:
    cycle_date = get_cur_cycle_date()

    df_run_calendar = generate_run_calendar(schedule_id=schedule_id)

    # Simulate getting the schedule metadata from API
    logging.info("Get schedule metadata")
    schedule = sh.Schedule.from_json(schedule_id)
    offset = schedule.run_calendar_offset

    prior_eff_dates = [
        get_prior_eff_date(cycle_date, snapshot.snapshot, df_run_calendar, offset)
        for snapshot in snapshots
    ]
    logging.info("Prior effective dates: %s", prior_eff_dates)
    return prior_eff_dates


def get_prior_eff_date(
    cycle_date: str, snapshot: str, df_run_calendar: pd.DataFrame, offset: int
) -> str:
    logging.debug("Prior snapshot: %s", snapshot)

    if snapshot == "t-1d":
        # df is sorted on the cycle date and so grab the last but one row's index name (cycle date).
        # Slice the dataframe till the cycle date.
        # iloc[-2] gets the last but one row.
        tm1d_cycle_date = df_run_calendar.loc[:cycle_date].iloc[-2].name
        prior_cycle_date = tm1d_cycle_date

    elif snapshot == "lme":
        # Derive the first and last dates of the previous month
        date_format = "%Y-%m-%d"
        cycle_datetime_obj = datetime.strptime(cycle_date, date_format)
        first_day_of_this_month = cycle_datetime_obj.replace(day=1)
        last_day_of_prev_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)
        last_day_of_prev_month_str = last_day_of_prev_month.strftime(date_format)
        first_day_of_prev_month_str = first_day_of_prev_month.strftime(date_format)
        # Select rows for previous month
        df_run_calendar_prev_month = df_run_calendar[
            first_day_of_prev_month_str:last_day_of_prev_month_str
        ]

        lme_cycle_date = df_run_calendar_prev_month.iloc[-1].name
        prior_cycle_date = lme_cycle_date

    else:
        prior_cycle_date = cycle_date

    prior_eff_date = get_eff_date_from_run_calendar(
        prior_cycle_date, df_run_calendar, offset
    )
    return prior_eff_date


def fmt_date_as_yyyymmdd(in_date: datetime.date) -> str:
    return datetime.strftime(in_date, "%Y%m%d")


def fmt_date_str_as_yyyymmdd(in_date_yyyy_mm_dd: str) -> str:
    return in_date_yyyy_mm_dd.replace("_", "").replace("-", "")
