#!/usr/bin/python

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes,email
from smtplib import SMTP
from email import encoders
from datosconfig import datos_config



class Correo:
    def enviar_correo(self,param):

        datos = {
            'emisor':'',
            'mime_message':''
        }
        cc = ','.join(param.get('destinos'))

        mime_message = MIMEMultipart()
        mime_message["From"] = 'Notificaciones <'+datos_config['emisor']+'>'
        mime_message["Subject"] = param.get('asunto')
        mime_message["To"] = datos_config['emisor']
        
        #Copias
        mime_message["Cc"] = cc
        
        destinos = param.get('destinos')
        html = param.get('html')
        #print destinos

        
        

        #mime_message.attach(MIMEText(body, "plain"))
        mime_message.attach(MIMEText(html, "html"))
        datos['emisor'] = datos_config['emisor']
        
        datos['mime_message'] = mime_message
        
        smtp = SMTP(datos_config['servsmtp'])
        smtp.starttls()
        smtp.login(datos_config['usuario'], datos_config['contrasenia'])
        smtp.sendmail(datos_config['emisor'], destinos,datos['mime_message'].as_string())
        smtp.quit()

