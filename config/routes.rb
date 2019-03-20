Rails.application.routes.draw do
  devise_for :users, :controllers => { registrations: 'registrations' }
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root :to => redirect('/dashboard')

  get '/dashboard', to: 'home#dashboard'
  get '/init_test', to: 'home#init_test'
  post '/after_test', to: 'home#after_test'
  get '/dashboard/feedback', to: 'home#feedback'
  get '/dashboard/teacher', to: 'home#teacher'
end
