import  functools
numbers =[1, 2, 3,8,2, 4]
names=["saba","Fadhl","Ali","Alwesabi"]

print(list(map(lambda x: x + x, numbers)))
print(list(zip(names, numbers)))
print(functools.reduce(lambda a, b: a if a > b else b, numbers))#find max 
print(list(filter(lambda x: x % 2 != 0, numbers)))#odd


