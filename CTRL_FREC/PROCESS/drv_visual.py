#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
DRIVER VISUALIZACION DE CTRL_FREC

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 2.1.0 16-04-2020 12:58
''' 



#                keys                 #name              #True_value   #False_value    #value_1     #value_2

visual_dic = {  
                'WEB_MODE':         [ 'SW1',                'AUTO',     'REMOTO',       'BOYA',     'TIMER'   ],
                'LMIN':             [ 'LMIN_TQ',            1                                                 ],
                'LMAX':             [ 'LMAX_TQ',            1.5                                               ],
                'PUMP_1_WEB_MODE':  [ 'SW2',                'ON',       'OFF',                                ],
                'TX_ERROR':         [ 'TX_ERROR',           'SI',       'NO',                                 ],
                
                'GABINETE_ABIERTO': [ 'GABINETE_ABIERTO',   'SI',       'NO',                                 ],
                'FALLA_ELECTRICA':  [ 'FALLA_ELECTRICA',    'SI',       'NO',                                 ],
                'FALLA_TERMICA_1':  [ 'FALLA_TERMICA_1',    'SI',       'NO',                                 ],
                
    }

#
class manage_dic():
    def __init__(self,dic_in):
        '''
        #Constructor
        '''
        self.my_dic = dic_in 
    
    
    def get_dic(self,keys,atributo):
        '''
        atributos validos:  name
                            True_value
                            False_value
                            value_1
                            value_2
        '''
        
        try:
            # CHEQUEO QUE ATRIBUTO SE ESTA PASANDO
            if atributo == 'name':
                lst = self.my_dic.get(keys)
                list_sel = lst[0]
            elif atributo == 'True_value':
                lst = self.my_dic.get(keys)
                list_sel = lst[1]
            elif atributo == 'False_value':
                lst = self.my_dic.get(keys)
                list_sel = lst[2]
            elif atributo == 'value_1':
                lst = self.my_dic.get(keys)
                list_sel = lst[3]
            elif atributo == 'value_2':
                lst = self.my_dic.get(keys)
                list_sel = lst[4]
            else:
                return None
        
            return list_sel
        
        except:
            return None
        
dic = manage_dic(visual_dic)
#value = dic.get_dic('LMIN', 'True_value')
#print(f'###########################{value}')

            
            
    