import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import scipy
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
from collections import defaultdict
from collections import OrderedDict


import json

col_list = ['Timestamp', 'Email Address', 'College Name?', 'Current Branch?', 'Current Year?', 'What is your Grade in College (GPA)?', 'How would you rate your puzzle solving efficiency?', 'Have you prepared for any olympiads/national level competitive examinations in your school days?', 'Have you actively participated in activities like chess or abacus etc?', 'Have you been "extensively" involved in the following? [Competitive Coding]', 'Have you been "extensively" involved in the following? [Sodtware Development]', 'Have you been "extensively" involved in the following? [ML/AI Projects or Research]', 'Have you been "extensively" involved in the following? [Mathematics and Logical Reasoning]', 'Have you been "extensively" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]', 'Have you been "extensively" involved in the following? [Literature/Blogging ]', 'What are your plans after your undergraduation?', 'Are you attentive during lectures at college?', 'Do you feel the lectures are slow paced or repetitive in general?', 'Do you ask questions to the professor, if you do not understand a particular concept during the lecture?', 'What do you do if you are not satisfied with the answer given by the professor? ', 'What do you do if you are not satisfied with a topic in lecture?', 'What is your study pattern in general?', 'What would you prefer during exams to score good marks?', 'When do you prefer to study?', 'How do you prefer to study for your university examinations?', 'Do you seriously perform college practical assignments and projects?', 'Would you do a particular task seriously even if you are not interested?', 'Would you put off a task if the deadline is not near', 'If you don’t understand a particular topic in the curriculum what do you prefer?', 'Do you feel a need to revise a theoretical topic learnt 2 days before?', 'How well do you think your GPA justifies your technical knowledge?', 'How well do you think your GPA justifies the amount of efforts you put in?', 'If you had an idea for a technical project, would you:', 'If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?', 'Are you proficient in the following? [Object Oriented Programming Concepts]', 'Are you proficient in the following? [C/C++]', 'Are you proficient in the following? [JAVA]', 'Are you proficient in the following? [Python]', 'Provide your preference for the following methods of learning [Books/Textual info on the Internet]', 'Provide your preference for the following methods of learning [Online courses/videos]', 'Provide your preference for the following methods of learning [Personalised classroom teaching (human)]']

final_df = pd.DataFrame(columns=col_list)


user_data_json = '{"Timestamp":"2\/14\/2019 13:39:07","Email Address":"abizerL123@gmail.com","College Name?":"Pune Institute of Computer Technology","Current Branch?":"Computer Engineering","Current Year?":"Fourth Year","What is your Grade in College (GPA)?":9.4,"How would you rate your puzzle solving efficiency?":"High","Have you prepared for any olympiads\/national level competitive examinations in your school days?":"Not Participated","Have you actively participated in activities like chess or abacus etc?":"No","Have you been \"extensively\" involved in the following? [Competitive Coding]":"Yes","Have you been \"extensively\" involved in the following? [Sodtware Development]":"Yes","Have you been \"extensively\" involved in the following? [ML\/AI Projects or Research]":"No","Have you been \"extensively\" involved in the following? [Mathematics and Logical Reasoning]":"Yes","Have you been \"extensively\" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]":"Yes","Have you been \"extensively\" involved in the following? [Literature\/Blogging ]":"No","What are your plans after your undergraduation?":"Job in technical domain (Software Developer, Data Scientist etc.)","Are you attentive during lectures at college?":"Yes","Do you feel the lectures are slow paced or repetitive in general?":"No","Do you ask questions to the professor, if you do not understand a particular concept during the lecture?":"Yes - Almost every time","What do you do if you are not satisfied with the answer given by the professor? ":"I ask multiple questions until the topic is clarified.","What do you do if you are not satisfied with a topic in lecture?":"I leave the topic and look at during examinations","What is your study pattern in general?":"I learn a topic to understand the core fundamentals\/learn the topics outside the examination syllabus for better understanding","What would you prefer during exams to score good marks?":"Understanding the syllabus even if it would result in spending more time","When do you prefer to study?":"When exams are around the corner by just focusing on the given syllabus","How do you prefer to study for your university examinations?":"I prefer detailed study of curriculum as well as the required background knowledge","Do you seriously perform college practical assignments and projects?":"Yes","Would you do a particular task seriously even if you are not interested?":"No","Would you put off a task if the deadline is not near":"Yes","If you don\u2019t understand a particular topic in the curriculum what do you prefer?":"Try again to understand the topic from multiple sources","Do you feel a need to revise a theoretical topic learnt 2 days before?":"Yes","How well do you think your GPA justifies your technical knowledge?":"is Apt or Overestimates my knowledge","How well do you think your GPA justifies the amount of efforts you put in?":"is Apt or Overestimates my efforts","If you had an idea for a technical project, would you:":"Delay the project and postpone it to some other time","If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?":"Yes","Are you proficient in the following? [Object Oriented Programming Concepts]":"Yes","Are you proficient in the following? [C\/C++]":"Yes","Are you proficient in the following? [JAVA]":"No","Are you proficient in the following? [Python]":"No","Provide your preference for the following methods of learning [Books\/Textual info on the Internet]":"Prefer","Provide your preference for the following methods of learning [Online courses\/videos]":"Prefer","Provide your preference for the following methods of learning [Personalised classroom teaching (human)]":"Prefer"}'

