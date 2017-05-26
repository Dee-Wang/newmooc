from django.core.mail import send_mail

from random import Random

from users.models import EmailVerifyRecord
from mymooc.settings import DEFAULT_FROM_EMAIL


def general_random_str(randomlength):
    str = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def send_email(email, send_type):
    email_record = EmailVerifyRecord()
    # 当验证码用于用户登陆后重置邮箱的时候，发送的验证码是4位的，其他情况下验证码是16位的
    if send_type == "change_email":
        code = general_random_str(4)
    else:
        code = general_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "在线学习网站的注册激活链接"
        email_body = "请点击下面的链接激活你的账户：http://127.0.0.1:8000/users/active_user/{0}".format(code)

    elif send_type == "forget_password":
        email_title = "在线学习网站密码重置链接"
        email_body = "请点击下面的链接重置密码：http://127.0.0.1:8000/users/reset_pwd/{0}".format(code)

    elif send_type == "change_email":
        email_title = "在线学习网站修改邮箱验证码"
        email_body = "这是您的验证码：{0}".format(code)

    send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
    if send_status:
        pass


