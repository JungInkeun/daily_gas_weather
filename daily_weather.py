from open_meteo import OpenMeteo
import pprint

async def run_weather():
    async with OpenMeteo() as client:
        # 🔥 FIX: Pass a list of required variables instead of True
        forecast = await client.forecast(
                latitude=50.064,
                longitude=-97.442,
                current=["temperature_2m", "apparent_temperature","wind_speed_10m"],
                daily=[
                    "temperature_2m_max", 
                    "temperature_2m_min",
                    "apparent_temperature_min",
                    "apparent_temperature_max", 
                    "precipitation_probability_max", # 최고 강수 확률
                    "rain_sum",                      # 예상 강우량 (mm)
                    "snowfall_sum"                   # 예상 적설량 (cm)
                ],
                timezone="America/Winnipeg"
            )
        
        current = forecast.current
        daily = forecast.daily

    return current, daily

def weather_body(current, daily):
    message_body = f"""📍 Grosse Isle Weather Info at 7 AM
    🌡️ Current Temp: {current.temperature_2m}°C
    💨 Current Wind Speed: {current.wind_speed_10m} km/h
    """

    if daily:
        message_body += f"""
    📈 Max Temp: {daily.temperature_2m_max[0]}°C
    📉 Min Temp: {daily.temperature_2m_min[0]}°C
    🧥 Max Feels Like: {daily.apparent_temperature_max[0]}°C
    🥶 Min Feels Like: {daily.apparent_temperature_min[0]}°C
    ☔ Precipitation Chance (Rain/Snow): {daily.precipitation_probability_max[0]}%
    🌧️ Rainfall: {daily.rain_sum[0]} mm
    ❄️ Snowfall: {daily.snowfall_sum[0]} cm
    """

    if current.wind_speed_10m >= 30:
        message_body += "\n⚠️ Strong winds: outdoor work may be difficult.\n"

    return message_body