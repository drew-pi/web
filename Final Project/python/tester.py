from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import requests
import json

response = requests.get('https://data.cityofnewyork.us/resource/kpav-sd4t.json')
print (response.status_code)
text = response.text
data = json.loads(text)
#print (data[:5])
safe = data



#choice = input('hello')
#possible statistics - part time vs full time
#student jobs/ manager jobs/ experience (non-manager)
#pay
#pay vs experience


def create_all_keys(jason):
    all_keys = []
    for dic in jason:
        for key in dic:
            if key not in all_keys:
                all_keys.append(key)
    return all_keys

all_keys = create_all_keys(data)
#pprint (all_keys)

all_keys_long_notAutomated_ = ['job_id', 'agency', 'posting_type', 'number_of_positions', 'business_title', 'civil_service_title',
             'title_classification', 'title_code_no', 'level', 'job_category', 'full_time_part_time_indicator',
             'career_level', 'salary_range_from', 'salary_range_to', 'salary_frequency', 'work_location', 'division_work_unit',
             'job_description', 'minimum_qual_requirements', 'preferred_skills', 'to_apply', 'residency_requirement',
             'posting_date', 'posting_updated', 'process_date', 'additional_information', 'work_location_1', 'post_until', 'hours_shift']

delete_key_long_notAutomated_ = ['posting_type','title_classification','title_code_no','level','job_description','minimum_qual_requirements',
               'preferred_skills','additional_information','to_apply','residency_requirement',]

def make_delete_keys(List,save_keys):
    newList = []
    for item in List:
        if item not in save_keys:
            newList.append(item)
    return newList

keep_keys = ['salary_range_from','salary_range_to','salary_frequency','job_category','full_time_part_time_indicator'] #Keys that I want the edited list to contain
delete_keys = make_delete_keys(all_keys,keep_keys)
#pprint (delete_keys)

def edit_list(List,delete_keys):
    for dic in List:
        for item in delete_keys:
            if item in dic:
                del dic[item]
    return List

edited_data = edit_list(data,delete_keys)



def shorten(string):
    if len(string.split()) > 1:
        string = ' '.join(string.split()[:1])
    else:
        string = string
    return string

    


def find_pay(List):
    newDict = {}
    for dic in List:
        pay = 0
        last = []
        last.append(float(dic['salary_range_from']))
        last.append(float(dic['salary_range_to']))
        if 'full_time_part_time_indicator' in dic and 'job_category' in dic:
            if dic['full_time_part_time_indicator'] == 'F':
                if dic['salary_frequency'] == 'Daily':
                    pay = sum(last)/len(last) * 251
                elif dic['salary_frequency'] == 'Hourly':
                    pay = sum(last)/len(last) * 6 *  251
                else:
                    pay = sum(last)/len(last)
            elif dic['full_time_part_time_indicator'] == 'P':
                if dic['salary_frequency'] == 'Daily':
                    pay = sum(last)/len(last) * 251
                elif dic['salary_frequency'] == 'Hourly':
                    pay = sum(last)/len(last) * 3 *  251
                else:
                    pay = sum(last)/len(last)
            newCat = shorten(dic['job_category'])
            #print (dic['job_category'])
            #print (newCat)
            if newCat not in newDict:
                newDict[newCat] = [pay]
            elif newCat in newDict and pay not in newDict[newCat]:
                newDict[newCat].append(pay)                                   
    return newDict

pays = find_pay(edited_data)
#pprint (pays)


# some random data

y1 = [76236, 94835,
                 74655,
                 102507,
                 85371,
                 174081,
                 50358,
                 53834,
                 72224,
                 66385,
                 111019,
                 26595,
                 101500,
                 90000,
                 53540,
                 65091,
                 93685,
                 102817,
                 99637,
                 42781,
                 75797,
                 60000,
                 93041,
                 82500,
                 108042,
                 110000,
                 117926,
                 88097,
                 124089,
                 103593,
                 94397,
                 81167,
                 132095,
                 120000,
                 105000,
                 96640,
                 89362,
                 66315,
                 102500,
                 116093,
                 83258,
                 77500,
                 69506,
                 89100,
                 130000,
                 98118,
                 77145,
                 47530,
                 78803,
                 132500]

y = np.array(y1)
#pprint (x)

x=['Tech']*len(y)
#pprint (y)
matplotlib.rcParams['font.size'] = 7.0




def scatter_hist(x, y, ax, ax_histy,total):
    # no labels
    #ax_histy.tick_params(axis="y", labelleft=False,labeltop=False,labelright=False)


    # the scatter plot:
    ax.scatter(x,y,5)

    # now determine nice limits by hand:
    #binwidth = 0.25
    #xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    #lim = (int(xymax/binwidth) + 1) * binwidth

    #bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histy.hist(total,60,orientation='horizontal',color='darkblue')


# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005


rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a square Figure
fig = plt.figure(figsize=(8, 8))

ax = fig.add_axes(rect_scatter)

ax_histy = fig.add_axes(rect_histy, sharey=ax)
#print (ax_histy)

#fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

total = []
for key in pays:
    for item in pays[key]:
        total.append(item)
    

# use the previously defined function
for key in pays:
        y = pays[key]
        x = [key]*len(y)
        scatter_hist(x, y, ax, ax_histy,total)



ax.set_title('Average pay for different types of Jobs')
ax.set_xlabel('Types of Jobs')
ax.set_ylabel('Estimated Annual Pay')



plt.show()