dirc=input("Choose top or down ")
if dirc.lower().__eq__("top"):
    try:
        top=int(input("Enter top number "))
        sum=0;i=1;
        while i<=top:
            sum+=i
            i+=1
        print(sum)
    except:
        print("Enter number jast!!!")
elif dirc.lower().__eq__("down"):
    try:
        down=int(input("Enter domn number "))
        sum=0;i=20;
        while i>=down:
            sum+=i
            i-=1
        print(sum)
    except:
        print("Enter number jast!!!")
else : print("I don’t understand")

