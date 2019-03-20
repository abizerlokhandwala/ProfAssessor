class RenameClassCol < ActiveRecord::Migration[5.1]
  def change
    rename_column :users, :class, :student_class
  end
end
