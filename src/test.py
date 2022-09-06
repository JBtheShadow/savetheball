class Parent:
    value = 12

    def __init__(self):
        self.otherValue = self.value * 100

    def printValue(self):
        print(self.value)

    def somethingElse(self):
        return self.value * 100

    # below errors out
    #otherValue = somethingElse()

class Child(Parent):
    value = 21

p, c = Parent(), Child()

p.printValue()
c.printValue()

print(p.otherValue, c.otherValue)