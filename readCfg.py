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

	print("Rendereando MYSQL queries and Table")
	query_table = "CREATE TABLE "+proy['name']+" ("
	index = 0
	for field in proy['content']:
		if((index+1)<len(proy['content'])):
			print("field: ",field," content: ",proy['content'][index+1])
			query_table += field['name']+" "
			if(field['type']=='text_single')or(field['type']=="textarea"):
				query_table += "VARCHAR("+field['size']+")"
				
				if(proy['content'][index+1]['type']=="submit"):
					
					print("----------------")
				else:
					query_table+=", "
			

			index+=1
		else:
			print("FIELD: ",field)
			query_table +=")"
		
			
	print(query_table)

elif(proy['config']['db'] == "mongo"):
	print("Rendering Mongo Schema and CRUD functions")