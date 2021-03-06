Rails.application.routes.draw do
  devise_for :users, :controllers => { registrations: 'registrations' }
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root :to => redirect('/dashboard')

  get '/dashboard', to: 'home#dashboard'
  get '/init_test', to: 'home#init_test'
  post '/after_test', to: 'home#after_test'
  get '/dashboard/feedback', to: 'home#feedback'
  get '/dashboard/teacher', to: 'home#teacher'
  get '/dashboard/all_group_details', to: 'home#all_group_details'
  get'/courses', to: 'home#courses'
  get'/java_course_analysis', to: 'home#java_course_analysis'
  get'/test_java', to: 'home#test_java'
  get'/java_results', to: 'home#java_results'
end
