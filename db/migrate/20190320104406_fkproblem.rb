class Fkproblem < ActiveRecord::Migration[5.1]
  def change
    add_foreign_key :student_attribute, :cluster, on_delete: :cascade
  end
end
