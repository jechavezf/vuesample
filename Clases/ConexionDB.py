#!/usr/bin/python
# -*- coding: utf-8 -*-
# Enviar reporte de registros borrados en la CTA_SALDO_VOL
#import informixdb#
import socket
import sys
import psycopg2
from datosconfig import datos_config



try:
    from ConfigParser import ConfigParser, SafeConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser, SafeConfigParser

class Conexion:

    
    # def connection_informix(self):

    #     host      = datos_config["host"]
    #     database  = datos_config["bd"]
    #     port      = datos_config["port"]
    #     user      = datos_config["user"]
    #     passw     = datos_config["passw"]

    #     try:   
    #         conn = informixdb.connect(database, user, passw) # % (host,user,passw)
    #         return conn
    #     except informixdb.DatabaseError as err:
    #         print ("Unable to connect to the database: ", err)
    #         print (err.action, err.sqlcode, err.diagnostics)


    def connection_postgresql(self):
        try:
            conn = psycopg2.connect(host=datos_config['hostaforeglobal'], 
                                            user=datos_config['useraforeglobal'], 
                                            password=datos_config['passwaforeglobal'], 
                                            dbname=datos_config['bdaforeglobal'])
            #cur = conn.cursor()
        
            return conn
        except:
            print ("Unable to connect to the database")
