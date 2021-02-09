class Friends:
    def __init__(self, name, age, job = 'Unemployed'):
        self.name = name
        self.age = age
        self.job = job

    def hasJob(self):
        if self.job == 'Unemployed':
            pass
        else:
            print ("Job : %s" % (self.job))

f = Friends('Jun', 30, 'Programmer')
f.hasJob()
