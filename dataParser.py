import json

def bytes_to_int(bytes): #transforma a hexadecimal cadenas de largas, para 1 byte usar ord(byte)
  return int(bytes.encode('hex'), 16)

def generateJson(bytes):
    data = json.dumps({
    	"a": ord(bytes[12]), 
    	"b": bytes_to_int(bytes[22:24]), 
    	"temperature": bytes_to_int(bytes[9:11])/10.0, 
    	"checksum": check_checksum(bytes), 
    	"length": check_length(bytes)
    	})
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