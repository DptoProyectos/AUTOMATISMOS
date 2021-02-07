ROYECTO DE SISTEMAS CON AUTOMATISMOS

FLOWCHART: project => https://drive.google.com/file/d/1YFjm_3HncAyEX1VBOtet1D0vdXyxPA-W/view?usp=sharing
		   serv_APP_selection => https://drive.google.com/file/d/1ImChibsiLTjf7Fgl6tJeAeD8pxPpUmb0/view?usp=sharing



# FORMA DE LLAMADA:
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


# TASKS
## TASK LEGEND 
	(-) => taks to do
	(*) => taks done

* actualizar el repositorio local con sus ramas y configurar el remoto
* crear el flowchart del automatismo
- descargar el automatismo que esta en el servidor y hacer un merge con el automatismo actual
- hacer que el automatismo actual funcione con recursos locales
- comparar el serv_APP_selection de los automatismos con el de test DLG.
- buscar mejor solucion para el uso de los logs
- meter toda la capaa de drivers dentro de la carpeta __CORE__




