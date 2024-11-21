class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.age == other.age
        return False

    def __lt__(self, other):
        if isinstance(other, Person):
            return self.age < other.age
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Person):
            return self.age > other.age
        return NotImplemented

# Création de deux instances de Person
person1 = Person("Alice", 30)
person2 = Person("Bob", 30)
person3 = Person("Charlie", 25)

# Comparaison des âges
print(person1 == person2)  # True, car les âges sont égaux
print(person1 == person3)  # False, car les âges sont différents
print(person1 < person3)   # False, car 30 n'est pas inférieur à 25
print(person1 > person3)   # True, car 30 est supérieur à 25
