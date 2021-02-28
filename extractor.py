from classes import Person, WorkSession
import datetime
import time
from re import search
import xlrd

__author__ = "Anders Rubach Ese"
__version__ = "2.1.0"
__email__ = "aes014@uit.no"


def print_msg(msg):
    print(f'  ->{msg}')


def get_person_object_from_excel(owner='N/A', path='test.xlsm', start_week=4, end_week=4):
    """
    Returns List of Work objects containing data from all work between start- and end-week
    """
    from utils.utils_time import xldate_as_datetime
    sheet_prefix = 'Uke'

    person = Person(owner, [], start_week, end_week)

    print(f'\nreading from {path}...')
    start_execution = round(time.time() * 1000)
    workbook = xlrd.open_workbook(path)
    for i in range(start_week, end_week + 1):
        sheet_name = f'{sheet_prefix}{i}'
        try:
            worksheet = workbook.sheet_by_name(sheet_name)
        except Exception as ex:
            print_msg(f'ERROR: {str(ex)} in \'{path}\'')
            end_week = i - 1
            break

        # Loop through all data from (A10:E10) vertically
        cur_row_x = 10 - 1  # Start row 10
        while True:
            date_float = worksheet.cell(cur_row_x, colx=0).value
            if type(date_float) != float:
                break  # Stop iteration if end vertically
            tmp_date_tuple = datetime.datetime(*xlrd.xldate_as_tuple(date_float, workbook.datemode))
            tmp_week_number = i
            tmp_time_start = worksheet.cell(cur_row_x, colx=1).value * 24
            tmp_time_end = worksheet.cell(cur_row_x, colx=2).value * 24
            tmp_duration = xldate_as_datetime(worksheet.cell(cur_row_x, colx=3).value, workbook.datemode)

            tmp_type_of_work = worksheet.cell(cur_row_x, colx=4).value
            for key in WorkSession.get_work_type_dictionary():
                if search(key.lower(), str(tmp_type_of_work).lower()):
                    tmp_type_of_work = WorkSession.get_work_type_dictionary().get(key)

            tmp_backlog_item_nr = worksheet.cell(cur_row_x, colx=5).value
            if any(tmp_backlog_item_nr == c for c in ['N/A', '', ' ', '-1']):
                tmp_backlog_item_nr = '0'  # Set to 0 if no backlog-item

            # Create work object and append it to list
            temp_work = WorkSession(date=tmp_date_tuple, week_number=tmp_week_number, time_start=tmp_time_start,
                                    time_end=tmp_time_end, duration=tmp_duration, work_type=tmp_type_of_work,
                                    item_nr=tmp_backlog_item_nr)
            person.WorkSession_list.append(temp_work)
            cur_row_x += 1

    print_msg(f'{round(time.time() * 1000) - start_execution}ms.')
    print_msg(f'Total work duration ->{person.get_total_work_duration()} week {start_week} to {end_week}')
    return person
