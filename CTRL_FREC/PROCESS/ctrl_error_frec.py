#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
DETECCION DE ERRORES EN CONTROL DE FRECUENCIA

Created on 15 mar. 2020 

@author: Yosniel Cabrera

Version 2.0.8 06-04-2020 16:28
''' 

## LIBRERIAS
import os


## CONEXIONES
from mypython import config_var, str2bool
from drv_logs import ctrl_logs
from CTRL_FREC.PROCESS.ctrl_library import error_process_frec
from drv_redis import Redis




def error_process(LIST_CONFIG):
    
    name_function = 'ERROR_PROCESS'
    
    conf = config_var(LIST_CONFIG)
    
    #VARIABLES DE EJECUCION
    print_log = str2bool(conf.lst_get('print_log'))
    DLGID = conf.lst_get('DLGID') 
    TYPE = conf.lst_get('TYPE')                  
    
    
    #VARIABLES DE CONFIGURACION
    SWITCH_OUTPUTS = str2bool(conf.lst_get('SWITCH_OUTPUTS'))
    EVENT_DETECTION = str2bool(conf.lst_get('EVENT_DETECTION'))
    
    ## INSTANCIAS
    logs = ctrl_logs('CTRL_FREC',DLGID,print_log)
    e = error_process_frec(LIST_CONFIG)
    redis = Redis()
    
    #---------------------------------------------------------
    ##ERROR PROCESS
    
    logs.print_log(__doc__)
    
    # ESCRIBO LA EJECUCION DEL SCRIPT
    logs.script_performance(f"{name_function}")
    
    # MUESTRO VARIABLES DE ENTRADA
    logs.print_in(name_function, 'print_log', print_log)
    logs.print_in(name_function, 'DLGID', DLGID)
    logs.print_in(name_function, 'TYPE', TYPE)
    #
    if SWITCH_OUTPUTS: logs.print_in(name_function, 'SWITCH_OUTPUTS', SWITCH_OUTPUTS)
    if EVENT_DETECTION: logs.print_in(name_function, 'EVENT_DETECTION', EVENT_DETECTION)
    #
    logs.print_inf(name_function, 'TEST_TX_ERRORS')
    e.test_tx()
    #
    logs.print_inf(name_function, 'VISUAL')
    e.visual()
    #
    logs.print_inf(name_function, 'EVENT_DETECTION')
    e.event_detection()
    
    
    
    
    '''
    if redis.hexist(f'{DLGID}_ERROR', '#_RUN'):
        no_RUN = int(redis.hget(f'{DLGID}_ERROR', '#_RUN'))
        no_RUN += 1
        redis.hset(f'{DLGID}_ERROR', '#_RUN',no_RUN)
    else:
        redis.hset(f'{DLGID}_ERROR', '#_RUN',0)
        '''
        
    
    
    
