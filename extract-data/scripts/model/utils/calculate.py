from random import randint
import os


def get_pct(total, num):
    if total != 0:
        return round(num / total * 100, 2)
    else:
        return 0


def elements_quick_sort(element_list):
    """
    Adapted from https://realpython.com/sorting-algorithms-python/ quicksort implementation
    """
    if len(element_list) < 2:
        return element_list

    before, equal, after = [], [], []

    # random pivot
    pivot = element_list[randint(0, len(element_list) - 1)]

    for element in element_list:
        if element.start_line < pivot.start_line:
            before.append(element)
        if (
            element.start_line == pivot.start_line
            and element.start_col < pivot.start_col
        ):
            before.append(element)
        if (
            element.start_line == pivot.start_line
            and element.start_col == pivot.start_col
        ):
            equal.append(element)
        if (
            element.start_line == pivot.start_line
            and element.start_col > pivot.start_col
        ):
            after.append(element)
        if element.start_line > pivot.start_line:
            after.append(element)

    return elements_quick_sort(before) + equal + elements_quick_sort(after)


def count_json_files(directory):
    json_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_count += 1
    return json_count
