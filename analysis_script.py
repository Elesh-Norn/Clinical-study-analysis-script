import pandas as pd, seaborn as sns, matplotlib.pyplot as plt, \
    scipy, numpy as np, os
from Anova import two_way_anova, one_way_anova
from pandas.plotting import parallel_coordinates
from config import LEGENDS, GLUCOSE_LIST, GLUCOSE_LIST_AUC, NORMAL_LIST, HEATMAP_LIST

# INIT PART
final_db = pd.read_excel('Final formated DB.xlsx')
p_value_df = pd.DataFrame(columns=['parameter', 'All p', 'Inu p', 'Malto p'])
sns.set_style("whitegrid")
# GLOBAL
PATH = ''

# Functions


def substract_parameter(df, parameter):
    """Add a column that is the substraction of the two time points of the
    study for a given parameter"""
    newcolumn = "Difference of "+parameter
    df = df.set_index('Patient ID')
    series_m0 = df.loc[df['Time point'] == 'M0', parameter]
    series_m3 = df.loc[df['Time point'] == 'M3', parameter]
    df2 = df.loc[df['Time point'] == 'M0']
    difference_list = series_m3.sub(series_m0)
    df2[newcolumn] = difference_list
    return difference_list, df2, newcolumn


def curveplots(df, parameter):
    """Will plot the curves for OGTT. parameter should be Insuline, C peptide
    or Glucose in string"""
    sns.set_style("whitegrid")
    if parameter == "Insuline":
        curve = "Insulin in mU/L"
        y = ['OGTT Insulin -10', 'OGTT Insulin -5', 'OGTT Insulin 0',
             'OGTT Insulin 30',	'OGTT Insulin 60',	'OGTT Insulin 90',
             'OGTT Insulin 120']
        x = [-10, -5, 0, 30, 60, 90, 120]

    elif parameter == "C peptide":
        curve = 'C peptide in mU/L'
        y = ['OGTT C-pep -10', 'OGTT C-pep -5', 'OGTT  C-pep 0',
             'OGTT C-pep 30', 'OGTT C-pep 60', 'OGTT C-pep 90',
             'OGTT C-pep 120']
        x = [-10, -5, 0, 30, 60, 90, 120]
    elif parameter == "Glucose":
        curve = "Glucose in mg/dl"
        y = ['OGTT Glucose 0', 'OGTT Glucose 30', 'OGTT Glucose 60',
             'OGTT Glucose 90', 'OGTT Glucose 120']
        x = [0, 30, 60, 90, 120]

    df2 = pd.DataFrame()
    for counter, elements in enumerate(y, 0):
        dummyframe = pd.DataFrame()
        dummyframe = dummyframe.assign(**{'Patient ID': df['Patient ID'],
                                          'Arm': df['Arm'],
                                          'Time point': df['Time point'],
                                          'Time': x[counter],
                                          curve: df[elements]})

        if counter == 0:
            df2 = dummyframe
        else:
            df2 = pd.concat([df2, dummyframe])

    plt.figure()
    g = sns.FacetGrid(df2, col='Arm', hue="Time point")
    g.map(sns.lineplot, 'Time', curve, ci="sd")
    g.add_legend()
    plt.show()


def swarmbox_m0_m3(df, parameter, hue_param=None):
    """Plot two boxplots and give some simple stats. hue_param=None can be
    changed for coloring the dots separatly"""

    df_difference, df2, newcolumn = substract_parameter(df, parameter)
    a = check_stats(df, parameter, df_difference, df2)

    # Graph boxplot
    plt.figure()
    sns.swarmplot(x='Arm', y=newcolumn, data=df2,
                  palette=sns.crayon_palette(('Vivid Violet',
                                              'Burnt Sienna', 'Shamrock')))
    ax = sns.boxplot(x='Arm', y=newcolumn, hue=hue_param, data=df2,
                     palette=sns.crayon_palette(('Sea Green', 'Navy Blue',
                                                 'Vivid Violet')))

    ax.set_ylabel(LEGENDS[parameter], fontsize=15)
    ax.set_xlabel('p= '+str(round(a[1], 3)), fontsize=15)

    plt.tight_layout()
    plt.savefig(PATH+"/"+f_s(parameter)+' boxplot', dpi=400)


