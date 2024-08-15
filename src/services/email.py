import smtplib
from email.message import EmailMessage

from settings import settings_obj


class EmailService:
    RESET_PASSWORD = "إعادة تعيين كلمة المرور"
    EMAIL_CONFIRM = "الرجاء توثيق الحساب الخاص بك"

    def get_email_template(
        self,
        username: str,
        subject: str,
        email_destiny: str,
        token: str,
    ) -> EmailMessage:
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = settings_obj.SMTP_USER
        email["To"] = email_destiny
        email.set_content(
            f"""<center><div dir="rtl">
                    <h1>توثيق البريد الإلكتروني</h1>
                    <h2>مرحبا {username}</h2>
                    <p>شكرا لاختيارك خدماتنا, الرجاء توثيق البريد الإلكتروني من خلال الضغط على الرابط أدناه</p>
                    <a href=https://tishreen.serveo.net/user/verify-email?token={token}><p>اضغط هنا</p></a>
                    </div><center>""",
            subtype="html",
        )

        return email

    def get_password_reset_template(
        self,
        subject: str,
        email_destiny: str,
        password: str,
    ):
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = settings_obj.SMTP_USER
        email["To"] = email_destiny
        email.set_content(
            f"""<center><div dir="rtl">
                    <h1>إعادة تعيين كلمة المرور</h1>
                    <h2>مرحبا</h2>
                    <p>هذه هي كلمة الخاصة بك</p>
                    <p>{password}</p>
                    <p>يرجى إعادة تعيينها عند تسجيل الدخول</p>
                    </div></center>""",
            subtype="html",
        )
        return email

    def send_email(
        self,
        username: str,
        subject,
        email_destiny: str,
        token: str,
    ) -> None:
        email: EmailMessage = self.get_email_template(
            username=username,
            subject=subject,
            email_destiny=email_destiny,
            token=token,
        )
        with smtplib.SMTP_SSL(
            host=settings_obj.SMTP_HOST, port=settings_obj.SMTP_PORT
        ) as server:
            server.login(
                user=settings_obj.SMTP_USER, password=settings_obj.SMTP_PASSWORD
            )
            server.send_message(email)

    def send_email_reset_password(
        self,
        subject,
        email_destiny: str,
        password: str,
    ) -> None:
        email: EmailMessage = self.get_password_reset_template(
            subject=subject,
            email_destiny=email_destiny,
            password=password,
        )
        with smtplib.SMTP_SSL(
            host=settings_obj.SMTP_HOST, port=settings_obj.SMTP_PORT
        ) as server:
            server.login(
                user=settings_obj.SMTP_USER, password=settings_obj.SMTP_PASSWORD
            )
            server.send_message(email)
