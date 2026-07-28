

from exercise4 import fidn_evenNumber_in_list, findOut_upper_lower_case, print_employee_info 

employees = [
    {
        "name": "Tina",
        "age": 30,
        "birthday": "1990-03-10",
        "job": "DevOps Engineer",
        "address": {
            "city": "New York",
            "country": "USA"
        }
    },
    {
        "name": "Tim",
        "age": 35,
        "birthday": "1985-02-21",
        "job": "Developer",
        "address": {
            "city": "Sydney",
            "country": "Australia"
        }
    },
    {
        "name": "Alice",
        "age": 28,
        "birthday": "1992-07-15",
        "job": "Backend Engineer",
        "address": {
            "city": "London",
            "country": "UK"
        }
    },
    {
        "name": "Bob",
        "age": 40,
        "birthday": "1980-11-05",
        "job": "Project Manager",
        "address": {
            "city": "Toronto",
            "country": "Canada"
        }
    },
    {
        "name": "Charlie",
        "age": 26,
        "birthday": "1994-01-20",
        "job": "Frontend Developer",
        "address": {
            "city": "Berlin",
            "country": "Germany"
        }
    },
    {
        "name": "David",
        "age": 32,
        "birthday": "1988-09-12",
        "job": "QA Engineer",
        "address": {
            "city": "Mumbai",
            "country": "India"
        }
    },
    {
        "name": "Emma",
        "age": 29,
        "birthday": "1991-06-18",
        "job": "Cloud Engineer",
        "address": {
            "city": "Singapore",
            "country": "Singapore"
        }
    },
    {
        "name": "Frank",
        "age": 37,
        "birthday": "1983-04-09",
        "job": "DevOps Engineer",
        "address": {
            "city": "Amsterdam",
            "country": "Netherlands"
        }
    },
    {
        "name": "Grace",
        "age": 31,
        "birthday": "1989-12-30",
        "job": "Data Engineer",
        "address": {
            "city": "Dublin",
            "country": "Ireland"
        }
    },
    {
        "name": "Henry",
        "age": 27,
        "birthday": "1993-08-14",
        "job": "Site Reliability Engineer",
        "address": {
            "city": "San Francisco",
            "country": "USA"
        }
    }
]

youngest_employee = print_employee_info(employees)
print(f"Youngest employee: {youngest_employee['name']}, Age: {youngest_employee['age']}")

upper_case_count, lower_case_count = findOut_upper_lower_case("Hello World!")
print(f"Upper case count: {upper_case_count}, Lower case count: {lower_case_count}")


even_numbers = fidn_evenNumber_in_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"Even numbers in the list: {even_numbers}")