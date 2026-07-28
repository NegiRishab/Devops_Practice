from datetime import datetime,timedelta

now= datetime.now()

birthday=input("please enter your date of birth in dd/mm/yyyy format")

birthday=datetime.strptime("15-12-2000", "%d-%m-%Y")

difference= now - birthday

days = difference.days

print(days)
