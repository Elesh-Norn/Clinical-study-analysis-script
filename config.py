# Thoses are list and legends i use in my the main scriptself.

LEGENDS = {'Weight': 'Weight in kg', 'Height': 'Height in cm',
            'BMI': 'BMI in kg/m²', 'W/H ratio': 'Waist/Hip ratio',
            'Systolic BP': 'Systolic blood pressure in mmHg',
            'Diastolic BP': 'Diastolic blood pressure in mmHg',
            'Bioimpedance R': 'Bio-impedance R',
            'R/height':'R/height', 'Xc/height':'Xc/height',
            'Fibroscan elasticity median': 'Elasticity median in kPa',
            'Fibroscan elasticity IQR':'Fibroscan elasticity IQR',
            'Fibroscan CAP median': 'CAP median in dB/m',
            'Fibroscan CAP IQR': 'Fibroscan CAP IQR',
            'HbA1c': 'HbA1c in %', 'bilirubin': 'Bilirubin in mg/dl',
            'Fasting total cholesterol': 'Fasting total cholesterol in mg/dl', 'Fasting LDL cholesterol': 'Fasting LDL in mg/dl',
            'Fasting HDL cholesterol': 'Fasting HDL in mg/dl', 'Fasting triglycerides': 'Fasting tryglycerides in mg/dl',
            'Apo-A1': 'Apo-A1 in g/l', 'AST': 'AST in U/l', 'ALT': 'ALT in U/l', 'gGT': 'gGT in U/l',
            'haptoglobin': 'Haptoglobin in U/L', 'α-2-macroglobulin': 'a2 macroglobulin in g/l', 'Fasting glycemia': 'Fasting glycemia (mg/dl)',
            'Average Fasting Glucose': 'Fasting glycemia (mg/dl)', 'Average Fasting Insulin': 'Fasting insulin (mU/l)',
            'Average Fasting C peptide': 'Fasting C peptide (mU/l)',
            'Matsuda index': 'Matsuda Index', 'HOMA ISI': 'HOMA ISI Index',
            'Stumvoll First Phase': 'Stumvoll 1PH', 'Stumvoll Second Phase': 'Stumvoll 2PH',
            'HOMA IR': 'HOMA IR Index', 'OGIS':'OGIS',
            'Oral Disposition index': 'Oral Disposition index',
            'AUC Insuline': 'Insulin AUCs', 'AUC Glucose': 'Glucose AUCs',
            'AUC C peptide': 'C peptide AUCs', 'IGI 30': 'IGI 30',
            'Mean BP':'Mean blood pressure in mmHg', 'Age':'Age',
            'Waist':'Waist in cm', 'IGI Cpept':'Insulogenic index calculated with C peptide',
            'HIE': 'Hepatic insulin extraction'}

GLUCOSE_LIST = ['Average Fasting Glucose', 'Average Fasting Insulin',
                'Average Fasting C peptide','HbA1c', 'Matsuda index',
                'HOMA ISI', 'HOMA IR', 'Oral Disposition index', 'IGI 30',
                'Stumvoll First Phase',
                'Stumvoll Second Phase', 'OGIS']

NORMAL_LIST = ['Age', 'Weight','BMI', 'W/H ratio','Systolic BP','Diastolic BP',
            'Bioimpedance R','R/height',
            'Fibroscan elasticity median',
            'Fibroscan CAP median', 'bilirubin',
            'Fasting total cholesterol', 'Fasting LDL cholesterol',
            'Fasting HDL cholesterol', 'Fasting triglycerides',
            'Apo-A1', 'AST', 'ALT', 'gGT',
            'haptoglobin', 'α-2-macroglobulin']

HEATMAP_LIST = ['Patient ID','Time point','Arm','Hospital', 'Hip', 'Waist',
             'Glucose tolerance','Dyslipidemia','Hypertension','NAFLD',
             'Bariatric surgery requested','start week 0','end week 12',
             'Active smoker', 'Insuline medication', 'Metformin',
             'Change of Insuline medication', 'Antibiotic','Exclusion',
             'CT L3 muscle area', 'CT L3 visceral fat area', 'CT L3 subcut fat area',
             'OGTT Glucose', 'OGTT Insuline', 'OGTT C peptide', 'OGTT Insuline?',
             'OGTT Glucose?','OGTT Glucose 0',
             'OGTT Glucose 30', 'OGTT Glucose 60','OGTT Glucose 90', 'OGTT Glucose 120',
             'OGTT Insulin -10', 'OGTT Insulin -5',	'OGTT Insulin 0', 'OGTT Insulin 30',
             'OGTT Insulin 60',	'OGTT Insulin 90', 'OGTT Insulin 120',
             'OGTT C-pep -10', 'OGTT C-pep -5', 'OGTT  C-pep 0', 'OGTT C-pep 30',
             'OGTT C-pep 60',	'OGTT C-pep 90',	'OGTT C-pep 120', 'Fibroscan probe',
             'Fibroscan Nb of valid measurements', 'Fibroscan Nb of total measurements ']

GLUCOSE_LIST_AUC = GLUCOSE_LIST
for item in ['AUC Insuline', 'AUC Glucose', 'AUC C peptide']:
    GLUCOSE_LIST_AUC.append(item)
