#Function to add 0 or more numbers way 1
def add(*s):
    return sum(s)

print(add(2,3))
print(add(2,3,4))

#Function to add 0 or more numbers way 2
def add(x,*s):
    return x+sum(s)

print(add(2,3))
print(add(2,3,4))