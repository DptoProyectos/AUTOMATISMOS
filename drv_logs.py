#!/drbd/www/cgi-bin/spx/AUTOMATISMOS/myenv/bin/python3.6
'''
Created on 20 mar. 2020

@author: root
'''

## LIBRERIAS
import os
import json

#CONEXIONES
from datetime import date
from datetime import datetime



class ctrl_logs(object):
    def __init__(self,project_folder_name,DLGID_CTRL,show_log):
        '''
        Constructor
        '''
        self.project_folder_name = project_folder_name
        self.DLGID_CTRL = DLGID_CTRL
        # GARANTIZO QUE SIEMPRE ME ENTRE UN BOOL
        try: self.show_log = json.loads(show_log.lower()) 
        except: self.show_log = show_log
                   
    def print_log(self,message):
        if self.show_log: print(message)
            
    def print_in(self,name_function,name_var,value_var):
        if self.show_log: print(f"{name_function} <= [{name_var} = {value_var}]")
    
    def print_out(self,name_function,name_var,value_var):
        if self.show_log: print(f"{name_function} => [{name_var} = {value_var}]")
    
    def print_inf(self,name_function,message):
        if self.show_log: print(f"{name_function} ==> {message}")
         
    def script_performance(self,message):
        
        # OBTENFO LA CARPETA EN DONDE SE ENCUENTRA EL ARCHIVO ACTUAL
        current_path = os.path.dirname(os.path.abspath(__file__))
        
        # CREO LA CARPETA DONDE VA A ESTAR EL LOG
        ## CREO LA CARPETA SOLO SI ESTA NO EXISTE
        if not(os.path.exists(f"{current_path}/{self.project_folder_name}/SCRIPT_PERFORMANCE/ctrl_process_{self.DLGID_CTRL}")): 
            os.makedirs(f"{current_path}/{self.project_folder_name}/SCRIPT_PERFORMANCE/ctrl_process_{self.DLGID_CTRL}",0o777)
        
        # OBTENGO LA FECHA FORMATEADA A 'AAAAMMDD'
        list_fecha = str(date.today()).split('-')
        fecha = list_fecha[0]+list_fecha[1]+list_fecha[2]
        
        # CREO EL ARCHIVO EN DONDE SE VAN A REGISTRAR LOS LOGS
        from io import open
        script_performance = open(f"{current_path}/{self.project_folder_name}/SCRIPT_PERFORMANCE/ctrl_process_{self.DLGID_CTRL}/{self.DLGID_CTRL}_{fecha}",'a')
        
        # OBTENGO LA HORA FORMATEADA A 'HH:MM:SSD'
        hora = str(datetime.now()).split(' ')[1].split('.')[0]
        
        # EXCRIBIMOS EL LOG
        script_performance.write(f"{hora} {message}\n") 
        
        # CERRAMOS EL LOG
        script_performance.close()
        

     
        