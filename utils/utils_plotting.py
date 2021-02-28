__author__ = "Anders Rubach Ese"
__version__ = "2.1.0"
__email__ = "aes014@uit.no"


def person_to_graph(person, path_out='./output/'):
    """
    :param person: Person object
    :param path_out: Path to output file
    :return: True if no errors
    """
    import matplotlib.pyplot as plt
    import numpy as np

    x_values = np.arange(person.start_week, person.end_week + 1)
    y_values = [0]
    last = person.start_week
    index = 0

    from utils.utils_time import time_to_seconds

    for i in range(0, len(person.WorkSession_list)):
        if last != person.WorkSession_list[i].week_number:
            last = person.WorkSession_list[i].week_number
            index += 1
            if person.WorkSession_list[index + 1] is not None:
                y_values.append(0)
        y_values[index] += time_to_seconds(person.WorkSession_list[i].duration)
    plt.plot(x_values, y_values, color="green")

    # TODO: Implement multiple x_values -> TOTAL + all work types using WorkSession.get_work_type_dictionary()...

    plt.title("Timer per uke")
    plt.xlabel("Ukenummer")
    plt.ylabel("Antall timer")
    plt.show()
