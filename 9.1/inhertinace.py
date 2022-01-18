#Single Inheritance
class Parent:
     def func1(self):
          print("this is function one")
class Child(Parent):
     def func2(self):
          print(" this is function 2 ")
print("Single Inheritance")          
ob = Child()
ob.func1()
ob.func2()

# Multiple Inheritance
class Parent:
       def func1(self):
        print("this is function 1")
class Parent2:
   def func2(self):
        print("this is function 2")
class Child(Parent , Parent2):
    def func3(self):
        print("this is function 3")
        
print("Multiple Inheritance")           
ob = Child()
ob.func1()
ob.func2()
ob.func3()


#Multilevel Inheritance
class Parent:
      def func1(self):
          print("this is function 1")
class Child(Parent):
      def func2(self):
          print("this is function 2")
class Child2(Child):
     def func3(self):
          print("this is function 3")
          
print("Multilevel Inheritance")       
ob = Child2()
ob.func1()
ob.func2()
ob.func3()

# Hierarchical Inheritance
class Parent:
      def func1(self):
          print("this is function 1")
class Child(Parent):
      def func2(self):
          print("this is function 2")
class Child2(Parent):
      def func3(self):
          print("this is function 3")
print("Hierarchical Inheritance") 
ob = Child()
ob1 = Child2()
ob.func1()
ob.func2()

