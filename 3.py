names=list()
for i in range(0,3):
    name=input("Enter name : ")
    names.append(name)
while 1:
    ch=input("Do you if they want to add another : ")
    if(ch.__eq__("yes")):
        name=input("Enter name : ")
        names.append(name)
    elif(ch.__eq__("no")):
        break
    else :print("Agin")
print("people numbers is %d they ar %s "%(len(names),names.__str__()))

