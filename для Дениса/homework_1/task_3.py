#Картозия,домашнее здание №1, задание 3
class UniqueObject:
     INSTANCE = None

     def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("Object has already been created")

     @classmethod
     def create_object(cls):
        if cls.INSTANCE is None:
             cls.INSTANCE = UniqueObject()
        return cls.INSTANCE

singletone = UniqueObject()
print(singletone.create_object())
