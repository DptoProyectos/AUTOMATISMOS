#!/drbd/www/cgi-bin/spx/AUTOMATISMOS/myenv/bin/python3.6


'''
Created on 8 mar. 2020

@author: Yosniel Cabrera
'''

## LIBRERIAS
import os    
from time import time   
gen_start_time = time()                                           

## CONEXIONES
from mypython import lst2str
                                             

LIST_CONFIG = [
                #VARIABLES DE EJECUCION
                'print_log', True,                          # VER LOS LOGS EN CONSOLA [ True | False ]
                'DLGID_CTRL', 'MER007',                     # ID DATALOGGER QUE EJECUTA LAS ACCIONES DE CONTROL
                
            ]



# CONVIERTO A STRIG
STR_CONFIG = lst2str(LIST_CONFIG)
#
# OBTENER LA CARPETA ANTERIOR A LA DE LA RUTA DEL ARCHIVO
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# LLAMADO DEL PROGRAMA 
os.system('{0}/serv_APP_selection.py {1}'.format(file_path,STR_CONFIG)) 
#
# CALCULO TIEMPO DE DEMORA
#print(f'call_ctrl_process_frec TERMINADO A {time()-gen_start_time} s')


#