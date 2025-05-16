import numpy as np
import tkinter as tk
import emoji

#global array to store all subjects with respectful attributes
empty = False
names = []
attributes = []
single_attributes = []
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def update():
    global empty
    try:
        with open("C:\\Users\\belko\\Documents\\Data\\subjects.txt") as s:
            c = s.readlines()
            for l in c:
                names.append(l.strip())
                fname = "C:\\Users\\belko\\Documents\\Data\\" + l.strip() + ".txt"
                with open(fname) as r:
                    a = r.readlines()
                    attributes.append(a[1].strip())
                    if a[1].strip() not in single_attributes:
                        single_attributes.append(a[1].strip())
        empty = False
    except:
        empty = True
        start()
    start()

def write_data():
    file = []
    global names
    global single_attributes

    print("enter 0 to exit")
    name = input("enter name of subject")
    
    if name == "0":
        start()

    while str(name) in names:
        name = input("Name already exists")
        if name == 0:
            start()
    
    na = str(name).strip()

    if len(names) > 1:
        print("existing attribute sets: ")
        for i in range(0, len(single_attributes)):
            print(str(i + 1) + ". " + single_attributes[i])

    atr1 = input("enter first attribute of " + na)
    if atr1 == 0:
        start()
    atr2 = input("enter second attribute of " + na)
    if atr2 == 0:
        start()
    ao = atr1.strip()
    at = atr2.strip()
    file.append(na)
    file.append(ao + " " + at)

    count = 1

    #collect inputs
    while True:
        value1 = float(input("enter " + ao + " of " + na + " " + str(count)))
        if value1 == 0:
            break;
        value2 = float(input("enter " + at + " of " + na + " " + str(count)))
        if value2 == 0:
            break;
        file.append(str(value1) + " " + str(value2))
        count += 1

    #create and write to file:
    #create file only if file with same name does not exist
    filename = na + ".txt"
    full = "C:\\Users\\belko\\Documents\\Data\\" + filename
    c = open(full, "x")
    c.close()

    #write to new file:
    w = open(full, "a")

    for i in range(0, len(file)):
        w.write(file[i])
        w.write("\n")

    w.close()

    subjects = open("C:\\Users\\belko\\Documents\\Data\\subjects.txt", "x")
    subjects.close()

    #add subject name to record of subjects
    with open("C:\\Users\\belko\\Documents\\Data\\subjects.txt", "a+") as r:
        alll = r.readlines()
        if(len(alll) == 1):
            r.write(na)
        else:
            r.write(na)
            r.write("\n")
    update()

def categorise_data():
    #get subject names and attributes, attributes of each subject stored at same index
    global names
    #names that have the set of chosen attributes
    selected_names = []
    #attributes for each subject
    global attributes 
    #different attributes
    global single_attributes

    def simularity(first, second, length, name):
        multipliers = []
        for i in range(0, length):
            currentvalue1 = attribute1[i]
            currentvalue2 = attribute2[i]
            multipliers.append(currentvalue1/currentvalue2)
        
        multipliers.sort()

        percentiles = [None]*101

        for i in range(101):
            percentiles[i] = np.percentile(multipliers, (i)*1)

        m = first/second

        similarity = 0
        similarityl = 0
        similarityu = 0
        percentile = 0
        percentilel = 0
        percentileu = 0

        for i in range(101):
            #decision tree:
            if i != 101:
                    if m >= percentiles[i] and m <= percentiles[i + 1] :
                        percentilel = i*1
                        percentileu = (i + 1)*1
                        if i*1 <= 50 and (i+1)*1 <= 50:
                            similarityl = 100 - (50 - ((i)*1))
                            similarityu = 100 - (50 - ((i+1)*1))
                        if i*1 >= 50 and (i + 1)*10 >= 50:
                            similarityl = 100 - (((i)*1) - 50)
                            similarityu = 100 - (((i + 1)*1) - 50)
                    if m == percentiles[i]:
                        percentile = i
                        if i != 0 or i != 100:
                            if i*1 <= 50:
                                similarity = 100 - (50 - (i*1))
                            if i*1 >= 50:
                                similarity = 100 - ((i*1) - 50)  
                        if i == 0 or i == 100:
                            similarity = 100
                    
        if similarityl == 0 and similarityu == 0:
            print("0.0% similarity to a " + name)
        if similarity != 0:
            print(str(similarity) + "% similarity to a " + name)
        else:   
            print(str((similarityl + similarityu)/2) + "% similarity to a " + name)

    #print available attributes, do not repeat
    print("Select the set of attributes that your object takes:")
    for i in range(0, len(single_attributes)):
        print(str(i + 1) + "." + " " + single_attributes[i])

    #choose set of attributes and by that select the appropriate subjects
    choice = int(input())
    selected_attributes = single_attributes[choice - 1]
    for i in range(0, len(names)):
        if attributes[i] == selected_attributes:
            selected_names.append(names[i])

    lengths = []
    attribute1 = []
    attribute2 = []

    if len(selected_names) > 1:
        for i in range(0, len(selected_names)):
            fname = "C:\\Users\\belko\\Documents\\Data\\" + selected_names[i] + ".txt"
            with open(fname) as read:
                alll = read.readlines()
                lengths.append(len(alll))
                for i in range(2, len(alll)):
                    #separate different attributes:
                    atrs = alll[i].split(" ")
                    attribute1.append(float(atrs[0]))
                    attribute2.append(float(atrs[1]))
    else:
        fname = "C:\\Users\\belko\\Documents\\Data\\" + selected_names[0] + ".txt"
        with open(fname) as read:
            alll = read.readlines()
            for i in range(2, len(alll)):
                #separate different attributes:
                atrs = alll[i].split(" ")
                attribute1.append(float(atrs[0]))
                attribute2.append(float(atrs[1]))

    #ask for input attribute values:
    print("Lets check the similarity your object has to the other objects")
    print("enter 0 to exit")
    atrs = selected_attributes.split(" ")

    while True:
        global nums
        first = float(input("enter the " + atrs[0] + " of the object"))
        if first == 0:
            break;
        second = float(input("enter the " + atrs[1] + " of the object"))
        if second == "0":
            break;
        if len(selected_names) > 1:
            for i in range(0, len(selected_names)):
                simularity(float(first), float(second), lengths[i], selected_names[i])
        else:
            simularity(float(first), float(second), len(attribute1), selected_names[0])
    
    start()

