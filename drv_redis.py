#!/drbd/www/cgi-bin/spx/aut_env/bin/python3.6
'''
Created on 20 mar. 2020

@author: Yosniel
'''

import redis

class Redis(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.connected = 'NULL'
        self.rh = 'NULL'
        try:
            self.rh = redis.Redis()
            self.connected = True
        except Exception as err_var:
            #print(module=__name__, function='__init__', dlgid=self.dlgid, msg='Redis init ERROR !!')
            #print(module=__name__, function='__init__', dlgid=self.dlgid, msg='EXCEPTION {}'.format(err_var))
            print(err_var)
            self.connected = False

    def hset (self,key,param,value):
        if self.connected:
            self.rh.hset( key, param, value)
            
    def hget (self,key,param):
        if self.connected:
            if self.rh.hexists(key, param): 
                value = self.rh.hget(key, param)
                return value.decode()
            else: return ''
            
    
    def hexist(self,key, param): 
        if self.connected: return self.rh.hexists(key, param) 
        
    def hdel (self,key,param):
        if self.connected:
            if self.rh.hexists(key, param): self.rh.hdel( key, param)
            