import json

def bytes_to_int(bytes): #transforma a hexadecimal cadenas de largas, para 1 byte usar ord(byte)
  return int(bytes, 16)

def generateJson(bytes):
    print("bytes::::",bytes[0:4])
    try:
        data = json.dumps({
        	#"a": ord(bytes[12]), 
            "energia_total": bytes_to_int(bytes[46:50]), 
            "corriente_acumulada": bytes_to_int(bytes[56:60]), 
            "potencia_acumulada": bytes_to_int(bytes[68:72])
            #"prueba": bytes_to_int("ffff") 
        	#"temperature": bytes_to_int(bytes[9:11])/10.0, 
        	#"checksum": check_checksum(bytes), 
        	#"length": check_length(bytes)
        	})
    except:
        data = json.dumps({})
    return data

def saveJson(data,json_file):
	with open(json_file, 'w') as outfile:
		json.dump(data,outfile)

def checksum(bytes):
    suma = 0
    for b in bytes:
        suma += ord(b)
    return suma

def check_checksum(bytes):
    return checksum(bytes[:-2]) == bytes_to_int(bytes[-2:])

def check_length(bytes):
	return ord(bytes[8]) == len(bytes[11:])