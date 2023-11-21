import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
def alert(svc):
    mailaddress = ''
    password = ''

    subject = f"{svc}のpodのCPU使用量が危ないです"
    text = f"{svc}のpodのCPU使用量が高くなっています\nこのままでは規定の応答時間を超えます"
    address_from = ''
    address_to = ''

    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(mailaddress, password)

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = address_from
    msg['To'] = address_to
    msg['Date'] = formatdate()

    smtpobj.send_message(msg)
    smtpobj.close()
