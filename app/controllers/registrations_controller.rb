class RegistrationsController < Devise::RegistrationsController

  private

  def sign_up_params
    params.require(:user).permit(:fname, :lname, :email, :password, :password_confirmation, :student_class, :role, :subject, :class, :dob)
  end

  def after_sign_up_path_for(resource)
      '/init_test' # Or :prefix_to_your_route
  end

end
