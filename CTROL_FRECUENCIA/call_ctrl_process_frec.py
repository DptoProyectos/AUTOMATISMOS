#!/usr/bin/python3 -u
'''
Created on 8 mar. 2020

@author: root
'''

## LIBRERIAS
import os                                               # EJECUCION DE ARCHIVOS CON PARAMETROS


############################# VARIABLES ################################


#VARIABLES GLOBALES DE CONFIGURACION
print_log = 'SI'                                       # VER LOS LOGS EN CONSOLA [ SI | NO ]
DLGID_CTRL = 'MER006'                                  # ID DATALOGGER QUE EJECUTA LAS ACCIONES DE CONTROL


# LLAMADO DEL PROGRAMA 
os.system('PROCESS/ctrl_process_frec.py %s %s %s'%(DLGID_CTRL,'CHARGE',print_log)) 