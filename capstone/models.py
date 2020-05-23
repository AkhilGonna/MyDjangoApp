from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class userinfo(models.Model):
    name = models.CharField(max_length= 100,primary_key=True)
    user_id = models.IntegerField()
    company = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(max_length = 254,blank=True,null=True)
    blog = models.CharField(max_length=100,blank=True,null=True)
    desc = models.TextField(blank=True,null=True)
    repos = models.IntegerField(blank=True,null=True)
    followers = models.IntegerField(blank=True,null=True)
    url = models.CharField(max_length=100,blank=True,null=True)
    prof_pic = models.ImageField(upload_to='prof_pics', blank=True, null=True)
    analysis_pic = models.ImageField(upload_to='analysis_pics', blank=True, null=True)
    exp_analysis_pic = models.ImageField(upload_to='analysis_pics', blank=True, null=True)

class repos_table(models.Model):
    repos_name = models.CharField(max_length=100)
    repos_id = models.IntegerField(primary_key=True)
    owner = models.CharField(max_length=100)
    repos_owner_id = models.IntegerField()
    desc = models.TextField(blank=True,null=True)
    create_date = models.CharField(max_length=10)
    update_date = models.CharField(max_length=10)
    forks = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    languages = ArrayField(models.CharField(max_length=100,blank=True))
    open_issues = models.IntegerField(default=0)

class language_table(models.Model):
    lang_code = models.CharField(max_length=100,primary_key=True)
    owner = models.CharField(max_length=100)
    owner_id = models.IntegerField()
    language = models.CharField(max_length=100)
    experience = models.FloatField(max_length=4)
    num_repos = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    recent_date = models.CharField(max_length=10)

class job_table(models.Model):
    job_id = models.IntegerField(primary_key=True)
    job_title = models.CharField(max_length=100)
    job_company = models.CharField(max_length=100)
    job_skills = ArrayField(models.CharField(max_length=100,blank=True))
    num_skills = models.IntegerField(blank=True)
    lang_score = ArrayField(models.FloatField(max_length=15,blank=True,null=True))
    job_exp = ArrayField(models.IntegerField(blank=True))
    company_rating = models.FloatField(max_length=2)
    job_age = models.IntegerField(default=0)
    link = models.CharField(max_length=100)

class recom_table(models.Model):
    recom_code = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    job_id = models.IntegerField()
    job_title = models.CharField(max_length=100)
    job_company = models.CharField(max_length=100)
    job_skills = ArrayField(models.CharField(max_length=100,blank=True))
    job_exp = ArrayField(models.IntegerField(blank=True))
    score = models.FloatField(max_length=4)
    match = models.IntegerField(blank=True)
    match_score = models.FloatField(max_length=4, blank=True)
    link = models.CharField(max_length=100)
    company_rating = models.FloatField(max_length=2)
    job_age = models.IntegerField(default=0)
    rank= models.IntegerField(default=0)

