my_list = [1, 2, 2, 4, 4, 5, 6, 8, 10, 13, 22, 35, 52, 83]

def find_number_of_list_greater_than(my_list, threshold):
     ans_list = []
     for i in my_list:
            if i > threshold:
                ans_list.append(i)
     return ans_list


print(find_number_of_list_greater_than(my_list, 50))

