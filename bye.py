#Byte-Verschluesselung
		
def bytekeys(a,b):
	def tobin(f):
		f = bin(f)
		return f[2:]
	
	def todec(f):
		f = "0b" + f
		return eval(f)
		
	def alphakey(a,b):
		a = ord(a);	b = ord(b)
		a = tobin(a);b = tobin(b)
		
		#Zahl maximal 256/255, also max. 1 Byte, auffullen mit Nullen
		while len(a) < 8:
			a = "0" + a
		while len(b) < 8:
			b = "0" + b
			
		#Alpha-Key wird erstellt
		akey = ""
		
		#Diff zur Elementzuweisung
		for i in range(8):
			if a[i] == "1" and a[i] == b[i]:
				akey += "1"
			else:
				akey += "0"
				
		return akey
	def betakeys(a,b):		
		akey = alphakey(a,b)
		a = ord(a);	b = ord(b)
		a = tobin(a); b = tobin(b)
		
		#Zahl maximal 256/255, also max. 1 Byte, auffullen mit Nullen
		while len(a) < 8:
			a = "0" + a
		while len(b) < 8:
			b = "0" + b
		
		#BetaKey:
		beta = ""
		for i in range(8):
			if akey[i] == "1":
				beta += "00"
			if akey[i] == "0" and a[i] == "0" and b[i] == "0":
				beta += "00"
				
			if akey[i] == "0" and a[i] == "1" and b[i] == "0":
				beta += "10" # 1 an Position i in String 0
			elif akey[i] == "0" and a[i] == "0" and b[i] == "1":
				beta += "01" # 1 an Position i in String 0
				
		return todec(beta[:8]),todec(beta[8:])
	return todec(alphakey(a,b)),betakeys(a,b)
	
	
	
