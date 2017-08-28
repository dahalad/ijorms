import requests, ast
from xml.etree import ElementTree
from .InformationExtraction import getData
from ..models import JobApplicant


def ranking(jobApplicant, applicant, job):
    """
    Match resume education, workexperience etc with job description and reward points
    :param jobApplicant: relationship between job and applicant
    :param applicant: job applicant
    :param job: job applied to
    :return: ranking
    """

    # Wait while processing
    while(not applicant.applicant_Edu):
        continue
    jobSkill = (job.skills).lower().split(',')
    jobWE = (job.work_experience).lower().split(',')
    jobEducation = (job.degree).lower().split(',')
    if(job.certification):
        jobCertification = (job.certification).lower().split(',')
    else:
        jobCertification = [""]

    eduscore = matchEducation((applicant.applicant_Edu).split('\n'), jobEducation)
    # if education requirements matches
    if(eduscore != -1):
        skillscore = matchSkill(applicant.skill_ontology, jobSkill, jobWE)
        wescore = matchWE(applicant.work_experience_ontology, jobWE, jobSkill)
        certiscore = matchCertification(applicant.certification_link, jobCertification, jobSkill, jobWE)
        jobApplicant.skillScore = (skillscore)
        jobApplicant.workExpScore = (wescore)
        jobApplicant.certificationScore = (certiscore)
        jobApplicant.educationScore = (eduscore)
    jobApplicant.save()
    allApplicants = JobApplicant.objects.filter(job=jobApplicant.job)
    sums = []
    for app in allApplicants:
        suma = 0
        suma += app.skillScore + app.workExpScore + app.educationScore + app.certificationScore
        sums.append(suma)
    sorted_unique = sorted(set(sums), reverse=True)
    ordinal_map = {val: i for i, val in enumerate(sorted_unique, 1)}
    ordinals = [ordinal_map[val] for val in sums]
    for ss in range(len(allApplicants)):
        allApplicants[ss].rank = ordinals[ss]
        allApplicants[ss].save()


def matchEducation(userEducation, jobEducation):
    """
    Matches the skills of user with job requirements
    :param userEducation: users education details
    :param jobEducation: job description educational details
    :return: education score for a job for a applicant
    """
    degree = {0: '', 1: 'associate', 2: 'bachelor', 3: 'master', 4: 'phd'}
    highestDegree = 0
    jobDegree = -1
    for i in userEducation:
        if (i.startswith('b') and highestDegree < 2):
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 2
        elif (i.startswith('m') and highestDegree < 3):
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 3
        elif (i.startswith('a') and highestDegree < 1):
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 1
        elif (i.startswith('p') or i == 'doctor' or i == 'doctorate') and highestDegree < 4:
            url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i.split(';')[0]
            response = requests.get(url)
            tree = ElementTree.fromstring(response.content)
            if(len(tree) != 0):
                q1 = "SELECT ?description WHERE { " + "<" + tree[0][
                    1].text + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
                data = getData(q1)['results']['bindings']
                if (len(data) != 0):
                    if (data[0].keys().__contains__('description')):
                        pp = data[0]['description']['value'].lower()
                        if pp.__contains__("degree"):
                            highestDegree = 4

    for jj in jobEducation:
        if (jj[0] == 'a' and jobDegree < 1):
            jobDegree = 1
        elif (jj[0] == 'b' and jobDegree < 2):
            jobDegree = 2
        elif (jj[0] == 'm' and jobDegree < 3):
            jobDegree = 3
        elif (jj[0] == 'p' or i == 'doctor' or i == 'doctorate') and jobDegree < 4:
            jobDegree = 4
    if(highestDegree < jobDegree):
        return -1
    else:
        return 1



def matchSkill(userSkillOntology, jobSkill, jobWE):
    """
    Match user's skills with job requirements
    :param userSkillOntology: User's skill ontology
    :param jobSkill: job's skill and experience requiremnets
    :param jobWE: experience requirements
    :return: scores for skill and experience
    """
    score = 0
    ontology = ast.literal_eval(userSkillOntology)
    for j in jobSkill:
        for k in ontology:
            if (j in k['label']):
                score += 1
                break
            else:
                p = ''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 0.5
                    break

    for j in jobWE:
        for k in ontology:
            if (j in k['label']):
                score += 0.25
                break
            else:
                p = ''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 0.125
                    break
    return score


def matchWE(userWEOntology, jobWE, jobSkill):
    ontology = ast.literal_eval(userWEOntology)
    score = 0
    for j in jobWE:
        for k in ontology:
            if (j == k['label']):
                score += 1
                break
            else:
                p = ''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 0.5
                    break

    for j in jobSkill:
        for k in ontology:
            if (j == k['label']):
                score += 1.5
                break
            else:
                p=''
                for nt in k['parent']:
                    p += nt + ' '
                if(j in p):
                    score += 1.25
                    break
    return score


def matchCertification(userCertificationLink, jobCertification, jobSkill, jobWE):
    score =0
    for i in jobCertification:
        url = "http://lookup.dbpedia-spotlight.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + i
        response = requests.get(url)
        tree = ElementTree.fromstring(response.content)
        if(len(tree) != 0):
            for j in userCertificationLink:
                if(j == tree[0][1].text):
                    score += 2

    for j in userCertificationLink:
        q1 = "SELECT ?description WHERE { " + "<" + j + ">" + "dbo:abstract ?description. filter langMatches(lang(?description),'EN')}"
        data = getData(q1)['results']['bindings']
        if (len(data) != 0):
            if (data[0].keys().__contains__('description')):
                pp = data[0]['description']['value'].lower()
                for sk in jobSkill:
                    if pp.__contains__(sk):
                        score += 0.25
                for we in jobWE:
                    if pp.__contains__(we):
                        score += 0.25

    return score
