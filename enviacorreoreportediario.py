#!/usr/bin/python
# -*- coding: utf-8 -*-
# Envio de reportes


from Clases.ConexionDB import Conexion
from Clases.Correo import Correo
from Clases.datosconfig import datos_config


try:
    from ConfigParser import ConfigParser, SafeConfigParser
except ImportError:
    # Python 3 
    from configparser import ConfigParser, SafeConfigParser

def reporte_diario():
    con = Conexion()
    data = []
    
    conn = con.connection_postgresql()
    cursor =  conn.cursor()

    cursor.execute('select * from fncoladminemailreporte()')
    for result in cursor:    
        data.append(result)

    
    cursor.close()
    conn.close() 
    return data  

def generar_destinos():
    con = Conexion()
    destinos = []
    
    conn = con.connection_postgresql()
    cursor =  conn.cursor()

    cursor.execute('SELECT TRIM(nombre),TRIM(correo) FROM coladminemailreporte WHERE tiporeporte = 1 AND estatusactivo = 1')
    for result in cursor:    
        destinos.append(result)
        
    cursor.close()
    conn.close() 
    return destinos  


def envia_correo():
    correo = Correo()
    data = reporte_diario()
    data_destino = generar_destinos()

    destinos = []
    fila = ''
    
    for x in range(len(data_destino)):
        #Anexar destino a nueva lista
        destinos.append(data_destino[x][1])

    for x in range(len(data)):
        fila += """
            \n<tr>
                <td>%s</td>
                <td>%d</td>
            </tr>
        """ % (data[x][0], data[x][1])

    html = """<!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
    width:100%;
    }
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th, td {
    padding: 15px;
    text-align: left;
    }
    table#t01 tr:nth-child(even) {
    background-color: #eee;
    }
    table#t01 tr:nth-child(odd) {
    background-color: #fff;
    }
    table#t01 th {
    background-color: black;
    color: white;
    }
    </style>
    </head>
    <body>

    <h2>Reporte diario</h2>
    <table id="t01">
    <tr>
        <th>Descripcion</th>
        <th>Total</th> 
    </tr>
    """+ fila +"""
    </table>
    <h3>Saludos<br>
    Incidencias Afore <br>
    EXT: 570-161</h3>   
    
    </html> """

    asunto = "Estadistico de usabilidad app / SMS"
    
    datos = {
        "asunto":asunto,
        "html": html,
        "destinos": destinos
    }

    correo.enviar_correo(datos)
   
if __name__ == "__main__":
    envia_correo()
