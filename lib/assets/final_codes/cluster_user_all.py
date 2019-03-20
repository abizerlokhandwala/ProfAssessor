import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import scipy
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
from collections import defaultdict
from collections import OrderedDict
from util import preprocessing_encoding
from util import calculate_membership
from util import get_levels
from util import fetch_data
import data_store
import json
import sys

import warnings
warnings.filterwarnings("ignore")


col_list = ['Timestamp', 'Email Address', 'College Name?', 'Current Branch?', 'Current Year?', 'What is your Grade in College (GPA)?', 'How would you rate your puzzle solving efficiency?', 'Have you prepared for any olympiads/national level competitive examinations in your school days?', 'Have you actively participated in activities like chess or abacus etc?', 'Have you been "extensively" involved in the following? [Competitive Coding]', 'Have you been "extensively" involved in the following? [Sodtware Development]', 'Have you been "extensively" involved in the following? [ML/AI Projects or Research]', 'Have you been "extensively" involved in the following? [Mathematics and Logical Reasoning]', 'Have you been "extensively" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]', 'Have you been "extensively" involved in the following? [Literature/Blogging ]', 'What are your plans after your undergraduation?', 'Are you attentive during lectures at college?', 'Do you feel the lectures are slow paced or repetitive in general?', 'Do you ask questions to the professor, if you do not understand a particular concept during the lecture?', 'What do you do if you are not satisfied with the answer given by the professor? ', 'What do you do if you are not satisfied with a topic in lecture?', 'What is your study pattern in general?', 'What would you prefer during exams to score good marks?', 'When do you prefer to study?', 'How do you prefer to study for your university examinations?', 'Do you seriously perform college practical assignments and projects?', 'Would you do a particular task seriously even if you are not interested?', 'Would you put off a task if the deadline is not near', 'If you don’t understand a particular topic in the curriculum what do you prefer?', 'Do you feel a need to revise a theoretical topic learnt 2 days before?', 'How well do you think your GPA justifies your technical knowledge?', 'How well do you think your GPA justifies the amount of efforts you put in?', 'If you had an idea for a technical project, would you:', 'If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?', 'Are you proficient in the following? [Object Oriented Programming Concepts]', 'Are you proficient in the following? [C/C++]', 'Are you proficient in the following? [JAVA]', 'Are you proficient in the following? [Python]', 'Provide your preference for the following methods of learning [Books/Textual info on the Internet]', 'Provide your preference for the following methods of learning [Online courses/videos]', 'Provide your preference for the following methods of learning [Personalised classroom teaching (human)]']

final_df = pd.DataFrame(columns=col_list)




