# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:35:06 2018

@author: Daph
"""
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
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
    