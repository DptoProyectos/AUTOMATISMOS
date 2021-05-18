#!/usr/aut_env/bin/python3.8
'''
LIBRERIA DE APLICACION CTRL_PpotPaysandu

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 1.0.0 15-04-2021 11:19

''' 

# LIBRERIAS
import redis
import json

#CONEXIONES
from CTRL_FREC.PROCESS.drv_visual import dic
from __CORE__.drv_logs import *
from __CORE__.drv_redis import Redis
from __CORE__.drv_dlg import mbusWrite, read_param
from __CORE__.mypython import config_var, str2bool, dec2bin
from __CORE__.drv_config import dbUrl
from drv_db_GDA import GDA


#from posix import read





# CLASES DE LA LIBRERIA
class ctrl_process(object):
    '''
    FUNCIONES USADAS POR ctrl_process.py
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
        
        
        ## INSTANCIAS
        self.logs = ctrl_logs(self.TYPE,'CTRL_PpotPaysandu',self.DLGID_CTRL,self.print_log)
        self.redis = Redis()
        self.gda = GDA(dbUrl)

    def getAndUpdateMode(self,WEB_Mode):
        '''
            funcion para obtener el modo de trabajo y actualizarlo en caso necesario
        '''
        name_function = 'GET_AND_UPDATE_MODE'

        # entradas
        self.logs.print_in(name_function, 'WEB_Mode', WEB_Mode)

        def readPlcMode():
            """
                lee el modo de trabajo en que actualmente se encuentra el tablero de control
                0 -> EMERGENCIA
                1 -> LOCAL
                2 -> REMOTO
            """

            # leo el modo en que actualmente esta trabajando el PLC
            MOD = read_param(self.DLGID_CTRL,'MOD')
            
            if MOD == "0": return "EMERGENCIA"
            elif MOD == "1": return "LOCAL"
            elif MOD == "2": return "REMOTO"
            else: 
                self.logs.print_in(name_function, 'MOD', MOD)
                self.logs.print_error(name_function, 'MODO DE TRABAJO NO ADMITIDO')
                self.logs.print_error(name_function, 'NO SE EJECUTA EL SCRIPT')
                quit()

        def IsWebModeChanged():
            """
                detecta si hubo un cambio en el modo de trabajo web
                0 -> EMERGENCIA
                1 -> LOCAL
                2 -> REMOTO
            """
            if not self.redis.hexist(self.DLGID_CTRL,'Last_WEB_Mode'):
                self.redis.hset(self.DLGID_CTRL,'Last_WEB_Mode',WEB_Mode)
            
            Last_WEB_Mode = self.redis.hget(self.DLGID_CTRL,'Last_WEB_Mode')

            if Last_WEB_Mode != WEB_Mode:
                self.redis.hset(self.DLGID_CTRL,'Last_WEB_Mode',WEB_Mode)
                return True
            else:
                return False

        def setToPlcMode(WEB_Mode):
            """
                se escribe el registro UMOD del PLC para que el mismo actualice el modo
            """
            if WEB_Mode == "EMERGENCIA":
                mbusWrite(self.DLGID_CTRL,'2097','interger',5)
            elif WEB_Mode == "REMOTO":
                mbusWrite(self.DLGID_CTRL,'2097','interger',7)
            else:
                pass

        def IsPlcModeUpdated():
            """
                se compara el modo de trabajo de la web con el modo actual de trabajo del PLC.
                Si son iguales se retorna true, en caso contrario false
            """
            plcMode = readPlcMode()

            if plcMode != "LOCAL":
                if WEB_Mode == plcMode:
                    return True 
                else:
                    return False 
            else:
                # el plc esta trabajando en modo local por lo que no se puede decir que este desactualizado con la web 
                # ya que la misma no trabaja en este modo
                # se asume que estan actualizados
                return True
            
        def updateWebMode(UMOD):
            """
                Se actualiza en la web el modo de la siguiente forma
                1-> EMERGENCIA
                3-> REMOTO
                En caso de valor 2 return True para indicar que se esta trabajando en modo local
            """
            if UMOD == "1":
                self.logs.print_inf(name_function,"SE ACTUALIZA EL MODO EN LA WEB")
                self.gda.WriteAutConf(self.DLGID_CTRL,'WEB_Mode','EMERGENCIA')
                self.redis.hset(self.DLGID_CTRL,'Last_WEB_Mode','EMERGENCIA')
                mbusWrite(self.DLGID_CTRL,'2097','interger',0)
            elif UMOD == "3":
                self.logs.print_inf(name_function,"SE ACTUALIZA EL MODO EN LA WEB")
                self.gda.WriteAutConf(self.DLGID_CTRL,'WEB_Mode','REMOTO')
                self.redis.hset(self.DLGID_CTRL,'Last_WEB_Mode','REMOTO')
                mbusWrite(self.DLGID_CTRL,'2097','interger',0)

        def IsUpdatePlcModePending():
            '''
               retorna true en caso de haber pendiente una actualizacion de modo hacia el PLC
            '''        
            if self.redis.hexist(self.DLGID_CTRL,'UpdatePlcModePending'):
                UpdatePlcModePending  = self.redis.hget(self.DLGID_CTRL,'UpdatePlcModePending')
            else:
                self.redis.hset(self.DLGID_CTRL,'UpdatePlcModePending','NO')
                UpdatePlcModePending = 'NO'

            if UpdatePlcModePending == 'SI': return True
            else: return False


            

        # actualizo el modo para el software a partir del modo en que se encuentra el plc
        SOFT_Mode = readPlcMode()
        self.logs.print_in(name_function, 'MOD', SOFT_Mode)

        if IsWebModeChanged():
            self.logs.print_inf(name_function,"HUBO CAMBIO DE MODO EN LA WEB")
            
            # mando a escribir el modo al plc
            self.logs.print_inf(name_function,"SE MANDA A ACTUALIZAR EL MODO EN EL PLC")
            setToPlcMode(WEB_Mode)

            # activo una bandera para idicar que se esta en un proceso de cambio de modo hacia el PLC
            self.redis.hset(self.DLGID_CTRL,'UpdatePlcModePending','SI')

        else:
            # verifico que este en proceso una actualizacion de modo en el plc
            if IsUpdatePlcModePending():
                # chequeo si se escribio se actualizo el modo del PLC. Si no lo hizo lo vuelvo a escribir.
                self.logs.print_inf(name_function,"PROCESO DE ACTUALIZACION DE MODO HACIA EL PLC PENDIENTE")
                if not IsPlcModeUpdated():
                    self.logs.print_inf(name_function,"SE MANDA NUEVAMENTE!!! A ACTUALIZAR EL MODO EN EL PLC")
                    setToPlcMode(WEB_Mode)
                else:
                    self.logs.print_inf(name_function,"MODO EN EL PLC ACTUALIZADO DE FORMA CORRECTA")
                    self.redis.hset(self.DLGID_CTRL,'UpdatePlcModePending','NO')
            else:
                # chequep si hay pedido para actualizar en la web
                UMOD = read_param(self.DLGID_CTRL,'UMOD')
                if UMOD == '0':
                    self.logs.print_inf(name_function,"NO HAY SOLICITUD DE ACTUALIZACION MODO")
                elif UMOD in ['1','3']:
                    # Actualizo el modo web
                    self.logs.print_inf(name_function,"HAY PEDIDO DE ACTUALIZACION WEB")
                    updateWebMode(UMOD)
        return SOFT_Mode

                
        
        

        



        self.logs.print_out(name_function, 'SOFT_Mode', SOFT_Mode)

        return SOFT_Mode

    def pump(self,actionOnthePump):
        '''
            funcion que manda a prender o apagar la bomba
        '''
        name_function = 'MAIN'

        if actionOnthePump == 'ON':
            self.logs.print_inf(name_function, 'PRENDO BOMBA')
            mbusWrite(self.DLGID_CTRL,'2096','interger',2)              # escribo el valor 2 en el registro 2097 para mandar a prender la bomba

        elif actionOnthePump == 'OFF':
            self.logs.print_inf(name_function, 'APAGO BOMBA')
            mbusWrite(self.DLGID_CTRL,'2096','interger',0)              # escribo el valor 0 en el registro 2097 para mandar a apagar la bomba
        
    def setFrequency(self,WEB_Frequency):
        '''
            funcion que manda a setear la frecuencia de trabajo del variador
        '''
        name_function = 'MAIN'

        UFREQ = int(read_param(self.DLGID_CTRL,'UFREQ'))

        # leo la variable IsfrequecyUpdating
        if not self.redis.hexist(self.DLGID_CTRL,'IsfrequecyUpdating'):
            self.redis.hset(self.DLGID_CTRL,'IsfrequecyUpdating','NO')
            IsfrequecyUpdating = self.redis.hget(self.DLGID_CTRL,'IsfrequecyUpdating')
        else:
            IsfrequecyUpdating = self.redis.hget(self.DLGID_CTRL,'IsfrequecyUpdating')

        # leo la variable lastUpdatedFrequecy
        if not self.redis.hexist(self.DLGID_CTRL,'lastUpdatedFrequecy'):
            self.redis.hset(self.DLGID_CTRL,'lastUpdatedFrequecy',0)
            lastUpdatedFrequecy = int(self.redis.hget(self.DLGID_CTRL,'lastUpdatedFrequecy'))
        else:
            lastUpdatedFrequecy = int(self.redis.hget(self.DLGID_CTRL,'lastUpdatedFrequecy'))

        # leo la variable countFrames
        if not self.redis.hexist(self.DLGID_CTRL,'countFrames'):
            self.redis.hset(self.DLGID_CTRL,'countFrames',0)
            countFrames = int(self.redis.hget(self.DLGID_CTRL,'countFrames'))
        else:
            countFrames = int(self.redis.hget(self.DLGID_CTRL,'countFrames'))
    
        if UFREQ == 0:
            if IsfrequecyUpdating == 'NO':
                if WEB_Frequency != 0:
                    self.logs.print_inf(name_function, 'SE MANDA A ACTUALIZAR LA FRECUENCIA {0}'.format(WEB_Frequency))
                    mbusWrite(self.DLGID_CTRL,'2098','interger',WEB_Frequency)
                    self.redis.hset(self.DLGID_CTRL,'IsfrequecyUpdating','SI')
                    self.redis.hset(self.DLGID_CTRL,'lastUpdatedFrequecy',WEB_Frequency)
                    self.redis.hset(self.DLGID_CTRL,'countFrames',0)
                else:
                    self.logs.print_inf(name_function, 'NO HAY PEDIDO DE FRECUENCIA PARA ACTUALIZAR')
            else:
                # dejo un frame de por medio para esperar un dato valido de UFREQ
                countFrames += 1
                if countFrames >= 2:
                    if lastUpdatedFrequecy == WEB_Frequency:
                        self.gda.WriteAutConf(self.DLGID_CTRL,'WEB_Frequency',0)
                        self.logs.print_inf(name_function, 'FRECUENCIA ACTUALIZADA CORRECTAMENTE')
                        self.redis.hset(self.DLGID_CTRL,'IsfrequecyUpdating','NO')
                        # 
                        # pongo en cero el registro modbus para evitar que se mande por error un valor y se comience un proceso de actualizacio de frecuencia
                        mbusWrite(self.DLGID_CTRL,'2098','interger',0)
                    else:
                        deltaFrequency = WEB_Frequency - lastUpdatedFrequecy
                        self.logs.print_inf(name_function, 'NUEVO VALOR DE ACTUALIZACION DE FRECUENCIA')
                        self.logs.print_inf(name_function, 'SE CONTINUA EL PROCESO DE VARIAR LA FRECUENCIA')
                        self.logs.print_inf(name_function, 'SE MANDA A ACTUALIZAR LA FRECUENCIA {0}'.format(deltaFrequency))
                        mbusWrite(self.DLGID_CTRL,'2098','interger',deltaFrequency)
                        self.redis.hset(self.DLGID_CTRL,'lastUpdatedFrequecy',WEB_Frequency)
                        self.redis.hset(self.DLGID_CTRL,'countFrames',0)
                else:
                    self.logs.print_inf(name_function, 'SE ESPERA UN NUEVO FRAME CON VALOR VALIDO EN UFREQ')
                    self.redis.hset(self.DLGID_CTRL,'countFrames',countFrames)
                    #
                    # pongo en cero el registro modbus para evitar que se mande por error un valor y se comience un proceso de actualizacio de frecuencia
                    mbusWrite(self.DLGID_CTRL,'2098','interger',0)
        else:
            self.logs.print_inf(name_function, 'ACTUALIZACION DE FRECUENCIA EN CURSO')
            self.logs.print_inf(name_function, 'SE ESPERA QUE SE TERMINE DE ACTUALIZAR LA FRECUENCIA')
            self.redis.hset(self.DLGID_CTRL,'countFrames',2)
            #
            # pongo en cero el registro modbus para evitar que se mande por error un valor y se comience un proceso de actualizacio de frecuencia
            mbusWrite(self.DLGID_CTRL,'2098','interger',0)

    def showStatesAndAlarms(self):
        '''
            funcion que lee el byte que deja el plc en el LINE y lo traduce a sus correspondientes alarmas y estados
        '''
        
        name_function = 'SHOW_STATES_&_ALARMS'

        self.logs.print_inf('MAIN',name_function)
               
        decStates = int(read_param(self.DLGID_CTRL,'ST'))
        binStates = dec2bin(decStates)

        listOfAlarmsAndStates = [
            # desctription                trueValue              falseValue              bit
            'AlrLowFlow',                   'SI',                   'NO',                 #0
            'StatePump',                    'ON',                   'OFF',                #1
            'AlrLowPressure',               'SI',                   'NO',                 #2
            'AlrLowCau',                    'SI',                   'NO',                 #3
            'AlrLowFlow',                   'SI',                   'NO',                 #4
            'AlrVarFail',                   'SI',                   'NO',                 #5
            'StateVar',                     'READY',                'FAIL',               #6
            'StateLineVar',                 'OK',                   'FAIL',               #7
        ]

        NumberOfZerosForFill = int(len(listOfAlarmsAndStates)/3) - len(binStates)

        if NumberOfZerosForFill > 0:
            # completo con ceros binStates
            while NumberOfZerosForFill > 0:
                binStates = '0{0}'.format(binStates)
                NumberOfZerosForFill -= 1
        elif NumberOfZerosForFill < 0:
            # esto ocurre porque dentro del registro modbus se esta mandando algun bit de alarma que no esta declarado
            self.logs.print_inf(name_function,'HAY MAS ESTADOS QUE ALARMAS DECLARADAS')

        # escribo los valores de alarmas para cada uno de los bits segun declaracion en listOfAlarmsAndStates
        bit = len(binStates)-1  
        for valueBit in binStates:
            if valueBit == '1':
                self.redis.hset(self.DLGID_CTRL,listOfAlarmsAndStates[3*bit],listOfAlarmsAndStates[3*bit+1])
                self.logs.print_out(name_function,listOfAlarmsAndStates[3*bit],listOfAlarmsAndStates[3*bit+1])
            else:
                self.redis.hset(self.DLGID_CTRL,listOfAlarmsAndStates[3*bit],listOfAlarmsAndStates[3*bit+2])
                self.logs.print_out(name_function,listOfAlarmsAndStates[3*bit],listOfAlarmsAndStates[3*bit+2])
            bit -= 1

    def setVisualVars(self):
        '''
            garantizo que las variables de visualizacion siempre existan
        '''

        if not self.redis.hexist(self.DLGID_CTRL,'PLC_SoftMode'):
            self.redis.hset(self.DLGID_CTRL,'PLC_SoftMode','REMOTO')
        
        if not self.redis.hexist(self.DLGID_CTRL,'TX_ERROR'):
            self.redis.hset(self.DLGID_CTRL,'TX_ERROR','NO')

        if not self.redis.hexist(self.DLGID_CTRL,'StatePump'):
            self.redis.hset(self.DLGID_CTRL,'StatePump','OFF')

        if not self.redis.hexist(self.DLGID_CTRL,'AlrLowPressure'):
            self.redis.hset(self.DLGID_CTRL,'AlrLowPressure','NO')

        if not self.redis.hexist(self.DLGID_CTRL,'AlrLowFlow'):
            self.redis.hset(self.DLGID_CTRL,'AlrLowFlow','NO')

        if not self.redis.hexist(self.DLGID_CTRL,'AlrLowCau'):
            self.redis.hset(self.DLGID_CTRL,'AlrLowCau','NO')

        if not self.redis.hexist(self.DLGID_CTRL,'AlrVarFail'):
            self.redis.hset(self.DLGID_CTRL,'AlrVarFail','NO')

        if not self.redis.hexist(self.DLGID_CTRL,'StateVar'):
            self.redis.hset(self.DLGID_CTRL,'StateVar','READY')

        if not self.redis.hexist(self.DLGID_CTRL,'StateLineVar'):
            self.redis.hset(self.DLGID_CTRL,'StateLineVar','OK')


    def checkAndSetControlVars(self):
        '''
            garantizo que las variables de control siempre existan
        '''
        # WEB_Mode
        if not self.gda.readAutConf(self.DLGID_CTRL,'WEB_Mode' ):
            self.gda.InsertAutConf(self.DLGID_CTRL, 'WEB_Mode', 'REMOTO')

        # WEB_ActionPump
        if not self.gda.readAutConf(self.DLGID_CTRL,'WEB_ActionPump' ):
            self.gda.InsertAutConf(self.DLGID_CTRL, 'WEB_ActionPump', 'OFF')

        # WEB_Frequency
        if not self.gda.readAutConf(self.DLGID_CTRL,'WEB_Frequency' ):
            self.gda.InsertAutConf(self.DLGID_CTRL, 'WEB_Frequency', 0)
        
      
        




class errorProcess(object):  
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
        self.TEST_OUTPUTS = str2bool(self.config.lst_get('TEST_OUTPUTS'))
        self.RESET_ENABLE = str2bool(self.config.lst_get('RESET_ENABLE'))
        self.EVENT_DETECTION = str2bool(self.config.lst_get('EVENT_DETECTION'))
        self.TIMER_POLL = str2bool(self.config.lst_get('TIMER_POLL'))
        #
        
        # INSTANCIAS
        self.logs = ctrl_logs(self.TYPE,'CTRL_FREC_error',self.DLGID,self.print_log)
        
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
            return 'noLine'
        
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
                self.logs.dlg_performance(f'< MAS DE {timer_poll} MIN CAIDO >')
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
                self.logs.dlg_performance(f'< MAS DE 10 MIN CAIDO > ')
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
                    # ESCRIBO EN REDIS ALARMA DE 1MIN EL EQUIPO CAIDO
                    self.redis.hset(self.DLGID, 'error_1min', 'SI')
                    #
                    # ESCRIBO EN EL LOG
                    self.logs.dlg_performance(f'< ERROR TX >')
                    #
                    return False
                else:
                    #
                    # ESCRIBO EN REDIS ALARMA DE 1MIN QUE INDICA QUE EL DATO QUE ESTA LLEGADNO ES VALIDO
                    self.redis.hset(self.DLGID, 'error_1min', 'NO')
                    #
                    return True
                    
    
             
    
                
    
        
      
                
     
           
    
            
                  
            
        
            
