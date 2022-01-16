#Question 1
# str_list = ["I", "Love", "Yemen"]
# print(" ".join(str_list))
#Question 2

#functiom
def third():
    while True:
        try:
            num=int(input("please enter number or 0 to exit : "))
            if num==0:
                break
            elif len(str(num))<3 :
                print(" enter number consist from 3 or more digits ") 
            else:
                print(str(num)[2])
        except:
            print("enter number !!!")
 #calling           
third()