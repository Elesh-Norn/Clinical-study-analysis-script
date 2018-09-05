import numpy
import scipy
import graph_functions as gf
import pandas as pd
from numpy import nan
import matplotlib.pyplot as plt
import seaborn as sns
from config import list_of_parameters
import sklearn.metrics


class Patient_Data:
    def __init__(self, dicM0, dicM3, patient_dic):
        self.dicM0 = dicM0
        self.dicM3 = dicM3
        self.patient_dic = patient_dic
        self.dfM0 = self.dataframe(self.dicM0)
        self.dfM3 = self.dataframe(self.dicM3)

    def get_nb(self):
        return self.nb

    def get_M0(self):
        return self.dicM0

    def get_M3(self):
        return self.dicM3

    def get_dfM0(self):
        return self.dfM0

    def get_dfM3(self):
        return self.dfM3

    def dataframe(self, dic):
        '''put info in a clean panda dataframe'''
        temp_dic = {}
        for items, values in dic.items():
            if isinstance(dic[items]['weight'], float) or isinstance(dic[items]['weight'], int):
                temp_dic[items] = {'weight': dic[items]['weight']}
            else:
                temp_dic[items] = {'weight': None}
        for parameters in list_of_parameters:
            for items, values in dic.items():
                if isinstance(dic[items][parameters], float) or isinstance(dic[items][parameters], int):
                    temp_dic[items][parameters] = dic[items][parameters]
                else:
                    temp_dic[items][parameters] = None
        for items, values in dic.items():
            for item2, value2 in self.patient_dic['F4GE001'].items():
                temp_dic[items][item2] = self.patient_dic[items][item2]
        df = pd.DataFrame.from_dict(temp_dic, orient='index')
        df.fillna(value=nan, inplace=True)

        return df

    def sort_paired_values(self, study_arm, metabolic_parameter, values, items):
        '''Most important method,
        Check if value is correct (integer or float) and if they're paired in the database (M0 and M3)'''
        if values['study_arm'] == study_arm and(isinstance(self.dicM3[items][metabolic_parameter], float) or isinstance(self.dicM3[items][metabolic_parameter], int))\
           and (isinstance(self.dicM0[items][metabolic_parameter], float) or isinstance(self.dicM0[items][metabolic_parameter], int)):
            return True

    def param_count(self, study_arm, metabolic_parameter):
        '''Count how many time a parameter appears for a given paired metabolic parameter,
        useful to know how many diabetics are there for example'''
        # Ugly temporary dics
        gender_list = []
        age_list = []
        gtolerance = []
        dyslipidemia_list = []
        hypertension_list = []
        nafld_list = []
        smoking_list = []
        bmi_list = []
        count = {}
        # Create a dictionary that describe the population (count, means of age, ect... and return it)
        for items, values in self.dicM0.items():
            if self.sort_paired_values(study_arm, metabolic_parameter, values, items) is True:
                gender_list.append(self.patient_dic[items]['Gender'])
                age_list.append(self.patient_dic[items]['Age'])
                gtolerance.append(self.patient_dic[items]['glucose tolerance'])
                dyslipidemia_list.append(self.patient_dic[items]['dyslipidemia'])
                hypertension_list.append(self.patient_dic[items]['hypertension'])
                nafld_list.append(self.patient_dic[items]['nafld'])
                smoking_list.append(self.patient_dic[items]['smoking'])
                bmi_list.append(values['BMI'])
        count = {'Age mean': numpy.nanmean(age_list), 'Age std': numpy.std(age_list),
                 'Gender': {'male': gender_list.count('male'), 'female': gender_list.count('female')},
                 'glucose tolerance': {'NGT': gtolerance.count('NGT'), 'IGT': gtolerance.count('IGT'),
                                       'IFG': gtolerance.count('IFG'), 'IFG/IGT': gtolerance.count('IFG/IGT'),
                                       'Diabetic': gtolerance.count('Diabetes')},
                 'Dyslipedemia': dyslipidemia_list.count('Yes'),
                 'Hypertension': hypertension_list.count('Yes'),
                 'nafld': nafld_list.count('Yes'), 'smoking': smoking_list.count('Yes')}
        return count

    def get_curve(self, study_arm, metabolic_parameter, curve):
        '''print me paired curve, useful to do it in prism. Can refactor this to give me AUCs'''
        temp_list = []
        print('M0 values are:')
        for items, values in self.dicM0.items():
            if self.sort_paired_values(study_arm, metabolic_parameter, values, items) is True:
                if curve == 'insulin':
                    temp_list = [values['insulin_m10'], values['insulin_m5'], values['insulin_0'],
                                 values['insulin_30'], values['insulin_60'], values['insulin_90'],
                                 values['insulin_120']]
                    list_of_time_point = [-10, -5, 0, 30, 60, 90, 120]
                    get_curves_and_auc(temp_list, items, list_of_time_point)

                elif curve == 'glucose':
                    temp_list = [values['glucose_0'], values['glucose_30'], values['glucose_60'],
                          values['glucose_90'], values['glucose_120']]
                    list_of_time_point = [0, 30, 60, 90, 120]
                    get_curves_and_auc(temp_list, items, list_of_time_point)
                elif curve == 'c_peptide':
                    temp_list = [values['c_peptide_m10'], values['c_peptide_m5'], values['c_peptide_0'],
                          values['c_peptide_30'], values['c_peptide_60'], values['c_peptide_90'],
                          values['c_peptide_120']]
                    list_of_time_point = [-10, -5, 0, 30, 60, 90, 120]
                    get_curves_and_auc(temp_list, items, list_of_time_point)
        print()
        print('M3 values are:')
        for items, values in self.dicM0.items():
            if self.sort_paired_values(study_arm, metabolic_parameter, values, items) is True:
                if curve == 'insulin':
                    temp_list = [self.dicM3[items]['insulin_m10'], self.dicM3[items]['insulin_m5'],
                          self.dicM3[items]['insulin_0'], self.dicM3[items]['insulin_30'], self.dicM3[items]['insulin_60'],
                          self.dicM3[items]['insulin_90'], self.dicM3[items]['insulin_120']]
                    list_of_time_point = [-10, -5, 0, 30, 60, 90, 120]
                    get_curves_and_auc(temp_list, items, list_of_time_point)
                elif curve == 'glucose':
                    temp_list = [self.dicM3[items]['glucose_0'], self.dicM3[items]['glucose_30'], self.dicM3[items]['glucose_60'],
                          self.dicM3[items]['glucose_90'], self.dicM3[items]['glucose_120']]
                    list_of_time_point = [0, 30, 60, 90, 120]
                    get_curves_and_auc(temp_list, items, list_of_time_point)
                elif curve == 'c_peptide':
                    temp_list = [self.dicM3[items]['c_peptide_m10'], self.dicM3[items]['c_peptide_m5'],
                          self.dicM3[items]['c_peptide_0'], self.dicM3[items]['c_peptide_30'], self.dicM3[items]['c_peptide_60'],
                          self.dicM3[items]['c_peptide_90'], self.dicM3[items]['c_peptide_120']]
                    list_of_time_point = [-10, -5, 0, 30, 60, 90, 120]
                    get_curves_and_auc(temp_list, items, list_of_time_point)

        #count = self.param_count(study_arm, metabolic_parameter)
        #gf.pie_graph(count, 'glucose tolerance', study_arm)

    def paired_comparaisonM0_M3(self, study_arm, metabolic_parameter, pie_parameter=None):
        '''Print simple statistics. Could expand to check if the distribution is normal then apply right test'''
        M0_list = []
        M3_list = []
        for items, values in self.dicM0.items():
            if self.sort_paired_values(study_arm, metabolic_parameter, values, items) is True:
                M0_list.append(values[metabolic_parameter])
                M3_list.append(self.dicM3[items][metabolic_parameter])
        print()
        print()
        print('              ________________________________________________________________________________________')
        print(metabolic_parameter, 'for', study_arm, 'group. n= ', str(len(M0_list)))
        print()
        print('Mean for M0 Values of ', metabolic_parameter, 'is', round(numpy.nanmean(M0_list),3), round(numpy.std(M0_list),3))
        print('Mean for M3 Values of ', metabolic_parameter, 'is', round(numpy.nanmean(M3_list),3), round(numpy.std(M3_list),3))
        print(scipy.stats.wilcoxon(M0_list, M3_list))

        print()
        print('Répartition '+study_arm+' for '+metabolic_parameter)
        print()
        count = self.param_count(study_arm, metabolic_parameter)
        print(count)
        return(count)
        if pie_parameter is not None:
            gf.pie_graph(count, pie_parameter, study_arm)

    def paired_values(self, metabolic_parameter):
        """print valor for paired values (MO and M3) of a metabolic_parameter"""
        print()
        print(metabolic_parameter, 'for Inuline Group')
        for items, values in self.dicM0.items():
            if self.sort_paired_values('inuline', metabolic_parameter, values, items) is True:
                print(items, values[metabolic_parameter], self.dicM3[items][metabolic_parameter])
        print()
        print(metabolic_parameter, 'for Maltodextrine Group')
        for items, values in self.dicM0.items():
            if self.sort_paired_values('maltodextrine', metabolic_parameter, values, items) is True:
                print(items, values[metabolic_parameter], self.dicM3[items][metabolic_parameter])

    def difference_M0_M3_mannwhitney(self, metabolic_parameter,  graph, patient_parameter=None, pie_parameter=None):
        '''Select, compare and graph paired values, between the two arms at the two time points. You can ask parameter subdivision and a pie repartition'''
        temp_dic = {}
        inu_M0_list = []
        inu_M3_list = []
        malto_M0_list = []
        malto_M3_list = []
        diff_inu_list = []
        diff_malto_list = []

    # This part select data, construct paired lists, and compare them
        for items, values in self.dicM0.items():
            if self.sort_paired_values('inuline', metabolic_parameter, values, items) is True:
                print(1)
                temp_dic[items] = {'M0 '+metabolic_parameter: values[metabolic_parameter],
                                   'M3 '+metabolic_parameter: self.dicM3[items][metabolic_parameter],
                                   'Difference': self.dicM3[items][metabolic_parameter] - values[metabolic_parameter],
                                   **self.patient_dic[items]}
                inu_M0_list.append(values[metabolic_parameter])
                inu_M3_list.append(self.dicM3[items][metabolic_parameter])

        for items, values in self.dicM0.items():
            if self.sort_paired_values('maltodextrine', metabolic_parameter, values, items,)is True:
                temp_dic[items] = {'M0 '+metabolic_parameter: values[metabolic_parameter],
                                   'M3 '+metabolic_parameter: self.dicM3[items][metabolic_parameter],
                                   'Difference': self.dicM3[items][metabolic_parameter] - values[metabolic_parameter],
                                   **self.patient_dic[items]}
                malto_M0_list.append(values[metabolic_parameter])
                malto_M3_list.append(self.dicM3[items][metabolic_parameter])

        for i in range(len(inu_M0_list)):
            diff_inu_list.append(inu_M0_list[i] - inu_M3_list[i])
        for i in range(len(malto_M3_list)):
            diff_malto_list.append(malto_M0_list[i] - malto_M3_list[i])
        count_inu = self.paired_comparaisonM0_M3('inuline', metabolic_parameter, patient_parameter)
        count_malto = self.paired_comparaisonM0_M3('maltodextrine', metabolic_parameter, patient_parameter)
        # Graph part
        if graph == 'swarmbox':
            gf.swarmboxM0_M3(diff_inu_list, diff_malto_list, temp_dic, metabolic_parameter, patient_parameter)
        elif graph == 'twoboxplot':
            gf.two_boxplot(temp_dic, metabolic_parameter,  patient_parameter)
        elif graph == 'parallel':
            gf.parallel(temp_dic, metabolic_parameter)
        else:
            print('You forgot to specify a type of graph')
        if pie_parameter is not None:
            gf.pie_graph(count_inu, pie_parameter, 'inuline')
            gf.pie_graph(count_malto, pie_parameter, 'maltodextrine')

    def swarm_correl_M0_M3(self, metabolic_parameter1, metabolic_parameter2, patient_parameter=None):
        temp_dic = {}
    # This part select data, construct paired lists
        for items, values in self.dicM0.items():
            if self.sort_paired_values('inuline', metabolic_parameter1, values, items) and\
               self.sort_paired_values('inuline', metabolic_parameter2, values, items) is True:
                temp_dic[items] = {'M0 '+metabolic_parameter1: values[metabolic_parameter1],
                                    'M3 '+metabolic_parameter1: self.dicM3[items][metabolic_parameter1],
                                    'M0 '+metabolic_parameter2: values[metabolic_parameter2],
                                    'M3 '+metabolic_parameter2: self.dicM3[items][metabolic_parameter2],
                                    'Difference '+metabolic_parameter1: self.dicM3[items][metabolic_parameter1] - values[metabolic_parameter1],
                                    'Difference '+metabolic_parameter2: self.dicM3[items][metabolic_parameter2] - values[metabolic_parameter2],
                                    'Study_arm': 'inuline', **self.patient_dic[items]}
        for items, values in self.dicM0.items():
            if self.sort_paired_values('maltodextrine', metabolic_parameter1, values, items) and\
               self.sort_paired_values('maltodextrine', metabolic_parameter2, values, items) is True:
                temp_dic[items] = {'M0 '+metabolic_parameter1: values[metabolic_parameter1],
                                   'M3 '+metabolic_parameter1: self.dicM3[items][metabolic_parameter1],
                                            'M0 '+metabolic_parameter2: values[metabolic_parameter2],
                                            'M3 '+metabolic_parameter2: self.dicM3[items][metabolic_parameter2],
                                            'Difference '+metabolic_parameter1: self.dicM3[items][metabolic_parameter1] - values[metabolic_parameter1],
                                            'Difference '+metabolic_parameter2: self.dicM3[items][metabolic_parameter2] - values[metabolic_parameter2],
                                            'Study_arm': 'maltodextrine', **self.patient_dic[items]}
        gf.correl_graph(temp_dic, metabolic_parameter1, metabolic_parameter2, patient_parameter)


