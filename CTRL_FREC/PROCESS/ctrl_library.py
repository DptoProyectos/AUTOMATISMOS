#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
LIBRERIA DE APLICACION CTRL_FREC

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.3 16-04-2020 12:58
''' 

# LIBRERIAS
import redis
import json

#CONEXIONES
from CTRL_FREC.PROCESS.drv_visual import dic
from drv_logs import *
from drv_redis import Redis
from drv_dlg import douts,pump1,emerg_system,read_param,dlg_detection
from mypython import lst2str,str2lst,str2bool,not_dec,config_var
from _ast import Pass




# CLASES DE LA LIBRERIA
class ctrl_process(object):
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
        self.logs = ctrl_logs(self.TYPE,self.DLGID_CTRL,self.print_log)
        self.redis = Redis()
        
    def chequeo_alarmas(self):
        
        name_function = 'CHEQUEO_ALARMAS'
        
        # PIERTA DEL GABINETE
        if read_param(self.DLGID_CTRL,'GA') == '1':
            self.logs.print_inf(name_function, 'GABINETE_ABIERTO')
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('GABINETE_ABIERTO', 'name'), dic.get_dic('TX_ERROR', 'True_value'))
        elif read_param(self.DLGID_CTRL,'GA') == '0':
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('GABINETE_ABIERTO', 'name'), dic.get_dic('TX_ERROR', 'False_value'))
        else:
            self.logs.print_inf(name_function, f"error in {name_function}, GA = {read_param(self.DLGID_CTRL,'GA')}")
            # DEJAR REGISTRO DEL ERROR
            self.logs.script_performance(f"error in {name_function}, GA = {read_param(self.DLGID_CTRL,'GA')}")
            
        # FALLA ELECTRICA
        if read_param(self.DLGID_CTRL,'FE') == '1':
            self.logs.print_inf(name_function, 'FALLA ELECTRICA')
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('FALLA_ELECTRICA', 'name'), dic.get_dic('FALLA_ELECTRICA', 'True_value'))
        elif read_param(self.DLGID_CTRL,'FE') == '0':
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('FALLA_ELECTRICA', 'name'), dic.get_dic('FALLA_ELECTRICA', 'False_value'))
        else:
            self.logs.print_inf(name_function, f"error in {name_function}, FE = {read_param(self.DLGID_CTRL,'FE')}")
            # DEJAR REGISTRO DEL ERROR
            self.logs.script_performance(f"error in {name_function}, FE = {read_param(self.DLGID_CTRL,'FE')}")
             
        # FALLA TERMICA 1
        if read_param(self.DLGID_CTRL,'FT1') == '1':
            self.logs.print_inf(name_function, 'FALLA TERMICA 1')
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('FALLA_TERMICA_1', 'name'), dic.get_dic('FALLA_ELECTRICA', 'True_value'))
        elif read_param(self.DLGID_CTRL,'FT1') == '0':
            # ESCRIBO LA ALARMA EN REDIS
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('FALLA_TERMICA_1', 'name'), dic.get_dic('FALLA_ELECTRICA', 'False_value'))
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
        if not(self.redis.hexist(self.DLGID_CTRL, 'SW2')): 
            self.redis.hset(self.DLGID_CTRL, 'SW2', 'OFF')
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
        if not(self.redis.hexist(self.DLGID_CTRL, dic.get_dic('LMIN', 'name'))): 
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('LMIN', 'name'), dic.get_dic('LMIN', 'True_value'))
        # SI NO EXISTE LMAX LO CREO CON VALOR 1.5
        if not(self.redis.hexist(self.DLGID_CTRL, dic.get_dic('LMAX', 'name'))): 
            self.redis.hset(self.DLGID_CTRL, dic.get_dic('LMAX', 'name'), dic.get_dic('LMAX', 'True_value'))
        #
        # LEO LAS VARIABLES LMIN Y LMAX
        LMIN = float(self.redis.hget(self.DLGID_CTRL, dic.get_dic('LMIN', 'name')))
        LMAX = float(self.redis.hget(self.DLGID_CTRL, dic.get_dic('LMAX', 'name')))
        
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
        
        # CHEQUEO SI LAS SALIDAS TIENEN QUE ACOPLARSE A ENTRADAS NPN o PNP Y MANDO A SETEAR EN CASO DE ENABLE_OUTPUTS
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

class error_process(object):  
    '''
    FUNCIONES USADAS POR ctrl_error_frec.py
    '''
    
    def __init__(self,LIST_CONFIG):
        '''
        Constructor
        '''
        #
        self.config = config_var(LIST_CONFIG)
        #
        
        #VARIABLES DE EJECUCION
        self.print_log = self.config.lst_get('print_log')
        self.DLGID = self.config.lst_get('DLGID')
        self.TYPE = self.config.lst_get('TYPE')
        #
        #VARIABLES DE CONFIGURACION
        self.SWITCH_OUTPUTS = str2bool(self.config.lst_get('SWITCH_OUTPUTS'))
        self.EVENT_DETECTION = str2bool(self.config.lst_get('EVENT_DETECTION'))
        
        ## INSTANCIAS
        self.logs = ctrl_logs(self.TYPE,self.DLGID,self.print_log)
        self.redis = Redis()   
        
    
    def test_tx(self):
        '''
        detecta errores tx y RTC
        return '' =>     si no existe el line del datalogger
        return False =>  si hay errores TX de cualquier tipo
        return True =>   cualquier otra opcion
        '''
        
        name_function = 'TEST_TX_ERRORS'
        
        # CHEQUEO DE ERROR TX
        #
        
        # CHEQUEO SI EXISTE EL LINE EN EL DATALOGGER
        if not(self.redis.hexist(self.DLGID, 'LINE')):
            self.logs.print_inf(name_function, f'NO EXISTE VARIABLE LINE EN {self.DLGID}')
            self.logs.print_inf(name_function, f'NO SE EJECUTA {name_function}')
            self.logs.script_performance(f'NO EXISTE VARIABLE LINE EN {self.DLGID}')
            return ''
        
        # DEVUELVO last_line CON EL LINE ANTERIOR Y current_line CON EL LINE ACTUAL
        if self.redis.hexist(f'{self.DLGID}_ERROR', 'last_line'):
            last_line = self.redis.hget(f'{self.DLGID}_ERROR', 'last_line')
            current_line = self.redis.hget(self.DLGID, 'LINE')
            self.redis.hset(f'{self.DLGID}_ERROR', 'last_line', current_line)
        else:
            last_line = self.redis.hget(self.DLGID, 'LINE')
            self.redis.hset(f'{self.DLGID}_ERROR', 'last_line', last_line)
            current_line = last_line
            return True
            
        # ASIGNO EL VALOR DE LA BATERIA PARA MOSTRARLO EN LOS LOGS
        if read_param(self.DLGID, 'BAT'):
            bat = read_param(self.DLGID, 'BAT')
        else:
            bat = read_param(self.DLGID, 'bt')
        
        
        
        def error_1min_TX(self):
            '''
            return True si hubo error de TX durante un minuto
            return False si no hubo error de TX durante un minuto
            '''
            
            if last_line == current_line:
                #
                return True
            else:
                #
                self.logs.print_inf(name_function, 'TX OK')
                #
                return False
        
        def RTC_error(self,error_1min):
            '''
            return False: si no se comprueba el RTC por error_1min
                          si no hay errores RTC
            return True:  si hay errores TRC 
                          
            '''
            
            # COMPRUEBO ERROR RTC SOLO SI NO HAY ERROR TX
            if error_1min: return False
                
            # DEVUELVO LOS VALORES DE last_fecha_data y last_hora_data asi como fecha_data y hora_data
            if self.redis.hexist(f'{self.DLGID}_ERROR', 'last_fecha_data') & self.redis.hexist(f'{self.DLGID}_ERROR', 'last_hora_data'):
                last_fecha_data = self.redis.hget(f'{self.DLGID}_ERROR', 'last_fecha_data')
                last_hora_data = self.redis.hget(f'{self.DLGID}_ERROR', 'last_hora_data')
                fecha_data = read_param(self.DLGID, 'DATE')
                hora_data = read_param(self.DLGID, 'TIME')
                #
                # ACTUALIZO last_fecha_data Y last_hora_data CON LOS VALORES ACTUALES
                self.redis.hset(f'{self.DLGID}_ERROR', 'last_fecha_data', fecha_data)
                self.redis.hset(f'{self.DLGID}_ERROR', 'last_hora_data', hora_data)
            else:
                fecha_data = read_param(self.DLGID, 'DATE')
                hora_data = read_param(self.DLGID, 'TIME')
                last_fecha_data = fecha_data
                last_hora_data = hora_data
                #
                # ACTUALIZO last_fecha_data Y last_hora_data CON LOS VALORES ACTUALES
                self.redis.hset(f'{self.DLGID}_ERROR', 'last_fecha_data', fecha_data)
                self.redis.hset(f'{self.DLGID}_ERROR', 'last_hora_data', hora_data)
                #
                return False
            #
            # CHEQUEO QUE NO ESTE CAMBIANDO LA FECHA Y HORA
            if fecha_data == last_fecha_data and hora_data == last_hora_data:
                self.logs.print_inf(name_function, 'RTC ERROR')
                self.logs.dlg_performance(f'< RTC ERROR >')
                return True
            else:
                self.logs.print_inf(name_function, 'RTC OK')
                return False
        
        def error_10min_TX(self,error_1min):
            '''
            return True si hubo error de TX durante mas 10 minuto
            return False si se restablece la cominicacion
            '''
            
            if error_1min:
                # INICIALIZO EL CONTADOR DE MINUTOS CON ERORR TX 
                if not(self.redis.hexist(f'{self.DLGID}_ERROR','count_error_tx')):
                    self.redis.hset(f'{self.DLGID}_ERROR', 'count_error_tx', 1)
                
                # LEO EL CONTADOS DE TIEMPO
                count_error_tx = int(self.redis.hget(f'{self.DLGID}_ERROR','count_error_tx'))
                
                # VEO EL ESTADO DEL CONTADOR    
                if count_error_tx >= 10:
                    #
                    return True
                else:
                    self.logs.print_inf(name_function, f'CONTADOR DE ERROR TX [{count_error_tx}]')
                    count_error_tx += 1
                    self.redis.hset(f'{self.DLGID}_ERROR','count_error_tx',count_error_tx)
                    #   
                    return False
            else:
                if self.redis.hexist(f'{self.DLGID}_ERROR','count_error_tx'):
                    self.redis.hdel(f'{self.DLGID}_ERROR','count_error_tx')   
                #
                return False
            
        def error_TPOLL_TX(self,timer_poll,error_1min):
            
            '''
            return True si hubo error de TX durante mas TPOLL minutos
            return False si se restablece la cominicacion
            '''
            
            if error_1min:
                # INICIALIZO EL CONTADOR DE MINUTOS CON ERORR TX 
                if not(self.redis.hexist(f'{self.DLGID}_ERROR','count_error_tx')):
                    self.redis.hset(f'{self.DLGID}_ERROR', 'count_error_tx', 1)
                
                # LEO EL CONTADOS DE TIEMPO
                count_error_tx = int(self.redis.hget(f'{self.DLGID}_ERROR','count_error_tx'))
                
                # VEO EL ESTADO DEL CONTADOR    
                if count_error_tx >= timer_poll:
                    #
                    return True
                else:
                    self.logs.print_inf(name_function, f'CONTADOR DE ERROR TX [{count_error_tx}]')
                    count_error_tx += 1
                    self.redis.hset(f'{self.DLGID}_ERROR','count_error_tx',count_error_tx)
                    #   
                    return False
            else:
                if self.redis.hexist(f'{self.DLGID}_ERROR','count_error_tx'):
                    self.redis.hdel(f'{self.DLGID}_ERROR','count_error_tx')   
                #
                return False
        
        
        # SI TENGO TIMER_POLL
        if self.config.lst_get('TIMER_POLL'):
            # LERO EL VALOR DE TPOLL PASADO
            timer_poll = int(self.config.lst_get('TIMER_POLL'))           
            #
            # CHEQUEO ERROR TX DURANTE UN MINUTO
            error_1min = error_1min_TX(self)
            #
            # CHEQUEO ERROR DE RTC
            RTC_error(self,error_1min)
            #
            # CHEQUEO ERRORES TX EN EL TPOLL DADO
            error_TPOLL = error_TPOLL_TX(self,timer_poll,error_1min)
            #
        else:
            # CHEQUEO ERROR TX DURANTE UN MINUTO
            error_1min = error_1min_TX(self)
            #
            # CHEQUEO ERROR DE RTC
            RTC_error(self,error_1min)
            #
            # CHEQUEO ERROR TX DURANTE 10 MINUTOS
            error_10min = error_10min_TX(self,error_1min)
            #
           
        # TRABAJO LOS LOGS
        if self.config.lst_get('TIMER_POLL'):
            if error_TPOLL:
                # MUESTRO LOG EN CONSOLA
                self.logs.print_inf(name_function, f'TX STOPPED FOR MORE THAN {timer_poll} MIN')
                #
                # ESCRIBO EN EL LOG
                self.logs.dlg_performance(f'< MAS DE {timer_poll} MIN CAIDO > [BAT = {bat}]')
                #
                return False
            else:
                return True
        else:    
            if error_10min:
                
                #
                # MUESTRO LOG EN CONSOLA
                self.logs.print_inf(name_function, 'TX STOPPED FOR MORE THAN 10 MIN')
                self.logs.print_out(name_function, dic.get_dic('TX_ERROR', 'name'), dic.get_dic('TX_ERROR', 'True_value'))
                #
                # ESCRIBO EN EL LOG
                self.logs.dlg_performance(f'< MAS DE 10 MIN CAIDO > [BAT = {bat}]')
                #
                # ESCRIBO EN REDIS LA ALARMA TX_ERROR CON VALOR DE ALARMA PRENDIDA
                self.redis.hset(self.DLGID, dic.get_dic('TX_ERROR', 'name'), dic.get_dic('TX_ERROR', 'True_value'))
                #
                return False
            else:
                #
                # ESCRIBO EN REDIS LA ALARMA TX_ERROR CON VALOR DE ALARMA APAGADA
                self.redis.hset(self.DLGID, dic.get_dic('TX_ERROR', 'name'), dic.get_dic('TX_ERROR', 'False_value'))
                #
                #MUESTRO LOGS EN CONSOLA DE QUE SE ESCRIBIO LA ALARMA DE ERROR TX EN REDIS
                self.logs.print_out(name_function, dic.get_dic('TX_ERROR', 'name'), dic.get_dic('TX_ERROR', 'False_value'))
                #
                if error_1min:
                    # MUESTRO LOG EN CONSOLA
                    self.logs.print_inf(name_function, 'TX STOPPED')
                    #
                    # ESCRIBO EN EL LOG
                    self.logs.dlg_performance(f'< ERROR TX > [BAT = {bat}]')
                    #
                    return False
                else:
                    return True
                    
                
                
                
            
        
    def visual(self): pass
             
    def event_detection(self):
        
        name_function = 'EVENT_DETECTION'
        
        # SI EVENT_DETECTION ES False INTERRUMPO LA FUNCION
        if not(self.EVENT_DETECTION == ''):
            if not(self.EVENT_DETECTION):
                self.logs.print_inf(name_function, 'EVENT_DETECTION INHABILITADO')
                return
        
            
        # PIERTA DEL GABINETE
        if read_param(self.DLGID,'GA') == '1':
            self.logs.print_inf(name_function, 'GABINETE_ABIERTO')
            #
            # ESCRIBO EN EL LOG
            self.logs.dlg_performance(f'< {name_function} > GABINETE_ABIERTO')
            
                
        # FALLA ELECTRICA
        if read_param(self.DLGID,'FE') == '1':
            self.logs.print_inf(name_function, 'FALLA_ELECTRICA')
            #
            # ESCRIBO EN EL LOG
            self.logs.dlg_performance(f'< {name_function} > FALLA_ELECTRICA')
            
            
        # FALLA TERMICA 1
        if read_param(self.DLGID,'FT1') == '1':
            self.logs.print_inf(name_function, 'FALLA_TERMICA_1')
            #
            # ESCRIBO EN EL LOG
            self.logs.dlg_performance(f'< {name_function} > FALLA_TERMICA_1')
                
        # TRABAJO EN MODO LOCAL
        if read_param(self.DLGID,'LM') == '1': 
            self.logs.print_inf(name_function, 'MODO_LOCAL')
            #
            # ESCRIBO EN EL LOG
            self.logs.dlg_performance(f'< {name_function} > MODO_LOCAL')
                
    def switch_outputs(self):
        
        name_function = 'SWITCH_OUTPUTS'
        
        #
        # SI ESTA HABILITADO EL SWITCH_OUTPUTS
        if not(self.SWITCH_OUTPUTS): 
            self.logs.print_inf(name_function, 'SWITCH_OUTPUTS INHABILITADO')
        
       
    
        
        
            
