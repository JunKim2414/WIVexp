class FourCal:
    def setdata(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result



a = FourCal()
a.setdata(4, 2)
sum = a.add()
print(sum)
