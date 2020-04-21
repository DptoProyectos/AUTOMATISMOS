#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
APLICACION DE CONTROL DE ERRORES EN CTRL_FREC

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.3 16-04-2020 12:58
''' 

## LIBRERIAS
import os


## CONEXIONES
from mypython import config_var, str2bool
from drv_logs import ctrl_logs
from drv_redis import Redis
from drv_dlg import dlg_detection




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
    logs = ctrl_logs(TYPE,DLGID,print_log)
    redis = Redis()
    #
    # INSTANCIA DE error_process
    import importlib.util
    #spec = importlib.util.spec_from_file_location("archivo", f"../{TYPE}/PROCESS/ctrl_library.py")
    spec = importlib.util.spec_from_file_location("archivo", f"/drbd/www/cgi-bin/spx/AUTOMATISMOS/{TYPE}/PROCESS/ctrl_library.py")
    archivo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(archivo)
    e = archivo.error_process(LIST_CONFIG)
    
    
    
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
    
    # ESCRIBO NUMERO DE EJECUCION
    redis.no_execution(f'{DLGID}_ERROR')
    
    # CHEQUEO ERROR TX
    logs.print_inf(name_function, 'TEST_TX_ERRORS')
    # LLAMO A FUNCIONES QUE SOLO CORREN SI NO HAY ERROR TX
    if e.test_tx():
    #if True:
        #
        # LLAMAO A FUNCIONES QUE SOLO CORREN CON DATALOGGER 8CH Y SIN ERRORES TX
        if dlg_detection(DLGID) == '8CH':
            #
            # DETECCION DE EVENTOS
            logs.print_inf(name_function, 'EVENT_DETECTION')
            e.event_detection()
            #
            # ALTERNO LAS SALIDAS
            logs.print_inf(name_function, 'SWITCH_OUTPUTS')
            e.switch_outputs()
            
            #
        elif dlg_detection(DLGID) == '5CH':
            # DATALOGGER DE 5CH DETECTADO
            #
            logs.print_inf(name_function, 'DLG 5CH NO SE DETECTAN EVENTOS')
            logs.print_inf(name_function, 'DLG 5CH NO SE ALTERNAN SALIDAS')
            
        else:
            # NO SE DETECTA EL TIPO DE DATALOGGER
            #
            logs.print_inf(name_function, 'NO SE DETECTA EL TIPO DE DATALOGGER')
            logs.script_performance(f'{name_function} => NO SE DETECTA EL TIPO DE DATALOGGER')
    else:
        logs.print_inf(name_function, 'NO SE DETECTAN EVENTOS POR ERROR TX')
            
    #
    logs.print_inf(name_function, 'VISUAL')
    e.visual()
    #
    
    
    
    
    
    
    '''
    if redis.hexist(f'{DLGID}_ERROR', '#_RUN'):
        no_RUN = int(redis.hget(f'{DLGID}_ERROR', '#_RUN'))
        no_RUN += 1
        redis.hset(f'{DLGID}_ERROR', '#_RUN',no_RUN)
    else:
        redis.hset(f'{DLGID}_ERROR', '#_RUN',0)
        '''
        
    
    
    