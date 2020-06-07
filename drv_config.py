#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
Created on 14 may. 2020

@author: Yosniel Cabrera

Version 1.1.1 07-06-2020
'''

import configparser
import os

'''
    Manejo de variables de configuracion usadas en el sistema
    
    variables de salida
        !GENERAL
        project_path         ruta en donde se encuentra la carpeta automatismos
        working_mode         modo en que se ejecuta el automatimso [ LOCAL | SPY | OSE ]
        
        !DATABASE
        dbuser               usuario con acceso a la base
        dbpasswd             password para acceder a la base
        dbhost               host en donde se encuentra la base
        dbaseName            nombre de la base de datos
        
'''

### project_path
project_path = os.path.dirname(os.path.abspath(__file__))

### serv_APP_config.ini
serv_APP_config = configparser.ConfigParser()
serv_APP_config.read(f"{project_path}/serv_APP_config.ini")
## configuracion del sistema
working_mode = serv_APP_config['CONFIG']['working_mode']
dbase2use = serv_APP_config['CONFIG']['dbase2use']
## configuracion de base de datos
dbuser = serv_APP_config[dbase2use]['dbuser']
dbpasswd = serv_APP_config[dbase2use]['dbpasswd']
dbhost = serv_APP_config[dbase2use]['dbhost']
dbaseName = serv_APP_config[dbase2use]['dbaseName']



