import requests, random, matplotlib, arrow, pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import urllib.request
import plotly
import plotly.io as pio
from IPython.display import SVG, display

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import userinfo, language_table, repos_table, job_table,recom_table


def analyse(request):
    return render(request, 'home.html')

#Fetching Repository data using API
def repo_fetch(user_data):
    #API Key
    token = 'ef57f5e210f422e08df558ad003b04f76c0c0c3a'
    headers = {'Authorization': 'token ' + token}

    page_no = 1
    url = user_data['repos_url'] + '?page=' + str(page_no) + '&per_page=100'
    repos_data = []
    while (True):
        requestObj = requests.get(url=url,headers=headers)
        response = requestObj.json()
        repos_data = repos_data + response
        repos_fetched = len(response)
        if (repos_fetched == 100):
            page_no = page_no + 1
            url = user_data['repos_url'] + '?page=' + \
                str(page_no) + '&per_page=100'
        else:
            break
        
    # repos_dataframe = {'Owner Name':repos_owner, 'Repos Name':repos_name, 'Desc':repos_desc,'Created Date':repos_created_date,'Updated Date':repos_updated_date, 'Forks':repos_forks, 'Stars':repos_star, 'Language':languages, 'Open issues':repos_open_issues, 'Commits URL':repos_commits_url}
    repos_dataframe = {'repos_owner':[], 'repos_owner_id':[], 'repos_name':[], 'repos_id':[], 'repos_desc':[],
                        'repos_created_date':[], 'repos_updated_date':[], 'repos_forks':[], 'repos_star':[],'repos_lang':[],
                        'repos_open_issues':[], 'repos_commits_url':[]}
    repos_lang = []   
    for i in range(len(repos_data)):
        repos_dataframe['repos_owner'].append(repos_data[i]['owner']['login'])
        repos_dataframe['repos_owner_id'].append(repos_data[i]['owner']['id'])
        repos_dataframe['repos_name'].append(repos_data[i]['name'])
        repos_dataframe['repos_id'].append(repos_data[i]['id'])
        repos_dataframe['repos_desc'].append(repos_data[i]['description'])
        repos_dataframe['repos_star'].append(repos_data[i]['stargazers_count'])
        url = requests.get(repos_data[i]['languages_url'], headers=headers)
        data1 = url.json()
        repos_lang.append(data1)
        repos_dataframe['repos_created_date'].append(repos_data[i]['created_at'][:-10])
        repos_dataframe['repos_updated_date'].append(repos_data[i]['updated_at'][:-10])
        repos_dataframe['repos_forks'].append(repos_data[i]['forks'])
        repos_dataframe['repos_open_issues'].append(repos_data[i]['open_issues'])
        repos_dataframe['repos_commits_url'].append(repos_data[i]['commits_url'])
        
    for i in repos_lang:
        repos_dataframe['repos_lang'].append(list(i.keys()))

    return(repos_dataframe)

def convert(languages):
    list_of_languages = []
    for i in languages:
        if i == []:
            continue
        else:
            for j in i:
                list_of_languages.append(j)
    languages_count = pd.Series(list_of_languages).value_counts()
    return(languages_count)

def experience(count,repos_dataframe):
    lang_exp = []; exp = []; recent_date = []; forks = []; stars = []
    exp_dataframe = {'lang_code':[], 'owner':[], 'owner_id':[], 'language':[], 'experience':[], 'forks':[], 'stars':[],
                     'recent_date':[]}

    for i in range(len(count.index)):
        lang_exp.append(count.index[i])
        temp_date = []
        temp_forks = 0
        temp_stars = 0
        for j in range(len(repos_dataframe['repos_lang'])):
            if count.index[i] in repos_dataframe['repos_lang'][j]:
                temp_date.append(repos_dataframe['repos_created_date'][j])
                temp_date.append(repos_dataframe['repos_updated_date'][j])
                temp_forks = temp_forks + repos_dataframe['repos_forks'][j]
                temp_stars = temp_stars + repos_dataframe['repos_star'][j]
        recent_date.append(max(temp_date))
        forks.append(temp_forks)
        stars.append(temp_stars)
        diff = arrow.get(max(temp_date)) - arrow.get(min(temp_date))
        days = (diff.days + 1)/365
        exp.append(days)

    for i in range(len(count.index)):
        lang_code = repos_dataframe['repos_owner'][1].lower() + '_' + lang_exp[i].replace(" ", "")
        exp_dataframe['lang_code'].append(lang_code)
        exp_dataframe['owner'].append(repos_dataframe['repos_owner'][1].lower())
        exp_dataframe['owner_id'].append(repos_dataframe['repos_owner_id'][1])
        exp_dataframe['language'].append(lang_exp[i])
        exp_dataframe['experience'].append(round(exp[i],4))
        exp_dataframe['forks'].append(forks[i])
        exp_dataframe['stars'].append(stars[i])
        exp_dataframe['recent_date'].append(recent_date[i])
    return(exp_dataframe)
