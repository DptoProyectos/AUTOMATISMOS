ROYECTO DE SISTEMAS CON AUTOMATISMOS

FLOWCHART: project 				-> 	https://drive.google.com/file/d/1YFjm_3HncAyEX1VBOtet1D0vdXyxPA-W/view?usp=sharing
		   serv_APP_selection 	-> 	https://drive.google.com/file/d/1ImChibsiLTjf7Fgl6tJeAeD8pxPpUmb0/view?usp=sharing
		   CTRL_FREC			->	
		   CTRL_PpotPaysandu	->  https://drive.google.com/file/d/1VDwYcD7yKF_tMaDpcf-pSyj6EQ-DgkTK/view?usp=sharing



ENVIROMENT: #!/usr/aut_env/bin/python3.8

# LOGS: 
## SYSLOG
	Los log utilizan el syslog de ubuntu. Para ello agregar al archivo /etc/rsyslog.d/50-default.conf la siguiente configuracion
	<<<<<<<<<<<
		:syslogtag, contains, "AUTO_CTRL" /var/log/autoCtrl.log
		:syslogtag, contains, "AUTO_CTRL" ~
	>>>>>>>>>>>

## Logrotate: 
	Para controlar el tamamano de los logs crear un archivo en la carpeta /etc/logrotate.d con la siguiete configuracion
	<<<<<<<<<<<
		/var/log/autoCtrl.log
		{
				rotate 3
				daily
				size 1G
				missingok
				notifempty
				delaycompress
				compress
				postrotate
						invoke-rc.d rsyslog rotate > /dev/null
				endscript
		}
	>>>>>>>>>>>


# FORMA DE EJECUCION:
## DETECCION DE ERRORES DESDE EL CRONTAB
/var/etc/crontab => 
	*/1 * * * * root /datos/cgi-bin/spx/AUTOMATISMOS/serv_error_APP_selection.py > /dev/null 2>&1
	NOTA: EN EL CRONTAB SE EJECUTA TODO LO RELACIONADO A DETECCION DE ERRORES


## PROCESS DEL AUTOMATIMSO DESDE EL SERVIDOR EN PYTHON
//drbd/www/cgi-bin/SPY/spy.conf =>
	
	[CALLBACKS_PATH]
	cbk_path = /datos/cgi-bin/spx/AUTOMATISMOS

	[CALLBACKS_PROGRAM]
	cbk_program = serv_APP_selection.py
	
	NOTA: CADA VEZ QUE EL DATALOGGER TRANSMITE SE LLAMA A LA FUNCION process_perf Y SE LE PASA EL DATALOGGER ID

