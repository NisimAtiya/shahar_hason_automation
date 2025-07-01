import os.path
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# הרשאות – Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    # הטוקן נשמר אחרי התחברות ראשונה
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # אם אין טוקן – מבצע התחברות
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # שומר טוקן להתחברויות עתידיות
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    message.attach(MIMEText(text, 'plain'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    sent_message = service.users().messages().send(userId=user_id, body=message).execute()
    print(f'✅ הודעה נשלחה! Message Id: {sent_message["id"]}')
    return sent_message

if __name__ == '__main__':
    # רשימת האירועים לדוגמה
    events = [
        ("היכל התרבות", "2025-07-01", "20:00"),
        ("זאפה תל אביב", "2025-07-10", "21:00"),
    ]

    # בנה את גוף ההודעה
    body = "שלום,\n\nהנה רשימת המופעים:\n\n"
    for idx, (place, date, hour) in enumerate(events, start=1):
        body += f"{idx}. מקום: {place}\n   תאריך: {date}\n   שעה: {hour}\n\n"
    body += "בברכה,\nהמערכת"

    # מיילים
    sender_email = "n207302072@gmail.com"   # כתובת הג'ימייל שלך
    recipient_email = "eliyashlomo7@gmail.com"  # הנמען

    # התחבר ל-Gmail API
    service = get_gmail_service()

    # צור הודעה
    message = create_message(sender_email, recipient_email, "רשימת המופעים", body)

    # שלח
    send_message(service, 'me', message)


