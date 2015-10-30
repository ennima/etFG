import json,os


def loadForm(jsonf):
	f = open(jsonf)
	j = json.load(f)
	#print(f)
	f.close()
	return j
def pathValidation():
	#Si no existe local_store crealo
	if(os.path.exists(proy['config']['local_store'])):
		print("local_store Dir ok")
	else:
		os.mkdir(proy['config']['local_store'])
def db_mysql():
	if(os.path.exists(path_sql)):
		print("SQL Dir ok")
	else:
		os.mkdir(path_sql)

	#Make connect file
	mysql_connect = "<?php \n"+php_credits+"$conn = new mysqli(\""+proy['config']['db_server']+"\", \""+proy['config']['db_user']+"\", \""+proy['config']['db_pass']+"\", \""+proy['config']['db_name']+"\"); \n"
	mysql_connect += 'if ($conn->connect_error) { \n  die("Connection failed: " . $conn->connect_error); \n} \n ?> '
	mysql_connect_file = open(proy['config']['local_store']+"connect.php",'w')
	mysql_connect_file.write(mysql_connect)
	mysql_connect_file.close()

	insert_header = "("
	print("Rendereando MYSQL queries and Table")
	query_table = "CREATE TABLE "+proy['name']+" ("
	query_table += "id int(6) unsigned zerofill not null auto_increment primary key,"
	index = 0
	for field in proy['content']:
		if((index+1)<len(proy['content'])):
			#print("field: ",field," content: ",proy['content'][index+1])
			if(field['type']=='button'):
				print("BOTON")
			else:
				query_table += field['name'].lower()+" "
				insert_header+= "`"+field['name'].lower()+"`"


			if(field['type']=='text_single')or(field['type']=="textarea")or((field['type']=="combo")):
				query_table += "VARCHAR("+field['size']+")"
				
			if(proy['content'][index+1]['type']=="submit"):
				
				print("----------------")
			else:
				if(field['type']=='button'):
					print("BUTTON")
				else:
					query_table+=", "
					insert_header+=", "

			index+=1
		else:
			#print("FIELD: ",field)
			query_table +=")"
			insert_header+=")"
		
			
	#print(query_table)
	#print("Inser: ",insert_header)
	tableFile = open(path_sql+"Table_"+proy['name']+".tab",'w')
	tableFile.write(query_table)
	tableFile.close()

def backend_php():
	print("Creating Php backend")
	
	requestVars = ""
	requestVars_array =[]
	for field in proy['content']:
		#print (field)
		if('catalog' in field):
			#print("Hay CATALOGO: ",field['catalog']['name'])
			print("Rendereando Catalogo ",field['catalog']['type'],proy['config']['db'])
			if(proy['config']['db'] == "mysql"):
				#Crear Tabla
				catalog_table = "CREATE TABLE "+field['catalog']['name'] +" ("
				#print("CATALOGO TABLE: ",catalog_table)

				size_val = 0
				for item in field['catalog']['list']:
					#print(len(item['val']))
					if(len(item['val'])>size_val):
						size_val = len(item['val'])
				size_val+=5
				catalog_have_id = False
				if('id' in field['catalog']['list'][0]):
					
					total_items = len(field['catalog']['list'])
					id_size = len(str(total_items)) + 1
					catalog_have_id = True
					

					#print("Have Id: ",id_size," val:",size_val)
					catalog_table += "id int("+str(id_size)+") not null primary key , val VARCHAR("+str(size_val)+"))"
					
					
				else:
					#print("Haven't id")
					catalog_have_id = False
					catalog_table += "id int(3) unsigned zerofill not null auto_increment primary key , val VARCHAR("+str(size_val)+"))"

				#print(catalog_table)
				f = open(path_sql+field['catalog']['name']+".tab","w")
				f.write(catalog_table)
				f.close()

				if(catalog_have_id):
					insert_catalog = "INSERT INTO "+field['catalog']['name']+" (id,val) VALUES "
				else:
					insert_catalog = "INSERT INTO "+field['catalog']['name']+" (val) VALUES "
				catalog_list_val = ""
				count = 0
				for item in field['catalog']['list']:
					#print("Cat: ",item)
					if(catalog_have_id):
						#print("("+item['id']+","+item['val']+")")
						catalog_list_val += "("+item['id']+",\""+item['val']+"\")"
					else:
						#print("("+item['val']+")")
						catalog_list_val += "(\""+item['val']+"\")"
					count+=1
					if(count<len(field['catalog']['list'])):
						catalog_list_val+=","
					else:
						catalog_list_val+=";"
					
				#print(catalog_list_val)
				insert_catalog+=catalog_list_val
				#print(insert_catalog)
				f = open(path_sql+field['catalog']['name']+"_contents.tab","w")
				f.write(insert_catalog)
				f.close()


		if(field['type']=="submit")or(field['type']=="button"):
			print("button")
		else:
			requestVars+="$field_"+field["name"].lower()+" = $_REQUEST['"+field["name"].lower()+"']; \n"
			requestVars_array.append("$field_"+field["name"].lower())

	#print (requestVars)
	#print(requestVars_array)

	#Make CRUD Qeryes
	query_values = ""
	for i in range(0,len(requestVars_array)):
		#print("i: ",i,"  val: ",requestVars_array[i])
		query_values+="\"'."+requestVars_array[i]+".'\""
		if(i<len(requestVars_array)-1):
			query_values+=","
	#print("query_values: ", query_values)
	crud_insert = "'INSERT INTO `"+ proy['name'] + "` " + insert_header + " VALUES ("+query_values+")'"
	#print(crud_insert)
	#Make Insert Query File
	
	php_insert = "<?php \n"+php_credits+"require('connect.php'); \n"+requestVars+"\n \n$query_insert = "+crud_insert+"; \necho $query_insert; \n if ($conn->query($query_insert) === TRUE) { \n    echo \"New record created successfully\"; \n } else {\n    echo \"Error: \" . $query_insert . \"<br>\" . $conn->error;\n } \n$conn->close();\n?>"
	php_insert_file = open(proy['config']['local_store']+"insert_"+proy['name']+".php",'w')
	php_insert_file.write(php_insert)
	php_insert_file.close()

	crud_delete ="DELETE FROM `test` WHERE `Name` = 'name'"	

