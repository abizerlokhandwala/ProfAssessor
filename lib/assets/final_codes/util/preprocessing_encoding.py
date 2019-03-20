import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import scipy
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
from collections import defaultdict

from util import fetch_data

comp_max = 9.98
entc_max = 9.3
it_max = 9.73
is_bin = 2

label_encode_dict = fetch_data.get_le_dict()
techweights = fetch_data.get_techweights()
nontechweights = fetch_data.get_nontechweights()


def delta_mapping(gpa):
  return (10-gpa)/(gpa-4)


def remap_techgpa_2(dfrow):
  global techweights
  gpa = dfrow['GPA']/100.00
  gpa_max_delta = delta_mapping(gpa)/2
  answers = dfrow.iloc[:,2:].values
  gpa_new = ((((answers*techweights).sum())*gpa_max_delta)+gpa)
  return gpa_new


def remap_nontechgpa_2(dfrow):
  global nontechweights
  gpa = dfrow['NontechScore']/100.00
  gpa_max_delta = delta_mapping(gpa)/2
  answers = dfrow.iloc[:,2:].values
  gpa_new = ((((answers*nontechweights).sum())*gpa_max_delta)+gpa)
  return gpa_new







def get_df_dummy(dfcat, input_email_df):
  df_dummy = pd.get_dummies(dfcat)
  df_dummy = df_dummy.iloc[1:,:]
  input_email_df = input_email_df.iloc[1:,:]

  input_email_df.head(10)

  return df_dummy,input_email_df




def get_cat_df(df):
  # dataframe to store only categorical attributes
  if (is_bin == 0) | (is_bin == 1):
     dfcat = df.loc[:, (df.columns != 'What is your Grade in College (GPA)?')]
  elif is_bin == 2:
    dfcat = df.loc[:, (df.columns != 'What is your Grade in College (GPA)?') & (df.columns != 'nontech score')]

  # Categorical boolean mask
  categorical_feature_mask = dfcat.dtypes==object
  # filter categorical columns using mask and turn it into a list
  categorical_cols = dfcat.columns[categorical_feature_mask].tolist()

  # apply le on categorical feature columns
  dfcat[categorical_cols] = dfcat[categorical_cols].apply(lambda col: label_encode_dict[col.name].transform(col))

  #Add a gpa column in categorical dataframe and convert to a categorical bin

  dfcat.insert(loc=0, column='GPA', value=df['What is your Grade in College (GPA)?'])

  if is_bin == 2:
    dfcat.insert(loc=1, column='NontechScore', value=df['nontech score'])

  if (is_bin == 0) | (is_bin == 2):
    dfcat['GPA'] = 100*dfcat['GPA']
    dfcat['GPA'] = dfcat['GPA'].astype(int)
  elif is_bin == 1:
    bin = [-1,0,7,7.5,8,8.25,8.5,8.75,9,9.25,9.5,10]
    category = pd.cut(dfcat['GPA'],bin)
    dfcat.insert(loc=0, column='Binned GPA', value=category)

  if is_bin == 2:
    dfcat['NontechScore'] = 100*dfcat['NontechScore']
    dfcat['NontechScore'] = dfcat['NontechScore'].astype(int)

  if is_bin == 1:
    dfcat['Binned GPA'] = dfcat['Binned GPA'].astype('str')
    dfcat['Binned GPA'] = dfcat['Binned GPA'].map({'(-1.0, 0.0]': 0,'(0.0, 7.0]': 0, '(7.0, 7.5]': 1, '(7.5, 8.0]': 2, '(8.0, 8.25]': 3, '(8.25, 8.5]': 4, '(8.5, 8.75]': 5, '(8.75, 9.0]': 6, '(9.0, 9.25]': 7, '(9.25, 9.5]': 8, '(9.5, 10.0]': 9})
    dfcat = dfcat.drop(['GPA'], axis = 1)
  dfcat.isnull().values.any()

  return dfcat





def calc_virtual_gpa(df):

#   tech_ans = df['How well do you think your GPA justifies your technical knowledge?']
#   nontech_ans = df['How well do you think your GPA justifies the amount of efforts you put in?']

#   print("USING DATAFRAME: ", df.head())

  tech_ans = df.iloc[0, df.columns.get_loc('How well do you think your GPA justifies your technical knowledge?')]
  nontech_ans = df.iloc[0, df.columns.get_loc('How well do you think your GPA justifies the amount of efforts you put in?')]
