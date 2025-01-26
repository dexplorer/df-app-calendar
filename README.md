[![app_calendar CI pipeline with Github Actions](https://github.com/dexplorer/df-app-calendar/actions/workflows/ci.yml/badge.svg)](https://github.com/dexplorer/df-app-calendar/actions/workflows/ci.yml)

# df-app-calendar

This package implements the application calendar. It generates the application run calendar based on the schedule and holiday metadata. Cycle date is used as a reference date to calculate the effective (as of) date for the data pipelines. Multiple schedules (daily, monthly, etc) can be configured. Date offsets can be configured if the effective date is different from the cycle date.

### Install

- **Install via setuptools**:
  ```sh
    python setup.py install
  ```

### Sample Metadata

#### Schedules
```
{
    "schedules": [
      {
        "schedule_id": "1",
        "application_id": "1",
        "schedule_desc": "Monday to Friday excluding NYSE holidays",
        "schedule_frequency": "daily",
        "run_calendar_offset": 0, 
        "holiday_groups": [
            "NYSE", 
            "Weekend" 
        ]
      },
      {
        "schedule_id": "2",
        "application_id": "1",
        "schedule_desc": "Monday to Friday excluding Federal Bank holidays",
        "schedule_frequency": "daily",
        "run_calendar_offset": 0, 
        "holiday_groups": [
            "Federal Bank",
            "Weekend"
        ]
      },
      {
        "schedule_id": "3",
        "application_id": "1",
        "schedule_desc": "Calendar Month End",
        "schedule_frequency": "monthly",
        "run_calendar_offset": 0, 
        "holiday_groups": [
        ]
      },
      {
        "schedule_id": "4",
        "application_id": "1",
        "schedule_desc": "Business Month End excluding NYSE holidays and weekdns",
        "schedule_frequency": "monthly",
        "run_calendar_offset": 0, 
        "holiday_groups": [
            "NYSE", 
            "Weekend" 
        ]
      }
    ]
  }
  
  ```

#### Holidays
```
{
  "holidays": [
    {
      "holiday_date": "2024-01-01",
      "holiday_desc": "New Year's Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-01-15",
      "holiday_desc": "Martin Luther King, Jr. Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-02-19",
      "holiday_desc": "Washington's Birthday",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-03-29",
      "holiday_desc": "Good Friday",
      "holiday_groups": [
        "NYSE"
      ]
    },
    {
      "holiday_date": "2024-05-27",
      "holiday_desc": "Memorial Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-06-19",
      "holiday_desc": "Juneteenth National Independence Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-07-04",
      "holiday_desc": "Independence Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-09-02",
      "holiday_desc": "Labor Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-10-14",
      "holiday_desc": "Columbus Day",
      "holiday_groups": [
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-11-11",
      "holiday_desc": "Veterans Day",
      "holiday_groups": [
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-11-28",
      "holiday_desc": "Thanksgiving Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    },
    {
      "holiday_date": "2024-12-25",
      "holiday_desc": "Christmas Day",
      "holiday_groups": [
        "NYSE",
        "Federal Bank"
      ]
    }
  ]
}

```
