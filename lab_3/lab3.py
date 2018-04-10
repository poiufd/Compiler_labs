N = ['E','T','F']
P = [('E','E+T'),('E','T'),('T','T*F'),('T','F'),('F','a'),('F','(E)')]
S = 'E'

def find_fold(imin,st):
	suff, temp_suff, new_suff = '','',''
	temp_i = -1
	imax = len(P)		
	for elem in st[2][::-1]:
		suff = elem + suff
		for i in range(len(P)):
			if suff == P[i][1] and i < imax and i > imin:
				imax = i
				temp_suff, temp_i = suff, i
				new_suff = P[i][0]
	return temp_suff, new_suff, temp_i				

def find_state(res):
	suff = res[-1][2]
	num = -1
	for rule,i in zip(res[::-1],range(len(res))):
		if rule[0] == 'q' and rule[2] == suff:
			num = i + 2
			break
	if num == -1:
		return -1
	else:			
		return res[-num]		

def algo(result,w):
	while True:
		#step1 - fold
		st = result[-1]
		while True:
			temp_suff, new_suff, temp_i = find_fold(-1,st)
			if temp_i == -1:
				break
			else:
				st = list(st)				
				st[2] = st[2].replace(temp_suff,new_suff)
				st[3] = str(temp_i+1) + st[3]
				st = tuple(st)
				result.append(st)	
		#step2 - move
		if result[-1][1] != len(w)+1:
			#move
			st = list(result[-1])
			i = st[1]
			st[1] = i+1
			st[2] += w[i-1]
			st[3] = 's' + st[3]
			result.append(tuple(st))
			#goto 1			
		else:
			#step3 - check
			st = list(result[-1])
			if st[2][1:] == S:
				st[0] = 't'
				result.append(tuple(st))
				break
			else:
				#step4 - return state
				if st[0] == 'q':
					st[0] = 'b'
					result.append(tuple(st))
				else:					
					#step5 - return
					while True:
						st = result[-1]
						try:
							new_st = find_state(result)
							new_st = list(new_st)
						#just rollback
							if (st[3][0] == 's'):
								st = list(st)
								i = st[1]
								st[1] = i-1
								st[2] = st[2][:-1]		
								st[3] = st[3][1:]	
								result.append(tuple(st))
							elif st[1] == len(w) + 1:
								new_st[0] = 'b'	
								result.append(tuple(new_st))	
							else:
								rule = int(st[3][0]) - 1
								temp_suff, new_suff, temp_i = find_fold(rule,new_st)
							# if found another fold
								if temp_i != -1:
									new_st[0] = 'q'				
									new_st[2] = new_st[2].replace(temp_suff,new_suff)
									new_st[3] = str(temp_i+1) + new_st[3]
									result.append(tuple(new_st))
									break 
								else:
									new_st[0] = 'q'
									i = new_st[1]
									new_st[1] = i+1
									new_st[2] += w[i-1]
									new_st[3] = 's' + new_st[3]
									result.append(tuple(new_st))
									break
						except:
							raise Exception("Error")
	

def main():
	result = []
	st = ('q',1,'$','e')
	w = 'a*a'
	result.append(st)
	
	try:
		algo(result,w)
		for state in result: print (state)
	except Exception as ex:
		print (ex)		




if __name__ == "__main__":
    main()
