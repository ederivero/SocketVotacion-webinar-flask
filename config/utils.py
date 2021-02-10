from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import requests
import os

msg = MIMEMultipart()
password = os.environ['email_password']
msg['From'] = 'votacioneswebinarcodigo@outlook.com'
msg['Subject'] = 'Link de Votacion - Webinar CodiGo'

def sendMail(to, nombre, hash):
    msg['To'] = ''
    message = ''
    msg['To'] = to
    message = 'Hola! {} \n Tu link para votar es: https://jorgegarba.github.io/webinar-votaciones/#/cedula?id={}'.format(nombre, hash)
    msg.attach(MIMEText(message,'plain'))
    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
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
    print(headers)
    r = requests.get(url, headers=headers)
    return r.json()
