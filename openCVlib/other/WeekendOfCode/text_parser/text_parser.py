import sys

def appEnd(flag):

	if flag==1:
		file.close()
	sys.exit()


path = "testfile.text" #input("path (e.x. testfile.text): ") #'testfile.text'

procType = "symbols" #input("Select process method (words, sentences, symbols): ")

minSymb = 20#int(input("Min count symbols: "))

maxSymb = 50#int(input("Max count symbols: "))

wordsNumb = 2#nt(input("Number of words: "))

#print(wordsNumb)

sentNumb = 4#int(input("Number of sentences: "))

file = open(path, encoding="utf8")  # 'r' winsows...


# print(file.read())


str1 = file.read()

# print(str1)

# wordsObj = str1.split(' ')
# concString = "";

# sordsNumb = 200

# for x in range(0, sordsNumb):
# 	concString += wordsObj[x] + ' '


# print(concString)

concString = ""

wordsObj = str1.split(' ') # split to words
sentObj = str1.split('.') # add &, !

if procType == "symbols":
    #print("symbols")
        if (len(concString) < maxSymb): #and len(concString) > minSymb
                print(concString)
        elif(len(concString) > maxSymb):
                print(concString[0 : maxSymb])
elif procType == "words":

	# wordsObj = str1.split(' ')
	
	
	for x in range(0, wordsNumb):
		concString += wordsObj[x] + ' '
		# print(len(concString.split(' '))) # words ammount

	if (len(concString) < maxSymb): #and len(concString) > minSymb
		print(concString)
	elif(len(concString) > maxSymb):
		print(concString[0 : maxSymb])
	# elif < min

	#print(concString)
    # print("words")
elif procType == "sentences":
	print("sentences")
	# sentObj = str1.split('.') # add &, !
	concString = ""

	for x in range(0, sentNumb):
		concString += sentObj[x] + '.'
		#print(len(concString.split(' '))) # words ammount

	if (len(concString.split(' ')) > wordsNumb):
		for x in range(0, wordsNumb):
			concString += wordsObj[x] + ' '
		# print(concString)
		# print("< words")
	# elif(len(concString.split(' ')) > wordsNumb):
		# wordsObj = str1.split(' ')
	# for x in range(0, wordsNumb):
	# 	concString += wordsObj[x] + ' '
	if(len(concString) < maxSymb and len(concString) > minSymb):
		# size = 0
		print(concString)
		print("< symbols")
	elif(len(concString) > maxSymb):
		print(concString[0 : maxSymb])
		# elif < min


	# if (len(concString.split(' ')) < maxSymb and len(concString.split(' ')) > minSymb):
	# 	print(concString)
	# elif(len(concString.split(' ')) > minSymb):
	# 	print(concString[0 : minSymb])

else:
    print("Please, read man, you sun of the bitch :)")
    appEnd(0)



#appEnd(1)