def save_fig(x_axis,y_axis, path,name):
    plt.figure(figsize=(20, 12))
    sns.barplot(x_axis,y_axis)
    plt.xlabel("Language experience in terms of years", fontsize=20)
    plt.xticks(rotation=90)
    plt.ylabel("Number of {}".format(name), fontsize=20)
    plt.title("Language distribution", fontsize=20)
    plt.savefig(path)

#main function for user analysis
def result(request):
    if request.method == 'POST':
        #API Key
        token = 'ef57f5e210f422e08df558ad003b04f76c0c0c3a'
        headers = {'Authorization': 'token ' + token}
        #Taking user input and fetching data from API
        github_username = request.POST['github_username']            
        url = ('https://api.github.com/users/{}'.format(github_username))
        requestObj = requests.get(url=url,headers=headers)
        user_data = requestObj.json()   #JSON data
        # Check for the Valid user
        if len(user_data) == 2:
            messages.warning(request, 'GitHub username is Invalid')
            return redirect('analyse')
        else:
            #Check of user in database
            if userinfo.objects.filter(name=github_username.lower()).exists():
                db_check = userinfo.objects.filter(name=github_username.lower())
                abc = (db_check[0].name)
                exp_order = language_table.objects.filter(owner=github_username.lower())
                exp_display = exp_order.order_by('experience').reverse()
                if db_check[0].repos == user_data['public_repos']:
                    return render(request, 'git.html', {'git_username': user_data['login'], 'git_id': user_data['id'], 'company': user_data['company'], 
                                'location': user_data['location'], 'repos': user_data['public_repos'], 'bio': user_data['bio'],
                                'url':user_data['html_url'], 'prof_pic':db_check[0].prof_pic,'analysis_pic': db_check[0].analysis_pic,'exp_pic': db_check[0].exp_analysis_pic,
                                'exp_data':exp_display})
            else:
                repos_dataframe = repo_fetch(user_data)     #Repository API call
                languages_count = convert(repos_dataframe['repos_lang'])     #Analysis on language
                exp_dataframe = experience(languages_count, repos_dataframe) #Analysis on experience of user

                
                analysis_pic_url = 'media/analysis_pics/'+ github_username.lower() + '.png'
                save_fig(languages_count.index,languages_count.values,analysis_pic_url,name='Repositories')

                prof_pic_url = 'media/prof_pics/'+ github_username.lower() + '.png'
                urllib.request.urlretrieve(user_data['avatar_url'], prof_pic_url)
                
                fig_df = {'lang':exp_dataframe['language'], 'exp':exp_dataframe['experience']}
                exp_analysis_pic_url = 'media/analysis_pics/exp_analysis/'+ github_username.lower() +'_exp'+ '.png'
                save_fig(fig_df['lang'],fig_df['exp'],exp_analysis_pic_url,name='Years')

                info = userinfo(name=user_data['login'].lower(), user_id=user_data['id'], company=user_data['company'], desc=user_data['bio'],
                                    email=user_data['email'], blog=user_data['blog'], followers=user_data['followers'], repos=user_data['public_repos'], 
                                    url=user_data['html_url'],prof_pic=prof_pic_url,analysis_pic=analysis_pic_url,exp_analysis_pic=exp_analysis_pic_url)
                info.save()

                for i in range(len(repos_dataframe['repos_id'])):
                    repos_tab = repos_table(owner=repos_dataframe['repos_owner'][i].lower(), repos_owner_id=repos_dataframe['repos_owner_id'][i], 
                                                repos_name=repos_dataframe['repos_name'][i], repos_id=repos_dataframe['repos_id'][i],
                                                desc=repos_dataframe['repos_desc'][i], create_date=repos_dataframe['repos_created_date'][i], 
                                                update_date=repos_dataframe['repos_updated_date'][i], languages=repos_dataframe['repos_lang'][i], 
                                                forks=repos_dataframe['repos_forks'][i], stars=repos_dataframe['repos_star'][i], 
                                                open_issues=repos_dataframe['repos_open_issues'][i])
                    repos_tab.save()
                for i in range(len(languages_count.index)):
                    experience_table = language_table(lang_code=exp_dataframe['lang_code'][i], owner=exp_dataframe['owner'][i],
                                    owner_id=exp_dataframe['owner_id'][i],language=exp_dataframe['language'][i], 
                                    experience=exp_dataframe['experience'][i], forks=exp_dataframe['forks'][i], 
                                    stars=exp_dataframe['stars'][i], recent_date=exp_dataframe['recent_date'][i], num_repos=languages_count.values[i])
                    experience_table.save()

                exp_order = language_table.objects.filter(owner=github_username.lower())
                exp_display = exp_order.order_by('experience').reverse()
                return render(request, 'git.html', {'git_username': user_data['login'], 'git_id': user_data['id'], 'company': user_data['company'], 
                                'location': user_data['location'], 'repos': user_data['public_repos'], 'bio': user_data['bio'],
                                'url':user_data['html_url'], 'prof_pic':prof_pic_url,'analysis_pic': analysis_pic_url, 'exp_pic':exp_analysis_pic_url,
                                'exp_data':exp_display})


