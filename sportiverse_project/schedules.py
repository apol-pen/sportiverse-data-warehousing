# schedules.py
from dagster import ScheduleDefinition
from .jobs import all_assets_job

daily_7am_schedule = ScheduleDefinition(
    job=all_assets_job,
    cron_schedule="* * * * *",  # every 1 minute for testing
    execution_timezone="Asia/Manila"
)