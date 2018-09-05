# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 13:33:26 2018

@author: kercy_000
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_excel('Glucostats exclusion.xlsx')

sns.set_style("darkgrid")


def lolliplot(df):

    my_range = range(1, len(df.index)+1)
    df = df.sort_values(by='All p')

    plt.scatter(df['Inu p'], my_range, color='lightgreen', alpha=1,
                label='Inuline p-value')
    plt.scatter(df['Malto p'], my_range, color='skyblue', alpha=1,
                label='Maltodextrine  p-value')
    plt.scatter(df['All p'], my_range, color='tomato', alpha=1,
                label='Comparaison  p-value')
    plt.hlines(y=my_range, xmin=0.05, xmax=df['All p'], color='tomato',
               alpha=0.3)
    plt.yticks(my_range, df['parameter'])
    plt.title('P-values comparisons',
              loc="left", fontsize=15)
    plt.xlabel('p-values', fontsize=14)
    plt.ylabel('Parameter', fontsize=14)
    plt.vlines(x=0.05, ymin=0, ymax=20, color='red')
    plt.legend(loc='lower right', frameon=True, facecolor='white')
    plt.tight_layout()
    plt.show()


def kittyplot(df):
    plt.figure()
    g = sns.catplot(x='Mean', y='Arm', col='parameter', 
                    col_wrap=2, height=2,
                    palette=sns.crayon_palette(('Sea Green', 'Navy Blue')),
                    data=df, kind='bar', sharex=False)
    plt.show()


lolliplot(df)
