class car:
    #constructor
    def __init__(self,year,mpg,speed) :
        self.year=year
        self.mpg=mpg
        self.speed=speed
        print("-- Car is created --")
    
    # methods
    def accelerate(self):
        return self.speed + 20

    def brake(self):
        return self.speed - 50
    
    #destructor
    def __del__(self):
        del self
        print("-- Care is deleted --")
        
#object
car1=car(2021,20,100)

#calling methods and attributes
print ("accelerate : ",car1.accelerate())
print("brake :",car1.brake())
print("year :",car1.year)
print("mpg :",car1.mpg)
print("speed :",car1.speed)

del car1