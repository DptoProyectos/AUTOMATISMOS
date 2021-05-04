#!/usr/aut_env/bin/python3.8
'''
APLICACION DE CONTROL CTRL_PpotPaysandu

Created on 15 apr. 2021

@author: Yosniel Cabrera

Version 1.0.0 15-04-2021 11:19
''' 


## LIBRERIAS EXTERNAS
from time import time  
#import sys
#import os
#import configparser


## CONEXIONES DE ARCHIVOS
from __CORE__.mypython import str2bool, config_var
from __CORE__.drv_logs import ctrl_logs
from __CORE__.drv_redis import Redis
from __CORE__.drv_dlg import mbusWrite
from __CORE__.drv_config import dbuser,dbpasswd,dbhost,dbaseName
from CTRL_PpotPaysandu.PROCESS.ctrl_library import ctrl_process
from drv_db_GDA import GDA

#from CTRL_FREC.PROCESS.drv_visual import dic


#from __CORE__.drv_config import serv_APP_config




ctrl_start_time = time() 


def control_process(LIST_CONFIG):
    ''''''
    
    name_function = 'CONTROL_PROCESS'
    
    conf = config_var(LIST_CONFIG)
    
    # VARIABLES DE EJECUCION
    DLGID_CTRL = conf.lst_get('DLGID_CTRL') 
    TYPE = conf.lst_get('TYPE')                  
    print_log = str2bool(conf.lst_get('print_log'))
    
    #VARIABLES DE CONFIGURACION
    ENABLE_OUTPUTS = str2bool(conf.lst_get('ENABLE_OUTPUTS'))
    
    
 ## INSTANCIAS
    logs = ctrl_logs(TYPE,'CTRL_PpotPaysandu',DLGID_CTRL,print_log)
    redis = Redis()
    ctrl = ctrl_process(LIST_CONFIG)
    gda = GDA(dbuser,dbpasswd,dbhost,dbaseName)
    
    #config = configparser.ConfigParser()
    
    
    
    #---------------------------------------------------------
    ##PROCESS
    
    logs.print_log(__doc__)
    
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
    
    
    
    WEB_Mode = gda.readAutConf(DLGID_CTRL,'WEB_Mode')
    WEB_ActionPump = gda.readAutConf(DLGID_CTRL,'WEB_ActionPump')
    WEB_Frequency = int(gda.readAutConf(DLGID_CTRL,'WEB_Frequency'))
    

    # muestro logs con variables de configuracio
    logs.print_in(name_function, 'WEB_Mode', WEB_Mode)
    logs.print_in(name_function, 'WEB_ActionPump', WEB_ActionPump)
    logs.print_in(name_function, 'WEB_Frequency', WEB_Frequency)

    SOFT_Mode = ctrl.getAndUpdateMode(WEB_Mode)

 # FUNCION MAIN
    name_function = 'MAIN'
   
    # muestro logs de las variables de entrada del software
    logs.print_in(name_function, 'SOFT_Mode', SOFT_Mode)

    
    # desativo la alarma para que se muestre en la web que se esta trabajando en modo local
    redis.hset(DLGID_CTRL,'PLC_LocalMode','SI')
    


    # REVISO EL MODO DE TRABAJO WEB
    if SOFT_Mode == 'EMERGENCIA':
        logs.print_inf(name_function, 'TRABAJO EN MODO EMERGENCIA')



    elif SOFT_Mode == 'REMOTO':
        logs.print_inf(name_function, 'TRABAJO EN MODO REMOTO')
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
        #
        # disparo alarma para que se muestre en la web que se esta trabajando en modo local
        redis.hset(DLGID_CTRL,'PLC_LocalMode','SI')



    else:
        logs.print_error(name_function, 'MODO DE TRABAJO NO ADMITIDO')


    
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
        
    
   
        
