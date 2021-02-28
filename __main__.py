from shutil import copyfile

from extractor import get_person_object_from_excel

start_week = 4
end_week = 7
itemNr = 8


path_root = 'assets/from_source/'
files = {
    'Anders': path_root+'Timeliste_Anders-Rubach-Ese.xlsm',
    'Alexander': path_root+'Timeliste_Johnsen_Alexander.xlsm'
}

for name in ['Anders', 'Alexander']:
    try:
        path_src = files.get(name)
        path_asset = f'assets/temps/TEMPORARY_FILE_{name}.xlsm'
        copyfile(fr'{path_src}', path_asset)

        person = get_person_object_from_excel(owner=name, path=path_asset, start_week=start_week, end_week=end_week)
        if itemNr is not None:
            print(f'{person.owner} has worked in total {person.get_duration_of_itemnr(itemNr)} on Itemnr {itemNr}\n')

        # person_to_graph(person)

    except PermissionError:
        print(f'Did not get permission to copy from\'{name}\'')
    except FileNotFoundError:
        print(f'File not found for \'{name}\'')

