#!/datos/cgi-bin/spx/aut_env/bin/python3.6
'''
Created on 29 jul. 2020

@author: root
'''

# ABRO EL ARCHIVO LOG
log = open('test.log','a')
# EXCRIBIMOS EL LOG
log.write(f"ESTO ESTA FUNCIONANDO\n") 
        
# CERRAMOS EL LOG
log.close()