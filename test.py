print "testing"

list1 = ['cat','dog','ele']
print list1[1]

age = {}
age['George'] = 10
age['Fred'] = 20
age['Joe'] = 30

print age['George']

class Animal:
	def __init__(self,name):
		self.name = name
	def talk(self):
		print 'im talking'
		print '%s is taking' %self.name

cat = Animal("Cat")
cat.talk()