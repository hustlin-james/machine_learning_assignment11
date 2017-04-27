import sys
import re
import math
from random import randint

class HandVectorObj():
    def __init__(self,obj_id,class_lbl,sign_meaning,time_series):
        self.obj_id = obj_id
        self.class_lbl = class_lbl
        self.sign_meaning = sign_meaning
        self.time_series = time_series


        self.my_str=self.obj_id+ " "+self.class_lbl+ " "+self.sign_meaning+"\n"+"\n".join(map(str,self.time_series))+"\n"
    def __str__(self):
        return self.my_str
    def __repr__(self):
        return self.my_str

def cost(x,y):
    val1 = math.pow(x[0] - y[0], 2)
    val2 = math.pow(x[1] - y[1], 2)
    return math.sqrt(val1+val2)

def dtw_distance(x, y):
    #print(x)
    #print(y)
    dtw_distance = 0.0
    # cost(training_list[0].time_series[0], test_list[0].time_series[0])
    m = len(x)
    n = len(y)
    c = [[0.0 for i in xrange(n)] for j in xrange(m)]
    c[0][0] = cost(x[0],y[0])

    i = 1
    j = 1

    while i < m:
        c[i][0] = c[i-1][0] + cost(x[i],y[0])
        i+=1
    
    while j < n:
        c[0][j] = c[0][j-1] + cost(x[0],y[j])
        j+=1

    i = 1

    while i < m:
        j=1
        while j < n:
            c[i][j] = min(c[i-1][j],c[i][j-1],c[i-1][j-1])+cost(x[i],y[j])
            j+=1
        i+=1

    return c[m-1][n-1] 


def compute(training_list, test_list):
    
    accuracy_sum = 0.0
    for test_obj in test_list:
        min_cost = float('inf')
        my_id = int(test_obj.obj_id)
        predicted_class_dict = {}
        predicted_class = 0
        actual_class = int(test_obj.class_lbl)
        accuracy = 0.0
        
        for train_obj in training_list:
            d = dtw_distance (test_obj.time_series,train_obj.time_series)
            if d < min_cost:
                min_cost = d
                predicted_class_dict = {int(train_obj.class_lbl):1}
            elif d == min_cost:
                if d in predicted_class_dict:
                    predicted_class_dict[ int(train_obj.class_lbl)] = predicted_class_dict[d] + 1
                else:
                    predicted_class_dict[int(train_obj.class_lbl)] = 1
        
        if len(predicted_class_dict.keys()) == 1 and actual_class in predicted_class_dict:
            accuracy = 1.0
            predicted_class = predicted_class_dict.keys()[0]
        else:
            if actual_class in predicted_class_dict:
                accuracy = 1.0/len(predicted_class_dict.keys())
                predicted_class = predicted_class_dict.keys()[randint(0,len(predicted_class_dict.keys())-1)]
            else:
                accuracy = 0.0
                predicted_class = predicted_class_dict.keys()[randint(0,len(predicted_class_dict.keys())-1)]

        
        accuracy_sum += accuracy
        print("ID=%5d, predicted=%3d, true=%3d, accuracy=%4.2f, distance = %.2f\n"%(my_id,predicted_class,actual_class,accuracy,min_cost))
    
    print("classification accuracy=%6.4f\n"%(accuracy_sum/len(test_list)))
   

def read_file(file_name):
    hand_objs = []
    with open(file_name, 'r') as myfile:
        data=myfile.read()

    obj_str_list = data.split('-------------------------------------------------')
    for obj_str in obj_str_list:
        f = [line for line in obj_str.split('\n') if line.strip() != '']
        #obj_id = f[0].split('object ID: ')[1]
        if len(f) != 0:
            obj_id = f[0].split('object ID: ')[1]
            class_lbl = f[1].split('class label: ')[1]
            sign_meaning = f[2].split('sign meaning: ')[1]
            assert f[3].find('dominant hand trajectory:') != -1
            
            idx = 4

            time_series = []
            while idx < len(f):
                d = f[idx].split()
                tup = (float(d[0]),float(d[1]))
                time_series.append(tup)
                idx += 1
            h = HandVectorObj(obj_id,class_lbl,sign_meaning,time_series)
            hand_objs.append(h) 
           
    return hand_objs

def main():
    training_file = sys.argv[1]
    test_file = sys.argv[2]

    training_list = read_file(training_file)
    test_list = read_file(test_file)

    compute(training_list,test_list)
if __name__ == "__main__":
    main()