class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  @@arr = ["aptitude", "indep_stud", "interest", "theory_knowledge", "prac_knowledge", "seriousness", "hardwork", "retention", "extra_curr"]
end
