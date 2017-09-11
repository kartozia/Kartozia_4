#Картозия,домашнее здание №1, задание 2
import random

class Pet:
    def __init__(self, name):
        self._name = name
    
    def get_name(self):
        return self._name
    
    def voice(self):
        return 'feed me'
    
    def isCute(self):
        return True
    
class Dog(Pet):   
    def __init__(self, name):
        super().__init__(name)
    
    def voice(self):
        return 'Woof'

class Shiba_inu(Dog):   
    def __init__(self, name):
        super().__init__(name)
    
    def voice(self):
        return 'Wow wow'

class Cat(Pet):   
    def __init__(self, name):
        super().__init__(name)
    
    def voice(self):
        return 'Meow'

class Fluffy(Cat):   
    def __init__(self, name):
        super().__init__(name)

    def voice(self):
        return 'Puuurrrrr'
    
class Grumpy(Cat):   
    def __init__(self, name):
        super().__init__(name)
    
    def isCute(self):
        return False

class Fox(Pet):   
    def __init__(self, name):
        super().__init__(name)

    def voice(self):
        return 'Ring-ding-ding-ding-dingeringeding'

    def isCute(self):
        if random.random() > 0.5:
            return False
        else:
            return True

pet = Fox('Masha')
print(pet.isCute())
