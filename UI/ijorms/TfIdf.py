import math
from .Dataset import getAsList


def tfidf(trainingSet, testSet):
    """
    Train and Test data for tfidf
    :param trainingSet: training set
    :param testSet: test set
    :return: predictions and weights
    """
    tfEducation, tfWorkExperience, tfSkill, tfCertification = calculateTfWeight(trainingSet)
    Idf = calculateIdfWeight(trainingSet)
    predictions, weights = getPredictionsTfIdf(testSet, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf)
    return predictions, weights


#calculation of the TF weights
def calculateTfWeight(trainingSet):
    """
    Calculates tf weights
    :param trainingSet: training set
    :return: results for each class
    """
    education, certification, workExperience, skill = getAsList(trainingSet)
    tfEducation = {}
    tfWorkExperience = {}
    tfSkill = {}
    tfCertification = {}

    for i in education:
        if(i not in tfEducation.keys()):
            # Log-frequency weighting, can use other (accuracy needs to be checked)
            tfEducation[i] = 1 + math.log10(sum(1 for p in education if p == i))
    for i in workExperience:
        if(i not in tfWorkExperience.keys()):
            tfWorkExperience[i] = 1 + math.log10(sum(1 for p in workExperience if p == i))
    for i in skill:
        if(i not in tfSkill.keys()):
            tfSkill[i] = 1 + math.log10(sum(1 for p in skill if p == i))
    for i in certification:
        if(i not in tfCertification.keys()):
            tfCertification[i] = 1 + math.log10(sum(1 for p in certification if p == i))
    return tfEducation, tfWorkExperience, tfSkill, tfCertification

# Uncomment following line to store in csv file for the first time
# def storeTFModel(tfCertification, tfEducation, tfSkill, tfWorkExperience):
#     with open('TFCertificationModel.csv', 'w') as out1:
#         writer1 = csv.writer(out1)
#         for entry1 in tfCertification:
#             writer1.writerow([entry1, tfCertification[entry1]])
#     out1.close()
#     with open('TFEducationModel.csv', 'w') as out2:
#         writer2 = csv.writer(out2)
#         for entry2 in tfEducation:
#             writer2.writerow([entry2, tfEducation[entry2]])
#     out2.close()
#     with open('TFSkillModel.csv', 'w') as out3:
#         writer3 = csv.writer(out3)
#         for entry3 in tfSkill:
#             writer3.writerow([entry3, tfSkill[entry3]])
#     out3.close()
#     with open('TFExperienceModel.csv', 'w') as out4:
#         writer4 = csv.writer(out4)
#         for entry4 in tfWorkExperience:
#             writer4.writerow([entry4, tfWorkExperience[entry4]])
#     out4.close()


def calculateIdfWeight(trainingSet):    #calculation of IDF weights
    """
    Calculates idf weights
    :param trainingSet: training data
    :return: idf value
    """
    education, certification, workExperience, skill = getAsList(trainingSet)
    temp = education + workExperience + skill + certification
    Idf = {}
    for i in temp:
        if(i not in Idf.keys()):
            Idf[i] = 0
            if(i in education):
                Idf[i] = Idf[i] + 1
            if(i in workExperience):
                Idf[i] = Idf[i] + 1
            if(i in skill):
                Idf[i] = Idf[i] + 1
            if(i in certification):
                Idf[i] = Idf[i] + 1
            Idf[i] = math.log10(4 / Idf[i])
    return Idf

# Uncomment following lines to store in csv file for the first time
# def storeIDFModel(Idf):
#     with open('IDFModel.csv', 'w') as out:
#         writer = csv.writer(out)
#         for entry in Idf:
#             writer.writerow([entry, Idf[entry]])
#     out.close()


def getPredictionsTfIdf(testSet, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf):     #get predictions for all the sentences
    """
    Get tfidf predictions for sentences
    :param testSet: test set
    :param tfEducation:
    :param tfWorkExperience:
    :param tfSkill:
    :param tfCertification:
    :param Idf:
    :return: Predictions
    """
    predictions = {}
    weights = {}
    predictionsCertification = []
    weightCertification = []
    predictionsEducation = []
    weightEducation = []
    predictionsSkill = []
    weightSkill = []
    predictionsWorkExperience = []
    weightWorkExperience = []

    for i in testSet['certification']:
        result, weig = predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf)
        predictionsCertification.append(result)
        weightCertification.append(weig)
    predictions['certification'] = predictionsCertification
    weights['certification'] = weightCertification

    for i in testSet['education']:
        result, weig = predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf)
        predictionsEducation.append(result)
        weightEducation.append(weig)
    predictions['education'] = predictionsEducation
    weights['education'] = weightEducation

    for i in testSet['skill']:
        result, weig = predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf)
        predictionsSkill.append(result)
        weightSkill.append(weig)
    predictions['skill'] = predictionsSkill
    weights['skill'] = weightSkill

    for i in testSet['workExperience']:
        result, weig = predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf)
        predictionsWorkExperience.append(result)
        weightWorkExperience.append(weig)
    predictions['workExperience'] = predictionsWorkExperience
    weights['workExperience'] = weightWorkExperience

    return predictions, weights


def predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf):      #prediction for one sentence
    """
    Get tfidf prediction for each sentence
    :param i:
    :param tfEducation:
    :param tfWorkExperience:
    :param tfSkill:
    :param tfCertification:
    :param Idf:
    :return: prediction
    """
    weight = {}
    weight['education'] = 0
    weight['workExperience'] = 0
    weight['skill'] = 0
    weight['certification'] = 0

    for word in i:
        if(word in tfEducation.keys()):
            weight['education'] = weight['education'] + tfEducation[word] * Idf[word]
        if(word in tfWorkExperience.keys()):
            weight['workExperience'] = weight['workExperience'] + tfWorkExperience[word] * Idf[word]
        if(word in tfSkill.keys()):
            weight['skill'] = weight['skill'] + tfSkill[word] * Idf[word]
        if(word in tfCertification.keys()):
            weight['certification'] = weight['certification'] + tfCertification[word] * Idf[word]
    if (len(set(list(weight.values()))) == 1):
        return 'Other', 0

    bestLabel, bestWeight = None, -1
    for classValue, weig in list(weight.items()):
        if (bestLabel is None or weight[classValue] > bestWeight):
            bestWeight = weig
            bestLabel = classValue

    return bestLabel, bestWeight