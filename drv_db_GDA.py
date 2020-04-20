#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
DRIVER PARA EL TRABAJO CON LA BASE DE DATOS GDA DE MySQL

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.0 16-04-2020 12:58
''' 

#LIBRERIAS
import os
import configparser
#import MySQLdb

# CANEXIONES
from sqlalchemy import create_engine
#from sqlalchemy import text
#from spy import Config
#from collections import defaultdict
#from spy_log import log


# LEO ARCHIVO DE CONFIGURACION
# OBTENFO LA CARPETA EN DONDE SE ENCUENTRA EL ARCHIVO ACTUAL
current_path = os.path.dirname(os.path.abspath(__file__))
# LEO EL ARCHIVO DE CONFIGURACION
config = configparser.ConfigParser()
config.read(f"{current_path}/serv_APP_config.ini")


class GDA(object):
    '''
    classdocs
    '''


    def __init__(self, modo='local', server='comms'):
        '''
        Constructor
        '''
    
        self.datasource = ''
        self.engine = ''
        self.conn = ''
        self.connected = False
        self.server = server
        self.url = ''

        if modo == 'spymovil':
            self.url = config['BDATOS']['url_gda_spymovil']
        elif modo == 'local':
            self.url = config['BDATOS']['url_gda_local']
        elif modo == 'ute':
            self.url = config['BDATOS']['url_gda_ute']
        return
    
    
    def print_inf(self):
        pass
        
    
    def connect(self, tag='GDA'):
        """
        Retorna True/False si es posible generar una conexion a la bd GDA
        """
        
        if self.connected:
            return self.connected
        '''
        try:
            self.engine = create_engine(self.url)
        except Exception as err_var:
            self.connected = False
            print('ERROR_{}: engine NOT created. ABORT !!'.format(tag))
            print('ERROR: EXCEPTION_{0} {1}'.format(tag, err_var))
            exit(1)
        '''
        print(self.url)
        self.engine = create_engine(self.url)

        
        
        '''try:
            self.conn = self.engine.connect()
            self.connected = True
        except Exception as err_var:
            self.connected = False
            print('ERROR_{}: NOT connected. ABORT !!'.format(tag))
            print('ERROR: EXCEPTION_{0} {1}'.format(tag, err_var))
            exit(1)

        return self.connected'''




gda = GDA('spymovil', 'SPY')
gda.print_inf()
answer = gda.connect()
print(answer)