def predict_value():
    global names
    length = 0
    attributes = []

    numbs = []
    print("choose your object:")
    with open("C:\\Users\\belko\\Documents\\Data\\subjects.txt") as r:
        all = r.readlines()
        for i in range(0, len(all)):
            print(str(i + 1) + ". " + all[i].strip())
            numbs.append(str(i + 1))

    choice = input()
    while choice not in numbs:
        choice = input("enter a number 1 to " + str(len(all)))
    
    fname = "C:\\Users\\belko\\Documents\\Data\\" + names[int(choice) - 1] + ".txt"

    with open(fname) as s:
        alll = s.readlines()
        length = len(alll) - 2
        attributes = alll[1].split(" ")
        
    data = [[None] * 2 for i in range(length)]
    multipliers = [None for i in range(length)]

    with open(fname) as r:
        all = r.readlines()
        for i in range(2, len(all)):
            atrs = all[i].split(" ")
            first = float(atrs[0].strip())
            second = float(atrs[1].strip())
            data[i-2][0] = first
            data[i-2][1] = second
            multipliers[i-2] = first / second

    multipliers.sort()
    percentiles = [None] * 101

    for i in range(101):
        percentiles[i] = np.percentile(multipliers, (i)*1)

    mid = np.percentile(multipliers, (50)*1)
    
    print("1. Predict " + attributes[0] + " from " + attributes[1])
    print("2. Predict " + attributes[1] + " from " + attributes[0])
    msg = "Please enter 1 or 2"
    choices = ["1", "2"]
    c = input()
    while c not in nums:
        c = input(msg)
    c = int(c)

    if c == 1:
        f = float(input("Please enter " + attributes[0]))
        print("Predicted " + attributes[1] + " = " + str(float(f) / mid))
    else:
        s = float(input("Please enter " + attributes[1]))
        print("Predicted " + attributes[0] + " = " + str(float(s) * mid))

    start()

def help():
    try:
        with open("C:\\Users\\belko\\Documents\\Data\\CaInstructions.txt", "r") as r:
            all = r.readlines()
            for i in range(0, len(all)):
                print(all[i].strip())
            print("\n")
        start()
    except:
        print("Instructions not available please download or request")
        print("\n")
        start()

def start():
    pen = emoji.emojize(":writing_hand:")
    chart = emoji.emojize(":chart_increasing:")
    category = emoji.emojize(":robot:")
    question_mark = emoji.emojize(":white_question_mark:")
    print("1. Write data" + pen)
    print("2. Predict Value" + chart)
    print("3. Categorise" + category)
    print("4. Help" + question_mark)
    
    choice = input()
    while choice not in nums:
        choice = input("Please enter a number 1 to 4")
    choice = int(choice)

    if choice == 1:
        write_data()
    if choice == 2:
        if empty == False:
            predict_value()
        else:
            print("You don't have any subjects yet, add some!")
            start()
    if choice == 3:
        if empty == False:
            categorise_data()
        else:
            print("You don't have any subjects yet, add some!")
            start()
    if choice == 4:
        help()

update()
    
