from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import requests
import os

msg = MIMEMultipart()
password = os.environ['password_mail']
msg['From'] = 'votacioneswebinarcodigo@outlook.com'
msg['Subject'] = 'Link de Votacion - Webinar CodiGo'

def sendMail(to, nombre, hash):
    msg['To'] = to
    message = 'Hola! {} \n Tu link para votar es: http://frontendwebinar.com/votar?id={}'.format(nombre, hash)
    msg.attach(MIMEText(message,'plain'))
    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        # server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False

def buscarPersona(dni):
    url = 'https://apiperu.dev/api/dni/{}'.format(dni)
    headers = {
        'Authorization':'Bearer '+os.environ['token_apiperu'], 
        'Content-Type':'application/json'}
    r = requests.get(url, headers=headers)
    return r.json()
