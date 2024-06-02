import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

def send_email(subject, body, sender, receiver, password):
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    # 添加邮件内容
    msg.attach(MIMEText(body, 'plain'))

    # 创建SMTP客户端
    smtp = smtplib.SMTP('smtp.office365.com', 587)

    # 开始TLS加密
    smtp.starttls()

    # 登录邮箱
    smtp.login(sender, password)

    # 发送邮件
    smtp.sendmail(sender, receiver, msg.as_string())

    # 关闭SMTP连接
    smtp.quit()


def get_links():
    url = 'https://www.isclab.org.cn/topics/iscc/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Cookie': 'session_prefix=833a0b5a5f99ec1782aab883766fb05e',
        'Referer': 'https://www.isclab.org.cn/',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.select('#wrap > div > div')[0]
    links = [a.get('href') for a in container.find_all('a') if a.get('href') is not None]
    links = list(set(links))
    links.remove('https://www.isclab.org.cn/topics/iscc/')
    links = [link for link in links if not link.startswith('https://www.isclab.org.cn/topics/iscc/page/')]
    print('工作中...')
    return links

# 设置发件人邮箱信息
sender_email = ''
sender_password = ''

# 设置收件人邮箱信息
receiver_email = ''
# 设置邮件主题和内容
email_subject = 'ISCC官网以己经更新'
email_body = '请及时查看'

# 存储上一次的结果
previous_links = None

def job():
    global previous_links
    # 执行get_links()
    new_links = get_links()
    # 如果新的结果和上一次的结果不同
    if new_links != previous_links:
        # 发送邮件
        send_email(email_subject, email_body, sender_email, receiver_email, sender_password)
        # 更新上一次的结果
        previous_links = new_links

while True:
    job()
    time.sleep(60)