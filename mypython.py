#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6

'''
Created on 23 mar. 2020

@author: Yosniel Cabrera
'''

# LIBRERIAS
import json

def lst2str(list):
    '''
    Convierto de lista a string
    
    EX:
    list = ['print_log', True, 'DLGID_CTRL', 'MER001']
    string = lst2str(list)
    string = print_log,True,DLGID_CTRL,MER001
    '''
    my_str = str(list[0])
    n = 0
    for param in list:
        if n < (len(list)-1): 
            n += 1
            my_str = f"{my_str},{str(list[n])}"
    
    return my_str

def str2lst (str):
    lst = str.split(',')
    if lst == ['']:
        return ''
    else:
        return lst

def str2bool(str):
    '''
        Funcion que garantiza que en su salida haya una variable tipo bool
    '''
    try: out = json.loads(str.lower()) 
    except: out = str
    return out
   
def not_dec(in_dec,bits):
    '''
    Invierte la representacion binaria del numero decimal entrado. Devuelve en decimal
    
    EX:
    in_dec = 1
    > 1
    out = not_dec(in_dec,3)
    out = 6
    > 110
    '''
    # ESXTRAIGO LOS DOS PRIMEROS CARACTERES BINARIOS
    out_char = ''
    n = 0
    for x in bin(in_dec):
        if n >= 2: out_char = f"{out_char}{x}"
        n += 1
    #
    # CALCULO LA LONGITUD STRING OBTENIDO
    n = 0
    for y in out_char:
        n +=1
    #
    # COMPLETO CON CEROS EL NUMERO DE BITS
    while n < bits:
        out_char = f"0{out_char}"
        n += 1
        
    # INVIERTO CADA CARACTER DEL STRING OBTENIDO
    out_bin = ''
    for x in out_char:
        out_bin = f"{out_bin}{int(not(int(x)))}"
        n += 1
    return int(out_bin,2)

class config_var():
    '''
    
    '''
    def __init__(self,vars):
        self.var = vars
    
    def str_get(self,param):
        my_list = self.var.split(',')
        try: return my_list[my_list.index(param)+1]
        except: return ''
     
    
    def lst_get(self,param):
        my_list = self.var
        try:return my_list[my_list.index(param)+1]
        except: return ''
             
        
    




    
    