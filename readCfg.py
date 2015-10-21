import json

def loadForm(jsonf):
	f = open(jsonf)
	j = json.load(f)
	#print(f)
	f.close()
	return j


proy = loadForm("proy.json")
print(proy['name'])


insert_header = ""
php_credits ="/*****************************\n 	Developer:"+proy['config']['developer']+"\n 	Agency:Miru Interactive \n******************************/\n\n"
if(proy['config']['db'] == "mysql"):
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
	tableFile = open(proy['config']['local_store']+"Table_"+proy['name']+".tab",'w')
	tableFile.write(query_table)
	tableFile.close()

elif(proy['config']['db'] == "mongo"):
	print("Rendering Mongo Schema and CRUD functions")
elif(proy['config']['db'] == "email"):
	print("Rendereando envio por mail")

if(proy['config']['backend']=="php"):
	print("Creating Php backend")
	
	requestVars = ""
	requestVars_array =[]
	for field in proy['content']:
		#print (field)
		if('catalog' in field):
			print("Hay CATALOGO: ",field['catalog']['name'])
			print("Rendereando Catalogo ",field['catalog']['type'],proy['config']['db'])
			if(proy['config']['db'] == "mysql"):
				#Crear Tabla
				catalog_table = "CREATE TABLE "+field['catalog']['name'] +" ("
				print("CATALOGO TABLE: ",catalog_table)

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
					

					print("Have Id: ",id_size," val:",size_val)
					catalog_table += "id int("+str(id_size)+") not null primary key , val VARCHAR("+str(size_val)+"))"
					
					
				else:
					print("Haven't id")
					catalog_have_id = False
					catalog_table += "id int(3) unsigned zerofill not null auto_increment primary key , val VARCHAR("+str(size_val)+"))"

				print(catalog_table)
				f = open(proy['config']['local_store']+field['catalog']['name']+".tab","w")
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
				print(insert_catalog)
				f = open(proy['config']['local_store']+field['catalog']['name']+"_contents.tab","w")
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

elif(proy['config']['backend']=="node"):
	print("Creating Node backend")

if(proy['config']['frontend']=="html"):
	print("Rendering Html Form")

elif(proy['config']['frontend']=="ejs"):
	print("Rendering Ejs Form View")