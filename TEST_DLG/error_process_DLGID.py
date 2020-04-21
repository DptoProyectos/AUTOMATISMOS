#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
LLAMADO CON PARAMETROS A APLICACION DE CONTROL DE ERRORES EN CTRL_FREC

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.6 17-04-2020 14:17
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
                'DLGID',            'UYCOL601',                     # ID DATALOGGER QUE EJECUTA LAS ACCIONES DE CONTROL
                'TYPE',             'TEST_DLG',                     # [ TEST_DLG | DELETED ] 
                                                                    # DELETED => PARA DEJAR DE EJECUTAR EL SCRIPT QUE DETECTA ERRORES
                
                
                #VARIABLES DE CONFIGURACION
                'SWITCH_OUTPUTS',   False,                          # ALTERNA LAS SALIDAS Y TESTEA QUE LAS ENTRADAS LAS SIGAN [ True | False]
                'EVENT_DETECTION',  False,                          # FORMA EN QUE EL VARIADOR DE VELOCIDAD DETECTA LAS ENTRADAS [ NPN (not_in)| PNP] 
                'TIMER_POLL',       5,                              # TIEMPO DE POLLEO (en min) AL CUAL ESTA TRABAJANDO EL EQUIPO A TESTEAR
            ]






# CONVIERTO A STRIG
STR_CONFIG = lst2str(LIST_CONFIG)
#
# OBTENER LA CARPETA ANTERIOR A LA DE LA RUTA DEL ARCHIVO
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# LLAMADO DEL PROGRAMA 
os.system('{0}/serv_error_APP_selection.py {1}'.format(file_path,STR_CONFIG)) 
#os.system('{0}/serv_APP_selection.py'.format(file_path)) 
#
# CALCULO TIEMPO DE DEMORA
#print(f'control_process_frec_{LIST_CONFIG[3]} TERMINADO A {time()-gen_start_time} s')



###