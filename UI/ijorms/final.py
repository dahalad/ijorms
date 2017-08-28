# =======================================================================================================================
# Uncomment in case of Windows
# Give path to the tika jar file
# os.environ['CLASSPATH'] = "C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/tika-app-1.14.jar"
# from jnius import autoclass # Import the Java classes we are going to need
# =======================================================================================================================

import copy
from ast import literal_eval
from tika import parser
from .Dataset import *
from .InformationExtraction import extractSkills, extractWorkExperience, extractEducation, extractCertification
from .NaiveBayes import sentenceClassifierNB, predict
from .PerformanceMeasure import performanceMeasure
from .TfIdf import tfidf



def classifiers():
    """
    Classifies the training data, test it with testing data and calculates the performance measures for each classifier
    """
    data = readDataset()
    splitRatio = 0.1
    splittedDataset = tenChunks(copy.deepcopy(data), splitRatio)

    totalTruePositiveNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalTrueNegativeNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalsePositiveNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalseNegativeNB = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}

    totalFmeasureNBCertification = 0
    totalFmeasureNBEducation = 0
    totalFmeasureNBSkill = 0
    totalFmeasureNBWorkExperience = 0

    totalAccuracyNBCertification = 0
    totalAccuracyNBEducation = 0
    totalAccuracyNBSkill = 0
    totalAccuracyNBWorkExperience = 0

    totalTruePositiveTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalTrueNegativeTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalsePositiveTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}
    totalFalseNegativeTfIdf = {'education':0, 'certification':0, 'skill':0, 'workExperience':0}

    totalFmeasureTfIdfCertification = 0
    totalFmeasureTfIdfEducation = 0
    totalFmeasureTfIdfSkill = 0
    totalFmeasureTfIdfWorkExperience = 0

    totalAccuracyTfIdfCertification = 0
    totalAccuracyTfIdfEducation = 0
    totalAccuracyTfIdfSkill = 0
    totalAccuracyTfIdfWorkExperience = 0

    # Train and Test 10 times for 10 chunks. Each chunk becomes test set once and training set other nine times
    for r in range(10):
        trainingSet = {'education': [], 'workExperience': [], 'skill': [], 'certification': []}
        testSet = splittedDataset[r]
        for j in list(set(range(0, 9)) - {r}):
            trainingSet['education'].extend(splittedDataset[j]['education'])
            trainingSet['workExperience'].extend(splittedDataset[j]['workExperience'])
            trainingSet['skill'].extend(splittedDataset[j]['skill'])
            trainingSet['certification'].extend(splittedDataset[j]['certification'])

        NBPrediction, NBProbability = sentenceClassifierNB(copy.deepcopy(trainingSet), copy.deepcopy(testSet))
        truePositiveNB, trueNegativeNB, falsePositiveNB, falseNegativeNB, accuracyNBCertification, accuracyNBEducation, accuracyNBSkill, accuracyNBWorkExperience, fmeasureNBCertification, fmeasureNBEducation, fmeasureNBSkill, fmeasureNBWorkExperience = performanceMeasure(NBPrediction)
        totalTruePositiveNB['certification'] += truePositiveNB['certification']
        totalTruePositiveNB['education'] += truePositiveNB['education']
        totalTruePositiveNB['skill'] += truePositiveNB['skill']
        totalTruePositiveNB['workExperience'] += truePositiveNB['workExperience']
        totalTrueNegativeNB['certification'] += trueNegativeNB['certification']
        totalTrueNegativeNB['education'] += trueNegativeNB['education']
        totalTrueNegativeNB['skill'] += trueNegativeNB['skill']
        totalTrueNegativeNB['workExperience'] += trueNegativeNB['workExperience']
        totalFalsePositiveNB['certification'] += falsePositiveNB['certification']
        totalFalsePositiveNB['education'] += falsePositiveNB['education']
        totalFalsePositiveNB['skill'] += falsePositiveNB['skill']
        totalFalsePositiveNB['workExperience'] += falsePositiveNB['workExperience']
        totalFalseNegativeNB['certification'] += falseNegativeNB['certification']
        totalFalseNegativeNB['education'] += falseNegativeNB['education']
        totalFalseNegativeNB['skill'] += falseNegativeNB['skill']
        totalFalseNegativeNB['workExperience'] += falseNegativeNB['workExperience']

        totalFmeasureNBCertification += fmeasureNBCertification
        totalFmeasureNBEducation += fmeasureNBEducation
        totalFmeasureNBSkill += fmeasureNBSkill
        totalFmeasureNBWorkExperience += fmeasureNBWorkExperience
        totalAccuracyNBCertification += accuracyNBCertification
        totalAccuracyNBEducation += accuracyNBEducation
        totalAccuracyNBSkill += accuracyNBSkill
        totalAccuracyNBWorkExperience += accuracyNBWorkExperience

        TfIdfPrediction, TfIdfWeight = tfidf(copy.deepcopy(trainingSet), copy.deepcopy(testSet))
        truePositiveTfIdf, trueNegativeTfIdf, falsePositiveTfIdf, falseNegativeTfIdf, accuracyTfIdfCertification, accuracyTfIdfEducation, accuracyTfIdfSkill, accuracyTfIdfWorkExperience, fmeasureTfIdfCertification, fmeasureTfIdfEducation, fmeasureTfIdfSkill, fmeasureTfIdfWorkExperience = performanceMeasure(TfIdfPrediction)
        totalTruePositiveTfIdf['certification'] += truePositiveTfIdf['certification']
        totalTruePositiveTfIdf['education'] += truePositiveTfIdf['education']
        totalTruePositiveTfIdf['skill'] += truePositiveTfIdf['skill']
        totalTruePositiveTfIdf['workExperience'] += truePositiveTfIdf['workExperience']
        totalTrueNegativeTfIdf['certification'] += trueNegativeTfIdf['certification']
        totalTrueNegativeTfIdf['education'] += trueNegativeTfIdf['education']
        totalTrueNegativeTfIdf['skill'] += trueNegativeTfIdf['skill']
        totalTrueNegativeTfIdf['workExperience'] += trueNegativeTfIdf['workExperience']
        totalFalsePositiveTfIdf['certification'] += falsePositiveTfIdf['certification']
        totalFalsePositiveTfIdf['education'] += falsePositiveTfIdf['education']
        totalFalsePositiveTfIdf['skill'] += falsePositiveTfIdf['skill']
        totalFalsePositiveTfIdf['workExperience'] += falsePositiveTfIdf['workExperience']
        totalFalseNegativeTfIdf['certification'] += falseNegativeTfIdf['certification']
        totalFalseNegativeTfIdf['education'] += falseNegativeTfIdf['education']
        totalFalseNegativeTfIdf['skill'] += falseNegativeTfIdf['skill']
        totalFalseNegativeTfIdf['workExperience'] += falseNegativeTfIdf['workExperience']

        totalFmeasureTfIdfCertification += fmeasureTfIdfCertification
        totalFmeasureTfIdfEducation += fmeasureTfIdfEducation
        totalFmeasureTfIdfSkill += fmeasureTfIdfSkill
        totalFmeasureTfIdfWorkExperience += fmeasureTfIdfWorkExperience
        totalAccuracyTfIdfCertification += accuracyTfIdfCertification
        totalAccuracyTfIdfEducation += accuracyTfIdfEducation
        totalAccuracyTfIdfSkill += accuracyTfIdfSkill
        totalAccuracyTfIdfWorkExperience += accuracyTfIdfWorkExperience

    # These are for measuring performance, print them out to get the results
    finalFmeasureNBCertification = totalFmeasureNBCertification * 0.1
    finalFmeasureNBEducation = totalFmeasureNBEducation * 0.1
    finalFmeasureNBSkill = totalFmeasureNBSkill * 0.1
    finalFmeasureNBWorkExperience = totalFmeasureNBWorkExperience * 0.1

    finalAccuracyNBCertification = totalAccuracyNBCertification * 0.1
    finalAccuracyNBEducation = totalAccuracyNBEducation * 0.1
    finalAccuracyNBSkill = totalAccuracyNBSkill * 0.1
    finalAccuracyNBWorkExperience = totalAccuracyNBWorkExperience * 0.1

    finalFmeasureTfIdfCertification = totalFmeasureTfIdfCertification * 0.1
    finalFmeasureTfIdfEducation = totalFmeasureTfIdfEducation * 0.1
    finalFmeasureTfIdfSkill = totalFmeasureTfIdfSkill * 0.1
    finalFmeasureTfIdfWorkExperience = totalFmeasureTfIdfWorkExperience * 0.1

    finalAccuracyTfIdfCertification = totalAccuracyTfIdfCertification * 0.1
    finalAccuracyTfIdfEducation = totalAccuracyTfIdfEducation * 0.1
    finalAccuracyTfIdfSkill = totalAccuracyTfIdfSkill * 0.1
    finalAccuracyTfIdfWorkExperience = totalAccuracyTfIdfWorkExperience * 0.1



