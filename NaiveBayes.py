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

def calculateProbability(x, mean, stdev):
    # print(x, " ", mean)
    if x > mean:
        return 10000
    else:
        return .0014

def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue  in summaries.keys():
        classSummaries = summaries[classValue]
        probabilities[classValue] = 1
        print(classValue)
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities

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
    # TODO Calculate Probabilities on trainingSet

    # TODO Estimate Output given values on Testing Set

    # TODO Calculate Stats

    # for testingSet in groups:
    #     t = [x for x in groups if x != testingSet]
    #     trainingSet = [j for i in t for j in i]
    #     print(len(testingSet)," ",len(trainingSet))
        
    
main()