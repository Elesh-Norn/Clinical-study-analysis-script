import pandas as pd, seaborn as sns, matplotlib.pyplot as plt, \
    scipy, numpy as np, os
from config import GLUCOSE_LIST_AUC
from statsmodels.stats import multitest
from scipy import stats
import graph_functions

# INIT PART
final_db = pd.read_excel('Final formated DB.xlsx')
p_value_df = pd.DataFrame(columns=['parameter', 'All p', 'Inu p', 'Malto p'])
sns.set_style("whitegrid")

# GLOBAL
PATH = ''

# Functions

def substract_parameter(df, parameter):
    """
    Add a column that is the substraction of the two time points of the
    study for a given parameter
    """
    newcolumn = "Difference of "+parameter
    df = df.set_index('Patient ID')
    series_m0 = df.loc[df['Time point'] == 'M0', parameter]
    series_m3 = df.loc[df['Time point'] == 'M3', parameter]
    df2 = df.loc[df['Time point'] == 'M0']
    difference_list = series_m3.sub(series_m0)
    df2.loc[:, newcolumn] = difference_list

    return difference_list, df2


def get_simple_df(df, parameter):
    """
    Create a small dataframe with only pairs, Time point and Arm.
    """
    df2 = pd.DataFrame()
    for elements in list(['Patient ID', 'Arm', 'Time point', parameter]):
        df2[elements] = df[elements]
    df2 = df2.dropna()
    return df2


def swarmbox_m0_m3(df, parameter, hue_param=None, save=False):
    """
    Plot two boxplots and give some simple stats. hue_param=None can be
    changed for coloring the dots separatly
    """

    difference_list, df2 = substract_parameter(df, parameter)
    a = check_stats(df, parameter, difference_list, df2)
    fig = graph_functions.swarmbox(df2, parameter, a, hue_param)
    fig.tight_layout()
    fig.show()

    if save:
        plt.savefig(PATH + "/" + f_s(parameter) + ' boxplot', dpi=400)


def simple_corell(df, parameter1, parameter2):
    """
    Plot parameter1 in function of parameter2 and try to draw a regression
    line. I tweek a bit the argument for my use
    """
    df2 = df
    sns.lmplot(parameter1, parameter2, data=df2,
               hue='Time point', col='Arm', ci=None)


def parallel(df, parameter, save=False):
    """
    Needs a dataframe and the parameter to call a graph with parallel
    plotting of Inuline and Maltodextrine between M0 and M3 separatly
    """

    # Initialisation part
    global p_value_df

    df2 = get_paired_df(df, parameter)

    # Stat part
    inutest = compare_two_groups(df2.loc[df2['Arm'] == 'inuline',
                                         parameter+' M0'],
                                 df2.loc[df2['Arm'] == 'inuline',
                                         parameter+' M3'], paired=True)
    maltotest = compare_two_groups(df2.loc[df2['Arm'] == 'maltodextrine',
                                           parameter+' M0'],
                                   df2.loc[df2['Arm'] == 'maltodextrine',
                                           parameter+' M3'], paired=True)
    df3 = df2.loc[df2['Arm'] == 'maltodextrine']
    df2 = df2.loc[df2['Arm'] == 'inuline']

    p_value_df.loc[parameter, 'Inu p'] = inutest[1]
    p_value_df.loc[parameter, 'Malto p'] = maltotest[1]

    # Graph part
    fig = graph_functions.parallel_graph(parameter, df2, df3, inutest, maltotest)
    fig.show()
    if save:
        plt.savefig(PATH+"/"+f_s(parameter)+' parallel plot', dpi=300)


def get_paired_df(df, parameter):
    # Create a df with only pairs
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    for elements in list(['Patient ID', 'Arm']):
        df2[elements] = df[elements]
        df3[elements] = df[elements]
    df2[parameter + ' M0'] = df.loc[df['Time point'] == 'M0', parameter]
    df2 = df2.set_index('Patient ID')
    df2 = df2.dropna()
    df3[parameter + ' M3'] = df.loc[df['Time point'] == 'M3', parameter]
    df3 = df3.set_index('Patient ID')
    df3 = df3.drop(columns=['Arm'])
    df3 = df3.dropna()
    df2 = pd.concat([df2, df3], axis=1, join_axes=[df2.index])
    df2 = df2.dropna()
    return df2


