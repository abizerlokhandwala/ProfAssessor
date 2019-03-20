class CreateStudentAttributes < ActiveRecord::Migration[5.1]
  def change
    create_table :student_attributes do |t|
      t.references :user, foreign_key: { on_delete: :cascade }
      t.float :aptitude
      t.float :indep_stud
      t.float :interest
      t.float :theory_knowledge
      t.float :prac_knowledge
      t.float :seriousness
      t.float :hardwork
      t.float :retention
      t.float :extra_curr
      t.string :attr_clusters
      t.timestamps
    end
  end
end