def db_mongo_node():
	if(os.path.exists(path_models)):
		print("Mongo_node Models Dir ok")
	else:
		os.mkdir(path_models)

	
	connect_js = "var mongoose = require('mongoose');\n"
	connect_js += "mongoose.connect('mongodb://"+proy['config']['db_server']+"/"+proy['config']['db_name']+"');\n"

	connect_js += "var db = mongoose.connection;\n"
	connect_js += "db.on('error', console.error.bind(console, 'connection error'));\n"
	connect_js += "db.once('open', function (callback){\n"
	connect_js += "	console.log('open db');\n"
	connect_js += "});"
	
	#print connect_js
	f = open(path_models+"connect.js","w")
	f.write(connect_js)
	f.close()

	mongoose_schema = "var mongoose = require('mongoose');\nvar Schema = mongoose.Schema;\n"
	schemaName = proy['name'].lower()+"_schema"
	modelName = proy['name'].lower().title()+"s"
	mongoose_schema += "var "+schemaName+" = new Schema({\n"
	for field in proy['content']:
		print field['type']
		if(field['type']=='button'):
			pass
		elif(field['type']=='button'):

	mongoose_schema += "});\n"
	mongoose_schema += "mongoose.model('"+modelName+"', "+schemaName+");"
	print (mongoose_schema)
proy = loadForm("proy2.json")
print(proy['name'])
pathValidation()
path_sql = proy['config']['local_store']+"sql\\"
path_models = proy['config']['local_store']+"models\\"
insert_header = ""
php_credits ="/*****************************\n 	Developer:"+proy['config']['developer']+"\n 	Agency:Miru Interactive \n******************************/\n\n"


if(proy['config']['db'] == "mysql"):
	db_mysql()

elif(proy['config']['db'] == "mongo"):
	print("Rendering Mongo Schema and CRUD functions")
	if(proy['config']['backend']=="node"):
		print("Making Mongoose schemas")
		db_mongo_node()

elif(proy['config']['db'] == "email"):
	print("Rendereando envio por mail")

elif(proy['config']['db'] == "json"):
	print("Rendereando envio por mail")
	
if(proy['config']['backend']=="php"):
	backend_php()

elif(proy['config']['backend']=="node"):
	print("Creating Node backend")

if(proy['config']['frontend']=="html"):
	print("Rendering Html Form")

elif(proy['config']['frontend']=="ejs"):
	print("Rendering Ejs Form View")