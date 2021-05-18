#!/usr/aut_env/bin/python3.8
'''
SERVICIO DE DETECCION DE AUTOMATISMOS

Created on 16 mar. 2020 

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

#---------------------------------------------------------------------------------------- 
# CONFIGURO LAS ENTRADAS DE CONFIGURACION 
if __name__ == '__main__':
    # LEO EL STR DE CONFIGURACION   
    
    try:    
        STR_CONFIG = sys.argv[1]
        LIST_CONFIG = STR_CONFIG.split(',')
    except:
        print('HELP')
        print('    ARGUMENT = DLGID_CTRL')
        print('    EX:')
        print('    ./serv_APP_selection.py DLGID_CTRL')
        quit()
        
    #
    # INSTANCIAS
    conf = config_var(STR_CONFIG) 
    redis = Redis()
    #
    
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
        
    
#----------------------------------------------------------------------------------------    
def read_config_var(DLGID_CTRL):
    ''''''
    
    FUNCTION_NAME = 'READ_CONFIG_VAR'
    
    ## INSTANCIAS
    logs = ctrl_logs(False,'servAppSelection',DLGID_CTRL,print_log)
    redis = Redis()
    # 
    # LEO LOS TAGS DE CONFIGURACION
    #if redis.hexist(DLGID_CTRL,'TAG_CONFIG'): 
    if gda.readAutConf(DLGID_CTRL,'TAG_CONFIG'): 
        #TAG_CONFIG = redis.hget(DLGID_CTRL,'TAG_CONFIG')
        TAG_CONFIG = gda.readAutConf(DLGID_CTRL,'TAG_CONFIG')
        TAG_CONFIG = TAG_CONFIG.split(',')
    else: 
        logs.print_inf(FUNCTION_NAME,'NO EXISTE LA VARIABLE TAG_CONFIG')
        logs.print_inf(FUNCTION_NAME,'NO SE EJECUTA EL SCRIPT')
        quit()
    #
    # LEO CONFIGUTACION DE LA REDIS
    logs.print_inf(FUNCTION_NAME,'LEO CONFIG EN REDIS')
    vars_config = []
    for param in TAG_CONFIG:
        vars_config.append(param)
        #vars_config.append(redis.hget(DLGID_CTRL,param))
        vars_config.append(gda.readAutConf(DLGID_CTRL,param))
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
    logs = ctrl_logs(False,'servAppSelection',DLGID_CTRL,print_log)
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
            #redis.hset(DLGID_CTRL,LIST_CONFIG[n],LIST_CONFIG[n+1])              # escritura de valores en la redis
            gda.InsertAutConf(DLGID_CTRL,LIST_CONFIG[n],LIST_CONFIG[n+1])       # escritura de valores en dbGda
            n += 2
    
    # ELIMINO LAS VARIABLES DE CONFIGURACION ANTERIORES
    #if redis.hexist(DLGID_CTRL,'TAG_CONFIG'):
    if gda.readAutConf(DLGID_CTRL,'TAG_CONFIG'):
        #last_TAG_CONFIG = redis.hget(DLGID_CTRL,'TAG_CONFIG')
        last_TAG_CONFIG = gda.readAutConf(DLGID_CTRL,'TAG_CONFIG')
    
           
        for param in last_TAG_CONFIG.split(','):
            #redis.hdel(DLGID_CTRL, param)
            gda.DeleteAutConf(DLGID_CTRL, param)
            
            
        #redis.hdel(DLGID_CTRL,'TAG_CONFIG')
        gda.DeleteAutConf(DLGID_CTRL,'TAG_CONFIG')
       
        
        
    # ESCRIBO EN REDIS EL NOMBRE DE LAS VARIABLES DE CONFIGURACION PARA QUE PUEDAN SER LEIDAS
    TAG_CONFIG = []
    n = 4
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            #redis.hset(DLGID_CTRL,LIST_CONFIG[n],LIST_CONFIG[n+1])
            gda.InsertAutConf(DLGID_CTRL,LIST_CONFIG[n],LIST_CONFIG[n+1])
            TAG_CONFIG.append(LIST_CONFIG[n])
            n += 2
    #redis.hset(DLGID_CTRL,'TAG_CONFIG',lst2str(TAG_CONFIG))
    gda.InsertAutConf(DLGID_CTRL,'TAG_CONFIG',lst2str(TAG_CONFIG)) 
    
    
    # LEO VARIABLES ESCRITAS
    n = 4
    check_config = []
    for param in LIST_CONFIG:
        if n < (len(LIST_CONFIG)): 
            check_config.append(LIST_CONFIG[n])
            #check_config.append(redis.hget(DLGID_CTRL,LIST_CONFIG[n]))
            check_config.append(gda.readAutConf(DLGID_CTRL,LIST_CONFIG[n]))
            n += 2
    #
    # MUESTRO VARIABLES LEIDAS
    n = 0
    for param in check_config:
        if n < (len(check_config)): 
            logs.print_out(FUNCTION_NAME,check_config[n],check_config[n+1])
            n += 2

def add_2_RUN(dlgid,type):
    '''
        funcion que anade a serv_error_APP_selection / RUN 
        el DLGID_CTRL y el DLGID_REF
    '''
    
    name_function = 'ADD_VAR_TO_RUN'
    
    # PREPARO EL RUN EN serv_error_APP_selection
    if gda.readAutConf('serv_error_APP_selection','RUN'):
        #TAG_CONFIG = redis.hget('serv_error_APP_selection', 'RUN')
        TAG_CONFIG = gda.readAutConf('serv_error_APP_selection', 'RUN')

        lst_TAG_CONFIG = str2lst(TAG_CONFIG)
        try:
            lst_TAG_CONFIG.index(dlgid)
            #logs.print_out(name_function, 'RUN', TAG_CONFIG)
        except:
            lst_TAG_CONFIG.append(dlgid)
            str_TAG_CONFIG = lst2str(lst_TAG_CONFIG)
            #redis.hset('serv_error_APP_selection', 'RUN', str_TAG_CONFIG)
            gda.InsertAutConf('serv_error_APP_selection', 'RUN', str_TAG_CONFIG)
            #logs.print_out(name_function, 'RUN', str_TAG_CONFIG)
            
    else:
        #redis.hset('serv_error_APP_selection', 'RUN', dlgid)
        gda.InsertAutConf('serv_error_APP_selection', 'RUN', dlgid)
        
    # PREPARO LA VARIABLE TYPE CON SU VALOR
    if not(gda.readAutConf(f'{dlgid}_ERROR', 'TAG_CONFIG')):
        #redis.hset(f'{dlgid}_ERROR', 'TAG_CONFIG', 'TYPE')
        gda.InsertAutConf(f'{dlgid}_ERROR', 'TAG_CONFIG', 'TYPE')
        #redis.hset(f'{dlgid}_ERROR', 'TYPE', type)
        gda.InsertAutConf(f'{dlgid}_ERROR', 'TYPE', type)
    
def show_var_list(lst):
    n = 0
    for param in lst:
        if n < (len(lst)): 
            logs.print_out(name_function,lst[n],lst[n+1])
            n += 2
    
def run_ctrl_process(LIST_CONFIG):
    if bool(LIST_CONFIG):
        #
        # INSTANCIO config_var CON EL NUEVO LIST_CONFIG Y LEO TYPE
        conf = config_var(LIST_CONFIG)
        TYPE = conf.lst_get('TYPE')
        #
        import importlib.util
        #
        '''
        spec = importlib.util.spec_from_file_location("archivo",'{0}/{1}/PROCESS/ctrl_process.py'.format(project_path,TYPE))
        archivo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(archivo)
        call_ctrl_process = True'''
              
        
        try:
            spec = importlib.util.spec_from_file_location("archivo",'{0}/{1}/PROCESS/ctrl_process.py'.format(project_path,TYPE))
            archivo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(archivo)
            call_ctrl_process = True
        except:
            logs.print_inf(name_function, f'NO SE ENCUENTRA ../{TYPE}/PROCESS/ctrl_process.py O EL MISMO TIENE ERRORES')
            call_ctrl_process = False
        #
        if call_ctrl_process:
            archivo.control_process(LIST_CONFIG)
            
def run_perforation_process(dlgid):
    
    text = '''
    
    PERFORACIONES EN PERL
    '''
    
    #logs.print_inf(name_function,text )
    
    import os;

    #path = '/datos/cgi-bin/spx/PERFORACIONES/'
    path = perforationProcessPath
    file = 'ext_call.pl'
    param = '--dlgid'
    param_value = dlgid
    
    '''
    # bloque para alternar las salidas mediante el error_perf_test cada vez que llega un dato del datlogger
    if dlgid == 'PTEST05':
        try:
            os.system('/datos/cgi-bin/spx/PERFORACIONES/TEST_EQUIPOS/error_perf_test_PTEST05.pl')
        except:
            logs.print_inf(name_function, 'ERROR AL CORRER CALLBACK PARA {0}'.format(dlgid))
    '''

    try:
        os.system('{0}{1} {2} {3}'.format(path,file,param,param_value));
    except:
        logs.print_inf(name_function, 'ERROR AL CORRER LAS PERFORACIONES EN PERL')
        
       
    
#----------------------------------------------------------------------------------------      

name_function = 'APP_SELECTION'

## INSTANCIAS
logs = ctrl_logs(False,'servAppSelection',DLGID_CTRL,print_log)
redis = Redis()
gda = GDA(dbUrl)

# SE CORRE EL PROCESO DE LAS PERFORACIONES EN PERL
run_perforation_process(DLGID_CTRL)

# AQUI COMIENZA LO QUE SERIA EL AUTOATISMO EN PYTON
text = '''
    
    AUTOMATISMOS EN PYTHON
    '''
#logs.print_inf(name_function,text )


## VARIABLES GLOBALES QUE LE ENTRAN A CORE
#logs.print_log(f"EXECUTE: {name_function}")      
#
# VARIABLES DE EJECUCION
if conf.str_get('print_log'):
    logs.print_in(name_function,'print_log',print_log)
    logs.print_in(name_function,'DLGID_CTRL',DLGID_CTRL)
#
## VARIABLES PARTICULARES QUE LE ENTRAN A APP_SELECTION
#

if TYPE in allowedTypes:
#if TYPE in str2lst(config['CTRL_CONFIG']['CTRL_ID']):
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
        #if redis.hexist(DLGID_CTRL,'TYPE'):
        if gda.readAutConf(DLGID_CTRL,'TYPE'):
            logs.print_inf(name_function,'READ_CONFIG_VAR')
            #LEO LAS VARIABLES DE CONFIGURACION
            LIST_CONFIG=read_config_var(DLGID_CTRL)
            
        else: 
            #logs.print_inf(name_function,'NO EXISTE LA VARIABLE TYPE')
            #logs.print_inf(name_function,'NO SE EJECUTA EL SCRIPT')
            LIST_CONFIG=[]



if bool(LIST_CONFIG):
    conf = config_var(LIST_CONFIG) 
    if conf.lst_get('TYPE') in allowedTypes:
        #
        # ANADO DLGID_CTRL A 'DLGID_CTRL_TAG_CONFIG' PARA QUE SE EJECUTE EL ctrl_error_frec
        add_2_RUN(conf.lst_get('DLGID_CTRL'),conf.lst_get('TYPE'))
        #
        # ANADO DLGID_REF A 'DLGID_CTRL_TAG_CONFIG' PARA QUE SE EJECUTE EL ctrl_error_frec
        if conf.lst_get('DLGID_REF'):
            add_2_RUN(conf.lst_get('DLGID_REF'),conf.lst_get('TYPE'))
        #
        # MUESTRO LAS VARIABLES QUE SE LE VAN A PASAR AL PROCESS Y LO LLAMO
        show_var_list(LIST_CONFIG)
        #
        # LLAMO AL PROCESS DEL AUTOMATISMO Y LE PASO LIST_CONFIG
        run_ctrl_process(LIST_CONFIG)
        #
    else: 
        logs.print_inf(name_function,f"[TYPE = {conf.lst_get('TYPE')}]")
        logs.print_inf(name_function,'VARIABLE TYPE CON VALOR NO RECONOCIDO ')
        

    
#   
# CALCULO TIEMPO DE DEMORA
#print(f'serv_APP_selection TERMINADO A {time()-sel_start_time} s')
#
