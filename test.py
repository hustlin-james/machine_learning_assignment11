from random import randint
def main():

    actual_class = 1
    predicted_class_dict = {1:2,2:1}

    # if len(predicted_class_dict.keys()) == 1 and actual_class in predicted_class_dict:
    #     accuracy = 1.0
    #     predicted_class = predicted_class_dict.keys()[0]
    # else:
    if actual_class in predicted_class_dict:
        accuracy = 1.0/len(predicted_class_dict.keys())
        predicted_class = predicted_class_dict.keys()[randint(0,len(predicted_class_dict.keys())-1)]
    else:
        accuracy = 0.0
        predicted_class = predicted_class_dict.keys()[randint(0,len(predicted_class_dict.keys())-1)]

    print(accuracy)

if __name__ == "__main__":
    main()