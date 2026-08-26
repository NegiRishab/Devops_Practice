employee = {
  "name": "Tim",
  "age": 30,
  "birthday": "1990-03-10",
  "job": "DevOps Engineer"
}

employee["job"] = " Software Engineer"
del employee["age"]

for key, value in employee.items():
   print(f"{key}: {value}")


dict_one = {'a': 100, 'b': 400} 
dict_two = {'x': 300, 'y': 200}  

dict_combined = {**dict_one, **dict_two}

max_value=0
min_value=0
total_value=0

for key, value in dict_combined.items():
    total_value += value
    if value > max_value:
        max_value = value
    if value < min_value or min_value == 0:
        min_value = value

print(f"Max value: {max_value}")
print(f"Min value: {min_value}")
print(f"Total value: {total_value}")
