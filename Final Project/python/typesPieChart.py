from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import requests
import json

response = requests.get('https://data.cityofnewyork.us/resource/kpav-sd4t.json')
print (response.status_code)
text = response.text
data = json.loads(text)



delete_keys = ['posting_type','title_classification','title_code_no','level','job_description','minimum_qual_requirements','preferred_skills','additional_information','to_apply','residency_requirement',]


def edit_list(List,delete_keys):
    for dic in List:
        for item in delete_keys:
            if item in dic:
                del dic[item]
    return List

edited_data = edit_list(data,delete_keys)



def dictStat (List,stat,shorten):
    newDict = {}
    for dic in List:
        if shorten == True:
            if stat in dic:
                if len(dic[stat].split()) > 1:
                    key = ' '.join(dic[stat].split()[:1])
                if len(dic[stat].split()) <= 1:
                    key = dic[stat]
                if key not in newDict:
                    newDict[key] = 1
                if key in newDict:
                    newDict[key] += 1
        else:
            if stat in dic:
                key = dic[stat]
                if key not in newDict:
                    newDict[key] = 1
                else:
                    newDict[key] += 1
    return newDict

            
career_level_stat = dictStat(edited_data,'career_level',True)
#pprint (career_level_stat)            
            
type_jobs_stat = dictStat(edited_data,'job_category',True)
#pprint (type_jobs_stat)





def listify (dic):
    newList = []
    for item in dic:
        string = str(dic[item]) + ' ' + str(item)
        newList.append(string)
    return newList


career_level_list = listify(career_level_stat)
#pprint (career_level_list)

type_jobs_list = listify(type_jobs_stat)
#pprint (type_jobs_list)


#------------Start of Graphing program-----------------------------------


fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

#recipe = career_level_list #this is the smaller one where the experience is shown
recipe = type_jobs_list #this is the larger one where experience is not shown, only job categories

data = [float(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]


def func(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))#absolute is the percentage of pct (individual values in data) out of allvals (sum of data)
    #print ('absolute',absolute)
    #print ('pct',pct)
    #print ('allvals',allvals)
    if pct > 9:
        return "{:.1f}%\n({:d} jobs)".format(pct, absolute)
        #print ("{:.1f}%\n({:d} jobs)".format(pct, absolute))#creates a string with the format percentage (absolute) and then data that corrosponds to the percentage


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),  #texts has something to do with the creating the writing in the pie chart
                                  textprops=dict(color="w")) #wedges has something to do with the legend
#autotexts has something to do with formating the words inside the pie chart
#print ('wedges',wedges)
#print ('texts',texts)
#print ('autotexts',autotexts)
#print ('autopct',lambda pct: func(pct, data))

ax.legend(wedges, ingredients,
          title="Job Type",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=6, weight="bold")

ax.set_title("Experience required for Jobs offered")#ax only useful in this phase of the program, I think ax sets up the plot

plt.show()