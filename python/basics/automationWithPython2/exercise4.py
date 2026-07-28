

def print_employee_info(employees):
    youngest_employee = employees[0]
    for employee in employees:
        if employee['age'] < youngest_employee['age']:
            youngest_employee = employee
    return youngest_employee


def findOut_upper_lower_case(string):
    upper_case_count = 0
    lower_case_count = 0
    for char in string:
        if char.isupper():
            upper_case_count += 1
        elif char.islower():
            lower_case_count += 1
    return upper_case_count, lower_case_count


def fidn_evenNumber_in_list(my_list):
    even_numbers = []
    for i in my_list:
        if i % 2 == 0:
            even_numbers.append(i)
    return even_numbers