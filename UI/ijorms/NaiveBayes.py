from .Dataset import getAsList
import math

# Naive Bayes classifier for resumes, earlier was for training dataset
# Can place this code in a single file to reduce the lines of code (to be done later)
def sentenceClassifierNB(trainingSet, testSet):
    """
    Naive Bayes sentence classifier
    :param trainingSet: training set
    :param testSet: test set
    :return: predictions and probabilites
    """
    hashtable, lengths = naiveBayesTrain(trainingSet)
    predictions, prob = getPredictions(hashtable, lengths, testSet)
    return predictions, prob


def naiveBayesTrain(trainingSet):
    """
    Train Naive Bayes Model with training set
    :param trainingSet: training set
    :return: hastable and vocabulary for naive bayes model
    """
    hashtable, lengths = generateHash(trainingSet)
    return hashtable, lengths

#generate hash table of probabilities
def generateHash(trainingSet):
    """
    Generate hash table and vocabulary
    :param trainingSet: training set
    :return: hashtable and vocabulary set
    """
    education, certification, workExperience, skill =  getAsList(trainingSet)
    vocabEducation = list(set(education))
    vocabCertification = list(set(certification))
    vocabWorkExperience = list(set(workExperience))
    vocabSkill = list(set(skill))
    total = len(vocabCertification) + len(vocabSkill) + len(vocabWorkExperience) + len(vocabEducation)

    # hashtable of probabilities generated below with add-1 laplace smoothing
    hashTable = {}
    for i in vocabCertification:
        hashTable[tuple([i,'certification'])] = (sum(1 for p in certification if p == i) + 1) / (len(certification)+(total))
    for i in vocabEducation:
        hashTable[tuple([i,'education'])] = (sum(1 for p in education if p == i)+1) / (len(education)+(total))
    for i in vocabSkill:
        hashTable[tuple([i,'skill'])] = (sum(1 for p in skill if p == i)+1) / (len(skill)+(total))
    for i in vocabWorkExperience:
        hashTable[tuple([i,'workExperience'])] = (sum(1 for p in workExperience if p == i)+1) / (len(workExperience)+(total))

    hashTable['certification'] = 0.25
    hashTable['education'] = 0.25
    hashTable['skill'] = 0.25
    hashTable['workExperience'] = 0.25
    lengths = {'certification': len(certification), 'education': len(education), 'skill': len(skill), 'workExperience': len(workExperience), 'total': total}  #number of words in each class

    return hashTable, lengths

# ======================================================================================================================
# To create csv file for the first time
# def storeLengths(lengths):
#     with open('Lengths.csv','w') as out:
#         writer = csv.writer(out)
#         for entry in lengths:
#             writer.writerow([entry, lengths[entry]])
#     out.close()

# def storeModel(hashTable):
#     with open ('NaiveBayesModel.csv','w') as out:
#         writer = csv.writer(out)
#         for entry in hashTable:
#             writer.writerow([entry, hashTable[entry]])
# ======================================================================================================================


def getPredictions(hashtable, lengths, testSet):
    predictions = {}
    prob = {}
    predictionsCertification = []
    probCertification = []
    predictionsEducation = []
    probEducation = []
    predictionsSkill = []
    probSkill = []
    predictionsWorkExperience = []
    probWorkExperience = []

    for i in testSet['certification']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsCertification.append(result)
            probCertification.append(probab)
    predictions['certification'] = predictionsCertification
    prob['certification'] = probCertification

    for i in testSet['education']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsEducation.append(result)
            probEducation.append(probab)
    predictions['education'] = predictionsEducation
    prob['education'] = probEducation

    for i in testSet['skill']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsSkill.append(result)
            probSkill.append(probab)
            if result == 'workExperience':
                print(i)
    predictions['skill'] = predictionsSkill
    prob['skill'] = probSkill


    for i in testSet['workExperience']:
        if(len(i) != 0):
            result, probab = predict(hashtable, lengths, i)
            predictionsWorkExperience.append(result)
            probWorkExperience.append(probab)
    predictions['workExperience'] = predictionsWorkExperience
    prob['workExperience'] = probWorkExperience

    return predictions, prob


def predict(hashtable, lengths, inVector):
    probabilities = calculateClassProbabilities(hashtable, lengths, inVector)
    if(probabilities['certification']-(math.log10(hashtable['certification'])) == probabilities['education']-(math.log10(hashtable['education'])) and probabilities['certification']-(math.log10(hashtable['certification'])) == probabilities['skill']-(math.log10(hashtable['skill'])) and probabilities['certification']-(math.log10(hashtable['certification'])) == probabilities['workExperience']-(math.log10(hashtable['workExperience']))):
        return 'Other', 0

    bestLabel, bestProb = None, -1
    for classValue, probability in list(probabilities.items()):
        if (bestLabel is None or probability > bestProb):
            bestProb = probability
            bestLabel = classValue


    return bestLabel, bestProb


def calculateClassProbabilities(hashtable, lengths, inVector):
    probabilities = {}
    for cls in ['certification', 'education', 'skill', 'workExperience']:
        probabilities[cls] = (math.log10(hashtable[cls]))
        for i in inVector:
            if((i, cls) in hashtable.keys()):
                probabilities[cls] += (math.log10(hashtable[(i, cls)]))
            else:
                probabilities[cls] += (math.log10((1 / (lengths['total'] + 1))))
    return probabilities