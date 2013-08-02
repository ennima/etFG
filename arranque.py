import os.path

def leeConfiguracion(archivo):
	if(os.path.exists(archivo)):
		f = open(archivo)

		for line in f:
			print line
	else:
		print "Archivo de Configuracion no encontrado: "+archivo

leeConfiguracion("config.conf")
