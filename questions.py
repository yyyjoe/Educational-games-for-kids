import random




class Generator(object):
    def __init__(self):
        self.counter=0
    

    def questions_generator(self,mode):
        modes={1:"+",
               2:"-",
               3:"*",
               4:"/"}
        if(mode not in modes):
            print("Please specify number from 1 to 4")
            return

        if(mode == 1):
            while True:
                num1,num2 = self.generate_random(0,10,0,10)
                result = num1+num2
                if(self.check_valid(result)):
                    break
        elif(mode == 2):
            while True:
                num1,num2 = self.generate_random(0,10,0,10)
                result = num1-num2
                if(self.check_valid(result)):
                    break   
        elif(mode == 3):
            while True:
                num1,num2 = self.generate_random(0,6,0,6)
                result = num1*num2
                if(self.check_valid(result)):
                    break
        elif(mode == 4):
            while True:
                num1,num2 = self.generate_random(0,10,1,10)
                if(num1%num2):
                    continue
                result = int(num1/num2)
                if(self.check_valid(result)):
                    break
        self.counter = self.counter+1
        return num1,num2,result
    

    def check_valid(self,num):
        if(num<0):
            return False
        ten=int(num/10)
        if(ten):
            return False
        return True

    
    def generate_random(self,start,end,start2,end2):
        num1 = random.randint(start,end)
        num2 = random.randint(start2,end2)
        return num1,num2
