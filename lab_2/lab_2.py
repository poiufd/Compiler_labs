import re
N = ['S','A','B']
P = [('S','0A'),('S','1S'),('S','e'),('A','0B'),('A','1A'),('B','0S'),('B','1B')]

def first_elem(l):
	result = []
	for rule in P:
		if rule[0]==l and not rule[1].isupper():
			result.append(rule[1])
	return "|".join(result)

def other_elem(l):
	result, koef = [], []
	for nont in N:
		for rule in P:
			if rule[0]==l and rule[1].endswith(nont):
				temp = rule[1][:-1]
				koef.append(temp)		
		result.append("|".join(koef))
		koef = []
	return result	

def make_equation():
	return [other_elem(nont)+[first_elem(nont)]   for nont in N]

def solve_equation(eq):
	#like Gauss forward part
	for i in range(len(eq)):
		line = eq[i]
		if '|' in line[i]:
			koef = '('+line[i]+')'+ '*'
		else:
			koef = line[i]+ '*'
		for j in range (len(line)):
			if j != i:
				if line[j] == 'e':
					eq[i][j] = koef
				elif line[j] != '':
					eq[i][j] = koef + line[j]	

		for j in range(i+1, len(eq)):
			next_line = eq[j]
			if next_line[i] != '':
				koef, next_line[i] = next_line[i], ''
				temp = [koef+line[k]+"|"+next_line[k] if k!=i and line[k]!='' else next_line[k] for k in range (len(eq)+1)]	
				eq[j] = map (lambda x: x[:-1] if x.endswith('|') else x,temp) 
	#last root
	roots = ['' for i in range(len(eq))]
	if eq[-1][-1] == '':
		roots[-1] = eq[-1][-2]
	else:
		roots[-1] = eq[-1][-1]	
	#backward
	flag = False
	for i in range (len(eq)-2,-1,-1):
		if flag:
			flag = False
			roots[i+1] = '('+roots[i+1]+')'
		line = eq[i]
		temp = [line[j] + roots[j] for j in range (len(line)-1) if line[j] != '' and j != i ]
		if line[-1] != '':
			temp = temp+[line[-1]]
		if len(temp)>1:
			temp = "|".join(temp)	
			flag = True
			roots[i] = temp
		else:
			roots[i] = temp[0]

	return roots

def main():
	roots = solve_equation(make_equation())
	print roots
#['1*01*0(01*01*0+1)*01*+1*', '1*0(01*01*0+1)*01*', '(01*01*0+1)*01*']
	nfa = re.compile(roots[0])
	if nfa.match('0001'):
		print "True"
	else:
		print "False"

if __name__ == "__main__":
    main()
