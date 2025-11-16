class MyInt():
	def __init__(self, value):
		self.v = value

	def __add__(self, other):
		return self.v + other.v	


n_1 = MyInt(input('1er nombre : '))
n_2 = MyInt(input('2eme nombre : '))

print("Somme : ", n_1 + n_2)
