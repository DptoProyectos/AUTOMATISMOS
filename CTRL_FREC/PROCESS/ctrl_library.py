#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
Created on 15 mar. 2020

version: 1.0.6

@author: Yosniel Cabrera
'''

# LIBRERIAS
import redis
import json

#CONEXIONES
from drv_logs import *
from drv_redis import Redis
from drv_dlg import *
from mypython import *
from drv_dlg import douts






# CLASES DE LA LIBRERIA
class ctrl_process_frec(object):
    '''
    FUNCIONES USADAS POR ctrl_process_frec.py
    '''
    
    def __init__(self,LIST_CONFIG):
        '''
        Constructor
        '''
        #
        ## DEFINICION DE VARIABLES DE LA CLASE
        self.config = config_var(LIST_CONFIG)
        self.print_log = self.config.lst_get('print_log')
        self.DLGID_CTRL = self.config.lst_get('DLGID_CTRL')
        self.TYPE = self.config.lst_get('TYPE')
        self.ENABLE_OUTPUTS = self.config.lst_get('ENABLE_OUTPUTS')
        self.ENABLE_OUTPUTS = str2bool(self.config.lst_get('ENABLE_OUTPUTS'))
        
        self.TYPE_IN_FREC = self.config.lst_get('TYPE_IN_FREC')
        self.DLGID_REF = self.config.lst_get('DLGID_REF')
        self.CHANNEL_REF = self.config.lst_get('CHANNEL_REF')
        self.TYPE_IN_FREC = self.config.lst_get('TYPE_IN_FREC')
        self.DLGID_REF_1 = self.config.lst_get('DLGID_REF_1')
        self.CHANNEL_REF_1 = self.config.lst_get('CHANNEL_REF_1')
        
        ## INSTANCIAS
        self.logs = ctrl_logs('CTRL_FREC',self.DLGID_CTRL,self.print_log)
        self.redis = Redis()
        
    def chequeo_alarmas(self):
        
        name_function = 'CHEQUEO_ALARMAS'
        
        # PIERTA DEL GABINETE
        if read_param(self.DLGID_CTRL,'GA') == '1':
            self.logs.print_inf(name_function, 'GABINETE ABIERTO')
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, 'GABINETE_ABIERTO', 'SI')
        elif read_param(self.DLGID_CTRL,'GA') == '0':
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, 'GABINETE_ABIERTO', 'NO')
        else:
            self.logs.print_inf(name_function, f"error in {name_function}, GA = {read_param(self.DLGID_CTRL,'GA')}")
            # DEJAR REGISTRO DEL ERROR
            self.logs.script_performance(f"error in {name_function}, GA = {read_param(self.DLGID_CTRL,'GA')}")
            
        # FALLA ELECTRICA
        if read_param(self.DLGID_CTRL,'FE') == '1':
            self.logs.print_inf(name_function, 'FALLA ELECTRICA')
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, 'FALLA_ELECTRICA', 'SI')
        elif read_param(self.DLGID_CTRL,'FE') == '0':
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, 'FALLA_ELECTRICA', 'NO')
        else:
            self.logs.print_inf(name_function, f"error in {name_function}, FE = {read_param(self.DLGID_CTRL,'FE')}")
            # DEJAR REGISTRO DEL ERROR
            self.logs.script_performance(f"error in {name_function}, FE = {read_param(self.DLGID_CTRL,'FE')}")
             
        # FALLA TERMICA 1
        if read_param(self.DLGID_CTRL,'FT1') == '1':
            self.logs.print_inf(name_function, 'FALLA TERMICA 1')
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, 'FALLA_TERMICA_1', 'SI')
        elif read_param(self.DLGID_CTRL,'FT1') == '0':
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, 'FALLA_TERMICA_1', 'NO')
        else:
            self.logs.print_inf(name_function, f"error in {name_function}, FT1 = {read_param(self.DLGID_CTRL,'FT1')}")
            # DEJAR REGISTRO DEL ERROR
            self.logs.script_performance(f"error in {name_function}, FT1 = {read_param(self.DLGID_CTRL,'FT1')}")
        
    def chequeo_sensor(self):
        
        name_function = 'CHEQUEO_SENSOR'
    
        # SI NO EXISTE LA VARIABLE ERR_SENSOR EN DLGID_REF LA CREO CON VALOR NO
        if not(self.redis.hexist(self.DLGID_REF, 'ERR_SENSOR')): self.redis.hset(self.DLGID_REF, 'ERR_SENSOR', 'NO')
                 
        return True
    
    def modo_remoto(self):
        
        name_function = 'MODO_REMOTO'
        pump_state = False
        #
        # SI NO EXISTE SW2 LO CREO CON VALOR OFF
        if not(self.redis.hexist(self.DLGID_CTRL, 'SW2')): self.redis.hset(self.DLGID_CTRL, 'SW2', 'OFF')
        #
        # REVISO LA ACCION TOMADA EN EL SERVER RESPECTO A LA BOMBA
        if self.redis.hget(self.DLGID_CTRL, 'SW2') == 'ON':
            self.logs.print_inf(name_function, 'PRENDER BOMBA')
            pump_state = True
            #
        elif self.redis.hget(self.DLGID_CTRL, 'SW2') == 'OFF':    
            self.logs.print_inf(name_function, 'APAGAR BOMBA')
            #
        else:
            self.logs.print_inf(name_function, f"error in {name_function}, SW2 = {read_param(self.DLGID_CTRL,'SW2')}")
            # DEJAR REGISTRO DEL ERROR
            self.logs.script_performance(f"error in {name_function}, SW2 = {read_param(self.DLGID_CTRL,'SW2')}")
        
        
        # REVISO ACCION DE LAS SALIDAS    
        if self.ENABLE_OUTPUTS:
            if pump_state:
                # SETEO LA MAXIMA FRECUENCIA PARA MADAR A PRENDER LA BOMBA
                if self.TYPE_IN_FREC == 'NPN':
                    douts(self.DLGID_CTRL,not_dec(7,3))
                elif self.TYPE_IN_FREC == 'PNP': 
                    douts(self.DLGID_CTRL,7)
                else: 
                    self.logs.print_inf(name_function, f"error in {name_function}, TYPE_IN_FREC = {self.TYPE_IN_FREC}")    
                    self.logs.script_performance(f"error in {name_function}, TYPE_IN_FREC = {self.TYPE_IN_FREC}")
                    
            # MANDOLA ACCION A LA BOMBA
            pump1(self.DLGID_CTRL, pump_state)    
                
        else:
            self.logs.print_inf(name_function, f"SALIDAS DESCACTIVADAS [ENABLE_OUTPUTS = {self.ENABLE_OUTPUTS}]")    
            self.logs.script_performance(f"{name_function} ==> SALIDAS DESCACTIVADAS [ENABLE_OUTPUTS = {self.ENABLE_OUTPUTS}]")
            
    def control_sistema(self):
        
        name_function = 'CONTROL_SISTEMA'
        
        # SI NO EXISTE LMIN LO CREO CON VALOR 1
        if not(self.redis.hexist(self.DLGID_CTRL, 'LMIN_TQA')): self.redis.hset(self.DLGID_CTRL, 'LMIN_TQA', 1)
        # SI NO EXISTE LMAX LO CREO CON VALOR 1.5
        if not(self.redis.hexist(self.DLGID_CTRL, 'LMAX_TQA')): self.redis.hset(self.DLGID_CTRL, 'LMAX_TQA', 1.5)
        #
        # LEO LAS VARIABLES LMIN Y LMAX
        LMIN = float(self.redis.hget(self.DLGID_CTRL, 'LMIN_TQA'))
        LMAX = float(self.redis.hget(self.DLGID_CTRL, 'LMAX_TQA'))
        
        if self.redis.hexist(self.DLGID_REF,'LINE'):
            REF = float(read_param(self.DLGID_REF,self.CHANNEL_REF))
        else:
            self.logs.script_performance(f"error in {name_function}, {self.CHANNEL_REF} = {read_param(self.DLGID_CTRL,self.CHANNEL_REF)}")
        
            
        self.logs.print_in(name_function, 'ENABLE_OUTPUTS', self.ENABLE_OUTPUTS)
        self.logs.print_in(name_function, 'TYPE_IN_FREC', self.TYPE_IN_FREC)
        self.logs.print_in(name_function, 'LMIN', LMIN)
        self.logs.print_in(name_function, 'LMAX', LMAX)
        self.logs.print_in(name_function, 'REF', REF)
        
        
        # SI NO FREC LMIN LO CREO CON VALOR 0
        if not(self.redis.hexist(self.DLGID_CTRL, 'FREC')): self.redis.hset(self.DLGID_CTRL, 'FREC', 0)
        # LEO EL VALOR DE LA FRECUENCIA ACTUAL
        FREC = int(self.redis.hget(self.DLGID_CTRL, 'FREC'))
        self.logs.print_in(name_function, 'LAST_FREC', FREC)
        
        if REF < LMIN:
            self.logs.print_inf(name_function, 'PRESION BAJA')
            if FREC < 7: 
                FREC += 1
                self.logs.print_inf(name_function, 'SE AUMENTA LA FRECUENCIA')
                #
            else: 
                self.logs.print_inf(name_function, 'SE ALCANZA FRECUENCIA MAXIMA')
                self.logs.script_performance(f'{name_function} ==> SE ALCANZA FRECUENCIA MAXIMA')
                        
            
        elif REF > LMAX:
            self.logs.print_inf(name_function, 'PRESION ALTA')
            if FREC > 0: 
                FREC -= 1
                self.logs.print_inf(name_function, 'SE DISMINUYE LA FRECUENCIA')
        else: 
            self.logs.print_inf(name_function, 'PRESION DENTRO DEL RANGO SELECCIONADO')    
        
        
        # CHEQUE SI LAS SALIDAS TIENEN QUE ACOPLARSE A ENTRADAS NPN o PNP Y MANDO A SETEAR EN CASO DE ENABLE_OUTPUTS
        if self.ENABLE_OUTPUTS:
            if self.TYPE_IN_FREC == 'NPN':
                douts(self.DLGID_CTRL,not_dec(FREC,3))
            elif self.TYPE_IN_FREC == 'PNP': 
                douts(self.DLGID_CTRL,FREC)
            else: 
                self.logs.print_inf(name_function, f"error in {name_function}, TYPE_IN_FREC = {self.TYPE_IN_FREC}")    
                self.logs.script_performance(f"error in {name_function}, TYPE_IN_FREC = {self.TYPE_IN_FREC}")
        else:
            self.logs.print_inf(name_function, f"SALIDAS DESCACTIVADAS [ENABLE_OUTPUTS = {self.ENABLE_OUTPUTS}]")    
            self.logs.script_performance(f"{name_function} ==> SALIDAS DESCACTIVADAS [ENABLE_OUTPUTS = {self.ENABLE_OUTPUTS}]")
        
        self.logs.print_out(name_function, 'CURR_FREC', FREC)    
        self.redis.hset(self.DLGID_CTRL,'FREC',FREC)
            
