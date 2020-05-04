#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:52:51 2020

@author: mulugetasemework
"""


#%%

''' 
Two methods, one to plot wordcloud and anther one pie charts

Method: "do_wordcloud":

-is a method to plot frequenies into a word cloud.
For demo purposes, fake data for ethnicity is generated



If you don't have the wordcloud package: do:
    # conda install -c conda-forge wordcloud
 
** however be aware of an error that can happed do to installation and dependencies
'''

'''
i.e. beware of the following error after you install wordcloud, you might get this, you might get this error

ValueError: 'transform' must be an instance of 'matplotlib.transform.Transform'

If so, just reinstall your matplotlib, the specific version you had before dependecies changed. 
In may case I had to do this:
conda install -c anaconda matplotlib==3.0.3

'''

'''
one good idea write-up/source: https://www.datacamp.com/community/tutorials/wordcloud-python
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import defaultdict

def do_wordcloud(frequency_data):
   
    ##### Create and generate a word cloud image, in two different ways, choose one  
    
    # approach 1
    # generate wordcloud directly from these frequencies
    # WordCloud().generate_from_frequencies() requires a dict
    
    # white background version
    wc = WordCloud(background_color="white",
                              width=1200, height=1000,
                              stopwords=STOPWORDS
                             ).generate_from_frequencies(fq)
    
    # approach 2, 
    #dict to list, to use WordCloud.generate()
    #    data = dict(zip(fq['Key'].tolist(), fq['Value'].tolist()))
    #    
    #    wc = WordCloud(background_color="white",
    #                              width=1200, height=1000,
    #                              stopwords=STOPWORDS
    #                             ).generate(str(df["ethnicity"]))
    
    #default, black background version 
    #wordcloud = WordCloud().generate(str(df.ethnicity))
    
    # Display the generated image:
    plt.figure(figsize=(5, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def plot_pie_chart(labels, sizes):
    
    # Data to plot
#    labels = 'White', 'African_American', 'Hispanice', 'Declined'
#    sizes = [215, 130, 245, 210]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice
    
    # Plot
    plt.figure(figsize=(5, 5))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')
    plt.show()    

## create fake data 
labels = 'White', 'African_American', 'Hispanic', 'Declined'
df = pd.DataFrame()
# creare a 100 row random data set for ethnicity
df["ethnicity"] = np.random.choice(labels, size=100)

#generate frequency
fq = defaultdict(int)
for w in df["ethnicity"]:
    fq[w] += 1


# call the methods to plot this data
    
#WordCloud
do_wordcloud(fq)
# pie chart
plot_pie_chart(fq.keys(), fq.values())

