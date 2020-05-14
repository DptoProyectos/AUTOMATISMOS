#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
Created on 14 may. 2020

@author: Yosniel Cabrera
'''

import configparser
import os



# project_path
project_path = os.path.dirname(os.path.abspath(__file__))


# serv_APP_config.ini
serv_APP_config = configparser.ConfigParser()
serv_APP_config.read(f"{project_path}/serv_APP_config.ini")



