# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20190319221439) do

  create_table "clusters", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=latin1" do |t|
    t.string "description"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "student_attributes", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=latin1" do |t|
    t.bigint "user_id"
    t.float "aptitude", limit: 24
    t.float "indep_stud", limit: 24
    t.float "interest", limit: 24
    t.float "theory_knowledge", limit: 24
    t.float "prac_knowledge", limit: 24
    t.float "seriousness", limit: 24
    t.float "hardwork", limit: 24
    t.float "retention", limit: 24
    t.float "extra_curr", limit: 24
    t.string "attr_clusters"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "clusters_id"
    t.index ["clusters_id"], name: "index_student_attributes_on_clusters_id"
    t.index ["user_id"], name: "index_student_attributes_on_user_id"
  end

  create_table "users", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=latin1" do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.string "fname", null: false
    t.string "lname", null: false
    t.string "student_class"
    t.string "subject"
    t.date "dob", null: false
    t.integer "role", null: false
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  add_foreign_key "student_attributes", "clusters", column: "clusters_id", on_delete: :cascade
  add_foreign_key "student_attributes", "users", on_delete: :cascade
end
