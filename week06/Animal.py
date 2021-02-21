from abc import ABCMeta, abstractmethod
class Animal(metaclass=ABCMeta):
    animal_type = ''
    size = ''
    nature = ''
    @property
    def ferocious(self):
        if self.size >= '中等' and self.animal_type == '食肉' and self.nature == '凶猛':
            return True
        else:
            return False

class Cat(Animal):
    name = ''
    voice = ''
    def __init__(self, name=None, animal_type=None, size=None, nature=None):
        self.name = name
        self.animal_type = animal_type
        self.size = size
        self.nature = nature
    @property
    def fit_for_pet(self):
        if super.ferocious:
            return False
        else:
            return True

class Dog(Animal):
    name = ''
    voice = ''
    def __init__(self, name=None, animal_type=None, size=None, nature=None):
        self.name = name
        self.animal_type = animal_type
        self.size = size
        self.nature = nature
    @property
    def fit_for_pet(self):
        if super.ferocious:
            return False
        else:
            return True

class Zoo(object):
    name = None
    animals = set()

    def __init__(self, name=None):
        self.name = name

    def add_animal(self,animal):
        self.animals.add(animal)

    def __getattr__(self, item): 
        for animal in self.animals:
            print(f'animal is {animal.__class__.__name__ },query is {item}')
            if animal.__class__.__name__ == item:
                return True
        # 不存在的属性返回默认值 'OK'
        raise AttributeError("No animal")

if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    print(have_cat)