user_data_json = '{"Timestamp":"2\/14\/2019 13:39:07","Email Address":"abizerL123@gmail.com","College Name?":"Pune Institute of Computer Technology","Current Branch?":"Computer Engineering","Current Year?":"Fourth Year","What is your Grade in College (GPA)?":9.4,"How would you rate your puzzle solving efficiency?":"High","Have you prepared for any olympiads\/national level competitive examinations in your school days?":"Not Participated","Have you actively participated in activities like chess or abacus etc?":"No","Have you been \"extensively\" involved in the following? [Competitive Coding]":"Yes","Have you been \"extensively\" involved in the following? [Sodtware Development]":"Yes","Have you been \"extensively\" involved in the following? [ML\/AI Projects or Research]":"No","Have you been \"extensively\" involved in the following? [Mathematics and Logical Reasoning]":"Yes","Have you been \"extensively\" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]":"Yes","Have you been \"extensively\" involved in the following? [Literature\/Blogging ]":"No","What are your plans after your undergraduation?":"Job in technical domain (Software Developer, Data Scientist etc.)","Are you attentive during lectures at college?":"Yes","Do you feel the lectures are slow paced or repetitive in general?":"No","Do you ask questions to the professor, if you do not understand a particular concept during the lecture?":"Yes - Almost every time","What do you do if you are not satisfied with the answer given by the professor? ":"I ask multiple questions until the topic is clarified.","What do you do if you are not satisfied with a topic in lecture?":"I leave the topic and look at during examinations","What is your study pattern in general?":"I learn a topic to understand the core fundamentals\/learn the topics outside the examination syllabus for better understanding","What would you prefer during exams to score good marks?":"Understanding the syllabus even if it would result in spending more time","When do you prefer to study?":"When exams are around the corner by just focusing on the given syllabus","How do you prefer to study for your university examinations?":"I prefer detailed study of curriculum as well as the required background knowledge","Do you seriously perform college practical assignments and projects?":"Yes","Would you do a particular task seriously even if you are not interested?":"No","Would you put off a task if the deadline is not near":"Yes","If you don\u2019t understand a particular topic in the curriculum what do you prefer?":"Try again to understand the topic from multiple sources","Do you feel a need to revise a theoretical topic learnt 2 days before?":"Yes","How well do you think your GPA justifies your technical knowledge?":"is Apt or Overestimates my knowledge","How well do you think your GPA justifies the amount of efforts you put in?":"is Apt or Overestimates my efforts","If you had an idea for a technical project, would you:":"Delay the project and postpone it to some other time","If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?":"Yes","Are you proficient in the following? [Object Oriented Programming Concepts]":"Yes","Are you proficient in the following? [C\/C++]":"Yes","Are you proficient in the following? [JAVA]":"No","Are you proficient in the following? [Python]":"No","Provide your preference for the following methods of learning [Books\/Textual info on the Internet]":"Prefer","Provide your preference for the following methods of learning [Online courses\/videos]":"Prefer","Provide your preference for the following methods of learning [Personalised classroom teaching (human)]":"Prefer"}'

def get_membership(processed_df, power):
    membership_values_all = []
    for attribute_index in range(0, 9):
        membership_values = calculate_membership.calc_membership_2(attribute_index, processed_df, False, True, power)
        membership_values_all.append(membership_values)
    return membership_values_all

def get_output(json_user_obj, final_membership_values_all,final_scaled_membership_values_all,min_cluster_index):
    json_output_str = ''

    output_mem_val_all = []
    for i in range(0, len(final_membership_values_all)):
        temp = (final_membership_values_all[i])
        output_mem_val_all.append(temp)

    json_output_str+=("{\"email\":\""+json_user_obj['Email Address']+"\",")
    # json_output_str+=("\"initial_cluster_mv\":\""+str((output_mem_val_all))+"\",")
    json_output_str+=("\"initial_cluster_mv\":\""+str(("placeholder"))+"\",")
    json_output_str+=("\"student_attribute_levels\":\""+str((final_scaled_membership_values_all))+"\",")
    json_output_str+=("\"student_final_cluster\":\""+str((min_cluster_index))+"\"}")

    return json_output_str

def get_output_all_data(user_email, final_membership_values_all,final_scaled_membership_values_all,min_cluster_index):
    json_output_str = ''

    output_mem_val_all = []
    for i in range(0, len(final_membership_values_all)):
        temp = (final_membership_values_all[i])
        output_mem_val_all.append(temp)

    json_output_str+=("{\"email\":\""+user_email+"\",")
    # json_output_str+=("\"initial_cluster_mv\":\""+str((output_mem_val_all))+"\",")
    json_output_str+=("\"initial_cluster_mv\":\""+str(("placeholder"))+"\",")
    json_output_str+=("\"student_attribute_levels\":\""+str((final_scaled_membership_values_all))+"\",")
    json_output_str+=("\"student_final_cluster\":\""+str((min_cluster_index))+"\"}")

    return json_output_str

