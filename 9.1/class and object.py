class car:
    # attributes
        year = 2016     
        mpg =  20       # mileage
        speed = 100     
    # methods
        def accelerate(self):
            return car.speed + 20

        def brake(self):
            return car.speed - 50
#object
car1=car()

#calling methods and attributes
print ("accelerate : ",car1.accelerate())
print("brake :",car1.brake())
print("year :",car1.year)
print("mpg :",car1.mpg)
print("speed :",car1.speed)