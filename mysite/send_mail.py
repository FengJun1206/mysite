# import os
# from django.core.mail import send_mail
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
#
#
# if __name__ == '__main__':
#     ##  纯文本邮件
#     # send_mail(
#     #     '来自 127.0.0.1:8080 的测试邮件',      # 主题 subject
#     #     '欢迎访问 127.0.0.1:8080，这里是。。。',    # 邮件内容
#     #     '18674447633@163.com',          # 发送方
#     #     ['1461024580@qq.com'],       # 接收方
#     # )
#
#     from django.core.mail import EmailMultiAlternatives
#     # HTML 格式邮件
#     subject, from_email, to = '来自127.0.0.1:8080的测试邮件', '18674447633@163.com', '1461024580@qq.com'
#     text_content = '欢迎访问 127.0.0.1:8080'
#     html_content = '<p>欢迎访问<a href="https://www.baidu.com" target=blank>www.baidu.com</a>，这里是xxx的博客网站</p>'
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(email, code):
    subject = '来自127.0.0.1:8080的测试邮件'
    text_content = '感谢注册 127.0.0.1:8080，这里是xxx的博客，如果你看到这条消息！' \
                   '说明你的邮箱服务器不支持 HTML 链接功能，请联系管理员！'
    html_content = """
                    <p>感谢注册<a href='https://{}/confirm/?code={}' target=blank>www.baidu.com</a>
                    这里是xxx的博客
                    </p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    """.format('127.0.0.1:8080', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
