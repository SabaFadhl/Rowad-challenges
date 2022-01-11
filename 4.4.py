while True:
    try:
        num = int(input("enter a number between 10 and 20 "))
        if num < 10:
            print("Too low")
        elif num > 20:
            print("Too high")
        else:
            print("Thank you")
            break
    except:
        print("Enter number jast!!!")
