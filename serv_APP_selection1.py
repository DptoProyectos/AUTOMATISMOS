#!/usr/aut_env/bin/python3.8
'''
SELECCION DE AUTOMATISMOS

@author: Yosniel Cabrera

Version 2.1.5 15-04-2021
''' 

# LIBRERIAS
import sys
import configparser
import os

# CONEXIONES
from __CORE__.mypython import config_var, lst2str, str2lst
from __CORE__.drv_redis import Redis
from __CORE__.drv_logs import ctrl_logs
from __CORE__.drv_config import allowedTypes, project_path
from __CORE__.drv_db_GDA import GDA
from __CORE__.drv_config import dbUrl, perforationProcessPath
from time import time   
sel_start_time = time() 