def job_recom(request):
    jobs = pd.read_csv('job_datasheet_updated_1000.csv')

    job_id = jobs['Job_id']; job_title = jobs['Job_Title']; company = jobs['Company']; tags = jobs['Skill']
    job_exp = jobs['Experience']; num_skills = jobs['No_of_Skills']; lang_score = jobs['Lang_score']; stars = jobs['stars']
    age = jobs['Age']; link = jobs['Link']
    if len(job_id) == job_table.objects.all().count():
        return render(request, 'job_recom.html')
    else:
        for i in range(len(jobs)):
            job_table_upload = job_table(job_id=job_id[i], job_title=job_title[i], job_company=company[i], job_skills=tags[i],
                                        job_exp=job_exp[i], company_rating=stars[i], job_age=age[i], lang_score=lang_score[i],
                                        link=link[i], num_skills=num_skills[i])
            job_table_upload.save()
        return render(request, 'job_recom.html')

def recommend(request):
    job_recom(request)
    if request.method == 'POST':
        github_username = request.POST['github_username']
        if language_table.objects.filter(owner=github_username.lower()).exists():
            # if recom_table.objects.filter(name=github_username.lower()).exists():
            #     report = recom_table.objects.filter(name=github_username.lower())
            #     jobs = job_table.objects.all().count()
            #     if jobs == len(report):
            #         report = report.order_by('match_score','score','job_age','company_rating').reverse()
            #         report = report.exclude(match_score=0)
            #         repot = report.exclude(score=0)
            #         return render(request, 'job_recom.html',{'result':report})
            # else:
            user_analysis = language_table.objects.filter(owner=github_username.lower())
            user_skills = []; user_exp = []
            for i in user_analysis:
                user_skills.append(i.language)
                user_exp.append(i.experience)
                
            jobs = job_table.objects.all()
            job_skills = []; lang_score = []; num_skills=[]; job_exp=[]; job_id=[];job_title=[]; company=[]; job_link=[]
            job_age=[]; company_rating=[]
            for i in jobs:
                job_skills.append(i.job_skills); num_skills.append(i.num_skills); lang_score.append(i.lang_score)
                job_exp.append(i.job_exp); job_id.append(i.job_id); job_title.append(i.job_title)
                company.append(i.job_company); job_link.append(i.link); job_age.append(i.job_age); company_rating.append(i.company_rating)

            job_match = []; match_score = []
            for i in range(len(job_skills)):
                match = 0
                for j in range(len(job_skills[i])):
                    if job_skills[i][j] in user_skills:
                        match = match + 1
                match_score.append(round((match/num_skills[i]),2))
                job_match.append(match)
            # print(job_match)

            user_score = []
            for i in range(len(match_score)):
                temp_score = 0
                for j in range(len(job_skills[i])):
                    if job_skills[i][j] in user_skills:
                        if user_exp[user_skills.index(job_skills[i][j])] < job_exp[i][j]:
                            score = (lang_score[i][j] * (user_exp[(user_skills.index(job_skills[i][j]))]/job_exp[i][j]))
                        else:
                            score = lang_score[i][j]
                        temp_score = temp_score + score
                # print(i,temp_score)
                user_score.append(round(temp_score,4))

                # arr = np.array(match_score)
                # top = arr.argsort()[::-1]
                # # print(top)
                
                # user_score = []
                # for i in (top):
                #     temp_score = 0
                #     for j in range(len(job_skills[i])):
                #         if job_skills[i][j] in user_skills:
                #             if user_exp[user_skills.index(job_skills[i][j])] < job_exp[i][j]:
                #                 score = (lang_score[i][j] * (user_exp[(user_skills.index(job_skills[i][j]))]/job_exp[i][j]))
                #             else:
                #                 score = lang_score[i][j]
                #             temp_score = temp_score + score
                #     print(i,temp_score)
                #     user_score.append(round(temp_score,4))

            rank = sorted((user_score), key= float,reverse=True)
            rank_arr = np.array(user_score)
            # print(arr)
            t = rank_arr.argsort()
            # print(t)
                
            rec_id =[]; rec_title=[]; rec_skills=[];rec_comp=[];rec_exp=[];rec_link=[];rec_score=[];rec_match=[];rec_match_score=[]
            rec_job_age =[]; rec_company_rating=[]
            for r in t:
                rec_id.append(job_id[r]); rec_title.append(job_title[r]); rec_skills.append(job_skills[r]); rec_comp.append(company[r])
                rec_exp.append(job_exp[r]); rec_link.append(job_link[r]); rec_score.append(round(user_score[r]*100,2))
                rec_match.append(job_match[r]); rec_match_score.append(match_score[r]); rec_job_age.append(job_age[r])
                rec_company_rating.append(company_rating[r])

            for i in range(len(job_id)):
                recom_code = github_username.lower() +'_'+ str(rec_id[i])
                recom_table_up = recom_table(recom_code=recom_code, name=github_username.lower(), job_id=rec_id[i], job_title=rec_title[i],
                                            job_company=rec_comp[i], job_skills=rec_skills[i], job_exp=rec_exp[i], score=rec_score[i],
                                            match=rec_match[i], link=rec_link[i], match_score=rec_match_score[i],
                                            job_age=rec_job_age[i], company_rating=rec_company_rating[i])
                recom_table_up.save()

            report = recom_table.objects.filter(name=github_username.lower())
            report = report.order_by('match_score','score','job_age','company_rating').reverse()
            report = report.exclude(match_score=0)
            repot = report.exclude(score=0)
            
            return render(request, 'job_recom.html',{'result':report})
    else:
        messages.warning(request, 'GitHub username does not exists in our database, Analyse first and try our recommendations ')
        return redirect('analyse')

def job_detail(request, id):
    job = job_table.objects.get(job_id=id)
    candidate_score = recom_table.objects.filter(job_id=id)
    candi = candidate_score.order_by('match_score','score').reverse()
    names=[]; rank_num=[];recom_code=[]
    for i in range(len(candi)):
        names.append(candi[i].name)
        rank_num.append(i+1)
        recom_code.append(candi[i].name+'_'+str(id))
    print(recom_code)
    for i in range(len(rank_num)):
        recom_table.objects.filter(recom_code=recom_code[i]).update(rank=rank_num[i])
    
    candidate_info = (userinfo.objects.filter(name__in=names))
    candidate_score = recom_table.objects.filter(job_id=id)
    candi = candidate_score.order_by('rank')
    context = {
        'job':job,
        'candidate':candi,
        'user_info': candidate_info,
    }
    return render(request, 'jobdetail.html',context)
