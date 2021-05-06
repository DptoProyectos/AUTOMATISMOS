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

from sqlalchemy import Table, select, create_engine, MetaData, update
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
        tableAuto = Table('automatismo', self.metadata, autoload=True, autoload_with=self.engine)
        tableAutoParam = Table('automatismo_parametro', self.metadata, autoload=True, autoload_with=self.engine)
        
        myJoin = tableAutoParam.join(tableAuto, tableAutoParam.c.id == tableAuto.c.id)
        sel = select([tableAutoParam.c.valor])
        sel = sel.where(tableAuto.c.dlgid == dlgId)
        sel = sel.where(tableAutoParam.c.nombre == param)
        rps = self.conn.execute(sel)
        rps = rps.fetchall()[0][0]
        return rps

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
            rps = self.conn.execute(sel)
            rps = rps.fetchall()[0][0]
        except:
            dlgExist = False
           
        # si el dlg no existe lo inserto en la tabla automatismos
        if not dlgExist:
            insert_statement = tb_automatismo.insert()\
            .values(dlgid = dlgId)
            self.engine.execute(insert_statement)

        # obtengo el valor del id del automatismo   
        sel = select([tb_automatismo.c.id])
        sel = sel.where(tb_automatismo.c.dlgid == dlgId)
        rps = self.conn.execute(sel)
        rps = rps.fetchall()[0][0]

        print(rps)
        
        
    


gda = GDA()


if gda.connect():
    print('esto esta ok')
    #print(gda.leer_df_inits())
    #print(gda.readAutTable('CTRLPAY01','WEB_Mode'))
    #print(gda.WriteAutConf('CTRLPAY01','WEB_Mode','LOCAL'))
    gda.InsertAutConf('CTRLPAY09','WEB_Mode','EMERGENCIA')
    #gda.WriteAutConf('CTRLPAY01','WEB_ActionPump','ON')
    #gda.WriteAutConf('CTRLPAY01','WEB_Frequency',0)
    #readAutTable('CTRLPAY01','WEB_Mode')
    #gda.leer_df_inits()
else:
    print('esto esta fail')


