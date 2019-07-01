from datetime import datetime, timedelta
from django.contrib.auth.models import Permission , User
from django.db import models
from django.utils import timezone


# Create your models here.



def user_directory_path(instance, filename):
    """
    Get path for the file
    :param instance: instace of job-applicant relationship
    :param filename: resume file name
    :return: the required path to the resume
    """
    #file will be uploaded to MEDIA_ROOT/username/<filename>
    return '{0}/{1}'.format(instance.applicant.username,filename)


def seven_days_hence():
    """
    Calculates the seven days after the job postings
    :return: seventh day after job posting
    """
    return timezone.now() + timezone.timedelta(days=7)


# Details of applicant
class Applicant(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to=user_directory_path)
    photo = models.ImageField()
    applicant_Skill = models.TextField(null=True, blank=True)
    skill_ontology = models.TextField(null=True, blank=True)
    applicant_WorkExp = models.TextField(null=True, blank=True)
    work_experience_ontology = models.TextField(null=True, blank=True)
    applicant_Cert = models.TextField(null=True, blank=True)
    certification_link = models.TextField(null=True, blank=True)
    applicant_Edu = models.TextField(null=True, blank=True)



    def __str__(self):
        return self.applicant.username+"'s CV"


# Detals of jobs
class Job(models.Model):
    title = models.TextField()
    company = models.TextField()
    category = models.TextField()
    post = models.TextField()
    number_of_vacancies = models.IntegerField()
    degree = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    work_experience = models.TextField(null=True, blank=True)
    certification = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(default=seven_days_hence())

    def __str__(self):
        return self.title

# relationship between a job and the applicant
class JobApplicant(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    appliedAt = models.DateTimeField(default=timezone.now)
    applicant = models.ForeignKey('Applicant', on_delete=models.CASCADE)
    skillScore = models.DecimalField(max_digits=7, decimal_places=4, default=0.0)
    workExpScore = models.DecimalField(max_digits=7, decimal_places=4, default=0.0)
    educationScore = models.DecimalField(max_digits=7, decimal_places=4, default=0.0)
    certificationScore = models.DecimalField(max_digits=7, decimal_places=4, default=0.0)
    rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.applicant.applicant.username + "'s score in " + self.job.title