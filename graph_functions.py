import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from config import LEGENDS, HEATMAP_LIST, GLUCOSE_LIST, GLUCOSE_LIST_AUC, NORMAL_LIST
from pandas.plotting import parallel_coordinates


def curveplots(df, parameter=None):
    """
    Will plot the curves for OGTT.
    Parameter should be Insuline, C peptide
    or Glucose in string
    """
    sns.set_style("whitegrid")

    # Generate x, y and legend in function of the curve asked.
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

    # Create a Dataframe to be passed to the graph function.
    df2 = pd.DataFrame()
    for counter, elements in enumerate(y, 0):
        dummyframe = pd.DataFrame()
        dummyframe = dummyframe.assign(**{'Patient ID': df['Patient ID'],
                                          'Arm': df['Arm'],
                                          'Time point': df['Time point'],
                                          'Time in minutes': x[counter],
                                          curve: df[elements]})
        if counter == 0:
            df2 = dummyframe
        else:
            df2 = pd.concat([df2, dummyframe])
    # Format and plot the figure

    plt.figure()
    g = sns.FacetGrid(df2, col='Arm', hue="Time point")
    g.map(sns.lineplot, 'Time in minutes', curve, ci="sd")
    g.add_legend()
    axes = g.axes.flatten()
    axes[0].set_title('Inuline', fontsize=20)
    axes[1].set_title('Maltodextrine', fontsize=20)
    axes[0].set_ylabel(curve, fontsize=15)
    plt.tight_layout()

    return plt.gcf()


def swarmbox(df, parameter, stat_table, hue=None):
    """
    Graph boxplot of a category, with each individual point
    :return: matplotlib figure
    """
    fig, ax = plt.subplots()
    sns.swarmplot(x='Arm', y="Difference of "+parameter, data=df, ax=ax,
                  palette=sns.crayon_palette(['Vivid Violet',
                                              'Burnt Sienna', 'Shamrock']))
    sns.boxplot(x='Arm', y="Difference of "+parameter, hue=hue, data=df, ax=ax,
                     palette=sns.crayon_palette(['Sea Green', 'Navy Blue',
                                                 'Vivid Violet']))

    ax.set_ylabel(LEGENDS[parameter], fontsize=15)
    ax.set_xlabel('p= ' + str(round(stat_table[1], 3)), fontsize=15)

    return fig


def do_heatmap(df):
    """
    Make a bottom heatmap
    """
    mask = np.zeros_like(df, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(df.values.tolist(), yticklabels=df.columns, xticklabels=df.columns, vmin=-1, vmax=1, center=0,
               cmap=cmap, linewidths=.1, mask = mask)

    return plt.gcf()

def revert_map(df):
    """
    Make a top heatmap
    """
    cmap = sns.light_palette("green", reverse=True)
    mask = np.zeros_like(df, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    mask = np.invert(mask)
    sns.heatmap(df.values.tolist(), yticklabels=df.columns, xticklabels=df.columns, vmin=0, vmax=1, center=0.00025,
               cmap=cmap, linewidths=.1, annot=True, mask=mask)

    return plt.gcf()



def heatmap(df, glucose=False):

    df = df.drop(HEATMAP_LIST, axis=1)
    if glucose is False:
        df = df.drop(GLUCOSE_LIST_AUC, axis=1)
    else:
        df = df.drop(NORMAL_LIST, axis=1)
        df = df.drop(['Masse Maigre', 'Masse Grasse', 'Height', 'Xc/height',
                      'Bioimpedance Xc'], axis=1)
    # Uncomment for gender correl
    # df.Gender.replace(['male', 'female'], [1, 0], inplace=True)
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

    return plt.gcf()


def parallel_graph(parameter, df_inu, df_malto, inutest, maltotest):

    f, axes = plt.subplots(1, 2, sharey='all')
    parallel_coordinates(df_inu, 'Arm',
                         cols=[parameter + ' M0', parameter + ' M3'],
                         color='mediumseagreen', ax=axes[0])
    parallel_coordinates(df_malto, 'Arm',
                         cols=[parameter + ' M0', parameter + ' M3'],
                         color='slateblue', ax=axes[1])
    axes[0].set(xticks=[])
    axes[0].set_title(fontsize=20, label='Inuline')
    axes[0].set_ylabel(LEGENDS[parameter], fontsize=15)
    axes[0].set_xlabel('p= ' + str(round(inutest[1], 5)), fontsize=15)
    axes[0].tick_params(labelbottom='off')
    axes[0].legend_.remove()
    axes[1].set(xticks=[])
    axes[1].set_title(fontsize=20, label='Maltodextrine')
    axes[1].set_xlabel('p= ' + str(round(maltotest[1], 3)), fontsize=15)
    axes[1].legend_.remove()

    return plt.gcf()

def lolliplot(df):
    """
    Return a visual comparison of a p-value table
    (use : df = pd.read_excel('p-value table.xlsx', , once it is generated)
    """
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

    return plt.gcf()