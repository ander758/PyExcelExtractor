class Person:
    def __init__(self, owner, work_list, start_week, end_week):
        self.owner = owner
        self.WorkSession_list = work_list  # List of WorkSession objects
        self.start_week = start_week
        self.end_week = end_week

    def get_duration_of_itemnr(self, item_nr):
        """
        :param item_nr: Given Itemnr as of Gantt-diagram
        :return: Total duration for given Itemnr
        """
        from utils import summarize_durations
        arr = []
        for work_session in self.WorkSession_list:
            if item_nr == work_session.item_nr:
                arr.append(work_session.duration)
        return summarize_durations(arr)

    def get_total_work_duration(self):
        """
        :return: Summed duration
        """
        from utils.utils_time import summarize_durations
        arr = []
        for work_session in self.WorkSession_list:
            arr.append(work_session.duration)
        return summarize_durations(arr)


class WorkSession:
    def __init__(self, date, week_number, time_start, time_end,
                 duration, work_type, item_nr=0):
        self.date         = date            # datetime-tuple - YYYY-MM-DD
        self.week_number  = week_number     # Integer - 4
        self.time_start   = time_start      # 24hr format - 13:00
        self.time_end     = time_end        # 24hr format - 14:25
        self.duration     = duration        # time as tuple (HH,MM,SS)
        self.type_of_work = work_type       # 0,1,2,3 - See work_type_reference Dict above
        self.item_nr      = int(item_nr)    # 8.1 - Backlog item as String, 0 if irrelevant

    @staticmethod
    def get_work_type_dictionary():
        return {
            'Teori:': 0,
            'Utvikling:': 1,
            'Administrativt:': 2,
            'Logg/Oppgaver:': 3,
            'Logg:': 3,
            'Oppgaver:': 3
        }

    @staticmethod
    def work_type_value_to_string(input_int):
        for key, value in WorkSession.get_work_type_dictionary.items():
            if value == input_int:
                return key[:-1]
