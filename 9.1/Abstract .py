class Animal(): 
    def feed(self):
        pass
class Lion(Animal):
    def feed(self):
        print("Feeding a lion with raw meat!") 

class Panda(Animal): 
    def feed(self): 
        print("Feeding a panda with some tasty bamboo!") 

class Snake(Animal): 
    def feed(self): 
        print("Feeding a snake with mice!")

zoo = [Lion(), Panda(), Snake()]

for animal in zoo:
    animal.feed() 