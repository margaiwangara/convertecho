import smtplib, json
from email.message import EmailMessage
from config import settings


def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = settings.GMAIL_ADDRESS
        sender_password = settings.GMAIL_PASSWORD
        receiver_address = message["username"]

        msg = EmailMessage()
        msg.set_content(f"Your MP3 id is: {mp3_fid}")
        msg["Subject"] = "ConvertEcho - MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg)
        session.quit()
        print("Mail sent")
    except Exception as err:
        print(err)
        return err
