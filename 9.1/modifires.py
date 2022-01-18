class Person:
    def __init__(self, name, age, height):
        self.name     = name   # public
        self._age     = age    # protected
        self.__height = height # private

p1 = Person("Saba",23,150)

print(p1.name)        # public: can be accessed
print(p1._age)        # protected: can be accessed but not advised
print(p1.__height)  # private: will give AttributeError