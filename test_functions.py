#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
TEST DE DRIVERS DE AUTOMATISMO

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.0 16-04-2020 12:58
''' 

print(__doc__)

import sys
import os


from drv_dlg import douts,read_param,pump1,emerg_system
from mypython import not_dec



# FUNCION PARA LEER EL VALOR DE LOS PARAMETROS DE ENTRADA DEL DATALOGGER
#DLGID = 'UYCOL601'
DLGID = 'MER007'
PARAM = 'DATE'   #[DATE,TIME, other names in the data's frame]
print(f"read_ param => {read_param(DLGID,PARAM)}")


# FUNCION PARA PONER EL VALOR EN LA SALIDA DIGITAL d2:d0
DLGID = 'MER006'
OUT_DEC = 7     # VALOR EN DECIMAL QUE VA A TOMAR LA SALIDA DIGITAL PARA EL VARIADOR DE FRECEUNCIA
#OUT_DEC = not_dec(OUT_DEC,3)        # PARA PROBAR INVIRTIENDO LAS SALIDAS SACAR COMENTARIO A ESTA LINEA
douts(DLGID,OUT_DEC)


# FUNCION PARA PRENDER LA BOMBA 1
DLGID = 'MER006'
ACTION = False     # [True = PRENDER | False = APAGAR]
pump1(DLGID,ACTION)

# FUNCION PARA PONER EL AUTOMATISMO A TRABAJAR POR EL SISTEMA DE EMERGENCIA
DLGID = 'MER006'
emerg_system(DLGID)




