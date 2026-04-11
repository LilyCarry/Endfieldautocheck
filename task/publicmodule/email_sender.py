# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 固定参数配置
SENDER_EMAIL = "baahpush@163.com"  # 发件人邮箱
SENDER_PASSWORD = "VMMg5xhPddrH2g7V"  # 邮箱密码/授权码
SMTP_SERVER = "smtp.163.com"  # SMTP服务器地址
SMTP_PORT = 465  # SMTP服务器端口（SSL）


def send_email(target, subject, content):
    """
    发送电子邮件函数

    参数：
    target  : str/list 收件人邮箱地址（多个地址用逗号分隔的字符串或列表）
    subject : str      邮件主题
    content : str      邮件正文内容
    """
    # 处理收件人格式
    if isinstance(target, str):
        recipients = [addr.strip() for addr in target.split(",")]
    else:
        recipients = target

    # 创建邮件对象
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8") # type: ignore
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(recipients)  # 显示用收件人列表

    try:
        # 使用SSL连接SMTP服务器
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False
if __name__=='__main__':
    send_email('baahpush@163.com','sendtest','ccb world')