# data_temp = ''' \
# {   \
# "Timestamp":"2\/14\/2019 13:39:07", \
# "Email Address":"abizerL123@gmail.com",\
# "College Name?":"Pune Institute of Computer Technology",
# "Current Branch?":"Computer Engineering",\
# "Current Year?":"Fourth Year",\
# "What is your Grade in College (GPA)?":9.4,\
# "How would you rate your puzzle solving efficiency?":"High","Have you prepared for any olympiads\/national level competitive examinations in your school days?":"Not Participated",\
# "Have you actively participated in activities like chess or abacus etc?":"No",\
# "Have you been extensively involved in the following? [Competitive Coding]":"Yes",\
# "Have you been extensively involved in the following? [Sodtware Development]":"Yes",\
# "Have you been extensively involved in the following? [ML\/AI Projects or Research]":"No",\
# "Have you been extensively involved in the following? [Mathematics and Logical Reasoning]":"Yes",\
# "Have you been extensively involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]":"Yes",\
# "Have you been extensively involved in the following? [Literature\/Blogging ]":"No",\
# "What are your plans after your undergraduation?":"Job in technical domain (Software Developer, Data Scientist etc.)",\
# "Are you attentive during lectures at college?":"Yes",\
# "Do you feel the lectures are slow paced or repetitive in general?":"No",\
# "Do you ask questions to the professor, if you do not understand a particular concept during the lecture?":"Yes - Almost every time",\
# "What do you do if you are not satisfied with the answer given by the professor? ":"I ask multiple questions until the topic is clarified.",\
# "What do you do if you are not satisfied with a topic in lecture?":"I leave the topic and look at during examinations",\
# "What is your study pattern in general?":"I learn a topic to understand the core fundamentals\/learn the topics outside the examination syllabus for better understanding",\
# "What would you prefer during exams to score good marks?":"Understanding the syllabus even if it would result in spending more time",\
# "When do you prefer to study?":"When exams are around the corner by just focusing on the given syllabus",\
# "How do you prefer to study for your university examinations?":"I prefer detailed study of curriculum as well as the required background knowledge",\
# "Do you seriously perform college practical assignments and projects?":"Yes",\
# "Would you do a particular task seriously even if you are not interested?":"No",\
# "Would you put off a task if the deadline is not near":"Yes",\
# "If you don\u2019t understand a particular topic in the curriculum what do you prefer?":"Try again to understand the topic from multiple sources",\
# "Do you feel a need to revise a theoretical topic learnt 2 days before?":"Yes",\
# "How well do you think your GPA justifies your technical knowledge?":"is Apt or Overestimates my knowledge",\
# "How well do you think your GPA justifies the amount of efforts you put in?":"is Apt or Overestimates my efforts",\
# "If you had an idea for a technical project, would you:":"Delay the project and postpone it to some other time",\
# "If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?":"Yes",\
# "Are you proficient in the following? [Object Oriented Programming Concepts]":"Yes",\
# "Are you proficient in the following? [C\/C++]":"Yes",\
# "Are you proficient in the following? [JAVA]":"No",\
# "Are you proficient in the following? [Python]":"No",\
# "Provide your preference for the following methods of learning [Books\/Textual info on the Internet]":"Prefer",\
# "Provide your preference for the following methods of learning [Online courses\/videos]":"Prefer",\
# "Provide your preference for the following methods of learning [Personalised classroom teaching (human)]":"Prefer"}
# '''
#
#
# user_data_json2 = '[{"Timestamp":"2\/14\/2019 13:39:07","Email Address":"abizerL123@gmail.com","College Name?":"Pune Institute of Computer Technology","Current Branch?":"Computer Engineering","Current Year?":"Fourth Year","What is your Grade in College (GPA)?":9.4,"How would you rate your puzzle solving efficiency?":"High","Have you prepared for any olympiads\/national level competitive examinations in your school days?":"Not Participated","Have you actively participated in activities like chess or abacus etc?":"No","Have you been \"extensively\" involved in the following? [Competitive Coding]":"Yes","Have you been \"extensively\" involved in the following? [Sodtware Development]":"Yes","Have you been \"extensively\" involved in the following? [ML\/AI Projects or Research]":"No","Have you been \"extensively\" involved in the following? [Mathematics and Logical Reasoning]":"Yes","Have you been \"extensively\" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]":"Yes","Have you been \"extensively\" involved in the following? [Literature\/Blogging ]":"No","What are your plans after your undergraduation?":"Job in technical domain (Software Developer, Data Scientist etc.)","Are you attentive during lectures at college?":"Yes","Do you feel the lectures are slow paced or repetitive in general?":"No","Do you ask questions to the professor, if you do not understand a particular concept during the lecture?":"Yes - Almost every time","What do you do if you are not satisfied with the answer given by the professor? ":"I ask multiple questions until the topic is clarified.","What do you do if you are not satisfied with a topic in lecture?":"I leave the topic and look at during examinations","What is your study pattern in general?":"I learn a topic to understand the core fundamentals\/learn the topics outside the examination syllabus for better understanding","What would you prefer during exams to score good marks?":"Understanding the syllabus even if it would result in spending more time","When do you prefer to study?":"When exams are around the corner by just focusing on the given syllabus","How do you prefer to study for your university examinations?":"I prefer detailed study of curriculum as well as the required background knowledge","Do you seriously perform college practical assignments and projects?":"Yes","Would you do a particular task seriously even if you are not interested?":"No","Would you put off a task if the deadline is not near":"Yes","If you don\u2019t understand a particular topic in the curriculum what do you prefer?":"Try again to understand the topic from multiple sources","Do you feel a need to revise a theoretical topic learnt 2 days before?":"Yes","How well do you think your GPA justifies your technical knowledge?":"is Apt or Overestimates my knowledge","How well do you think your GPA justifies the amount of efforts you put in?":"is Apt or Overestimates my efforts","If you had an idea for a technical project, would you:":"Delay the project and postpone it to some other time","If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?":"Yes","Are you proficient in the following? [Object Oriented Programming Concepts]":"Yes","Are you proficient in the following? [C\/C++]":"Yes","Are you proficient in the following? [JAVA]":"No","Are you proficient in the following? [Python]":"No","Provide your preference for the following methods of learning [Books\/Textual info on the Internet]":"Prefer","Provide your preference for the following methods of learning [Online courses\/videos]":"Prefer","Provide your preference for the following methods of learning [Personalised classroom teaching (human)]":"Prefer"}]'
# # print("user_data_json: ", user_data_json)
#
# user_data_json3 = '{"email":"saurabhkshirsagar35@gmail.com"}'

