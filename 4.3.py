while True:
    try:
        num = int(input("how many people the user wants to invite to a party : "))
        if num < 10:
            i=1
            while i<=num:
                name = str(input("Enter name : "))
                print("%s has been invited"%name)
                i+=1
        else:
            print("Too many people")
            
    except:
        print("Enter number jast!!!")
