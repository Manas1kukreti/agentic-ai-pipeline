print(" notification_agent imported")

import smtplib
from email.mime.text import MIMEText

from groq import Groq
import os


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# MANAGER EMAIL
# =========================================================

MANAGER_EMAIL = "virenkhapra123@gmail.com"


# =========================================================
# SENDER EMAIL
# =========================================================

SENDER_EMAIL = "testpurpose917@gmail.com"


# =========================================================
# APP PASSWORD
# =========================================================

SENDER_PASSWORD = "yurwgblgotrhrbjf"


# =========================================================
# SEND FAILURE NOTIFICATION
# =========================================================

def send_failure_notification(validation_result):

    print("\n SENDING FAILURE NOTIFICATION...\n")

    try:

        # =========================================================
        # CREATE LLM PROMPT
        # =========================================================

        prompt = f"""
You are an AI Notification Agent.

Generate a professional email for an admin.

Context:
The financial extraction pipeline failed validation
after multiple retry attempts.

Validation Result:
{validation_result}

Instructions:
1. Generate a professional email subject
2. Generate a professional email body
3. Keep the tone formal and corporate
4. Mention that manual verification is required
5. Mention validation failure
6. End the email professionally
7. After Regards in next line instead of "AI Notification Agent" add EY

Return ONLY in this format:

SUBJECT:
<subject here>

BODY:
<body here>
"""


        # =========================================================
        # SEND TO GROQ
        # =========================================================

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )


        # =========================================================
        # GET GENERATED RESPONSE
        # =========================================================

        generated_text = (
            response.choices[0]
            .message.content
        )

        print("\n GENERATED EMAIL:\n")
        print(generated_text)


        # =========================================================
        # EXTRACT SUBJECT
        # =========================================================

        subject = (
            generated_text
            .split("BODY:")[0]
            .replace("SUBJECT:", "")
            .strip()
        )


        # =========================================================
        # EXTRACT BODY
        # =========================================================

        body = (
            generated_text
            .split("BODY:")[1]
            .strip()
        )


        # =========================================================
        # CREATE EMAIL MESSAGE
        # =========================================================

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = MANAGER_EMAIL


        # =========================================================
        # CONNECT TO GMAIL SMTP SERVER
        # =========================================================

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()


        # =========================================================
        # LOGIN TO GMAIL
        # =========================================================

        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )


        # =========================================================
        # SEND EMAIL
        # =========================================================

        server.send_message(msg)


        # =========================================================
        # CLOSE SERVER
        # =========================================================

        server.quit()

        print("\n FAILURE EMAIL SENT SUCCESSFULLY\n")


        # =========================================================
        # SUCCESS RESPONSE
        # =========================================================

        return {
            "status": "notification_sent",
            "subject": subject
        }


    except Exception as e:

        print("\n NOTIFICATION ERROR:\n")
        print(e)


        # =========================================================
        # FAILURE RESPONSE
        # =========================================================

        return {
            "status": "notification_failed",
            "error": str(e)
        }