def simple_corell(df, parameter1, parameter2):
    """Plot parameter1 in function of parameter2 and try to draw a regression
    line. I tweek a bit the argument for my use"""
    df2 = df
    sns.lmplot(parameter1, parameter2, data=df2,
               hue='Time point', col='Arm', ci=None)


def parallel(df, parameter):
    """Needs a dataframe and the parameter to call a graph with parallel
    plotting of Inuline and Maltodextrine between M0 and M3 separatly"""

    # Initialisation part
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    f, axes = plt.subplots(1, 2, sharey='all')
    global p_value_df

    # Create a df with only pairs
    for elements in list(['Patient ID', 'Arm']):
        df2[elements] = df[elements]
        df3[elements] = df[elements]
    df2[parameter+' M0'] = df.loc[df['Time point'] == 'M0', parameter]
    df2 = df2.set_index('Patient ID')
    df2 = df2.dropna()
    df3[parameter+' M3'] = df.loc[df['Time point'] == 'M3', parameter]
    df3 = df3.set_index('Patient ID')
    df3 = df3.drop(columns=['Arm'])
    df3 = df3.dropna()
    df2 = pd.concat([df2, df3], axis=1, join_axes=[df2.index])
    df2 = df2.dropna()

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
    parallel_coordinates(df2, 'Arm',
                         cols=[parameter+' M0', parameter+' M3'],
                         color='mediumseagreen', ax=axes[0])
    parallel_coordinates(df3, 'Arm',
                         cols=[parameter+' M0', parameter+' M3'],
                         color='slateblue', ax=axes[1])
    axes[0].set(title='Inuline', xticks=[])
    axes[0].set_ylabel(LEGENDS[parameter], fontsize=15)
    axes[0].set_xlabel('p= '+str(round(inutest[1], 3)), fontsize=15)
    axes[0].tick_params(labelbottom='off')
    axes[0].legend_.remove()
    axes[1].set(title='Maltodextrine', xticks=[])
    axes[1].set_xlabel('p= '+str(round(maltotest[1], 3)), fontsize=15)
    axes[1].legend_.remove()

    plt.savefig(PATH+"/"+f_s(parameter)+' parallel plot', dpi=400)


def compare_two_groups(group1, group2, paired=False):
    """Do stats for paired or unpaired comparison between groups and return
    them"""
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


def check_stats(df, parameter, df_difference, df2):
    """Do the stats of M0/M3 and the difference of a parameter between inulin,
    and maltodextrine"""

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
    plt.savefig(PATH+"/"+f_s(parameter)+' histogramme', dpi=400)

    return difference_test


def heatmap(df, glucose=False):

    df = df.drop(HEATMAP_LIST, axis=1)
    if glucose is False:
        df = df.drop(GLUCOSE_LIST_AUC, axis=1)
    else:
        df = df.drop(NORMAL_LIST, axis=1)
        df = df.drop(['Masse Maigre', 'Masse Grasse', 'Height', 'Xc/height',
                      'Bioimpedance Xc'], axis=1)
    df.Gender.replace(['male', 'female'], [1, 0], inplace=True)
    df = df.drop(df.columns[df.columns.str.contains('unnamed', case=False)],
                 axis=1)

    # Generate a mask for the upper triangle
    df_corr = df.corr()
    mask = np.zeros_like(df_corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    df_corr = df.corr()

    # Colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.clustermap(df_corr, vmin=-1, vmax=1,
                   linewidths=.1, cmap=cmap,
                   xticklabels=df_corr.columns, yticklabels=df_corr.columns)
    plt.show()


def f_s(parameter):
    """format string to make valid filename"""
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


def write_stats(list_of_analysis):
    """Do all analysis and graph for a given list between;
    GLUCOSE_LIST
    GLUCOSE_LIST_AUC
    NORMAL_LIST"""
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
    writer = pd.ExcelWriter('Glucostats exclusion.xlsx')
    p_value_df.to_excel(writer, 'Sheet1')
    writer.save()

# Example of selection of the subset of patient i want


final_db = final_db.loc[final_db['Exclusion'] == 'No']
final_db = final_db.loc[final_db['Change of Insuline medication'] == 'NO']

organise_results(final_db, 'Weight')
