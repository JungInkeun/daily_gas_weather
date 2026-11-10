# 알림용 외부 라이브러리
import smtplib
from email.mime.text import MIMEText
import os
import requests

# 메시지 정리
def msg(costco_price, gasoline_lowest_price, gasoline_text, diesel_text, feel_lowest_temp, weather_msg):
    message = f"""Gas Price : ${gasoline_lowest_price} Feel like min : {feel_lowest_temp}C"""

    costco_body = f"Costco Kenaston Price : ${costco_price}"
    # 이메일 설정
    msg = MIMEText(message+"\n\n"+costco_body+"\n\n"+gasoline_text+"\n\n"+diesel_text+"\n\n"+weather_msg)
    msg['Subject'] = f"Gas Price : ${gasoline_lowest_price} Feel like min : {feel_lowest_temp}C"
    msg['From'] = "imw200814@gmail.com"           # 보내는 사람
    msg['To'] = "imw200814@gmail.com"           # 받는 사람

    # Gmail SMTP 서버 연결
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("imw200814@gmail.com", os.environ["GMAIL_APP_PASSWORD"])  # Secrets 사용
        server.send_message(msg)