# def NaiveBayesModel():
#     data = readDataset()
#     generateHash(data)

# def TFModel():
#     data = readDataset()
#     calculateTfWeight(data)
#     calculateIdfWeight(data)


# get plain text using Apache Tika
def getText(filename):
    """
    Parses the given file.
    :param filename: Input file
    :return: parsed content
    """

    # Uncomment following lines for Windows
    # Tika = autoclass('org.apache.tika.Tika')
    # Metadata = autoclass('org.apache.tika.metadata.Metadata')
    # FileInputStream = autoclass('java.io.FileInputStream')
    # tika = Tika()
    # meta = Metadata()
    # text = tika.parseToString(FileInputStream(filename), meta)

    parsed = parser.from_file(filename)
    text = parsed['content']
    return text

#preprocess the test resume to get tokens
def preprocess(content):
    """
    Cleans the data
    :param content: parsed data
    :return: cleaned data
    """
    c = content.lower()
    c = c.replace('.\n', '\n')
    for punc in [',',':','|','/',';','-','–','—','(',')']:
        c = c.replace(punc,' ')
    c = c.split('\n')
    c = list(filter(lambda x: x != '', c))
    tokens = []
    for i in c:
        token = i.split(' ')
        token = list(filter(lambda x: x != '', token))
        tokens.append(token)

    return tokens


