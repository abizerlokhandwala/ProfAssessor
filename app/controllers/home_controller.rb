class HomeController < ApplicationController
  before_action :authenticate_user!

  def dashboard
    if current_user.role.to_i==0 then #if student
      @name = current_user.fname+" "+current_user.lname
      @email = current_user.email
      @student_class = current_user.student_class
      @attr_val = current_user.student_attribute.get_all_attribute_score_std
      @comments = current_user.student_attribute.get_comments
    else  #else teacher
      @name = current_user.fname+" "+current_user.lname
      @email = current_user.email
      @subject = current_user.subject
      @cluster_details = Cluster.all
    end
  end

  def init_test
    if current_user.role.to_i==0 then
      @arr_questions = ["College Name?","Current Branch?","Current Year?","What is your Grade in College (GPA)?","How would you rate your puzzle solving efficiency?","Have you prepared for any olympiads/national level competitive examinations in your school days?","Have you actively participated in activities like chess or abacus etc?","Have you been \"extensively\" involved in the following? [Competitive Coding]","Have you been \"extensively\" involved in the following? [Sodtware Development]","Have you been \"extensively\" involved in the following? [ML/AI Projects or Research]","Have you been \"extensively\" involved in the following? [Mathematics and Logical Reasoning]","Have you been \"extensively\" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]","Have you been \"extensively\" involved in the following? [Literature/Blogging ]","What are your plans after your undergraduation?","Are you attentive during lectures at college?","Do you feel the lectures are slow paced or repetitive in general?","Do you ask questions to the professor, if you do not understand a particular concept during the lecture?","What do you do if you are not satisfied with the answer given by the professor? ","What do you do if you are not satisfied with a topic in lecture?","What is your study pattern in general?","What would you prefer during exams to score good marks?","When do you prefer to study?","How do you prefer to study for your university examinations?","Do you seriously perform college practical assignments and projects?","Would you do a particular task seriously even if you are not interested?","Would you put off a task if the deadline is not near","If you don’t understand a particular topic in the curriculum what do you prefer?","Do you feel a need to revise a theoretical topic learnt 2 days before?","How well do you think your GPA justifies your technical knowledge?","How well do you think your GPA justifies the amount of efforts you put in?","If you had an idea for a technical project, would you:","If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?","Are you proficient in the following? [Object Oriented Programming Concepts]","Are you proficient in the following? [C/C++]","Are you proficient in the following? [JAVA]","Are you proficient in the following? [Python]","Provide your preference for the following methods of learning [Books/Textual info on the Internet]","Provide your preference for the following methods of learning [Online courses/videos]","Provide your preference for the following methods of learning [Personalised classroom teaching (human)]"]

      render 'init_test'
    else
      redirect_to '/dashboard'
    end
  end

  def after_test
    @arr_questions = ["College Name?","Current Branch?","Current Year?","What is your Grade in College (GPA)?","How would you rate your puzzle solving efficiency?","Have you prepared for any olympiads/national level competitive examinations in your school days?","Have you actively participated in activities like chess or abacus etc?","Have you been \"extensively\" involved in the following? [Competitive Coding]","Have you been \"extensively\" involved in the following? [Sodtware Development]","Have you been \"extensively\" involved in the following? [ML/AI Projects or Research]","Have you been \"extensively\" involved in the following? [Mathematics and Logical Reasoning]","Have you been \"extensively\" involved in the following? [Social Activities (College Fest Organization or similar managerial or club activities)]","Have you been \"extensively\" involved in the following? [Literature/Blogging ]","What are your plans after your undergraduation?","Are you attentive during lectures at college?","Do you feel the lectures are slow paced or repetitive in general?","Do you ask questions to the professor, if you do not understand a particular concept during the lecture?","What do you do if you are not satisfied with the answer given by the professor? ","What do you do if you are not satisfied with a topic in lecture?","What is your study pattern in general?","What would you prefer during exams to score good marks?","When do you prefer to study?","How do you prefer to study for your university examinations?","Do you seriously perform college practical assignments and projects?","Would you do a particular task seriously even if you are not interested?","Would you put off a task if the deadline is not near","If you don’t understand a particular topic in the curriculum what do you prefer?","Do you feel a need to revise a theoretical topic learnt 2 days before?","How well do you think your GPA justifies your technical knowledge?","How well do you think your GPA justifies the amount of efforts you put in?","If you had an idea for a technical project, would you:","If you had an exam tomorrow, of a subject not of your interest, would you study hard to maintain a good score?","Are you proficient in the following? [Object Oriented Programming Concepts]","Are you proficient in the following? [C/C++]","Are you proficient in the following? [JAVA]","Are you proficient in the following? [Python]","Provide your preference for the following methods of learning [Books/Textual info on the Internet]","Provide your preference for the following methods of learning [Online courses/videos]","Provide your preference for the following methods of learning [Personalised classroom teaching (human)]"]

    send_data = Hash.new
    send_data["Timestamp"] = "132/64/79"
    send_data["Email Address"] = current_user.email
    for i in 0...39 do
      if i==3 then
        send_data[@arr_questions[i]] = params[:init_test]["Q"+i.to_s].to_f
      else send_data[@arr_questions[i]] = params[:init_test]["Q"+i.to_s].to_s
      end
    end
    result = (`python3 lib/assets/final_codes/cluster_user.py #{"'"+send_data.to_json+"'"}`)
    result = JSON.parse(result)
    StudentAttribute.student_after_clustering(result,current_user.id)
    redirect_to '/dashboard'
  end

  def feedback
    respond_to do |format|
      format.html
      format.js
    end
  end

  def teacher
    student_class = params[:student_class]
    @data = StudentAttribute.get_pie_data(student_class)
    render :js => "pie_chart_func(#{@data.to_json});"
  end

end
