def nested_lists_maker(nested_lists_len: int, original_list: list):
    new_list = []
    final_sub_list = []
    if len(original_list) > nested_lists_len:
        while len(original_list) >= nested_lists_len:
            sub_list = original_list[:nested_lists_len]
            for i in sub_list:
                original_list.remove(i)
            new_list.append(sub_list)
        if len(original_list) != 0:
            for j in original_list:
                final_sub_list.append(j)
            new_list.append(final_sub_list)
        return new_list
    else:
        return original_list

print(nested_lists_maker(3, ["a", "c", "fv", "fegd", "flek", "fwf", "bgbb", "ffw", "w[ww[w"]))
