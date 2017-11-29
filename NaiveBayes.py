import csv
import math
def loadCsv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset

def splitData(data):
    
    groups = [[],[],[],[],[]]
    # print(len(data))
    for i in range(len(data)):
        groupNum = i%5
        groups[groupNum].append(data[i])
        
    return groups

def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated


def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)

def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries

def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    # print(separated[1][0])
    summaries = {}
    for classValue in separated.keys():
        instances = separated[classValue]
        summaries[classValue] = summarize(instances)
    return summaries

# def calculateProbability(x, mean, stdev):
#     # print(x, " ", mean)
#     if x > mean:
#         return 10000
#     else:
#         return .0014

# def calculateClassProbabilities(summaries, inputVector):
#     probabilities = {}
#     for classValue  in summaries.keys():
#         classSummaries = summaries[classValue]
#         probabilities[classValue] = 1
#         print(classValue)
#         for i in range(len(classSummaries)):
#             mean, stdev = classSummaries[i]
#             x = inputVector[i]
#             probabilities[classValue] *= calculateProbability(x, mean, stdev)
#     return probabilities


def calculateProbability(data):
    probabilities = {}

    probabilities[0] = len(data[0]) / (len(data[0]) + len(data[1]))
    probabilities[1] = len(data[1]) / (len(data[0]) + len(data[1]))
    classValues = [0,1]
    #Dict Keys = Attr Number value | spamValue
    for classValue in classValues:
        for attrNum in range(57):
            keyString = str(attrNum) + " "
            occurances = {}
            for entry in data[classValue]:
                attrValue = entry[0]
                if attrValue not in occurances.keys():
                    occurances[attrValue] = 0
                occurances[attrValue]+=1
            for key,value in occurances.items():
                keyString += str(key) + " | " + str(classValue)
                prob = value/len(data[classValue])
                probabilities[keyString] = prob
                keyString = str(attrNum) + " "
    
    return probabilities

def predict(probabilities, testingSet):
    predictions = []
    k0 = 0
    k1 = 1
    for entry in testingSet:
        entry = testingSet[0]
        # print(entry)
        probs = [1,1]
        
        for attrIndex in range(len(entry)):
            keyString = str(attrIndex) + " " + str(entry[attrIndex]) + " | "
            keyString0 = keyString+str(0)
            keyString1 = keyString+str(1)
            # print(probs)
            if keyString0 not in probabilities.keys():
                k0+=1
                probs[0]*= .0014
            else:
                probs[0]*= probabilities[keyString0]

            if keyString1 not in probabilities.keys():
                k1+=1
                probs[1]*= .0014
            else:
                probs[1]*= probabilities[keyString1]
        
        predictions.append(probs.index(max(probs)))


    print(k0," ", k1)
    return predictions

def main():
    filename = 'spambase.data'
    dataset = loadCsv(filename)
    print('Loaded data file {0} with {1} rows'.format(filename, len(dataset)))
    groups = splitData(dataset)
    # summaries = summarizeByClass(groups[1])
    # # print(groups[0][1])
    # prob = calculateClassProbabilities(summaries, groups[1][0])
    # print(prob)
    testingSet = groups[0]
    t = [x for x in groups if x != testingSet]
    trainingSet = [j for i in t for j in i]
    print(len(testingSet)," ",len(trainingSet))
    splitTrainingSet = separateByClass(trainingSet)
    
    #Calculate Probabilities on trainingSet
    probs = calculateProbability(splitTrainingSet)

    # TODO Estimate Output given values on Testing Set
    predictions = predict(probs,testingSet)
    print(predictions)
    # TODO Calculate Stats

    # for testingSet in groups:
    #     t = [x for x in groups if x != testingSet]
    #     trainingSet = [j for i in t for j in i]
    #     print(len(testingSet)," ",len(trainingSet))
        
    
main()