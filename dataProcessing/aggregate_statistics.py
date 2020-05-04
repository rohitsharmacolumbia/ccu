import numpy as np
import pandas as pd
from datetime import date

#!pip install xlrd
#!pip install openpyxl

input_path = '../data/dataIn/CCU_patientData_allPatients_active.xlsx'
output_current = '../data/dataOut/CCU_current_patientData_aggregated.xlsx'
output_all = '../data/dataOut/CCU_all_patientData_aggregated.xlsx'

print("*************** Reading Files (Step 1/4) ***************")
xl = pd.ExcelFile(input_path)
df = pd.read_excel(xl, 'patientData')
df = df.drop(columns=df.columns[47:])

df = df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'))

# convert all dates to datetime objects
df['date_of_intubation'] = df['date_of_intubation'].apply(lambda date: pd.to_datetime(date) if date != '.' else np.NaN)
df['date_of_extubation_or_trach'] = df['date_of_extubation_or_trach'].apply(lambda date: pd.to_datetime(date) if date != '.' else np.NaN)
df['start_date_of_paralytics'] = df['start_date_of_paralytics'].apply(lambda date: pd.to_datetime(date) if date != '.' else np.NaN)
df['stop_date_of_paralytics'] = df['stop_date_of_paralytics'].apply(lambda date: pd.to_datetime(date) if date != '.' else np.NaN)
df['start_date_of_cvvh'] = df['date_started_cvvh'].apply(lambda date: pd.to_datetime(date) if date != '.' else np.NaN)
df['stop_date_of_cvvh'] = df['end_date_for_cvvh'].apply(lambda date: pd.to_datetime(date) if (date != '.' and date != 'iHD started 4/13') else np.NaN)

# calculate time elapsed for missing entries
def time_period(start_time, days):
  if pd.isnull(start_time):
    total_days = np.NaN
  elif days == '.' or pd.isnull(days):
    time_delta = pd.to_datetime(date.today())-start_time
    total_days = time_delta.days
  else:
    total_days = days
  return total_days


print("*************** Statistics Calculation (Step 2/4) ***************")

df['days_intubated'] = df.apply(lambda row: time_period(row['date_of_intubation'], row['days_intubated']), axis=1 )
df['days_paralyzed'] = df.apply(lambda row: time_period(row['start_date_of_paralytics'], row['days_paralyzed']), axis=1 )
df['days_cvvh'] = df.apply(lambda row: time_period(row['start_date_of_cvvh'], row['days_on_cvvh']), axis=1 )

current_df = pd.date_range(start=min(df['ccu_admit_date_formatted']), end=pd.to_datetime(date.today())).to_frame().rename(columns={0:'date'}).reset_index(drop=True)
all_df = pd.date_range(start=min(df['ccu_admit_date_formatted']), end=pd.to_datetime(date.today())).to_frame().rename(columns={0:'date'}).reset_index(drop=True)

# all the patients currently in ccu
def current_patients(given_date):
  return df[(df['ccu_admit_date_formatted'] <= given_date) & ((df['ccu_discharge_date_formatted'].isna()) | (df['ccu_discharge_date_formatted'] >= given_date))]
# current + past patients in ccu
def all_patients(upto_date):
  return df[df['ccu_admit_date_formatted'] <= upto_date]

current_df['in_ccu'] = current_df.date.apply(lambda date: len(current_patients(date)))
all_df['in_ccu'] = all_df.date.apply(lambda date: len(all_patients(date)))

current_df['average_age'] = current_df.date.apply(lambda date: round(current_patients(date)['age'].mean(), 2))
all_df['average_age'] = all_df.date.apply(lambda date: round(all_patients(date)['age'].mean(), 2))

current_df['average_los'] = current_df.date.apply(lambda date: round(current_patients(date)['ccu_los'].mean(), 2))
all_df['average_los'] = all_df.date.apply(lambda date: round(all_patients(date)['ccu_los'].mean(), 2))

all_df['deceased'] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)['deceased_y/n'] == 'Y']))

