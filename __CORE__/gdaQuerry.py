#!/usr/aut_env/bin/python3.8
'''
Insert into automatismo (dlgid)
Values ('CTRLPAY01');

Insert into automatismo_parametro (auto_id, nombre, valor)
Values (2,'WEB_Mode','REMOTO');

Insert into automatismo_parametro (auto_id, nombre, valor)
Values (2,'WEB_ActionPump','ON');

Insert into automatismo_parametro (auto_id, nombre, valor)
Values (2,'WEB_Frequency','0');

select valor from automatismo_parametro
where auto_id = '2'
and nombre = 'WEB_Mode'
'''

from sqlalchemy import Table, select, create_engine, MetaData, update, delete
from sqlalchemy.orm import sessionmaker

engine = None
conn = None

metadata = False
#url = 'mysql+pymysql://pablo:spymovil@192.168.0.8/GDA'
url = 'postgresql+psycopg2://admin:pexco599@192.168.0.6/GDA'



class GDA(object):
    '''
        trabajo con base de datos con la estructura GDA
        parametros necesarios
        dbuser
        dbpasswd
        dbhost
        dbaseName
    '''

    def __init__(self):
        '''
            Constructor
        '''
        self.engine = None
        self.conn = None
        self.connected = False
        self.metadata = None
        self.session = None
        #self.url = 'mysql+pymysql://pablo:spymovil@192.168.0.8/GDA'
        self.url = 'postgresql+psycopg2://admin:pexco599@192.168.0.6/GDA'
      
    def connect(self):
        """
           Retorna True/False si es posible generar una conexion a la bd GDA
        """
        try:
            self.engine = create_engine(url)
            Session = sessionmaker(bind=self.engine) 
            self.session = Session()
        except Exception as err_var:
            print('ERROR: engine NOT created. ABORT !!')
            print('ERROR: EXCEPTION {0}'.format(err_var))
            return False

        try:
            self.conn = self.engine.connect()
        except Exception as err_var:
            print('ERROR: NOT connected. ABORT !!')
            print('ERROR: EXCEPTION {0}'.format(err_var))
            return False

        self.metadata = MetaData()
        return True

    def readAutConf(self,dlgId,param):
        '''
            lee el valor del parametro param para el dlgId de GDA
        '''
        tb_automatismo = Table('automatismo', self.metadata, autoload=True, autoload_with=self.engine)
        tb_automatismoParametro = Table('automatismo_parametro', self.metadata, autoload=True, autoload_with=self.engine)
        
        # obtengo el valor del id del automatismo   
        sel = select([tb_automatismo.c.id])
        sel = sel.where(tb_automatismo.c.dlgid == dlgId)
        autoId = self.conn.execute(sel)
        autoId = autoId.fetchall()

        if autoId:
            # obtengo el valor del parametro  
            autoId = autoId[0][0]
            sel = select([tb_automatismoParametro.c.valor])
            sel = sel.where(tb_automatismoParametro.c.auto_id == autoId)
            sel = sel.where(tb_automatismoParametro.c.nombre == param)
            value = self.conn.execute(sel)
            
            value = value.fetchall()
            if value: return value[0][0]

    def WriteAutConf(self,dlgId,param,value):
        """
            actualiza el valor de parametro para el automatismo autoId de la tabla automatismo_parametro de GDA
        """
        tb_automatismo = Table('automatismo', self.metadata, autoload=True, autoload_with=self.engine)
        tb_automatismoParametro = Table('automatismo_parametro', self.metadata, autoload=True, autoload_with=self.engine)

        # obtengo el valor del id del automatismo   
        sel = select([tb_automatismo.c.id])
        sel = sel.where(tb_automatismo.c.dlgid == dlgId)
        rps = self.conn.execute(sel)
        rps = rps.fetchall()[0][0]

        # actualizo el valor del parametro
        update_statement = tb_automatismoParametro.update()\
            .where(tb_automatismoParametro.c.auto_id == rps)\
            .where(tb_automatismoParametro.c.nombre == param)\
            .values(valor = value)

        self.engine.execute(update_statement)

    def InsertAutConf(self,dlgId,param,value):
        tb_automatismo = Table('automatismo', self.metadata, autoload=True, autoload_with=self.engine)
        tb_automatismoParametro = Table('automatismo_parametro', self.metadata, autoload=True, autoload_with=self.engine)
        
        # reviso si el dlg ya existe
        dlgExist = True
        try:
            # obtengo el valor del id del automatismo   
            sel = select([tb_automatismo.c.id])
            sel = sel.where(tb_automatismo.c.dlgid == dlgId)
            autoId = self.conn.execute(sel)
            autoId = autoId.fetchall()[0][0]
        except:
            dlgExist = False
           
        # si el dlg no existe lo inserto en la tabla automatismos
        if not dlgExist:
            insert_statement = tb_automatismo.insert()\
            .values(dlgid = dlgId)
            self.engine.execute(insert_statement)

            # obtengo el valor del nuevo id del automatismo creado
            sel = select([tb_automatismo.c.id])
            sel = sel.where(tb_automatismo.c.dlgid == dlgId)
            autoId = self.conn.execute(sel)
            autoId = autoId.fetchall()[0][0]
        
        # chequeo si existe el parametro para el datalogger
        paramExist = True
        try:
            # obtengo el valor del id del automatismo   
            sel = select([tb_automatismoParametro.c.id])
            sel = sel.where(tb_automatismoParametro.c.auto_id == autoId)
            sel = sel.where(tb_automatismoParametro.c.nombre == param)
            rps = self.conn.execute(sel)
            rps = rps.fetchall()[0][0]
        except:
            paramExist = False

        # si el parametro no existe lo inserto en la tabla automatismos con su correspondiente valor
        if not paramExist:
            insert_statement = tb_automatismoParametro.insert()\
            .values(auto_id = autoId)\
            .values(nombre = param)\
            .values(valor = value)
            self.engine.execute(insert_statement)

        # si el parametro existe le hacemos un update
        else:
            # actualizo el valor del parametro
            update_statement = tb_automatismoParametro.update()\
                .where(tb_automatismoParametro.c.auto_id == autoId)\
                .where(tb_automatismoParametro.c.nombre == param)\
                .values(valor = value)

            self.engine.execute(update_statement)

    def DeleteAutConf(self,dlgId,param):
        tb_automatismo = Table('automatismo', self.metadata, autoload=True, autoload_with=self.engine)
        tb_automatismoParametro = Table('automatismo_parametro', self.metadata, autoload=True, autoload_with=self.engine)
        
        # obtengo el valor del id del automatismo   
        sel = select([tb_automatismo.c.id])
        sel = sel.where(tb_automatismo.c.dlgid == dlgId)
        autoId = self.conn.execute(sel)
        autoId = autoId.fetchall()[0][0]
        print(autoId)

        # obtengo el valor del id del automatismo   
        sel = select([tb_automatismoParametro.c.id])
        sel = sel.where(tb_automatismoParametro.c.auto_id == autoId)
        sel = sel.where(tb_automatismoParametro.c.nombre == param)
        paramId = self.conn.execute(sel)
        paramId = paramId.fetchall()[0][0]
        print(paramId)
                
        # elimino el paramatro
        sql = (delete(tb_automatismoParametro)
            .where(tb_automatismoParametro.c.id == paramId))
        self.conn.execute(sql)
        
       
gda = GDA()


if gda.connect():
    print('esto esta ok')
    #print(gda.leer_df_inits())
    #print(gda.readAutTable('CTRLPAY01','WEB_Mode'))
    #print(gda.WriteAutConf('CTRLPAY01','WEB_Mode','LOCAL'))
    gda.InsertAutConf('CTRLPAY01','WEB_Frequency','EMERGENCIA')
    print(gda.readAutConf('CTRLPAY01','WEB_Frequency'))
    gda.DeleteAutConf('CTRLPAY01','WEB_Frequency')
    print(gda.readAutConf('CTRLPAY01','WEB_Frequency'))
    #gda.WriteAutConf('CTRLPAY01','WEB_ActionPump','ON')
    #gda.WriteAutConf('CTRLPAY01','WEB_Frequency',0)
    #readAutTable('CTRLPAY01','WEB_Mode')
    #gda.leer_df_inits()
else:
    print('esto esta fail')


