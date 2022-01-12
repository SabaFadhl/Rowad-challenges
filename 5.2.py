from random import randrange
import sys
def rand():
    #------------------1--------------------------
    try:
            print("Enter low and high number ")
            low = int(input("low =  "))
            high = int(input("high =  "))
            return randrange(low,high)
           
    except:
            print("Enter number jast!!!")
            return


def ask():
    #--------------------2-----------------------
    comp_num=rand()    
    print("I am thinking of a number…")
    while True:
        try:
            guess = int(input("guess the number : "))
            if check(guess,comp_num):break
        except:
            print("Enter number jast!!!")
            
def check(guess,comp_num):
    #--------------------3-----------------------
    if guess.__eq__(comp_num) :
        print("Correct, you win")
        return True 
    elif guess.__lt__(comp_num) : 
        print("too low") 
    elif guess.__gt__(comp_num) : 
        print("too high") 

ask()# calling -start program