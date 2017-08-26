def main():
	file = open("test.txt","r")
	if file:
		#print ('read\t' + file.read() + '\n')
		i = file.readline()
		print ('readline  ' + i + '\n')
		i = file.readline()
		ans1 = 7
		if i == ans1:
			print ('Test passed')
		#print ('readlines\t' + str(file.readlines()) + '\n')
	file.close()
if __name__ == '__main__':
	main()
