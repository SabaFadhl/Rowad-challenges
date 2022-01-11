try:
    while True:
        num=int(input("Enter number smaller 50 "))
        if num<50:break
        
    sum=0;i=50;
    while i>=num:
        sum+=i
        i-=1
    print(sum)
except:
    print("Enter number jast!!!")

