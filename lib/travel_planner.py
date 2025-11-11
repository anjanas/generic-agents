# The `call_weather_api_mocked` mocks calling a weather API to get weather data
# TODO: Fill in the missing parts marked with **********

from project_lib import call_weather_api_mocked
import pandas as pd

pd.set_option("display.max_colwidth", None)  # Show full content in DataFrame cells

weather_for_dates = [
    call_weather_api_mocked(
        date=ts.strftime("%Y-%m-%d"), city=vacation_info.destination
    )
    for ts in pd.date_range(
        # TODO: Fill in the missing start and end dates from vacation_info
        start=vacation_info.start_date,
        end=vacation_info.end_date,
        # start=**********
        # end=***********
        freq="D",
    )
]

weather_for_dates_df = pd.DataFrame(weather_for_dates)

weather_for_dates_df

from project_lib import call_activities_api_mocked

activities_for_dates = [
    activity
    for ts in pd.date_range(
        # TODO: Fill in the missing start and end dates from vacation_info
        
        # start=**********
        # end=***********
        freq="D",
    )
    for activity in call_activities_api_mocked(
        date=ts.strftime("%Y-%m-%d"), city=vacation_info.destination
    )
]

activities_for_dates_df = pd.DataFrame(activities_for_dates)

activities_for_dates_df