def compare_two_groups(group1, group2, paired=False):
    """
    Do stats for paired or unpaired comparison between groups and return them
    """
    if len(group1) > 8 and len(group2) > 8:
        stat1, norm1 = scipy.stats.normaltest(group1)
        stat2, norm2 = scipy.stats.normaltest(group2)
        if len(group1) <= 30 and len(group2) <= 30:
            if norm1 <= 0.05 or norm2 <= 0.05:
                normality = 'not normal (respectively, p=' + \
                            str(round(norm1, 3)) + ' and p=' + \
                            str(round(norm2, 3)) + ')'
                if paired is False:
                    u, m = scipy.stats.mannwhitneyu(group1, group2)
                else:
                    u, m = scipy.stats.wilcoxon(group1, group2)
                name_test, test = 'Mann Whitney', m
                return name_test, test, normality
            else:
                if paired is False:
                    t, t_test = scipy.stats.ttest_ind(group1, group2)
                else:
                    t, t_test = scipy.stats.ttest_rel(group1, group2)
                normality = 'normal (respectively, p=' + \
                            str(round(norm1, 3)) + ' and p=' + \
                            str(round(norm2, 3)) + ')'
                name_test, test = 't-Test', t_test
                return name_test, test, normality
        else:
            if paired is False:
                t, t_test = scipy.stats.ttest_ind(group1, group2)
            else:
                t, t_test = scipy.stats.ttest_rel(group1, group2)
            normality = 'sample size <30 and so considered normal under the ' \
                        'Central limit theorem.'
            name_test, test = 't-Test', t_test
            return name_test, test, normality


def check_stats(df, parameter, df_difference, df2, save=False):
    """
    Do the stats of M0/M3 and the difference of a parameter between inulin,
    and maltodextrine
    """

    # initialise DF needed
    df_m0 = df.loc[df['Time point'] == 'M0', parameter]
    df_m3 = df.loc[df['Time point'] == 'M3', parameter]
    stat_df = pd.DataFrame()
    global p_value_df

    # Add descriptive stats of M0
    stat_df['All M0'] = df_m0.describe()
    stat_df['Inuline M0'] = df_m0.loc[df['Arm'] == 'inuline'].describe()
    stat_df['Maltodextrine M0'] = df_m0.loc[df['Arm'] == 'maltodextrine'].describe()

    # Add descriptive stats of M3
    stat_df['All M3'] = df_m3.describe()
    stat_df['Inuline M3'] = df_m3.loc[df['Arm'] == 'inuline'].describe()
    stat_df['Maltodextrine M3'] = df_m3.loc[df['Arm'] == 'maltodextrine'].describe()

    # Add descriptive stats of the difference
    stat_df['Difference'] = df_difference.describe()
    stat_df['Difference Inu'] = df2.loc[df2['Arm'] == 'inuline',
                                        'Difference of '+parameter].describe()
    stat_df['Difference Malto'] = df2.loc[df2['Arm'] == 'maltodextrine',
                                          'Difference of '+parameter].describe()
    print(stat_df.head())

    # Create an excell writter object of this dataframe
    if save:
        writer = pd.ExcelWriter(PATH+"/"+f_s(parameter)+' descriptive stat.xlsx')
        stat_df.to_excel(writer, 'Sheet1')
        writer.save()

    # Create unpaired DF for checking normality and stats testing.
    list1 = df2.loc[df2['Arm'] == 'inuline', 'Difference of '+parameter].dropna()
    list2 = df2.loc[df2['Arm'] == 'maltodextrine',
                    'Difference of '+parameter].dropna()
    
    difference_test = compare_two_groups(list1, list2, paired=False)

    p_value_df.loc[parameter, 'All mean'] = stat_df.loc['mean', 'Difference']
    p_value_df.loc[parameter, 'All std'] = stat_df.loc['std', 'Difference']
    p_value_df.loc[parameter, 'All p'] = difference_test[1]
    p_value_df.loc[parameter, 'Inu mean'] = stat_df.loc['mean', 'Difference Inu']
    p_value_df.loc[parameter, 'Inu std'] = stat_df.loc['std', 'Difference Inu']
    p_value_df.loc[parameter, 'Malto mean'] = stat_df.loc['mean', 'Difference Malto']
    p_value_df.loc[parameter, 'Malto std'] = stat_df.loc['std', 'Difference Malto']
    p_value_df.loc[parameter, 'Inu Start'] = stat_df.loc['mean', 'Inuline M0']
    p_value_df.loc[parameter, 'Inu Start std'] = stat_df.loc['std', 'Inuline M0']
    p_value_df.loc[parameter, 'Malto Start'] = stat_df.loc['mean', 'Maltodextrine M0']
    p_value_df.loc[parameter, 'Malto Start std'] = stat_df.loc['std', 'Maltodextrine M0']
    p_value_df.loc[parameter, 'All Start'] = stat_df.loc['mean', 'All M0']
    p_value_df.loc[parameter, 'All Start std'] = stat_df.loc['std', 'All M0']

    g = sns.FacetGrid(df2[['Arm', 'Difference of '+parameter]], col='Arm')
    g.map(sns.distplot, "Difference of "+parameter)
    if save:
        plt.savefig(PATH+"/"+f_s(parameter)+' histogramme', dpi=400)

    return difference_test

