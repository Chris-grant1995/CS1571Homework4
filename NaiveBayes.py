import csv

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

def column(matrix, i):
    return [row[i] for row in matrix]

def calculateProbability(data):
    
    probabilities = {}

    probabilities[0] = len(data[0]) / (len(data[0]) + len(data[1]))
    probabilities[1] = len(data[1]) / (len(data[0]) + len(data[1]))
    classValues = [0,1]
    
    for classValue in classValues:
        means = [mean(attribute) for attribute in zip(*data[classValue])]
        del means[-1]
        keyStr = "mean" + str(classValue)
        probabilities[keyStr] = means
        
        for i in range(len(means)):
            lessThanCount = 0
            greaterThanCount = 0
            for entry in data[classValue]:
                if entry[i] <= means[i]:
                    lessThanCount+=1
                else:
                    greaterThanCount+=1
            keyStrLess = str(i) + "Less|" + str(classValue)
            keyStrGreat = str(i) + "Great|" + str(classValue)

            if lessThanCount == 0:
                probabilities[keyStrLess] = .0014
            else:
                probabilities[keyStrLess] = lessThanCount/len(data[classValue])
            if greaterThanCount == 0:
                probabilities[keyStrGreat] = .0014
            else:
                probabilities[keyStrGreat] = greaterThanCount/len(data[classValue])
            # print(lessThanCount, " ", greaterThanCount)
    return probabilities

def predict(probabilities, testingSet):
    predictions = []
    mean0 = probabilities["mean0"]
    mean1 = probabilities["mean1"]
    for entry in testingSet:
        probs = [probabilities[0],probabilities[1]]
        for i in range(len(mean0)):
            value = entry[i]
            mean0Value = mean0[i]
            mean1Value = mean1[i]

            if value <= mean0Value:
                keyStr = str(i) + "Less|0"
                predict0Value = probabilities[keyStr]
            else:
                keyStr = str(i) + "Great|0"
                predict0Value = probabilities[keyStr]
            probs[0] *= predict0Value

            if value <= mean1Value:
                keyStr = str(i) + "Less|1"
                predict1Value = probabilities[keyStr]
            else:
                keyStr = str(i) + "Great|1"
                predict1Value = probabilities[keyStr]
            probs[1] *= predict1Value
        # print(probs)
        predictions.append(probs.index(max(probs)))

    # print(k0," ", k1)
    return predictions

def calculateStats(predictions,testingSet):
    falseNegatives = 0
    falsePositives = 0
    correctPredictions = 0
    for i in range(len(predictions)):
        predict = predictions[i]
        result = testingSet[i]
        if predict == 0 and result == 1:
            falseNegatives+=1
        elif predict == 1 and result == 0:
            falsePositives+=1
        else:
            correctPredictions+=1
    return (falsePositives,falseNegatives,correctPredictions)

def additionalOutputDataSplitting(groups):
    print("Iteration\t Training Positive Samples\t Training Negative Samples\t Testing Positive Samples\t Testing Negative Samples")
    for count in range(len(groups)):
        testingSet = groups[count]
        t = [x for x in groups if x != testingSet]
        trainingSet = [j for i in t for j in i]
        splitTrainingSet = separateByClass(trainingSet)
        splitTestingSet = separateByClass(testingSet)
        print(str(count + 1) + " \t" + str(len(splitTrainingSet[1])) + " \t" + str(len(splitTrainingSet[0])) + " \t " + str(len(splitTestingSet[1])) + " \t" + str(len(splitTestingSet[0])))

def additionalOutputProbabilities(groups):
    print("Values are rounded to .2 Decimal Places for Readability")
    printStr = "iter\t"
    for i in range(57):
        featureNum = i+1
        lessNotSpam = "Pr(F{}<= mui | NotSpam)".format(featureNum)
        printStr+= lessNotSpam + "\t"

        greatNotSpam = "Pr(F{}> mui | NotSpam)".format(featureNum)
        printStr+= greatNotSpam + "\t"

        lessSpam = "Pr(F{}<= mui | Spam)".format(featureNum)
        printStr+= lessSpam + "\t"

        greatSpam = "Pr(F{}> mui | Spam)".format(featureNum)
        printStr+= greatSpam + "\t"
    print(printStr)
    for count in range(len(groups)):
        testingSet = groups[count]
        t = [x for x in groups if x != testingSet]
        trainingSet = [j for i in t for j in i]
        # print(len(testingSet)," ",len(trainingSet))
        splitTrainingSet = separateByClass(trainingSet)
        probs = calculateProbability(splitTrainingSet)
        printStr = str(count +1)
        for i in range(57):
            
            # float("{0:.2f}".format(probs[keyStr]))


            keyStr = str(i) + "Less|0"
            lessNotSpam = float("{0:.2f}".format(probs[keyStr]))
            keyStr = str(i) + "Great|0"
            greatNotSpam = float("{0:.2f}".format(probs[keyStr]))
            keyStr = str(i) + "Less|1"
            lessSpam = float("{0:.2f}".format(probs[keyStr]))
            keyStr = str(i) + "Great|1"
            greatSpam = float("{0:.2f}".format(probs[keyStr]))
            printStr+="\t" + str(lessNotSpam)
            printStr+="\t" + str(greatNotSpam)
            printStr+="\t" + str(lessSpam)
            printStr+="\t" + str(greatSpam)    
        print(printStr)        

def main():
    filename = 'spambase.data'
    dataset = loadCsv(filename)
    groups = splitData(dataset)
    # summaries = summarizeByClass(groups[1])
    # # print(groups[0][1])
    # prob = calculateClassProbabilities(summaries, groups[1][0])
    # print(prob)

    additionalOutputDataSplitting(groups)
    print("")
    additionalOutputProbabilities(groups)

    for count in range(len(groups)):
        testingSet = groups[count]
        t = [x for x in groups if x != testingSet]
        trainingSet = [j for i in t for j in i]
        # print(len(testingSet)," ",len(trainingSet))
        splitTrainingSet = separateByClass(trainingSet)
        
        #Calculate Probabilities on trainingSet
        probs = calculateProbability(splitTrainingSet)
        # print(probs["0Less|0"] + probs["0Great|0"])
        # TODO Estimate Output given values on Testing Set
        predictions = predict(probs,testingSet)
        # print(predictions)

        # # print(predictions)
        testingSetResults = column(testingSet, -1)
        # print(testingSetResults)
        results = calculateStats(predictions,testingSetResults)
        # print(results)    
        print("Class", count + 1, "False Positives:", results[0], "False Negatives:", results[1],"Error Rate:", (results[0] + results[1])/(results[0] + results[1] + results[2]))
        
    
main()