def loadAll():
    """
    Reads hashtables and calculate weights
    :return: TF Values
    """
    hashTable = {}
    lengths = {}
    Idf = {}
    tfCertification = {}
    tfEducation = {}
    tfSkill = {}
    tfWorkExperience = {}
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/NaiveBayesModel.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        # i[0] kina gareko vanda csv file ma skill, workexp, etc ko chhutai rakheko chha, aru ko vane tuple ma rakehko
        # chha, like so '(keyword, class)', prob_value ani hashtable ma rakhne ho
        for i in reader:
            if (i[0] == 'skill' or i[0] == 'workExperience' or i[0] == 'education' or i[0] == 'certification'):
                hashTable[i[0]] = float(i[1])
            else:
                # literal eval le chai tuple mai rakhidinchha
                hashTable[literal_eval(i[0])] = float(i[1])
    inp.close()
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/Lengths.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            lengths[i[0]] = float(i[1])
    inp.close()
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/IDFModel.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            Idf[i[0]] = float(i[1])
    inp.close()
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/TFCertificationModel.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfCertification[i[0]] = float(i[1])
    inp.close()
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/TFEducationModel.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfEducation[i[0]] = float(i[1])
    inp.close()
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/TFSkillModel.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfSkill[i[0]] = float(i[1])
    inp.close()
    with open('C:/Users/Sweta/Desktop/Final Year Project/Integrated-Final/major/UI/ijorms/TFExperienceModel.csv', 'r') as inp:
        reader = list(csv.reader(inp))
        for i in reader:
            tfWorkExperience[i[0]] = float(i[1])
    inp.close()
    return hashTable, lengths, Idf, tfCertification, tfEducation, tfSkill, tfWorkExperience



def main(filename):
    """
    Extracts information from resume and creates ontology tree
    :param filename: fie
    :return: extracted information and ontology tree
    """
    content = getText(filename)
    tokens = preprocess(content)

    hashTable, lengths, Idf, tfCertification, tfEducation, tfSkill, tfWorkExperience = loadAll()
    result = {'Other':[], 'certification': [], 'education': [], 'skill': [], 'workExperience': []}
    for i in tokens:
        label, prob = predict(hashTable, lengths, i)
        result[label].append(i)
    ##information extract garda gardai ontology pani banai rako chha
    IEskills, ontologySkill = extractSkills(result['skill'])
    print(IEskills)
    IEWorkExperience, ontologyWorkExperience = extractWorkExperience(result['workExperience'])
    print (IEWorkExperience)
    IEeducation = extractEducation(result['education'])
    print(IEeducation)
    IEcertification, linksCertification = extractCertification(result['certification'])
    print(IEcertification)
    return IEskills, ontologySkill, IEWorkExperience, ontologyWorkExperience, IEeducation, IEcertification, linksCertification
