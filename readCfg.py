import json

def loadForm(jsonf):
	f = open(jsonf)
	j = json.load(f)
	#print(f)
	f.close()
	return j


def neighborhood(iterable):
	iterator = iter(iterable)
	prev = None
	item = next(iterator)  # throws StopIteration if empty.
	for next in iterator:
		print("Here")
		yield (prev,item,next)
		prev = item
		item = next
	yield (prev,item,None)

proy = loadForm("proy.json")
print(proy['name'])


insert_header = ""
if(proy['config']['db'] == "mysql"):
	insert_header = "("
	print("Rendereando MYSQL queries and Table")
	query_table = "CREATE TABLE "+proy['name']+" ("
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
		
			
	print(query_table)
	print("Inser: ",insert_header)
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
		print (field)
		if(field['type']=="submit")or(field['type']=="button"):
			print("button")
		else:
			requestVars+="$field_"+field["name"]+" = $_REQUEST['"+field["name"]+"']; \n"
			requestVars_array.append("$field_"+field["name"])

	print (requestVars)
	print(requestVars_array)

	#Make CRUD Qeryes
	query_values = ""
	for i in range(0,len(requestVars_array)):
		print("i: ",i,"  val: ",requestVars_array[i])
		query_values+="\"'."+requestVars_array[i]+".'\""
		if(i<len(requestVars_array)-1):
			query_values+=","
	print("query_values: ", query_values)
	crud_insert = "'insert INTO `"+ proy['name'] + "` " + insert_header + " VALUES ("+query_values+")'"
	print(crud_insert)
elif(proy['config']['backend']=="node"):
	print("Creating Node backend")