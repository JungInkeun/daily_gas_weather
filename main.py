# 기본 라이브러리
from datetime import datetime
from zoneinfo import ZoneInfo 

#날씨 라이브러리
import asyncio
from daily_weather import run_weather, weather_body

#기름정보 라이브러리
from daily_gas_diesel import TellMeGasDieselPrice

#메일발송
from email_code import msg


now = datetime.now(ZoneInfo("America/Winnipeg")).strftime("%Y-%m-%d, %H:%M:%S")

#날씨 정보
async def weather():
    current, daily = await run_weather()
    return weather_body(current, daily), current, daily

weather_msg, current, daily = asyncio.run(weather())
feel_lowest_temp = daily.apparent_temperature_max[0] #최저체감온도


#기름값 정보
async def gas():
    gas_data = TellMeGasDieselPrice()
    stations = await gas_data.call_data()

    return gas_data, stations

gas_data, stations = asyncio.run(gas())
gasoline = gas_data.get_gas_price(stations)
diesel = gas_data.get_diesel_price(stations)

diesel_list = gas_data.sorted_price(diesel, 'diesel_price')
gasoline_list = gas_data.sorted_price(gasoline, 'regular_gas')
gasoline_lowest_price = gasoline_list[list(gasoline_list.keys())[0]]['regular_gas'] #가솔린 최저가
costco_price = gas_data.get_costco_price(stations)

gasoline_text, diesel_text = gas_data.get_string(gasoline_list, diesel_list)

#메일발송
msg(costco_price, gasoline_lowest_price, gasoline_text, diesel_text, feel_lowest_temp, weather_msg)



