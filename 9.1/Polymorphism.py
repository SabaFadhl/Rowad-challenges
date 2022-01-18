#1
class Vehicle:
    def message(self):
        print("Parent class method")

class Cab(Vehicle):
    def message(self):
        print("Child Cab class method")

class Bus(Vehicle):
    def message(self):
        print("Child Bus class method")


x = Vehicle()
x.message()
y= Cab()
y.message()
z = Bus()
z.message()

#2
class Message:
    
    def details(self, phrase=None):
    
        if phrase is not None:
            print('My message - ' + phrase)
        else:
            print('Welcome T\Maher')
       

# Object
x = Message()
    
# Call the method with no parameter
x.details()
    
# Call the method with a parameter
x.details('Life is beautiful')