#   print("tech: ", tech_ans, " non tech: ", nontech_ans)


  oldtech  = (df.iloc[0, df.columns.get_loc('GPA')])/100.0
  oldnontech = (df.iloc[0, df.columns.get_loc('NontechScore')])/100.0

  #oldtech = df['GPA']/100.00
  #oldnontech = df['NontechScore']/100.00

  #ans = 0 means apt or overstimates
  if tech_ans == 1:
#     print("1 tech before: ", new_techgpa)
    #call function to calculate virtual GPA
    new_techgpa = remap_techgpa_2(df)
#     print("1 tech after: ", new_techgpa)
  else:
#     print("2 tech before: ", new_techgpa)
    new_techgpa = oldtech
#     print("2 tech after: ", new_techgpa)


  if nontech_ans == 1:
    #call function to calculate virtual GPA
    new_nontechgpa = remap_nontechgpa_2(df)
  else:
    new_nontechgpa = oldnontech

#   print("************* NEW GPAS NONTECH: ", new_nontechgpa.iloc[0], " TECH: ", new_techgpa.iloc[0], "SHAPPPPEEEE: TECH", type(new_techgpa), "SHAPPPPEEEE: NONTECH", new_nontechgpa.size)

#   print("TYPE OF NONTECH: ", type(new_nontechgpa))


  # print("type: ", str(type(new_techgpa)), "type: ", str(type(new_nontechgpa)))
  if((str(type(new_nontechgpa))== "<class 'numpy.float64'>")and((str(type(new_techgpa))== "<class 'numpy.float64'>"))):
    df.iloc[0, df.columns.get_loc('GPA')] = new_techgpa/1.0
    df.iloc[0, df.columns.get_loc('NontechScore')] = new_nontechgpa/1.0
  elif((str(type(new_nontechgpa))== "<class 'numpy.float64'>")and (not (str(type(new_techgpa))== "<class 'numpy.float64'>"))):
    new_techgpa.reset_index(drop=True,inplace=True)
    if((new_techgpa.size) == 2):
      df.iloc[0, df.columns.get_loc('GPA')] = new_techgpa.iloc[1]
    elif((new_techgpa.size) == 1):
      df.iloc[0, df.columns.get_loc('GPA')] = new_techgpa.iloc[0]
    df.iloc[0, df.columns.get_loc('NontechScore')] = new_nontechgpa/1.0
  elif((str(type(new_techgpa))== "<class 'numpy.float64'>")and (not (str(type(new_nontechgpa))== "<class 'numpy.float64'>"))):
    new_nontechgpa.reset_index(drop=True,inplace=True)
    if((new_nontechgpa.size) == 2):
      df.iloc[0, df.columns.get_loc('NontechScore')] = new_nontechgpa.iloc[1]
    if((new_nontechgpa.size) == 1):
      df.iloc[0, df.columns.get_loc('NontechScore')] = new_nontechgpa.iloc[0]
    df.iloc[0, df.columns.get_loc('GPA')] = new_techgpa/1.0
  else:
    new_nontechgpa.reset_index(drop=True,inplace=True)
    new_techgpa.reset_index(drop=True,inplace=True)
    if((new_techgpa.size) == 2):
      df.iloc[0, df.columns.get_loc('GPA')] = new_techgpa.iloc[1]
    elif((new_techgpa.size) == 1):
      df.iloc[0, df.columns.get_loc('GPA')] = new_techgpa.iloc[0]
    if((new_nontechgpa.size) == 2):
      df.iloc[0, df.columns.get_loc('NontechScore')] = new_nontechgpa.iloc[1]
    if((new_nontechgpa.size) == 1):
      df.iloc[0, df.columns.get_loc('NontechScore')] = new_nontechgpa.iloc[0]

    df.iloc[0, df.columns.get_loc('GPA')] = df.iloc[0, df.columns.get_loc('GPA')]/100.0
    df.iloc[0, df.columns.get_loc('NontechScore')] = df.iloc[0, df.columns.get_loc('NontechScore')]/100.0

  # if (dfemail.iloc[0])["Email Address"] in knowset:
    # print((dfemail.iloc[0])["Email Address"], " THIS Old Tech: ", oldtech, "AND THIS New Tech: ", df.iloc[0, df.columns.get_loc('GPA')], " Old NonTech: ", oldnontech, " New NonTech: ", df.iloc[0, df.columns.get_loc('NontechScore')])

  return df




