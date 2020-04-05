#!/drbd/www/cgi-bin/spx/AUTOMATISMOS/myenv/bin/python3.6
'''
Created on 20 mar. 2020

@author: Yosniel Cabrera
'''

#CONEXIONES
from drv_redis import Redis


# FUNCIONES
def douts(dlgid,out_dec):
    '''
    DESCRIPTION
        Se encarga de poner en la salida digital (d2,d1,d0) el valor que se le pasa en decimal sin afectar las otras entradas
        
    LEYENDA:
        dlgid => datalogger id
        out_dec => numero decimal que se va a querer porner en las salidas digitales (d2,d1,d0)
        EJ: douts(MER006,7)
    '''
    ## INSTANCIAS
    redis = Redis()
    #
    # LEO LA SALIDA ACTUAL SETEADA
    last_out = redis.hget(dlgid,'OUTPUTS')
    # APLICO LA MASCARA 0000011
    last_out = int(last_out) & int('0000011',2)
    # 
    #
    #
    # APLICO LA MASCARA 0000111 A no_dec
    out_dec = int(out_dec) & int('0000111',2)
    # HAGO UN BITWISE LEFT 3 UNIDADES
    out_dec = out_dec << 3
    #
    #
    # CONCATENO LOS DOS PRIMEROS BITS CON LA SALIDA DIGITAL
    out = out_dec | last_out
    #
    #
    # MANDO A SETEAR LAS SALIDAS DEL DATALOGGER
    redis.hset(dlgid,'OUTPUTS',out)
    
def pump1(dlgid,action):
    '''
    DESCRIPTION
        Se encarga de prender o apagar la bomba 1 del sistema
        
    LEYENDA:
        dlgid => datalogger id
        action => [True (PRENDER BOMBA) | False (APAGAR BOMBA)]
        EJ: pump1('MER006',True)
    '''
    ## INSTANCIAS
    redis = Redis()
    #
    #
    # LEO LA SALIDA ACTUAL SETEADA
    last_out = redis.hget(dlgid,'OUTPUTS')
    # APLICO LA MASCARA 1111100
    last_out = int(last_out) & int('1111100',2)
    #
    #
    # VEO QUE ACCION ES LA SELECCIONADA
    if action: out = last_out | int('11',2)
    else: out = last_out | int('1',2)
    #
    #
    # MANDO A SETEAR LAS SALIDAS DEL DATALOGGER
    redis.hset(dlgid,'OUTPUTS',out)
    
def read_param(dlgid,param):
    '''
    DESCRIPTION
        Se encarga de leer del datalogger el canal con el nombre 'param'
        
    LEYENDA:
        dlgid => datalogger id
        param => nombre del canal que se quiere leer
                 si se quiere leer la fecha param = DATE
                 si se quiere leer la hora param = TIME
        EJ: read_param('MER001','PA')
    '''
    
    def head_detect(line, key_word):
        '''
        DETECTA SI LA CABECERA DEL line HAY ESTE key_word
        '''
        i = 0
        match = 0
        for char in key_word:
            if line[i] == char:
                match += 1
            i += 1
        if match == 4: return True
        else: return False
    
    
    ## INSTANCIAS
    redis = Redis()
    # LEO LINE
    if redis.hexist(dlgid, 'LINE'): line = redis.hget(dlgid,'LINE')
    else: line = ''
    
    # DETECTO SI EXISTE CABECERA LINE
    if head_detect(line,'LINE'):
        parsed_line = line.split(';')
        #
        # CREO UNA LISTA A PARTIR DE SEPARAR LOS CAMPOS DEL LINE
        n = 0
        my_list = []
        for elements in parsed_line:
            fields = elements.split(':')
            my_list.append(fields[0])
            try:
                my_list.append(fields[1])
            except:
                pass
      
            n = n+1
            
        # VEO SI SE ESTA SELECCIONADO DATE O TIME 
        if param == 'DATE': out = my_list[1]
        else: 
            try:
                out = my_list[my_list.index(param)+1]
            except:
                out = '' 
        return out
        
    else:
        
        parsed_line = line.split(',')
        #
        # CREO UNA LISTA A PARTIR DE SEPARAR LOS CAMPOS DEL LINE
        n = 0
        my_list = []
        for elements in parsed_line:
            fields = elements.split('=')
            my_list.append(fields[0])
            try:
                my_list.append(fields[1])
            except:
                pass
      
            n = n+1  
        #
        # VEO SI SE ESTA SELECCIONADO DATE O TIME 
        if param == 'DATE': out = my_list[1]
        elif param == 'TIME': out = my_list[2]
        else: 
            try:
                out = my_list[my_list.index(param)+1]
            except:
                out = '' 
        return out

def emerg_system(dlgid):
    '''
    DESCRIPTION
        Se encarga de poner a funcionar el sitema de emergencia
        
    LEYENDA:
        dlgid => datalogger id
        EJ: pump1('MER006',True)
    '''
    ## INSTANCIAS
    redis = Redis()
    #
    #
    # LEO LA SALIDA ACTUAL SETEADA
    last_out = redis.hget(dlgid,'OUTPUTS')
    # APLICO LA MASCARA 1111010
    last_out = int(last_out) & int('1111010',2)
    #
    #
    # MANDO A SETEAR LAS SALIDAS DEL DATALOGGER
    redis.hset(dlgid,'OUTPUTS',last_out)
    

 