def f_s(parameter):
    """
    format string to make valid filename
    """
    if '/' in parameter:
        return parameter.replace("/", "-")
    else:
        return parameter


def organise_results(df, parameter, note=None):
    global PATH
    if note is not None:
        if not os.path.exists(f_s(parameter)+note):
            os.makedirs(f_s(parameter)+note)
        PATH = f_s(parameter)+note
    else:
        if not os.path.exists(f_s(parameter)):
            os.makedirs(f_s(parameter))
        PATH = f_s(parameter)
    parallel(df, parameter)
    swarmbox_m0_m3(df, parameter)


def write_stats(list_of_analysis, save=False):
    """
    Do all analysis and graph for a given list between;
    GLUCOSE_LIST
    GLUCOSE_LIST_AUC
    NORMAL_LIST
    """
    global p_value_df

    for item in list_of_analysis:
        p_value_df = p_value_df.append({'parameter': item}, ignore_index=True)
    p_value_df = p_value_df.set_index('parameter')
    for item in list_of_analysis:
        organise_results(final_db, item, note=' without medication')

    if list_of_analysis == GLUCOSE_LIST_AUC:
        # Perform separates analysis for the subset of the database that have a
        # complete Curve and not just the start
        df1 = final_db.loc[final_db['OGTT Insuline'] == 'Yes']
        df2 = final_db.loc[final_db['OGTT Glucose'] == 'Yes']
        df3 = final_db.loc[final_db['OGTT C peptide'] == 'Yes']
        organise_results(df1, 'AUC Insuline', note=' exclusion')
        organise_results(df2, 'AUC Glucose', note=' exclusion')
        organise_results(df3, 'AUC C peptide', note=' without medication')
    if save:
        writer = pd.ExcelWriter('Glucostats exclusion.xlsx')
        p_value_df.to_excel(writer, 'Sheet1')
        writer.save()

def spearman_p_value_DataFrame(df):
    """
    Return a correlation table and another table with p_value as DataFrame
    """
    p_value_df = pd.DataFrame(columns = df.columns, index= df.columns)
    corrdf = pd.DataFrame(columns = df.columns, index= df.columns)
    for a in df.columns:
        for b in df.columns:
            _thearray = np.column_stack((df[a].tolist(), df[b].tolist()))
            r, p = stats.spearmanr(_thearray)
            p_value_df.loc[[a], [b]] = p
            corrdf.loc[[a], [b]] = r
    return p_value_df, corrdf

def correct_p_values(df):
    """
    From a p-value table, return a corrected one
    with holm correction.
    """
    p_value_df = pd.DataFrame(columns = df.columns, index= df.columns)
    _, p, sidak, bf = multitest.multipletests(df.values.flatten(), method='holm')
    counter = 0
    for a in df.columns:
        for b in df.columns:
            p_value_df.loc[[a], [b]] = p[counter]
            counter +=1
    return p_value_df


final_db = final_db.loc[final_db['Exclusion'] == 'No']
final_db = final_db.loc[final_db['Change of Insuline medication'] == 'NO']
final_db = final_db.loc[final_db['OGTT C peptide'] == 'Yes']

def correl_graph(df, x, y, save=False):

    df = df[[x,y]].dropna()

    if save is True:
        writer = pd.ExcelWriter('Verif Excel.xlsx')
        df.to_excel(writer, 'Sheet1')
        writer.save()
    slope, intercept, r_value, d, e = scipy.stats.linregress(np.log(df[x]), df[y])
    sns.lmplot(x=x, y=y, logx=True, data=df)
    legend = 'y = '+str(round(slope,2))+'ln(x) + '+str(round(intercept, 2))+'\n'+'R**2 = '+str(round(r_value**2,4))
    x_box_coor = plt.gca().get_xlim()[1] - plt.gca().get_xlim()[1]/3
    y_box_coor = plt.gca().get_ylim()[1] - plt.gca().get_ylim()[1] / 6
    plt.gca().text(x_box_coor, y_box_coor, legend, style='italic',
            bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10, 'lw':10})
