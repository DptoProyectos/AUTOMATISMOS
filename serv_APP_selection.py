#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
Created on 22 mar. 2020

@author: Yosniel Cabrera

Version 2.0.6 06-04-2020 10:41
'''

# LIBRERIAS
import sys
import configparser
import os

# CONEXIONES
from mypython import config_var, lst2str
from CTRL_FREC.PROCESS.ctrl_process_frec import control_process
from drv_redis import Redis
from drv_logs import ctrl_logs
from time import time   
from email import quoprimime
sel_start_time = time() 






# CONFIGURO LAS ENTRADAS DE CONFIGURACION 
if __name__ == '__main__':
    # LEO EL STR DE CONFIGURACION       
    STR_CONFIG = sys.argv[1]
    LIST_CONFIG = STR_CONFIG.split(',')
    #
    # INSTANCIA DE config_var
    conf = config_var(STR_CONFIG) 
    config = configparser.ConfigParser()
    redis = Redis()
    #
    ### ABRO ARCHIVO DE CONFIGURACION
    # OBTENFO LA CARPETA EN DONDE SE ENCUENTRA EL ARCHIVO ACTUAL
    current_path = os.path.dirname(os.path.abspath(__file__))
    # LEO EL ARCHIVO DE CONFIGURACION
    config.read(f"{current_path}/serv_APP_config.ini")
    #
    # CHEQUEO QUE TIPO DE LLAMADA SE ESTA HACIENDO
    ## SI SE LE PASA UN str ASIGNO VALORES ENTRADOS
    if conf.str_get('DLGID_CTRL'):
        print_log = conf.str_get('print_log')
        DLGID_CTRL = conf.str_get('DLGID_CTRL')
        if conf.str_get('TYPE'): TYPE = conf.str_get('TYPE')
        else:  TYPE = 'CHARGE'
    ## SE SE LE PASA UN SOLO ARGUMENTO SE LO ASIGNO A DLGID
    else:
        print_log = False
        DLGID_CTRL = sys.argv[1]
        TYPE = 'CHARGE'
        
    
    
    
    
        

def read_config_var(DLGID_CTRL):
    ''''''
    
    FUNCTION_NAME = 'READ_CONFIG_VAR'
    
    ## INSTANCIAS
    logs = ctrl_logs('CTRL_FREC',DLGID_CTRL,print_log)
    redis = Redis()
    # 
    # LEO LOS TAGS DE CONFIGURACION
    if redis.hexist(DLGID_CTRL,'TAG_CONFIG'): 
        TAG_CONFIG = redis.hget(DLGID_CTRL,'TAG_CONFIG')
        TAG_CONFIG = TAG_CONFIG.split(',')
    else: 
        logs.print_inf(FUNCTION_NAME,'NO EXISTE LA VARIABLE TAG_CONFIG')
        logs.print_inf(FUNCTION_NAME,'NO SE EJECUTA EL SCRIPT')
        sys.exit()
    #
    # LEO CONFIGUTACION DE LA REDIS
    logs.print_inf(FUNCTION_NAME,'LEO CONFIG EN REDIS')
    vars_config = []
    for param in TAG_CONFIG:
        vars_config.append(param)
        vars_config.append(redis.hget(DLGID_CTRL,param))
    #
    # MUESTRO VARIABLES LEIDAS
    n = 0
    for param in vars_config:
        if n < (len(vars_config)): 
            logs.print_out(FUNCTION_NAME,vars_config[n],vars_config[n+1])
            n += 2
    #
    # CONCATENO LAS VARIABLES DE EJECUCION Y DE CONFIGURACION
    list_out = []
    LIST_CONFIG = ['print_log', print_log, 'DLGID_CTRL', DLGID_CTRL, 'TYPE', TYPE]
    n = 0
    for param in LIST_CONFIG:
        if n < 4:
            list_out.append(LIST_CONFIG[n])
            n +=1
    
    for param in vars_config:
        list_out.append(param)
    
    return list_out
        
def upgrade_config(DLGID_CTRL,LIST_CONFIG):
    ''''''
    
    FUNCTION_NAME = 'UPGRADE_CONFIG'
    
    #
    ## INSTANCIAS
    logs = ctrl_logs('CTRL_FREC',DLGID_CTRL,print_log)
    #
    # IMPRIMIR VARIABLES DE CONFIGURACION
    n = 4
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            logs.print_in(FUNCTION_NAME,LIST_CONFIG[n],LIST_CONFIG[n+1])
            n += 2
    #
    # ESCRIBO EN REDIS LAS VARIABLES DE CONFIGURACION
    logs.print_inf(FUNCTION_NAME, 'ACTUALIZO CONFIG EN REDIS' )
    n = 4
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            redis.hset(DLGID_CTRL,LIST_CONFIG[n],LIST_CONFIG[n+1])
            n += 2
    
    # ELIMINO LAS VARIABLES DE CONFIGURACION ANTERIORES
    if redis.hexist(DLGID_CTRL,'TAG_CONFIG'):
        last_TAG_CONFIG = redis.hget(DLGID_CTRL,'TAG_CONFIG')
    
           
        for param in last_TAG_CONFIG.split(','):
            redis.hdel(DLGID_CTRL, param)
            
        redis.hdel(DLGID_CTRL,'TAG_CONFIG')
       
        
        
    # ESCRIBO EN REDIS EL NOMBRE DE LAS VARIABLES DE CONFIGURACION PARA QUE PUEDAN SER LEIDAS
    TAG_CONFIG = []
    n = 4
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            redis.hset(DLGID_CTRL,LIST_CONFIG[n],LIST_CONFIG[n+1])
            TAG_CONFIG.append(LIST_CONFIG[n])
            n += 2
    redis.hset(DLGID_CTRL,'TAG_CONFIG',lst2str(TAG_CONFIG))
    
    
    # LEO VARIABLES ESCRITAS
    n = 4
    check_config = []
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            check_config.append(LIST_CONFIG[n])
            check_config.append(redis.hget(DLGID_CTRL,LIST_CONFIG[n]))
            n += 2
    #
    # MUESTRO VARIABLES LEIDAS
    n = 0
    for param in check_config:
        if n < (len(check_config)): 
            logs.print_out(FUNCTION_NAME,check_config[n],check_config[n+1])
            n += 2

    


name_function = 'APP_SELECTION'

## INSTANCIAS
logs = ctrl_logs('CTRL_FREC',DLGID_CTRL,print_log)
redis = Redis()

## VARIABLES GLOBALES QUE LE ENTRAN A CORE
logs.print_log(f"EXECUTE: {name_function}")      
#
# VARIABLES DE EJECUCION
if conf.str_get('print_log'):logs.print_in(name_function,'print_log',print_log)
logs.print_in(name_function,'DLGID_CTRL',DLGID_CTRL)
#if conf.str_get('TYPE'): logs.print_in(name_function,'TYPE',TYPE)

   
        
## VARIABLES PARTICULARES QUE LE ENTRAN A APP_SELECTION

if TYPE in config['CTRL_CONFIG']['CTRL_ID']:
    # IMPRIMIR VARIABLES DE CONFIGURACION
    n = 4
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            logs.print_in(name_function,LIST_CONFIG[n],LIST_CONFIG[n+1])
            n += 2
    #
    # ACTUALIZO LA CONFIGURACION
    logs.print_inf(name_function,'UPGRADE CONFIG')
    upgrade_config(DLGID_CTRL,LIST_CONFIG)
    #

else:
        #CHEQUEO SI EXISTE LA VARIABLE TYPE
        if redis.hexist(DLGID_CTRL,'TYPE'):
            logs.print_inf(name_function,'READ_CONFIG_VAR')
            #LEO LAS VARIABLES DE CONFIGURACION
            LIST_CONFIG=read_config_var(DLGID_CTRL)
            
        else: 
            logs.print_inf(name_function,'NO EXISTE LA VARIABLE TYPE')
            logs.print_inf(name_function,'NO SE EJECUTA EL SCRIPT')
            LIST_CONFIG=[]


# MUESTRO LAS VARIABLES QUE SE LE VAN A PASAR AL PROCESS Y LO LLAMO
if bool(LIST_CONFIG):
    n = 0
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            logs.print_out(name_function,LIST_CONFIG[n],LIST_CONFIG[n+1])
            n += 2
    
    conf = config_var(LIST_CONFIG) 
    if conf.lst_get('TYPE') in config['CTRL_CONFIG']['CTRL_ID']:
        control_process(LIST_CONFIG)
        #pass
    else: 
        logs.print_inf(name_function,f"[TYPE = {conf.lst_get('TYPE')}]")
        logs.print_inf(name_function,'VARIABLE TYPE CON VALOR NO RECONOCIDO ')
        

    
#   
# CALCULO TIEMPO DE DEMORA
#print(f'serv_APP_selection TERMINADO A {time()-sel_start_time} s')
#
