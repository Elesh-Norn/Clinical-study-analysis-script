# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:35:06 2018

@author: Daph
"""
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
import statsmodels.formula.api as smf
from analysis_script import final_db

from scipy import stats


def two_way_anova(data, parameter):
    data = data.rename(columns={'Time point': 'Time_point'})
    formula = parameter+' ~ C(Time_point) + C(Arm) + C(Time_point):C(Arm)'
    model = ols(formula, data).fit()
    aov_table = anova_lm(model, typ=2)
    # eta_squared(aov_table)
    # omega_squared(aov_table)
    return(aov_table)


def one_way_anova(data, parameter):
    data = data.rename(columns={'Time point': 'Time_point'})
    data_lm = ols(parameter+' ~ C(Arm, Sum)*C(Time_point, Sum)',
                  data=data).fit()
    table = sm.stats.anova_lm(data_lm, typ=2)
    # Type 2 ANOVA DataFrame
    return(table)

def get_simple_df(df, parameter1, parameter2):
    # Create a df with only pairs
    df2 = pd.DataFrame()
    for elements in list(['Patient ID', 'Arm', 'Time point', parameter1, parameter2]):
        df2[elements] = df[elements]
    df2 = df2.dropna()
    return df2


data = final_db
data = get_simple_df(data, 'Weight', 'Hospital')
data = data.rename(columns={'Time point': 'Time_point'})
data = data.rename(columns={'Patient ID': 'Patient_ID'})

vc = {'Hospital': '0 + C(Hospital)'}
md = smf.mixedlm("Weight ~ Time_point", data, groups=data['Arm'], vc_formula=vc)
mdf = md.fit()

print(mdf.summary())
