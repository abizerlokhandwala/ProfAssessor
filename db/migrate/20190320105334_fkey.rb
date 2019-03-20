class Fkey < ActiveRecord::Migration[5.1]
  def change
    # add_reference :student_attributes, :cluster, index: true
    add_foreign_key :student_attributes, :clusters, foreign_key: {on_delete: :cascade}
  end
end
