# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

def rand_name
  (0...rand(5..8)).map{ (65 + rand(26)).chr }.join
end

def get_3_rand
  num = 1.0
  fi = rand(0.0..0.9)
  se = num-fi
  te = se/2
  se = se/2
  return "[#{fi.round(2)},#{se.round(2)},#{te.round(2)}]"
end

def get_3_fin
  fin=""
  for i in (0...9)
    fin+=get_3_rand
    fin+=","
  end
  fin=fin[0...-1]
  fin+=""
  return fin
end

# for i in (0...10)
#   # p rand_name*3
#   User.create!(email: rand_name+"@"+rand_name+".com", password: rand_name*3, fname: rand_name, lname: rand_name, student_class: "BE1", dob: "2000-10-10", role: 0).save
# end

# for i in (0...10)
#   # p get_3_fin
#   StudentAttribute.create!(user_id: i+1, aptitude: rand(1.0..50.0), indep_stud: rand(1.0..50.0), interest: rand(1.0..50.0), theory_knowledge: rand(1.0..50.0), prac_knowledge: rand(1.0..50.0), seriousness: rand(1.0..50.0), hardwork: rand(1.0..50.0), retention: rand(1.0..50.0), extra_curr: rand(1.0..50.0), attr_clusters: get_3_fin).save
# end

# for i in (0..5)
#   Cluster.create(:description => rand_name).save
# end

# for i in (1..11)
#   lol = StudentAttribute.find(i)
#   lol.cluster_id = rand(1..5)
#   lol.save
# end

all_users = `python3 lib/assets/final_codes/cluster_user_all.py`
all_users_array = all_users.split("#")
cnt = 1
for i in all_users_array
  lol = JSON.parse(i)
  attributes = JSON.parse(lol["student_attribute_levels"])
  # puts attributes[0]
  User.create!(id: cnt,email: lol["email"].to_s, password: "pict123", fname: lol["email"].split("@")[0], lname: rand_name, student_class: "BE"+rand(1..3).to_s, dob: "2000-10-10", role: 0).save
  StudentAttribute.create!(user_id: cnt, aptitude: attributes[0], indep_stud: attributes[1], interest: attributes[2], theory_knowledge: attributes[3], prac_knowledge: attributes[4], seriousness: attributes[5], hardwork: attributes[6], retention: attributes[7], extra_curr: attributes[8], attr_clusters: "123", cluster_id: 1+lol["student_final_cluster"].to_i).save
  cnt+=1
end
