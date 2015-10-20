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
	query_table += "id int(3) unsigned zerofill not null auto_increment primary key,"
	index = 0
	for field in proy['content']:
		if((index+1)<len(proy['content'])):
			#print("field: ",field," content: ",proy['content'][index+1])
			if(field['type']=='button'):
				print("BOTON")
			else:
				query_table += field['name']+" "
				insert_header+= "`"+field['name']+"`"


			if(field['type']=='text_single')or(field['type']=="textarea"):
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
		if(field['type']=="submit")or(field['type']=="button"):
			print("button")
		else:
			requestVars+="$field_"+field["name"]+" = $_REQUEST['"+field["name"]+"']; \n"
			requestVars_array.append("$field_"+field["name"])

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