# unclear what current average intubated/paralyzed days would be
all_df['average_days_intubated'] = all_df.date.apply(lambda date: round(all_patients(date)['days_intubated'].mean(), 2))
all_df['average_days_paralyzed'] = all_df.date.apply(lambda date: round(all_patients(date)['days_paralyzed'].mean(), 2))
all_df['average_days_cvvh'] = all_df.date.apply(lambda date: round(all_patients(date)['days_cvvh'].mean(), 2))

current_df['chf'] = current_df.date.apply(lambda date: len(current_patients(date)[current_patients(date)['known_to_chf_formatted'] == 'Yes']))
all_df['chf'] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)['known_to_chf_formatted'] == 'Yes']))

current_df['mechanical_support'] = current_df.date.apply(lambda date: len(current_patients(date)[current_patients(date)['mechanical_support_formatted'] == 'Yes']))
all_df['mechanical_support'] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)['mechanical_support_formatted'] == 'Yes']))

current_df['trach'] = current_df.date.apply(lambda date: len(current_patients(date)[current_patients(date)['trach_(yes/no)']=='Yes']))
all_df['trach'] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)['trach_(yes/no)']=='Yes']))

current_df['proned'] = current_df.date.apply(lambda date: len(current_patients(date)[current_patients(date)['proned']=='Yes']))
all_df['proned'] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)['proned']=='Yes']))

current_df['iNo'] = current_df.date.apply(lambda date: len(current_patients(date)[current_patients(date)['ino']=='Yes']))
all_df['iNo'] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)['ino']=='Yes']))

current_df['intubated'] = current_df.date.apply(lambda date: len(df[(df['intubated']=='Yes') & (df['date_of_intubation'] <= date) & ((df['date_of_extubation_or_trach'].isna()) | (df['date_of_extubation_or_trach'] >= date))]))
all_df['intubated'] = all_df.date.apply(lambda date: len(df[(df['intubated']=='Yes') & (df['date_of_intubation'] <= date)]))

current_df['paralytics'] = current_df.date.apply(lambda date: len(df[(df['paralytics_while_in_ccu'] == 'Yes') & (df['start_date_of_paralytics'] <= date) & ((df['stop_date_of_paralytics'].isna()) | (df['stop_date_of_paralytics'] >= date))]))
all_df['paralytics'] = all_df.date.apply(lambda date: len(df[(df['paralytics_while_in_ccu'] == 'Yes') & (df['start_date_of_paralytics'] <= date)]))

current_df['cvvh'] = current_df.date.apply(lambda date: len(df[(df['cvvh_(y/n)'] == 'Yes') & (df['start_date_of_cvvh'] <= date) & ((df['stop_date_of_cvvh'].isna()) | (df['stop_date_of_cvvh'] >= date))]))
all_df['cvvh'] = all_df.date.apply(lambda date: len(df[(df['cvvh_(y/n)'] == 'Yes') & (df['start_date_of_cvvh'] <= date)]))

#missing data: when was the test for covid19
dummies = ['gender', 'race', 'ethnicity', 'ccu_location', 'admitted_from_formatted', 'emr_diagnosis', 'covid+_(y/n/nt_not_tested)', 'indication_for_cvvh',  'discharged_to']

print("*************** Creating Dummies (Step 3/4) ***************")

df[dummies] = df[dummies].applymap(lambda x: x.lower().strip().replace(' ', '_') if isinstance(x, str) else np.NaN)
df = pd.get_dummies(df, columns=dummies)

for col in df.columns[41:]:
  all_df[col] = all_df.date.apply(lambda date: len(all_patients(date)[all_patients(date)[col] == 1]))
for col in df.columns[41:138]:
  current_df[col] = current_df.date.apply(lambda date: len(current_patients(date)[current_patients(date)[col] == 1]))


#write output
#current_df.to_csv('/content/drive/My Drive/current_df.csv', index=False)
#all_df.to_csv('/content/drive/My Drive/all_df.csv', index=False)
print("*************** Exporting Data (Step 4/4) ***************")
current_df.to_excel(output_current,sheet_name='patientStatisticsByDay')
all_df.to_excel(output_all,sheet_name='patientStatisticsByDay')
print("*************** Complete - Files saved in data/dataOut ***************")