def get_stats_on_one_metabolic_parameter(dic, metabolic_parameter, study_arm=None):
    '''Give Mean + Std for a metabolic parameter, at a particular time point (dicM0 or dicM3), unpaired'''
    temp_list = []
    if study_arm == None:
        for items, values in dic.items():
            if (isinstance(dic[items][metabolic_parameter], float) or isinstance(dic[items][metabolic_parameter], int)):
                temp_list.append(dic[items][metabolic_parameter])
    else:
        for items, values in dic.items():
            if values['study_arm'] == study_arm and (isinstance(dic[items][metabolic_parameter], float) or isinstance(dic[items][metabolic_parameter], int)):
                temp_list.append(dic[items][metabolic_parameter])
    print('Mean for M0 Values of ', metabolic_parameter, 'is', numpy.nanmean(temp_list), numpy.std(temp_list))
    return temp_list


def unpaired_comparaison(dic, metabolic_parameter):
    '''Will compare between the two arms, at a particular time point(M0 or M3)'''
    print('Inuline:')
    list1 = get_stats_on_one_metabolic_parameter(dic, metabolic_parameter, 'inuline')
    print('Maltodextrine')
    list2 = get_stats_on_one_metabolic_parameter(dic, metabolic_parameter, 'maltodextrine')
    s, p = scipy.stats.mannwhitneyu(list1, list2, use_continuity=True, alternative='two-sided')
    print('p-value of M0 inuline VS M0 Maltodextrine is ', round(p, 2))


def heatmap_pearson(df):
    gf.heatmap(df)


def get_curves_and_auc(temp_list, items, list_of_time_point):
    list_of_index_to_remove = []
    for i in range(len(temp_list)):
        if temp_list[i] == None:
            list_of_index_to_remove.append(i)
    if len(list_of_index_to_remove) >= 2:
        pass
    else:
        for indexes in list_of_index_to_remove:
            del(list_of_time_point[indexes])
            del(temp_list[indexes])
        auc = sklearn.metrics.auc(list_of_time_point, temp_list)
        print(items, round(auc,0))