def check_kmeans_cluster(user_data_json):
    # print("user_data_json: ", user_data_json)
    # json_user_obj = user_data_json.json()

    user_data_json = user_data_json.replace("\"extensively\"", "extensively")

    # user_data_json = json.dumps(user_data_json)
    print(user_data_json)


    # print("------------------------------")


    # json_user_obj = json.dumps(user_data_json)
    json_user_obj = json.loads(user_data_json)


    json_user_obj['Have you been "extensively" involved in the following? [ML/AI Projects or Research]'] = json_user_obj.pop('Have you been extensively involved in the following? [ML/AI Projects or Research]')
    json_user_obj['Have you been "extensively" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]'] = json_user_obj.pop('Have you been extensively involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]')
    json_user_obj['Have you been "extensively" involved in the following? [Literature/Blogging ]'] = json_user_obj.pop('Have you been extensively involved in the following? [Literature/Blogging ]')
    json_user_obj['Have you been "extensively" involved in the following? [Competitive Coding]'] = json_user_obj.pop('Have you been extensively involved in the following? [Competitive Coding]')
    json_user_obj['Have you been "extensively" involved in the following? [Mathematics and Logical Reasoning]'] = json_user_obj.pop('Have you been extensively involved in the following? [Mathematics and Logical Reasoning]')
    json_user_obj['Have you been "extensively" involved in the following? [Sodtware Development]'] = json_user_obj.pop('Have you been extensively involved in the following? [Sodtware Development]')

    # print(json_user_obj['Have you been "extensively" involved in the following? [Sodtware Development]'])

    # print(str(json_user_obj))


        # if(x == ("Have you been extensively involved in the following? [ML/AI Projects or Research]")):
        #     xtemp = x
        #     x['nickname'] = "Have you been extensively involved in the following? [ML/AI Projects or Research]"
        #     print("OLD: ", xtemp, " NEW: ", x)
        # if(x == ("Have you been extensively involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]")):
        #     xtemp = x
        #     x['nickname'] = "Have you been extensively involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]"
        #     print("OLD: ", xtemp, " NEW: ", x)
        # if(x == ("Have you been extensively involved in the following? [Literature/Blogging ]")):
        #     xtemp = x
        #     x['nickname'] = "Have you been extensively involved in the following? [Literature/Blogging ]"
        #     print("OLD: ", xtemp, " NEW: ", x)
        # if(x == ("Have you been extensively involved in the following? [Competitive Coding]")):
        #     xtemp = x
        #     x['nickname'] = "Have you been extensively involved in the following? [Competitive Coding]"
        #     print("OLD: ", xtemp, " NEW: ", x)
        # if(x == ("Have you been extensively involved in the following? [Mathematics and Logical Reasoning]")):
        #     xtemp = x
        #     x['nickname'] = "Have you been extensively involved in the following? [Mathematics and Logical Reasoning]"
        #     print("OLD: ", xtemp, " NEW: ", x)


    # print("type: ", type(json_user_obj) )
    user_dataframe = pd.DataFrame.from_records((json_user_obj), index=[0])
    # print(user_dataframe.head().T)
    # print(final_df.columns.values)
    # final_df.append(pd.Series(), ignore_index = True)
    print(final_df.shape)

    new_df = user_dataframe[col_list].copy()

    # for column in final_df:
    #     final_df.iloc[0,final_df.columns.get_loc(column)] = user_dataframe.iloc[0,user_dataframe.columns.get_loc(column)]


    print(new_df.head().T)
    return


check_kmeans_cluster(user_data_json)
