import copy
import os

KEY_LIST = 'KeyList.txt'
DIR_LIST = 'DirList.txt'


class Index:
    def __init__(self):
        self.dirs = self.first_add_dir()
        self.files = self.get_files()
        self.keys = self.first_add_key()
        self.dict = self.get_indexs()

    def DirecoryExists(self, dir):
        return os.path.isdir(dir)

    def first_add_key(self):
        try:
            with open(KEY_LIST, "r", encoding='UTF-8') as file:
                x = file.read()
        except Exception:
            with open(KEY_LIST, 'w', encoding='utf-8') as f:
                f.write('')
            return []
        if x == '':
            return []
        x = x.split('\n')
        return x

    # +ключ
    def add_key(self, key):
        if len(str(key)) != 1:
            return "FALSE! THIS STR IS NOT A CHAR!!!"
        with open(KEY_LIST, 'a+', encoding='utf-8') as file:
            if self.keys != []:
                file.write('\n')
            file.write(str(key).upper())
            self.KeyListExsist = True
            file.close()
        self.keys.append(key.upper)
        return self.keys

    # -ключ
    def delete_key(self, key):
        with open(KEY_LIST, "r", encoding='utf-8') as f:
            helper_bool = True
            for elem in self.keys:
                if elem != key:
                    helper_bool = False
            if helper_bool:
                self.keys = []
                d = ''
            else:
                d = f.read()
                d = d.replace((str(key) + '\n'), '')
                d = d.replace('\n' + str(key), '')
                self.keys = d.split('\n')
            with open(KEY_LIST, 'w', encoding='utf-8') as file:
                file.write(d)
        return self.keys

    def first_add_dir(self):
        try:
            with open(DIR_LIST, 'r', encoding='UTF-8') as file:
                x = file.read()
        except Exception:
            with open(DIR_LIST, 'w', encoding='utf-8') as f:
                f.write('')
            return []
        if x == '':
            return []
        x = x.split('\n')
        return x

        # добавить папку

    def add_dir(self, dir):
        if self.DirecoryExists(dir):
            with open(DIR_LIST, 'a+', encoding='utf-8') as file:
                if self.dirs != []:
                    file.write('\n')
                file.write(str(dir))
                file.close()
            self.dirs.append(dir)
        return self.dirs

        # удалить папку

    def delete_dir(self, dir):
        with open(DIR_LIST, 'r', encoding='utf-8') as f:
            helper_bool = True
            for elem in self.dirs:
                if elem != dir:
                    helper_bool = False
            if helper_bool:
                self.dirs = []
                d = ''
            else:
                d = f.read()
                d = d.replace((str(dir) + '\n'), '')
                d = d.replace('\n' + str(dir), '')
                self.dirs = d.split('\n')
            with open(DIR_LIST, 'w', encoding='utf-8') as file:
                file.write(d)
        return self.dirs

    # возвращает именя файлов
    def get_files(self):
        dirs = self.dirs
        files = []
        for dir in dirs:
            dir = [os.path.join(dir, _) for _ in os.listdir(dir) if _.endswith(r'.txt')]
            for file in dir:
                files.append(file)
        self.files = files
        return self.files

    def create_index(self, key):
        array_of_index = {}
        for elem in self.files:
            helper_array = []
            f = open(elem, encoding='utf-8')
            x = f.read().lower().title()
            founder = x.find(key)
            while founder >= 0:
                helper_array.append(founder)
                founder = x.find(key, founder + 1)
            if bool(helper_array):
                array_of_index[elem] = helper_array
        return array_of_index

    def get_indexs(self):
        dict_dir_with_index = {}
        for key in self.keys:
            dict_dir_with_index[key] = {}
            dict_of_index = self.create_index(key)
            dict_dir_with_index[key].update(dict_of_index)
        return dict_dir_with_index

    def get_index_first(self, key, name):
        not_alph = ['\\', '!', '№', ';', '%', ':', '?', '*', '(', ')', '_', '-', '+', '=', '<', '>', '?', ',', '.', '/',
                    '#', '|', '\ ', '~', '\'', '\"', '\n', '\t', '', ' ']
        x = self.get_file(name=name) + "____"
        i = 1
        while not x[self.dict[key][name][0] + i] in not_alph:
            i += 1
        return self.dict[key][name][0], self.dict[key][name][0] + i

    def get_file(self, name):
        with open(name, 'r', encoding='UTF-8') as file:
            return file.read()

    def dict_string(self, dict, isname=False):
        helper_string = ''
        sum_len = 0
        helper_bool = True
        for key_1, key_2 in dict.items():
            helper_string += str(key_1) + '\n'
            for key_2, value in dict[key_1].items():
                if helper_bool:
                    helper_string += str(key_2) + '\n'
                    if isname:
                        helper_bool = False
                helper_string += str(value) + '\n'
                sum_len += len(value)
                helper_string += 'Количество найденных вхожений - ' + str(len(value)) + '\n'
            helper_string += 'Сумма вхождений по ключу - ' + str(sum_len) + '\n\n'
            sum_len = 0
        return helper_string

    def get_statistic(self, key=False, name=False, dir=False):
        helper_dict = copy.deepcopy(self.dict)
        names_array = []
        if name and dir:
            return 'ERROR', list(name)

        if not key and not name and not dir:
            return self.dict_string(self.dict), list(self.files)
        if not name and key in self.keys and not dir:
            for key_1 in list(self.dict):
                if key_1 != key:
                    helper_dict.pop(key_1)
                else:
                    for key in list(self.dict[key_1]):
                        names_array.append(key)
            return self.dict_string(helper_dict), names_array

        if not key and name in self.files:
            for key_1 in list(self.dict):
                for key_2 in list(self.dict[key_1]):
                    if key_2 != name:
                        helper_dict[key_1].pop(key_2)
            return self.dict_string(self.dict, isname=True), list(name)

        if key in self.keys and not name and not dir:
            for key_1 in list(self.dict):
                if key_1 != key:
                    helper_dict[key_1].pop(key_1)
                else:
                    for key in list(self.dict[key_1]):
                        names_array.append(key)
            return self.dict_string(helper_dict), names_array

        if key in self.keys and (name in self.files):
            return str(key) + '\n' + str(name) + '\n' + str(self.dict[key][name]), list(name)

        if dir in self.dirs and key in self.keys:
            for key_1 in list(self.dict):
                for key_2 in list(self.dict[key_1]):
                    if key_2[0: len(dir)] != dir:
                        helper_dict[key_1].pop(key_2)
            for key_1 in list(self.dict):
                if key_1 != key:
                    helper_dict.pop(key_1)
                else:
                    for key in list(self.dict[key_1]):
                        names_array.append(key)
            return self.dict_string(helper_dict), names_array

        if dir in self.dirs and not key:
            for key_1 in list(self.dict):
                for key_2 in list(self.dict[key_1]):
                    if key_2[0: len(dir)] != dir:
                        helper_dict[key_1].pop(key_2)
                    else:
                        names_array.append(key_2)
            return self.dict_string(helper_dict), names_array

        return '\n' + 'FALSE!!!' + '\n', []