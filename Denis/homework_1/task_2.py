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
        return 'Wow so cool'

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

class Owner:
    def __init__(self, animal):
        self.animal = animal
    def can_you_pet(self):
        if self.animal.isCute() == True:
             return 'You can pet %s and it says %s' % (self.animal.get_name(), self.animal.voice())
        else:
            return "%s don't touch me!" % (self.animal.voice())
        
pet = Fox('Juniper')
person = Owner(pet)
print(person.can_you_pet())
#полиморфизм: каждый питомец наследует методы класса Pet.По умолчанию все питомцы
# милые и их можно гладить. Но, например, класс Grumpy в методе isCute возвращает
# False и хозяюину его нельзя трогать, Fox дружелюбна по настроению, а Шиба-ину всегда
# рада хозяину
        
