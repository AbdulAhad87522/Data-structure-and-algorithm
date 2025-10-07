#example 1.5
#import numpy 
#arrar = []
#min = 1
#max = 20
#n = 5
    
#3arr = numpy.random.randint(min , max , 5)
#print(arr)

#example 1.8




with open("test.txt", "r") as f:
    lines = f.read()
    
print(lines)
numbers = [] 
arr = lines.split() 
for s in arr: 
    num = s 
    numbers.append(num) 
 
print(numbers) 

arr = ['uet' , 'lahore' , 'main campus']
f = open(file="test.txt" , mode="w")
for i in arr:
    f.write (i + "/n")
print("data printed")
