N = ['S','F']
P = [("S","F"),("S","(S+F)"),('F','1')]
S = 'S'

def find1(nont,el):
	for rule in P:
		if rule[0] == nont and rule[1][0] == el:
			return rule[1]
	return False

def find2(nont):
	for rule in P:
		if rule[0] == nont and rule[1][0] in N:
			return rule
	return False

def _find(nont,el):
	found1 = find1(nont,el)
	found2 = find2(nont)
	if found1:
		return found1
	elif found2:
		try:
			return _find (found2[1][0],el) + found2[1][1:]
		except Exception as ex:
			raise Exception("Error")		
	else:
		raise Exception("Error")	

def rec_des_parsing(w):
	result = ''
	for symbol in w:
		if result == '':
			result = _find('S',symbol)[1:] + result
		elif result[0] in N:
			result = _find(result[0],symbol)[1:] + result[1:]
		elif result[0] == symbol:
			result = result[1:]
	if result == '':
		return True
	else:
		return False	
				 	

def main():
	try:
		print(rec_des_parsing('(1+1)'))
	except Exception as ex:
		print False	


if __name__ == "__main__":
    main()

