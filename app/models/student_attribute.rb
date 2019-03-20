class StudentAttribute < ApplicationRecord
  belongs_to :user
  belongs_to :cluster

  @@arr = ["aptitude", "indep_stud", "interest", "theory_knowledge", "prac_knowledge", "seriousness", "hardwork", "retention", "extra_curr"]

  def get_attribute_score(index)
    StudentAttribute.find(self.id)[@@arr[index]]
  end

  def self.get_attribute_score_max(index)
    StudentAttribute.maximum(@@arr[index])
  end

  def self.get_attribute_score_min(index)
    StudentAttribute.minimum(@@arr[index])
  end

  def get_all_attribute_score_std
    my_score_std = []
    for i in (0...@@arr.size)
      my_score = get_attribute_score(i)
      max_score = StudentAttribute.get_attribute_score_max(i)
      my_score = (my_score) / (max_score)
      my_score_std << my_score
    end
    my_score_std
  end

  def get_students_greater(index)
    users_class_id = User.where("student_class = ?", self.user.student_class).pluck(:id)
    StudentAttribute.where("user_id in (?) and #{@@arr[index]} > ?",users_class_id ,self[@@arr[index]]).count
  end

  def get_students_greater_2(index1, index2)
    users_class_id = User.where("student_class = ?", self.user.student_class).pluck(:id)
    StudentAttribute.where("user_id in (?) and (#{@@arr[index1]}+#{@@arr[index2]}) > ?",users_class_id ,self[@@arr[index1]]+self[@@arr[index2]]).count
  end

  def get_comments
    comments = []
    apti = get_students_greater(0)
    indep = get_students_greater(1)
    hardwork = get_students_greater(6)
    combined_knowledge = get_students_greater_2(3,4)
    extra_curr = get_students_greater(8)

    users_class_id = User.where("student_class = ?", self.user.student_class).pluck(:id)
    total = StudentAttribute.where("user_id in (?)",users_class_id).count

    if apti<total/2 then
      comments << "You're Aptitude is better than #{100*(total-apti)/total}% of your class! Keep it up!"
    else
      comments << "#{100*apti/total}% of your class has better Aptitude than you, work on it!"
    end

    if hardwork<total/2 then
      comments << "You're more hardworking than #{100*(total-hardwork)/total}% of your class! Keep it up!"
    else
      comments << "#{100*hardwork/total}% of the class puts in more hardwork than you do, work on it!"
    end

    if indep<total/2 then
      if combined_knowledge<total/2 then
        comments << "You're Technical Knowledge is greater than #{100*(total-combined_knowledge)/total}% of your class! Don't stop now though, keep the hardwork consistent to keep the lead!"
      else
        comments << "#{100*combined_knowledge/total}% of your class is technically smarter than you, but you can bridge that gap by consistently working towards your goal, dont give up!"
      end
    else
      if combined_knowledge<total/2 then
        comments << "You're Technical Knowledge is greater than #{100*(total-combined_knowledge)/total}% of your class, but you can do even better if you start to consistently study and take efforts on your own, you can be the best!"
      else
        comments << "#{100*combined_knowledge/total}% of your class studies more than you, and hence score better. You can be one of them too, bridge that gap by consistently working towards your goal, dont give up!"
      end
    end

    if extra_curr<total/2 then
      comments << "You're part of the top #{100*(extra_curr)/total}% of your class who are into extra curricular activities! Keep it up!"
    else
      comments << "#{100*extra_curr/total}% of your class is into activities apart from class studies, all work no play makes jack a dull boy!"
    end

    comments
  end

  def self.get_pie_data(student_class)
    users_class_id = User.where("student_class = ?", student_class).pluck(:id)
    all_students = StudentAttribute.where("user_id in (?)",users_class_id)
    data = Array.new
    for i in (1..Cluster.all.count)
      temp = Hash.new
      temp["label"] = "Cluster "+i.to_s
      temp["count"] = all_students.where("clusters_id = ?", i).count
      data << temp
    end
    data
  end

end
