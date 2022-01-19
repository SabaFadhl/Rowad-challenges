class Schoolmembers:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def detail(self):
        print('Name: {0} , Age: {1}'.format(self.name, self.age), end=" ")

class Teachers(Schoolmembers):
    def __init__(self, name, age, salary):
        Schoolmembers.__init__(self, name, age)
        self.salary = salary
        
    def detail(self):
        Schoolmembers.detail(self)
        print(', salary: {0}'.format(self.salary))

class Students(Schoolmembers):
    passORfails=" "
    def __init__(self, name, age, marks):
        Schoolmembers.__init__(self, name, age)
        self.marks = marks    
    
    
    def detail(self):
        Schoolmembers.detail(self)
        print(', marks: {0}'.format(self.marks))
        
    
    def succeed(self):
        if(self.marks>=50):
            print ("the student is successful ")
        else:
            print("the student is fails")


t = Teachers('Maher', 40, 80000)
s = Students('Saba', 25, 98)


members = [t, s]
for m in members:
    if(m is t):
        m.detail()
    else:
        m.detail()
        print(m.succeed())
        