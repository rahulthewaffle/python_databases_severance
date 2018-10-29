#object methods

test = 'abc'
type(test) #prints type of object
dir(test) #lists all object methods

#object test with PartyAnimal

class PartyAnimal:
    x = 0
    name = ''

    def __init__(self, z) :
        self.name = z
        print(self.name, 'constructed')

    def __del__(self) :
        print(self.name, 'is kill', self.x)

    def party(self) :
        self.x = self.x + 1
        print(self.name, 'party count', self.x)

s = PartyAnimal("Sally")
j = PartyAnimal("Jim")

s.party()
s.party()
j.party
s.party()

s = 42
print('s contains', s)
