# Clinical study analysis script

This is a personal script i use to analyse data coming from a clinical study with 150+ patient at different time points.

I use mainly seaborn, matplotlib, pandas, and scipy to analyse my data.

Since it's data from the real world, they are messy and most of the work is 
to select and process the good data for the right scientific question.  

I can use Jupyter Notebook to look at them, or independantly with tkinter widget 
integrated to matplotlib.

Main logic is in analysis_script. It contains the functions i need to generate
beautiful graphs, statistics in the aim to have repeatable and reliable 
analysis. 

Anova contains code to make one or two way anova.

graph_functions contains the functions used for the graphs

Config contains legend or list related to the study.
Since the data are unpublished, i'm not releasing them.  
