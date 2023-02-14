from pprint import pprint
import csv
import re


with open('data/phonebook_raw.csv', 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

def change_data(el):
    data = ','.join(el)
    if el[0].count(' ') == 1:
        pattern_fio = r'^(\w*).(\w*).(\w*)\,{2}'
    else:
        pattern_fio = r'^(\w*).(\w*).(\w*)\,{2,3}'
    pattern_num = r'(\+7|8)\s?\(?(\d{3})\)?.?(\d{3}).?(\d{2}).?(\d{2})'
    repl_fio = r'\1,\2,\3,'
    repl_num = r'+7(\2)\3-\4-\5'
    res = re.sub(pattern_fio, repl_fio, data)
    resalt = re.sub(pattern_num, repl_num, res)
    pattern_dop = r'\(?доб\.\s?(\d*)\)?'
    repl_dop = r'доб.\1'
    search = re.search(pattern_dop, resalt)
    if search is not None:
        resalt = re.sub(pattern_dop, repl_dop, resalt)
    return resalt.split(',')

def merge_of_records(resalt, n_contacts_list):
    for el_n in n_contacts_list:
        if resalt[0:2] == el_n[0:2]:
            index = n_contacts_list.index(el_n)
            new_resalt = []
            merge_list = list(zip(resalt, el_n))
            for el in merge_list:
                if el[0] == el[1]:
                    new_resalt.append(el[0])
                elif el[0] == '':
                    new_resalt.append(el[1])
                else:
                    new_resalt.append(el[0])
            n_contacts_list.pop(index)
            n_contacts_list.insert(index, new_resalt)
    

def create_phonebook():
    n_contacts_list = []
    info = []
    for el in contacts_list:
        resalt = change_data(el)

        if tuple(resalt[0:2]) not in info:
            n_contacts_list.append(resalt)
        else:
            merge_of_records(resalt, n_contacts_list)

        info.append(tuple(resalt[0:2]))
    return n_contacts_list

if __name__ == '__main__':
    with open("data/phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(create_phonebook())