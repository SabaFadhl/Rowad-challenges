total=0
while total<=50:
    try:
        
        num = int(input("input a number : "))
        total+=num
        if total>50 :
            print("the total is over 50")
            break
        print("The total is {0}".format(total))
    except:
        print("Enter number jast!!!")
    