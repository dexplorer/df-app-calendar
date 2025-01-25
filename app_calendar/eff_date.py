# from utils import file_io as uff
from metadata import dataset as ds
from metadata import holiday as hd
from metadata import schedule as sh
from functools import lru_cache
from datetime import datetime
from dateutil import rrule

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
    print(src_file_records)
    print(len(src_file_records))
    try:
        if src_file_records and len(src_file_records) == 1:
            cycle_date = src_file_records[0]["cycle_date"]
            print(cycle_date)
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


def generate_run_calendar(
    schedule: sh.Schedule, calendar_start_date: str, calendar_end_date: str
):
    """
    Generate run calendar for the schedule.
    """

    # Simulate getting the holiday metadata from API
    logging.info("Get holiday metadata")
    # holiday = hd.Holiday.from_json(holiday_date=cycle_date)
    holidays = hd.get_all_holidays_from_json()

    run_calendar = []
    for dt in rrule.rrule(
        rrule.DAILY,
        dtstart=datetime.strptime(calendar_start_date, "%Y-%m-%d"),
        until=datetime.strptime(calendar_end_date, "%Y-%m-%d"),
    ):
        if dt.strftime("%d") == "01":
            print(f"Working on date {dt}")

        if not check_if_cycle_date_is_holiday(
            cycle_date=dt.strftime("%Y-%m-%d"), schedule=schedule, holidays=holidays
        ):
            rc_item = {
                "schedule_id": schedule.schedule_id,
                "calendar_date": dt.strftime("%Y-%m-%d"),
            }
            run_calendar.append(rc_item)

    return run_calendar


def get_eff_date_from_run_calendar(cycle_date: str, run_calendar: list, offset: int):
    eff_date = None
    for idx, rc_item in enumerate(run_calendar):
        if rc_item["calendar_date"] == cycle_date:
            eff_rc_item = run_calendar[idx + offset]
            eff_date = eff_rc_item["calendar_date"]

    try:
        if not eff_date:
            raise ValueError(
                "Cycle date is not found in the run calendar (i.e. holiday)"
            )
        elif not check_if_valid_date(given_date=eff_date, date_format="%Y-%m-%d"):
            raise ValueError(
                "Effective date is either invalid or not in the expected YYYY-MM-DD format."
            )
        else:
            return eff_date
    except ValueError as error:
        logging.error(error)
        raise


def check_if_valid_date(given_date: str, date_format: str):
    try:
        if given_date and isinstance(datetime.strptime(given_date, date_format), datetime):
            return True
    except ValueError as error:
        return False

def get_cur_eff_date(schedule_id: str) -> str:
    # Simulate getting the cycle date from API
    # Run this from the parent app
    cycle_date = get_cur_cycle_date()

    # Simulate getting the schedule metadata from API
    logging.info("Get schedule metadata")
    schedule = sh.Schedule.from_json(schedule_id)

    try:
        calendar_start_date = "2024-01-01"
        calendar_end_date = "2024-12-31"
        run_calendar = generate_run_calendar(
            schedule=schedule,
            calendar_start_date=calendar_start_date,
            calendar_end_date=calendar_end_date,
        )
        eff_date = get_eff_date_from_run_calendar(
            cycle_date=cycle_date,
            run_calendar=run_calendar,
            offset=schedule.run_calendar_offset,
        )
        return eff_date
        # return datetime.strptime("2024-12-26", "%Y-%m-%d")
    except ValueError as error:
        logging.error(error)
        raise


def get_prior_eff_date(cur_eff_date: str, snapshot: str) -> datetime.date:
    logging.debug("prior snapshot - %s", snapshot)

    if cur_eff_date == "2024-12-26":
        if snapshot == "t-1d":
            prior_eff_date = "2024-12-25"
        elif snapshot == "lme":
            prior_eff_date = "2024-11-30"
        else:
            prior_eff_date = "2024-12-25"
        return prior_eff_date
    else:
        return cur_eff_date


def fmt_date_as_yyyymmdd(in_date: datetime.date) -> str:
    return datetime.strftime(in_date, "%Y%m%d")


def fmt_date_str_as_yyyymmdd(in_date_yyyy_mm_dd: str) -> str:
    return in_date_yyyy_mm_dd.replace("_", "").replace("-", "")


def get_prior_eff_dates(schedule_id: str, snapshots: list[ds.DataSnapshot]):
    cur_eff_date = get_cur_eff_date(schedule_id=schedule_id)
    prior_eff_dates = [
        get_prior_eff_date(cur_eff_date, snapshot.snapshot) for snapshot in snapshots
    ]
    logging.debug("Prior effective dates - %s", prior_eff_dates)
    return prior_eff_dates
