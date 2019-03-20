class Addcascade < ActiveRecord::Migration[5.1]
  def change
    remove_foreign_key :student_attributes, :users
    add_foreign_key :student_attributes, :users, on_delete: :cascade
  end
end
