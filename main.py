import PySimpleGUI as sg
import Index as inx

HEAD = 'Курсовая работа по Технологии Обработки Информации. Вариант №39'
INFO = '2022 © _ _'


# окно для добавления ключевого слова
def win_add_key():
    layout = [
        [
            sg.Text('Новое ключевое слово'),
            sg.In(size=(20, 1), key='-NEW_KEY_WORD-'),
            sg.Button('Сохранить', size=(10, 1), key='-SAVE_KEY-'),
            sg.Button('Отмена', size=(10, 1), key='-CANCEL-')
        ]
    ]
    window_add = sg.Window('Добавить ключевое слово', layout)
    input_text = window_add['-NEW_KEY_WORD-']
    while True:
        event_add, value_add = window_add.read()
        if event_add == '-CANCEL-' or event_add == sg.WIN_CLOSED:
            break
        if event_add == '-SAVE_KEY-':
            if value_add['-NEW_KEY_WORD-'] == '' or len(value_add['-NEW_KEY_WORD-']) > 1:
                win_error()
            elif value_add['-NEW_KEY_WORD-'] in inx.Index().keys:
                win_warning('Такой ключ уже существует!')
                input_text.update('')
            else:  # ДОБАВЛЕНИЕ КЛЮЧА
                inx.Index().add_key(value_add['-NEW_KEY_WORD-'])
                window['-KEY_LIST-'].update(inx.Index().keys)
                window['-KEY_LISTBOX-'].update(values=[key for key in inx.Index().keys])
                input_text.update('')
    window_add.close()


# окно для удаления ключевого слова
def win_delete_key():
    keys = inx.Index().keys
    if keys == []:
        win_warning('Список ключевых символов пуст!')
    else:
        layout = [
            [
                sg.Text('Удаление ключевого слова'),
                sg.InputCombo(values=[key for key in keys], size=(20, 1), readonly=True,
                              key='-DELETE_KEY_WORD-'),
                sg.Button('Удалить', size=(10, 1), key='-DELETE_KEY-'),
                sg.Button('Отмена', size=(10, 1), key='-CANCEL-')
            ]
        ]
        window_del = sg.Window('Удалить ключевое слово', layout)
        input_text = window_del['-DELETE_KEY_WORD-']
        while True:
            event_del, value_del = window_del.read()
            if event_del == '-CANCEL-' or event_del == sg.WIN_CLOSED:
                break
            if event_del == '-DELETE_KEY-':  # УДАЛЕНИЕ КЛЮЧА
                if value_del['-DELETE_KEY_WORD-'] == '':
                    win_error()
                else:
                    inx.Index().delete_key(value_del['-DELETE_KEY_WORD-'])
                    window['-KEY_LIST-'].update(inx.Index().keys)
                    window['-KEY_LISTBOX-'].update(values=[key for key in inx.Index().keys])
                    window_del['-DELETE_KEY_WORD-'].update(values=[key for key in inx.Index().keys])
                    input_text.update('')

        window_del.close()


# добавление папки в список
def add_folder():
    new_folder = value['-FOLDER-']
    if not inx.Index().DirecoryExists(new_folder):
        win_error()
    else:
        folders = inx.Index().dirs
        if new_folder in folders:
            win_warning('Такая папка уже существует!')
            window['-FOLDER-'].update('')
        else:
            inx.Index().add_dir(new_folder)
            window['-FOLDER_LIST-'].update(inx.Index().dirs)
            window['-FOLDER-'].update('')


# удаление папки из списка
def delete_folder():
    delete_folder = value['-FOLDER-']
    if not inx.Index().DirecoryExists(delete_folder):
        win_error()
    else:
        folders = inx.Index().dirs
        if not (delete_folder in folders):
            win_warning('Такой папки нет в списке!')
            window['-FOLDER-'].update('')
        else:
            inx.Index().delete_dir(delete_folder)
            window['-FOLDER_LIST-'].update(inx.Index().dirs)
            window['-FOLDER-'].update('')


def win_file():
    index_ = inx.Index()
    key = value['-KEY_LISTBOX-']
    file = value['-FILE_LIST_COMBO-']
    if file == '':
        win_error()
    else:
        text = ''
        for line in index_.get_file(file).split('\n'):
            text += line + '\n'
        index_key = index_.get_index_first(key, file)
        text = text[:index_key[0]] + '☞' + text[index_key[0]:index_key[1]].upper() + '☚' + text[index_key[1]:]
        layout = [
            [sg.Text(text, size=(100, 20), background_color='white', key='-TEXT-')],
            [sg.OK(auto_size_button=True, key='-OK-')]
        ]
        frame = [[sg.Frame(file, layout, element_justification='center', title_location='n')]]
        window_file = sg.Window('Просмотр файла', frame)

        while True:
            event_file, value_file = window_file.read()
            if event_file == sg.WIN_CLOSED or event_file == '-OK-':
                break
        window_file.close()


# вывод сообщения об ошибке
def win_error():
    layout = [
        [sg.Text('Что-то пошло не так...')],
        [sg.Button('OK', size=(10, 1), key='-OK-')]
    ]
    frame = [[sg.Frame('Упс...Ошибка!', layout, element_justification='center', title_location='n')]]
    window = sg.Window('', frame, size=(180, 100))
    while True:
        event, values = window.read()
        if event == '-OK-' or event == sg.WIN_CLOSED:
            break
    window.close()


