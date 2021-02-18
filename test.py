#!/usr/aut_env/bin/python3.8
'''
Created on 28 jul. 2020

@author: root
'''

import os;

CBK = '/datos/cgi-bin/spx/PERFORACIONES/ext_call.pl';
param = '--dlgid';


#os.system('{0} {1}'.format(CBK,self.dlgid));
dlgid = 'UYPC03';

os.system('{0} {1} {2} '.format(CBK,param,dlgid));

