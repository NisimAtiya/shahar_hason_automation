import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv


load_dotenv()



def send_event_to_same_email(artist, events, to_email):
    import os
    import smtplib
    from email.message import EmailMessage

    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = f"✨ רשימת ההופעות של {artist}"

    body = f"""שלום 👋,

להלן רשימת ההופעות הקרובות הזמינות של {artist} 🎤:

"""

    for idx, (place, date, hour) in enumerate(events, start=1):
        body += (
            f"{idx}. 📍 מקום: {place}\n"
            f"   📅 תאריך: {date}\n"
            f"   🕒 שעה: {hour}\n\n"
        )

    body += """נתראה שם! 🌟

בברכה,
"""

    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
            print("✅ Mail sended")
    except Exception as e:
        print("❌ Error with sending mail: ", e)











