#!/usr/aut_env/bin/python3.8
'''
SERVICIO DE DETECCION DE AUTOMATISMOS

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.4 28-04-2020
''' 

import sys
from spy_log import *

STR_CONFIG = ''

if __name__ == '__main__':
    STR_CONFIG = sys.argv[1]
    config_logger()
    log(module=__name__, server='ULI', function='serv_APP_selection2', dlgid=STR_CONFIG, msg="ESTO ESTA FUNCIONANDO")

# # ABRO EL ARCHIVO LOG
# log = open('/var/log/test2.log','a')
# # EXCRIBIMOS EL LOG
# log.write(f"ESTO ESTA FUNCIONANDO\n") 
# log.write(f"EL DLGID ES {STR_CONFIG}\n") 
        
# # CERRAMOS EL LOG
# log.close()
