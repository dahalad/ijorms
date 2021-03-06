from .Dataset import getAsList
from .PerformanceMeasure import performanceMeasure
from .TfIdf import calculateTfWeight, calculateIdfWeight

#Naive Bayes classifier
def sentenceClassifierBag(trainingSet, testSet):
    """
    Sentence classifier for training and testing
    :param trainingSet: training data
    :param testSet: testing data
    :return: predictions of sentence and probability for that prediction
    """
    hashtable, lengths = naiveBayesTrain(trainingSet)
    predictions, prob = getPredictions(hashtable, lengths, testSet)
    return predictions, prob


def naiveBayesTrain(trainingSet):
    """
    Naive Bayes Trainer
    :param trainingSet: training data
    :return: hashtable for probalities and lengths of data
    """
    hashtable, lengths = generateHash(trainingSet)
    return hashtable, lengths

#generate hash table of probabilities
def generateHash(trainingSet):
    """
    Generate hashtable from training set.
    :param trainingSet: training data
    :return: hashtable and lengths of data
    """
    education, certification, workExperience, skill =  getAsList(trainingSet)
    tfEducation, tfWorkExperience, tfSkill, tfCertification = calculateTfWeight(education, workExperience, skill, certification)
    Idf = calculateIdfWeight(education, workExperience, skill, certification)

    vocabEducation = list(set(education))
    vocabCertification = list(set(certification))
    vocabWorkExperience = list(set(workExperience))
    vocabSkill = list(set(skill))
    # cardinality of vocabulary set otherwise referred to as lengths of data
    total = len(vocabCertification) + len(vocabSkill) + len(vocabWorkExperience) + len(vocabEducation)

    hashTable = {}
    # hashtable of probabilities generated below with add-1 laplace smoothing
    for i in vocabCertification:
        hashTable[tuple([i,'certification'])] = (sum((tfCertification[i] * Idf[i]) for p in certification if p == i) + 1) / (len(certification)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))
    for i in vocabEducation:
        hashTable[tuple([i,'education'])] = (sum((tfEducation[i] * Idf[i]) for p in education if p == i)+1) / (len(education)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))
    for i in vocabSkill:
        hashTable[tuple([i,'skill'])] = (sum((tfSkill[i] * Idf[i]) for p in skill if p == i)+1) / (len(skill)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))
    for i in vocabWorkExperience:
        hashTable[tuple([i,'workExperience'])] = (sum((tfWorkExperience[i] * Idf[i]) for p in workExperience if p == i)+1) / (len(workExperience)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))

    # considering equiprobable class, can consider non-equiprobable classes too
    hashTable['certification'] = 0.25
    hashTable['education'] = 0.25
    hashTable['skill'] = 0.25
    hashTable['workExperience'] = 0.25
    lengths = {'certification': len(certification), 'education': len(education), 'skill': len(skill), 'workExperience': len(workExperience), 'total': total}  #number of words in each class

    return hashTable, lengths


#get predictions for all the sentences
def getPredictions(hashtable, lengths, testSet):
    """
    Get predictions for all the sentences.
    :param hashtable: hashtable of probabilities
    :param lengths: cardinality of vocabulary set in each classes
    :param testSet: testing data
    :return: prediction classes with probability
    """
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
        if len(i) != 0:
            result, probab = predict(hashtable, lengths, i)
            predictionsCertification.append(result)
            probCertification.append(probab)
    predictions['certification'] = predictionsCertification
    prob['certification'] = probCertification

    for i in testSet['education']:
        if len(i) != 0:
            result, probab = predict(hashtable, lengths, i)
            predictionsEducation.append(result)
            probEducation.append(probab)
    predictions['education'] = predictionsEducation
    prob['education'] = probEducation

    for i in testSet['skill']:
        if len(i) != 0:
            result, probab = predict(hashtable, lengths, i)
            predictionsSkill.append(result)
            probSkill.append(probab)
    predictions['skill'] = predictionsSkill
    prob['skill'] = probSkill

    for i in testSet['workExperience']:
        if len(i) != 0:
            result, probab = predict(hashtable, lengths, i)
            predictionsWorkExperience.append(result)
            probWorkExperience.append(probab)
    predictions['workExperience'] = predictionsWorkExperience
    prob['workExperience'] = probWorkExperience

    return predictions, prob


