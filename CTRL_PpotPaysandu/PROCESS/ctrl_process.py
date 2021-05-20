#!/usr/aut_env/bin/python3.8
'''
CTRL_PpotPaysandu 

Version 1.0.0 15-04-2021 11:19
''' 


## LIBRERIAS EXTERNAS
from time import time  



## CONEXIONES DE ARCHIVOS
from __CORE__.mypython import str2bool, config_var
from __CORE__.drv_logs import ctrl_logs
from __CORE__.drv_redis import Redis
from __CORE__.drv_dlg import mbusWrite
from __CORE__.drv_config import dbUrl
from __CORE__.drv_db_GDA import GDA
from CTRL_PpotPaysandu.PROCESS.ctrl_library import ctrl_process






ctrl_start_time = time() 


def control_process(LIST_CONFIG):
    ''''''
    
    name_function = 'CONTROL_PROCESS'
    processName = 'CTRL_PpotPaysandu'
    
    conf = config_var(LIST_CONFIG)
    
    # VARIABLES DE EJECUCION
    DLGID_CTRL = conf.lst_get('DLGID_CTRL') 
    TYPE = conf.lst_get('TYPE')                  
    print_log = str2bool(conf.lst_get('print_log'))
    LOG_LEVEL = conf.lst_get('LOG_LEVEL') 
    
    #VARIABLES DE CONFIGURACION
    ENABLE_OUTPUTS = str2bool(conf.lst_get('ENABLE_OUTPUTS'))
    
    
 ## INSTANCIAS
    logs = ctrl_logs(TYPE,'CTRL_PpotPaysandu',DLGID_CTRL,print_log,LOG_LEVEL)
    redis = Redis()
    ctrl = ctrl_process(LIST_CONFIG)
    gda = GDA(dbUrl)
    
        
    #---------------------------------------------------------
    ##PROCESS
    
    #logs.print_log(__doc__)
    logs.basicLog(__doc__)
    
    # ESCRIBO LA EJECUCION DEL SCRIPT
    logs.print_log(f"{name_function}")
    
    # MUESTRO VARIABLES DE ENTRADA
    logs.print_in(name_function, 'print_log', print_log)
    logs.print_in(name_function, 'DLGID_CTRL', DLGID_CTRL)
    logs.print_in(name_function, 'TYPE', TYPE)
    logs.print_in(name_function, 'ENABLE_OUTPUTS', ENABLE_OUTPUTS)
      


    # CHEQUEO QUE EXISTAN LOS LINES DEL DATALOGGER DE CONTROL Y EL DE REFERENCIA.
    if not(redis.hexist(DLGID_CTRL,'LINE')): 
        #logs.script_performance(f'{name_function} ==> NO EXISTE LINE {DLGID_CTRL}')
        logs.print_inf(name_function,f'NO EXISTE LINE {DLGID_CTRL}')
        logs.print_inf(name_function,'EJECUCION INTERRUMPIDA')
        quit()
    
    # Garantizo que las variables que se van a usar en la visualizacion siempre existan
    ctrl.setVisualVars()

    # Garantizo que las variable de control esten siempre disponibles para el automatismo
    ctrl.checkAndSetControlVars()

    
    WEB_Mode = conf.lst_get('WEB_Mode')
    WEB_ActionPump = conf.lst_get('WEB_ActionPump')
    WEB_Frequency = int(conf.lst_get('WEB_Frequency'))
    
    # muestro logs con variables de configuracio
    logs.print_in(name_function, 'WEB_Mode', WEB_Mode)
    logs.print_in(name_function, 'WEB_ActionPump', WEB_ActionPump)
    logs.print_in(name_function, 'WEB_Frequency', WEB_Frequency)

    SOFT_Mode = ctrl.getAndUpdateMode(WEB_Mode)

 # FUNCION MAIN
    name_function = 'MAIN'
   
    # muestro logs de las variables de entrada del software
    logs.print_in(name_function, 'SOFT_Mode', SOFT_Mode)
    
     
    # DETECTO MODO DE TRABAJO
    if SOFT_Mode == 'EMERGENCIA':
        logs.print_inf(name_function, 'TRABAJO EN MODO EMERGENCIA')
        redis.hset(DLGID_CTRL,'PLC_SoftMode','EMERGENCIA')

    elif SOFT_Mode == 'REMOTO':
        logs.print_inf(name_function, 'TRABAJO EN MODO REMOTO')
        redis.hset(DLGID_CTRL,'PLC_SoftMode','REMOTO')
        #
        # accion sobre la bomba
        if not WEB_ActionPump in ['ON','OFF']:
            logs.print_error(name_function, 'ACCION NO ADMITIDA')
        else: 
            ctrl.pump(WEB_ActionPump)
            #
        # seteo de frecuencia
        if WEB_ActionPump == 'ON':
            ctrl.setFrequency(WEB_Frequency)

    elif SOFT_Mode == 'LOCAL':
        logs.print_inf(name_function,"TRABAJANDO EN MODO LOCAL DESDE EL TABLERO")
        redis.hset(DLGID_CTRL,'PLC_SoftMode','LOCAL')
        
    else:
        logs.print_error(name_function, 'MODO DE TRABAJO NO ADMITIDO')


    # Preparo para la visualizacion web los estados y alarmas del sistema
    ctrl.showStatesAndAlarms()
    
    #
    # CALCULO TIEMPO DE DEMORA
    #print('')
    #print('TIME_ALALYSIS')
    #print(f'ctrl_process_frec TERMINADO A {time()-ctrl_start_time} s') 
    
    
        
        
        
## VARIABLES DEL SCRIPT PARA EJECUCION LOCAL       
if __name__ == '__main__':
    # PREPARO EL SCRIPT PARA LLAMADA LOCAL. SE TOMA LA CONFIGURACION ESCRITA AL INICIO
    LIST_CONFIG = [
                #VARIABLES DE EJECUCION
                'print_log',        True,                             # VER LOS LOGS EN CONSOLA [ True | False ]
                'DLGID_CTRL',       'CTRLPAY01',                      # ID DATALOGGER QUE EJECUTA LAS ACCIONES DE CONTROL
                'TYPE',             'CTRL_PpotPaysandu',              # CUANDO TIENE LE VALOR CHARGE SE CARGA LA CONFIGURACION DE LA db
                
                #VARIABLES DE CONFIGURACION
                'ENABLE_OUTPUTS',   True,                             # ACTIVA Y DESACTIVA LA ACCION DE LAS SALIDAS PARA ESTE DLGID_CTRL [ True | False]
            ]        

    control_process(LIST_CONFIG)
        
    
   
        
