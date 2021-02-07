#!/datos/cgi-bin/spx/aut_env/bin/python3.8
'''
Created on 14 may. 2020

@author: Yosniel Cabrera

Version 1.1.2 07-06-2020
'''

import configparser
import os
from mypython import str2bool


'''
    Manejo de variables de configuracion usadas en el sistema
    
    variables de salida
        !GENERAL
        project_path         ruta en donde se encuentra la carpeta automatismos
        working_mode         modo en que se ejecuta el automatimso [ LOCAL | SPY | OSE ]
        path_log             ruta en donde van a estar los logs
        easy_log             habilita (True) o deshabilita (False) los logs de adentro de la carpeta AUTOMATISMOS/..
        
        !DATABASE
        dbuser               usuario con acceso a la base
        dbpasswd             password para acceder a la base
        dbhost               host en donde se encuentra la base
        dbaseName            nombre de la base de datos
        
        
        
'''

project_path = os.path.dirname(os.path.abspath(__file__))

## serv_APP_config.ini
serv_APP_config = configparser.ConfigParser()
serv_APP_config.read(f"{project_path}/serv_APP_config.ini")
working_mode = serv_APP_config['CONFIG']['working_mode']
path_log = serv_APP_config['CONFIG']['path_log']
easy_log = str2bool(serv_APP_config['CONFIG']['easy_log']) 
dbase2use = serv_APP_config['CONFIG']['dbase2use']
dbuser = serv_APP_config[dbase2use]['dbuser']
dbpasswd = serv_APP_config[dbase2use]['dbpasswd']
dbhost = serv_APP_config[dbase2use]['dbhost']
dbaseName = serv_APP_config[dbase2use]['dbaseName']




