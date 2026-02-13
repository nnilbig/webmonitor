import requests
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.header import Header

# 從環境變數讀取秘密資訊 (這是為了安全！)
TARGET_URL = "https://www.chuncheonmarathon.com/"
KEYWORD = "2025"
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_alert_email(found_url, found_keyword):
    # (這部分維持你剛才的代碼內容...)
    subject = f'🔔 監控警報：{found_keyword} 出現了！'
    body = f'系統偵測到關鍵字：{found_keyword}\n監控網址：{found_url}\n時間：{time.strftime("%Y-%m-%d %H:%M:%S")}'
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, [RECEIVER_EMAIL], msg.as_string())

def test_monitor():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        if response.status_code == 200 and KEYWORD in response.text:
            print(f"找到 {KEYWORD} 了！發送郵件中...")
            send_alert_email(TARGET_URL, KEYWORD)
        else:
            print(f"狀態正常，尚未發現關鍵字。")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    test_monitor()