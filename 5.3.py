import sys

names=["maher","saba","salwa"]
while True:
    print('''
      Choose number :
      1- add a name to the list
      2- change a name in the list
      3- delete a name from the list 
      4- view all the names in the list
      5- exit''')
    num=int(input("Enter your choice : "))
    try:  
        if num==1:
            new=input("Enter name ")
            names.append(new)
            print(names)
        elif num==2:
            old=input("Enter old name ")
            new=input("Enter new name ")
            if old not in names :print(old," not found")
            else:
                names.insert(names.index(old),new)
                names.remove(old)
            print(names)
        elif num==3:
            delete=input("Enter  name to delete it ")
            if delete not in names :print(delete," not found")
            else:
                names.remove(delete)
        elif num==4:
            for i in range(1,len(names)+1):print (i,"-",names[i])
        elif num==5:
          break
          #exit()
        else:
            print ("Choose number from 1 to five ") 
    except:
         print ("Enter number ")
        
