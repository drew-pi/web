import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ['27 Communications',
 '126 Constituent',
 '132 Administration',
 '122 Finance,',
 '105 Engineering,',
 '100 Building',
 '141 Technology,',
 '19 Information',
 '62 Public',
 '3 Community',
 '97 Legal',
 '18 Policy,',
 '28 Social',
 '14 Health',
 '9 Clerical',
 '9 Maintenance',
 '3 Policy']

data = [float(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]


def func(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))#absolute is the percentage of pct (individual values in data) out of allvals (sum of data)
    #print ('absolute',absolute)
    #print ('pct',pct)
    #print ('allvals',allvals)
    if pct > 9:
        return "{:.1f}%\n({:d} jobs)".format(pct, absolute)#creates a string with the format percentage (absolute) and then data that corrosponds to the percentage


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),  #texts has something to do with the creating the writing in the pie chart
                                  textprops=dict(color="w")) #wedges has something to do with the legend
#autotexts has something to do with formating the words inside the pie chart


ax.legend(wedges, ingredients,
          title="Job Type",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=6, weight="bold")

ax.set_title("Types of Jobs offered")#ax only useful in this phase of the program, I think ax sets up the plot

plt.show()