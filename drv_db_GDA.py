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
from sqlalchemy import text
#from spy import Config
from collections import defaultdict
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
    
    
#    def print_inf(self):
#        pass
        
    
    def connect(self, tag='GDA'):
        """
        Retorna True/False si es posible generar una conexion a la bd GDA
        """
        
        if self.connected:
            return self.connected
        
        try:
            self.engine = create_engine(self.url)
        except Exception as err_var:
            self.connected = False
            print('ERROR_{0}: engine NOT created. ABORT !!'.format(tag))
            print('ERROR: EXCEPTION_{0} {1}'.format(tag, err_var))
            exit(1)
        
               
        try:
            self.conn = self.engine.connect()
            self.connected = True
        except Exception as err_var:
            self.connected = False
            print('ERROR_{0}: NOT connected. ABORT !!'.format(tag))
            print('ERROR: EXCEPTION_{0} {1}'.format(tag, err_var))
            exit(1)

        return self.connected

    def read_dlg_conf(self, dlgid, tag='GDA'):
        '''
        Leo la configuracion desde GDA
                +----------+---------------+------------------------+----------+
                | canal    | parametro     | value                  | param_id |
                +----------+---------------+------------------------+----------+
                | BASE     | RESET         | 0                      |      899 |
                | BASE     | UID           | 304632333433180f000500 |      899 |
                | BASE     | TPOLL         | 60                     |      899 |
                | BASE     | COMMITED_CONF |                        |      899 |
                | BASE     | IMEI          | 860585004331632        |      899 |

                EL diccionario lo manejo con 2 claves para poder usar el metodo get y tener
                un valor por default en caso de que no tenga alguna clave
        '''
        #log(module=__name__, server=self.server, function='read_dlg_conf', dlgid=dlgid, level='SELECT', msg='start_{}'.format(tag))

        if not self.connect(tag):
            #log(module=__name__, server=self.server, function='read_dlg_conf', dlgid=dlgid, msg='ERROR_{}: can\'t connect !!'.format(tag))
            return

        #sql = """SELECT spx_unidades_configuracion.nombre as 'canal', spx_configuracion_parametros.parametro, 
        #            spx_configuracion_parametros.value, spx_configuracion_parametros.configuracion_id as \"param_id\" FROM spx_unidades,
        #            spx_unidades_configuracion, spx_tipo_configuracion, spx_configuracion_parametros 
        #            WHERE spx_unidades.id = spx_unidades_configuracion.dlgid_id 
        #            AND spx_unidades_configuracion.tipo_configuracion_id = spx_tipo_configuracion.id 
        #            AND spx_configuracion_parametros.configuracion_id = spx_unidades_configuracion.id 
        #            AND spx_unidades.dlgid = '{}'""".format (dlgid)
        
        sql = """SELECT spx_unidades_configuracion.nombre as 'canal', spx_configuracion_parametros.parametro, 
                    spx_configuracion_parametros.value, spx_configuracion_parametros.configuracion_id as 'param_id' FROM spx_unidades,
                    spx_unidades_configuracion, spx_tipo_configuracion, spx_configuracion_parametros 
                    WHERE spx_unidades.id = spx_unidades_configuracion.dlgid_id 
                    AND spx_unidades_configuracion.tipo_configuracion_id = spx_tipo_configuracion.id 
                    AND spx_configuracion_parametros.configuracion_id = spx_unidades_configuracion.id 
                    AND spx_unidades.dlgid = '{}'""".format (dlgid)            
                    
                    
                    
                    
        try:
            query = text(sql)
        except Exception as err_var:
            #log(module=__name__, server=self.server, function='read_dlg_conf', dlgid=dlgid, msg='ERROR_{0}: SQLQUERY: {1}'.format(tag, sql))
            #log(module=__name__, server=self.server, function='read_dlg_conf', dlgid=dlgid, msg='ERROR_{0}: EXCEPTION {1}'.format(tag, err_var))
            return False

        try:
            rp = self.conn.execute(query)
        except Exception as err_var:
            #log(module=__name__, server=self.server, function='read_dlg_conf', dlgid=dlgid,msg='ERROR_{}: exec EXCEPTION {}'.format(tag, err_var))
            return False

        results = rp.fetchall()
        #print(results)
        d = defaultdict(dict)
        for row in results:
            #print(row)
            canal, pname, value, pid = row
            #print(canal)
            #print(pname)
            d[(canal, pname)] = value
            #log(module=__name__, server=self.server, function='read_dlg_conf', dlgid=dlgid, level='SELECT', msg='BD_{0} conf: [{1}][{2}]=[{3}]'.format( tag,canal, pname, d[(canal, pname)]))

        return d


gda = GDA()
#gda.print_inf()
answer = gda.connect()
dlg_config = gda.read_dlg_conf('MER001')
print(dlg_config)
key = ('BASE', 'TPOLL')
value = dlg_config.get(key)
print(value)
