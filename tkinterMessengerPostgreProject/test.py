dict_1 = {1: {"value": 34}, 2: {"value": 1}, 3: {"value": 104}}

sorted_dict = dict(
    sorted(dict_1.items(), key=lambda item: item[1]['value']))

# print(sorted_dict)

for i in dict_1.items():
    print(i[1])