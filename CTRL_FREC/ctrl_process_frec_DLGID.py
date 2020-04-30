#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
LLAMADO CON PARAMETROS A APLICACION DE CONTROL CTRL_FREC

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.1 16-04-2020 12:58
''' 

## LIBRERIAS
import os                                                   

## CONEXIONES
from mypython import lst2str
from time import time 

  
gen_start_time = time()  
                                             

LIST_CONFIG = [
                #VARIABLES DE EJECUCION
                'print_log',        True,                           # VER LOS LOGS EN CONSOLA [ True | False ]
                'DLGID_CTRL',       'MER004',                       # ID DATALOGGER QUE EJECUTA LAS ACCIONES DE CONTROL
                'TYPE',             'CTRL_FREC',                    # [ CTRL_FREC | ]
                
                
                #VARIABLES DE CONFIGURACION
                'ENABLE_OUTPUTS',   True,                           # ACTIVA Y DESACTIVA LA ACCION DE LAS SALIDAS PARA ESTE DLGID_CTRL [ True | False]
                'TYPE_IN_FREC',     'NPN',                          # FORMA EN QUE EL VARIADOR DE VELOCIDAD DETECTA LAS ENTRADAS [ NPN (not_in)| PNP] 
                'DLGID_REF',        'MER005',                       # DATALOGGER QUE SE USA DE REFERENCIA PARA EL AUTOMATIMO
                'CHANNEL_REF',      'PMP',                          # NOMBRE DEL CANAL CON LA MEDIDA DE REFERENCIA PARA EL AUTOMATISMO
                'DLGID_REF_1',      '',                             # DATALOGGER AUXILIAR QUE SE VA A USAR DE REFERENCIA EN CASO DE FALLAS DE COMUNICACION DEL PRINCIPAL
                'CHANNEL_REF_1',    '',                             # NOMBRE DEL CANAL AUXILIAR CON LA MEDIDA DE REFERENCIA PARA EL AUTOMATISMO
                
            ]









# CONVIERTO A STRIG
STR_CONFIG = lst2str(LIST_CONFIG)




    
# OBTENER LA CARPETA ANTERIOR A LA DE LA RUTA DEL ARCHIVO
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# LLAMADO DEL PROGRAMA 
os.system('{0}/serv_APP_selection.py {1}'.format(file_path,STR_CONFIG)) 
#os.system('{0}/serv_APP_selection.py'.format(file_path)) 
#
# CALCULO TIEMPO DE DEMORA
#print(f'control_process_frec_{LIST_CONFIG[3]} TERMINADO A {time()-gen_start_time} s')



###