def process_input(df, comp_max, entc_max, it_max):

  college = str(df.iloc[0, df.columns.get_loc('College Name?')])
  branch = str(df.iloc[0, df.columns.get_loc('Current Branch?')])
  year = str(df.iloc[0, df.columns.get_loc('Current Year?')])

  if (college != 'Pune Institute of Computer Technology'):
    print("Student not from PICT")
    return -1

  #drop first year students
  df = df.loc[df['Current Year?'] != 'First Year']
  df = df.loc[df['What is your Grade in College (GPA)?'] !=0]

  #check student branch
  if(branch == 'Computer Engineering'):
    max_val = comp_max
  elif(branch == 'EnTC'):
    max_val = entc_max
  elif(branch == 'IT'):
    max_val= it_max

  max_val=max_val/1.0
  min_value = 0

  df.reset_index(drop=True,inplace=True)

  old_gpa = df.iloc[0, df.columns.get_loc('What is your Grade in College (GPA)?')]
  old_gpa = np.float64(old_gpa)
  min_value = np.float64(min_value)
  newtemp = ((old_gpa - min_value) / (max_val - min_value))*10.0
#   print("oldgpa valtype: ", (old_gpa), " : ", (max_val), " : ",(min_value), " : ",(old_gpa - min_value)," : ",(max_val)," : ", newtemp)
  df.iloc[0, df.columns.get_loc('What is your Grade in College (GPA)?')] = newtemp
  # print("Max_val: ",max_val," Old GPA: ", old_gpa, "New GPA: ", df.iloc[0, df.columns.get_loc('What is your Grade in College (GPA)?')])

  if (is_bin == 0) | (is_bin == 1):
    df.loc[-1] = ['2/14/2019 13:39:07','admin','Pune Institute of Computer Technology','Computer Engineering','Fourth Year',9.99,'Average','Not Participated','No','No','No','No','No','No','No',"Job in technical domain (Software Developer, Data Scientist etc.)",'No','No','No - I do NOT ask questions or I prefer to look at the topic on my own','I leave the topic to look at it later on.','I leave the topic and look at during examinations','I learn a topic only to score marks in college/university examination','Short term memorization of syllabus just to spend lesser time','When exams are around the corner by just focusing on the given syllabus','I study topics that are limited to the examination curriculum irrespective of my understanding of the topic','No','No','Yes','Memorize the topic and its contents OR Leave it','Yes','is Apt or Overestimates my knowledge','is Apt or Overestimates my efforts','Delay the project and postpone it to some other time','No/Average performance','No','No','No','No','Do not prefer','Do not prefer','Do not prefer']
  elif is_bin == 2:
    df.insert(loc=6, column='nontech score', value=df['What is your Grade in College (GPA)?'])
    df.loc[-1] = ['2/14/2019 13:39:07','admin','Pune Institute of Computer Technology','Computer Engineering','Fourth Year',9.99, 9.99,'Average','Not Participated','No','No','No','No','No','No','No',"Job in technical domain (Software Developer, Data Scientist etc.)",'No','No','No - I do NOT ask questions or I prefer to look at the topic on my own','I leave the topic to look at it later on.','I leave the topic and look at during examinations','I learn a topic only to score marks in college/university examination','Short term memorization of syllabus just to spend lesser time','When exams are around the corner by just focusing on the given syllabus','I study topics that are limited to the examination curriculum irrespective of my understanding of the topic','No','No','Yes','Memorize the topic and its contents OR Leave it','Yes','is Apt or Overestimates my knowledge','is Apt or Overestimates my efforts','Delay the project and postpone it to some other time','No/Average performance','No','No','No','No','Do not prefer','Do not prefer','Do not prefer']

  df.sort_index(inplace=True)
  df.index = df.index + 1  # shifting index

  input_email_df = df.copy()

  df = df.drop(['Timestamp','Email Address','Current Branch?', 'Current Year?'], axis = 1)
  df = df.drop(['College Name?'], axis = 1)


  dfcat = get_cat_df(df)

  df_dummy, input_email_df = get_df_dummy(dfcat, input_email_df)
  df_final = calc_virtual_gpa(df_dummy)

  return df_final




def preprocess_data(input_user_df):
  processed_input_df = process_input(input_user_df, comp_max, entc_max, it_max)
  return processed_input_df
