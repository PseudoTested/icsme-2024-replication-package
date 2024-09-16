import os

from model.subject import Subject


def load_subjects(root_dir):
    subjects_list = []
    print(os.listdir(root_dir))
    for subject_id in os.listdir(root_dir):
        if subject_id != 'projects.json' and not subject_id.startswith('.'):
            print(subject_id)
            subject = Subject(subject_id)
            subject.parse_pit_mutants()
            subjects_list.append(subject)

    return subjects_list


if __name__ == "__main__":
    print("Use read-projects.py")
