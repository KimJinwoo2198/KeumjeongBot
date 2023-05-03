import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from keumjeong import email_password,email_id
from jinja2 import Template

def render_template(**data):
    with open('./Email.html', encoding="UTF8") as f:
        template = Template(f.read())
    return template.render(**data)

def mail_sender(number,code):
    try:
        data = {
            'to': f'{number}@keumjeong.hs.kr',
            'from': 'KeumJeongHs<noreply@mycompany.com>',
            'subject': '[금정고] 이메일 인증을 완료해주세요.',
            'item': {'Code': code}
        }
        msg = MIMEMultipart('alternative')
        msg['subject'] = '[금정고] 이메일 인증을 완료해주세요.'
        msg['To']=f'{number}@keumjeong.hs.kr'
        msg['from']='KeumJeongHs<noreply@mycompany.com>'
        msg.attach(MIMEText(render_template(**data), 'html'))

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(email_id, email_password)
        s.sendmail('KeumJeongHs<noreply@mycompany.com>', f'{number}@keumjeong.hs.kr', msg.as_string())
        return 'success'
    except:
        return 'fail'