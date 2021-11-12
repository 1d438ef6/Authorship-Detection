import json


a = [0,0,0]
for i in range(1,8138):
    p = "D:/Studium/Softwareprojekt/train/train/dataset-wide/truth-problem-" + str(i) + ".json"
    print(p)
    try:
        with open(p) as jsonFile:
                data = json.load(jsonFile)
        a[data["authors"]-1] += 1
    except:
        print('e')
print(a)
