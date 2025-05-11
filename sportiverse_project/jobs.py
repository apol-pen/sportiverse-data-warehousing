from dagster import define_asset_job
from .assets import *

all_assets_job = define_asset_job(name="all_assets_job")