#prediction for one sentence
def predict(hashtable, lengths, inVector):
    """
    Get best class label for each sentences
    :param hashtable: hashtable of probabilities
    :param lengths: vocabulary sets of each classes
    :param inVector:
    :return: Best label, best probability
    """
    probabilities = calculateClassProbabilities(hashtable, lengths, inVector)
    if len(set(list(probabilities.values()))) == 1:
        return 'Other', 0

    bestLabel, bestProb = None, -1
    for classValue, probability in list(probabilities.items()):
        if (bestLabel is None or probability > bestProb):
            bestProb = probability
            bestLabel = classValue

    return bestLabel, bestProb


#calculation of probabilities that the sentence belongs to each of the four classes
def calculateClassProbabilities(hashtable, lengths, inVector):
    """
    Calculates the probability that each sentence belongs to each of four classes
    :param hashtable: hashtable of probabilities
    :param lengths: vocabulary sets of each classes
    :param inVector:
    :return: probabilities of each sentence for each class
    """
    probabilities = {}
    for cls in ['certification', 'education', 'skill', 'workExperience']:
        probabilities[cls] = hashtable[cls]
        for i in inVector:
            if((i, cls) in hashtable.keys()):
                probabilities[cls] *= hashtable[(i, cls)]
            else:
                #handling unknown words, i.e., those that are not seen in training set
                probabilities[cls] *= (1 / (lengths['total'] + 1))

    return probabilities


def calculateBagPerformanceMeasure(NBPrediction):
    """
    Calculates the performance measure of bag model
    :param NBPrediction: Naive Bayes Predictions
    :return: Performance measure
    """
    truePositive = {}
    falseNegative = {}
    falsePositive = {}
    trueNegative = {}

    truePositive['education'] = NBPrediction['education'].count('education')
    falseNegative['education'] = len(NBPrediction['education']) - truePositive['education']
    falsePositive['education'] = NBPrediction['certification'].count('education') + NBPrediction['skill'].count('education') + NBPrediction['workExperience'].count('education')
    trueNegative['education'] = (len(NBPrediction['certification']) + len(NBPrediction['skill']) + len(NBPrediction['workExperience'])) - falsePositive['education']

    truePositive['certification'] = NBPrediction['certification'].count('certification')
    falseNegative['certification'] = len(NBPrediction['certification']) - truePositive['certification']
    falsePositive['certification'] = NBPrediction['education'].count('certification') + NBPrediction['skill'].count('certification') + NBPrediction['workExperience'].count('certification')
    trueNegative['certification'] = (len(NBPrediction['education']) + len(NBPrediction['skill']) + len(NBPrediction['workExperience'])) - falsePositive['certification']

    truePositive['skill'] = NBPrediction['skill'].count('skill')
    falseNegative['skill'] = len(NBPrediction['skill']) - truePositive['skill']
    falsePositive['skill'] = NBPrediction['education'].count('skill') + NBPrediction['certification'].count('skill') + NBPrediction['workExperience'].count('skill')
    trueNegative['skill'] = (len(NBPrediction['education']) + len(NBPrediction['certification']) + len(NBPrediction['workExperience'])) - falsePositive['skill']

    truePositive['workExperience'] = NBPrediction['workExperience'].count('workExperience')
    falseNegative['workExperience'] = len(NBPrediction['workExperience']) - truePositive['workExperience']
    falsePositive['workExperience'] = NBPrediction['education'].count('workExperience') + NBPrediction['certification'].count('workExperience') + NBPrediction['skill'].count('workExperience')
    trueNegative['workExperience'] = (len(NBPrediction['education']) + len(NBPrediction['certification']) + len(NBPrediction['skill'])) - falsePositive['workExperience']

    return performanceMeasure(truePositive, trueNegative, falsePositive, falseNegative)