# вывод предупреждающего сообщения
def win_warning(message):
    layout = [
        [sg.Text(message, size=(25, 4), justification='center')],
        [sg.Button('OK', size=(10, 1), key='-OK-')]
    ]
    frame = [[sg.Frame('!!!', layout, element_justification='center', title_location='n')]]
    window = sg.Window('Предупреждение!', frame, size=(250, 150))
    while True:
        event, values = window.read()
        if event == '-OK-' or event == sg.WIN_CLOSED:
            break
    window.close()


# вывод списка файлов в ListBox
def update_list_files(list_files):
    window['-LIST_FILES-'].update(file for file in list_files)


# вывод статистики
def statistic(check):
    key = value['-KEY_LISTBOX-']
    output = window['-STATISTIC-']
    file_list = window['-FILE_LIST_COMBO-']
    keys = inx.Index().keys
    # если индекс сформирован
    if check:
        if keys == []:
            win_warning('Список ключевых символов пуст!')
        else:
            # с ключом
            statistic = inx.Index().get_statistic(key=key)
            output.update([elem for elem in statistic[0].split('\n')])
            file_list.update(values=[name_file for name_file in statistic[1]])
    else:
        win_error()


# формирование индекса
def create_index():
    index_ = inx.Index()
    keys = index_.keys
    dirs = index_.dirs
    if keys == []:
        win_warning('Список ключевых символов пуст!')
        return False
    if dirs == []:
        win_warning('Список папок пуст!')
        return False
    else:
        global dict_index
        dict_index = inx.Index().dict
        window['-STATISTIC-'].update(values=['Индекс успешно сформирован!'])
        return True


def list_col_1():
    folders = inx.Index().dirs
    list_column = [
        [sg.Listbox(values=[folder for folder in folders], size=(35, 5), horizontal_scroll=True,
                    key='-FOLDER_LIST-')],
        [sg.Text('Введите путь к папке:')],
        [
            sg.InputText(size=(25, 1), enable_events=True, key='-FOLDER-'),
            sg.FolderBrowse()
        ],
        [
            sg.Button('Добавить', size=(15, 1), key='-ADD_FOLDER-'),
            sg.Button('Удалить', size=(15, 1), key='-DELETE_FOLDER-')
        ],
        [sg.Button('Показать файлы', size=(35, 1), key='-SHOW_LIST_FILES-')]
    ]
    return list_column


def list_col_2():
    list_column = [
        [sg.Listbox(values=[key for key in inx.Index().keys], size=(30, 10), key='-KEY_LIST-')],
        [
            sg.Button('Добавить', size=(10, 1), key='-ADD_KEY-'),
            sg.Button('Удалить', size=(10, 1), key='-DELETE_KEY-')
        ],
        [sg.Button('Сформировать индекс', size=(35, 1), key='-CREATE_INDEX-')],
    ]
    return list_column


def view_column_1():
    view_column = [
        [sg.Listbox(values=[file for file in index_.files], size=(55, 25), horizontal_scroll=True, key='-LIST_FILES-')]
    ]
    return view_column


def view_column_2():
    view_column = [
        [
            sg.Text('Ключевое слово'),
            sg.InputCombo(values=[key for key in inx.Index().keys], readonly=True, size=(20, 5),
                          key='-KEY_LISTBOX-'),
            sg.Button('Поиск', size=(10, 1), key='-FIND-')
        ],
        [sg.Listbox(values=[], size=(55, 17), horizontal_scroll=True, key='-STATISTIC-')],
        [
            sg.InputCombo(values=[], readonly=True, size=(32, 5), key='-FILE_LIST_COMBO-'),
            sg.Button('Показать файл', size=(13, 1), key='-SHOW_FILE-')
        ]
    ]
    return view_column


def tab_1():
    tab_select_folder = [
        [
            sg.Frame('Выбор папок', list_col_1(), vertical_alignment='top', size=(250, 400)),
            sg.Frame('Список файлов в папках', view_column_1(), vertical_alignment='top', size=(400, 400))
        ]
    ]
    return tab_select_folder


def tab_2():
    tab_index = [
        [
            sg.Frame('Выбор ключевого слова', list_col_2(), vertical_alignment='top', size=(200, 400)),
            sg.Frame('Поиск выбранного ключевого слова', view_column_2(), vertical_alignment='top', size=(400, 400))
        ],
    ]
    return tab_index


index_ = inx.Index()
check_create_index = False

if __name__ == '__main__':
    sg.theme('BluePurple')

    layout = [
        [
            sg.TabGroup(
                [[
                    sg.Tab('Файлы и папки', tab_1()),
                    sg.Tab('Индекс и Поиск', tab_2())
                ]],
                tab_location='topleft', size=(600, 400))
        ],
        [
            sg.Button('Выход', size=(10, 1), key='-EXIT-'),
            sg.Text(INFO, pad=(130, 0), auto_size_text=True)
        ]
    ]

    window = sg.Window(HEAD, layout)
    dict_index = {}
    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        if event == '-SHOW_LIST_FILES-':
            update_list_files(inx.Index().files)
        if event == '-ADD_FOLDER-':
            add_folder()
            check_create_index = False
        if event == '-DELETE_FOLDER-':
            delete_folder()
            check_create_index = False
        if event == '-ADD_KEY-':
            win_add_key()
            check_create_index = False
        if event == '-DELETE_KEY-':
            win_delete_key()
            check_create_index = False
        if event == '-FIND-':
            statistic(check_create_index)
        if event == '-CREATE_INDEX-':
            check_create_index = create_index()
        if event == '-SHOW_FILE-':
            win_file()
    window.close()