def check_kmeans_cluster(user_data_json):

    # print("*******", user_data_json)
    user_data_json = user_data_json.replace("\"extensively\"", "extensively")
    json_user_obj = json.loads(user_data_json)

    # print(str(json_user_obj))
    #
    # json_user_obj['Have you been "extensively" involved in the following? [ML/AI Projects or Research]'] = json_user_obj.pop('Have you been extensively involved in the following? [ML/AI Projects or Research]')
    # json_user_obj['Have you been "extensively" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]'] = json_user_obj.pop('Have you been extensively involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]')
    # json_user_obj['Have you been "extensively" involved in the following? [Literature/Blogging ]'] = json_user_obj.pop('Have you been extensively involved in the following? [Literature/Blogging ]')
    # json_user_obj['Have you been "extensively" involved in the following? [Competitive Coding]'] = json_user_obj.pop('Have you been extensively involved in the following? [Competitive Coding]')
    # json_user_obj['Have you been "extensively" involved in the following? [Mathematics and Logical Reasoning]'] = json_user_obj.pop('Have you been extensively involved in the following? [Mathematics and Logical Reasoning]')
    # json_user_obj['Have you been "extensively" involved in the following? [Sodtware Development]'] = json_user_obj.pop('Have you been extensively involved in the following? [Sodtware Development]')

    user_dataframe = pd.DataFrame.from_records((json_user_obj), index=[0])
    new_df = user_dataframe[col_list].copy()

    # print("******************")

    # print(new_df.head().T)
    processed_df = preprocessing_encoding.preprocess_data(new_df)

    final_membership_values_all = get_membership(processed_df, 2)

    final_scaled_membership_values_all= get_levels.get_ind_levels(final_membership_values_all)

    distance_min, min_cluster_index = get_levels.apply_kmeans(final_scaled_membership_values_all)

    # print(get_output(json_user_obj,final_membership_values_all,final_scaled_membership_values_all,min_cluster_index))

    return get_output(json_user_obj,final_membership_values_all,final_scaled_membership_values_all,min_cluster_index)


def check_kmeans_cluster_all_data(new_df):


    # print("working on: ", new_df.head().T)
    # new_df = pd.DataFrame([user_data_list], columns = col_list)

    # user_dataframe = pd.DataFrame.from_records((json_user_obj), index=[0])
    # new_df = user_dataframe[col_list].copy()

    processed_df = preprocessing_encoding.preprocess_data(new_df)
    if(str(processed_df) == '-1'):
        # print("RETURNING")
        return -1


    final_membership_values_all = get_membership(processed_df, 2)

    final_scaled_membership_values_all= get_levels.get_ind_levels(final_membership_values_all)

    distance_min, min_cluster_index = get_levels.apply_kmeans(final_scaled_membership_values_all)

    # print(get_output(json_user_obj,final_membership_values_all,final_scaled_membership_values_all,min_cluster_index))

    return get_output_all_data(new_df['Email Address'],final_membership_values_all,final_scaled_membership_values_all,min_cluster_index)






#====================================FOR ONE DATA==================================

# user_data_json2 = (sys.argv)
# # print("################################", user_data_json2)
# print(check_kmeans_cluster(str(user_data_json2[1])))





# temp = "['cluster_user.py', "
# tlen = len(temp)
# print("LENGGTYHHHHH: ", (user_data_json2).shape)




#====================================FOR FULL DATA==================================

all_data_list = (fetch_data.get_all_data())

# print(type(all_data_list.iloc[2]))

all_data_json = {}

out_string = ''
# print((all_data_list[0]))
#
#


data_length = len(all_data_list)

# print(data_length)

for i in range (0, data_length):
    out = check_kmeans_cluster_all_data(pd.DataFrame([all_data_list.iloc[i]], columns = col_list))
    # all_data_json.append(str(out.iloc[0]))
    out_string+=(str(out.iloc[0]))+'#'
    # print(((i+1)/data_length)*100)

# print((str(all_data_json[2].iloc[0])))
# print(json.dump(all_data_json))

print(out_string[:-1])
