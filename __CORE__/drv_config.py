#!/usr/aut_env/bin/python3.8
'''
Created on 14 may. 2020

@author: Yosniel Cabrera

Version 1.1.2 07-06-2020
'''

import configparser
import os
from __CORE__.mypython import str2bool, str2lst            


'''
    Manejo de variables de configuracion usadas en el sistema
    
    variables de salida
        !GENERAL
        project_path         ruta en donde se encuentra la carpeta automatismos
        working_mode         modo en que se ejecuta el automatimso [ LOCAL | SPY | OSE ]
        path_log             ruta en donde van a estar los logs
        easy_log             habilita (True) o deshabilita (False) los logs de adentro de la carpeta AUTOMATISMOS/..
        allowedTypes         lista con valores que puede tener la variabl de redis DLGID:TYPE para que se corra el automatismo
        
        !DATABASE
        dbuser               usuario con acceso a la base
        dbpasswd             password para acceder a la base
        dbhost               host en donde se encuentra la base
        dbaseName            nombre de la base de datos
        
        
        
'''

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




## Lectura del config.ini
serv_APP_config = configparser.ConfigParser()
serv_APP_config.read(f"{project_path}/config.ini")

# GENERAL_CONFIG
path_log =  serv_APP_config['GENERAL_CONFIG']['path_log']
easy_log = str2bool(serv_APP_config['GENERAL_CONFIG']['easy_log']) 
sql_config2use = serv_APP_config['GENERAL_CONFIG']['sql_config2use']
redis_config2use = serv_APP_config['GENERAL_CONFIG']['redis_config2use']
allowedTypes = str2lst(serv_APP_config['GENERAL_CONFIG']['allowedTypes'])        


# SQL_config2use
dbuser = serv_APP_config[sql_config2use]['dbuser']
dbpasswd = serv_APP_config[sql_config2use]['dbpasswd']
dbhost = serv_APP_config[sql_config2use]['dbhost']
dbaseName = serv_APP_config[sql_config2use]['dbaseName']


# REDIS_config2use
rddbhost = serv_APP_config[redis_config2use]['host']




