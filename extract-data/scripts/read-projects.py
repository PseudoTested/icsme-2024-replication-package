import csv
from typing import List

import pandas as pd

from model.java_class import JavaClass
from model.main import load_subjects
from model.subject import Subject
from model.utils.calculate import get_pct
from model.utils.check import is_covered, is_pseudo_tested, mutant_is_killed, is_required
from model.utils.check import is_killed_mutant, get_pseudo_tested_children

subjects_list = load_subjects("../project-data/")

# Setup
with open("output-data/0-subject-summary-data.csv", "w") as c:
    csv_writer = csv.writer(
        c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow(
        [
            r"Subject Name",
            r"Git hash",
            r"Test #",
            r"Assertion #",
            r"Methods #",
            r"Methods # cov",
            r"Methods # pseudo",
            r"Methods % covered",
            r"Methods % pseudo",
            r"Statements #",
            r"Statements # cov",
            r"Statements # pseudo",
            r"Statements # PTSIRM",
            r"Statements % covered",
            r"Statements % pseudo",
            r"PIT Mutants #",
            r"PIT Mutants # Killed",
            r"PIT Mutants % Killed",
        ]
    )

# Output data
subject: Subject
for subject in subjects_list:
    # Methods
    methods_in_subject = subject.get_methods()
    covered_methods_in_subject = set(filter(is_covered, methods_in_subject))
    required_methods_in_subject = set(filter(is_required, methods_in_subject))
    pseudo_tested_methods_in_subject = set(filter(is_pseudo_tested, methods_in_subject))
    # Statements
    statements_in_subject: List = subject.get_statements()
    covered_statements_in_subject = set(filter(is_covered, statements_in_subject))
    pseudo_tested_statements_in_subject = set(filter(is_pseudo_tested, covered_statements_in_subject))
    pseudo_tested_statements_in_required_methods_in_subject = set()
    for method in covered_methods_in_subject:
        if is_required(method):
            method.set_child_elements(statements_in_subject)
            pseudo_statements = get_pseudo_tested_children(method)

            pseudo_tested_statements_in_required_methods_in_subject.update(pseudo_statements)

    # Gregor Mutants
    pit_mutants = subject.get_mutants()
    pit_mutants_killed = set(filter(is_killed_mutant, pit_mutants))
    
    with open("output-data/0-subject-summary-data.csv", "a") as c:
        csv_writer = csv.writer(
            c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(
            [
                subject.subject_id,
                subject.hash_code,
                subject.test_count,
                subject.assertions_count,
                int(len(methods_in_subject)),
                int(len(covered_methods_in_subject)),
                int(len(pseudo_tested_methods_in_subject)),
                float(get_pct(len(methods_in_subject),
                              len(covered_methods_in_subject))),
                float(get_pct(len(methods_in_subject),
                              len(pseudo_tested_methods_in_subject))),
                int(len(statements_in_subject)),
                int(len(covered_statements_in_subject)),
                int(len(pseudo_tested_statements_in_subject)),
                int(len(pseudo_tested_statements_in_required_methods_in_subject)),
                float(get_pct(len(statements_in_subject),
                              len(covered_statements_in_subject))),
                float(get_pct(len(statements_in_subject),
                              len(pseudo_tested_statements_in_subject))),
                int(len(pit_mutants)),
                int(len(pit_mutants_killed)),
                float(get_pct(len(pit_mutants), len(pit_mutants_killed)))
            ]
        )

from model.utils.check import is_killed_mutant
from model.coverage_element import CoverageElement

# Setup
with open("output-data/1-class-summary-data.csv", "w") as c:
    csv_writer = csv.writer(
        c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow(
        [
            r"Subject Name",
            r"Class Name",
            r"Methods #",
            r"Methods # cov",
            r"Methods # not-cov",
            r"Methods # req",
            r"Methods # pseudo",
            r"Methods % covered",
            r"Methods % pseudo",
            r"Statements #",
            r"Statements # cov",
            r"Statements # not-cov",
            r"Statements # req",
            r"Statements # pseudo",
            r"Statements # PTSIRM",
            r"Statements % covered",
            r"Statements % pseudo",
            r"# PIT mutants",
            r"# PIT mutants killed",
            r"% PIT mutants killed"
        ]
    )

# Output data
subject: Subject
for subject in subjects_list:
    print(subject.subject_id)
    classes = subject.classes

    for red4j_class in classes:
        # Methods
        methods_in_class = classes[red4j_class].get_methods()
        covered_methods_in_class = list(filter(is_covered, methods_in_class))
        pseudo_tested_methods_in_class = list(filter(is_pseudo_tested, methods_in_class))
        # Statements
        statements_in_class: List = classes[red4j_class].get_statements()
        covered_statements_in_class = list(filter(is_covered, statements_in_class))
        pseudo_tested_statements_in_class = list(filter(is_pseudo_tested, statements_in_class))
        pseudo_tested_statements_in_required_methods_in_class = set()
        for method in covered_methods_in_class:
            if is_required(method):
                method.set_child_elements(statements_in_class)
                pseudo_statements = get_pseudo_tested_children(method)
                pseudo_tested_statements_in_required_methods_in_class.update(pseudo_statements)
        pit_mutants = []
        for m in methods_in_class:
            m: CoverageElement
            pit_mutants.extend(m.pit_mutants)

        with open("output-data/1-class-summary-data.csv", "a") as c:
            csv_writer = csv.writer(
                c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            csv_writer.writerow(
                [
                    subject.subject_id,
                    red4j_class,
                    int(len(methods_in_class)),
                    int(len(covered_methods_in_class)),
                    int(len(methods_in_class) - len(covered_methods_in_class)),
                    int(len(covered_methods_in_class) - len(pseudo_tested_methods_in_class)),
                    int(len(pseudo_tested_methods_in_class)),
                    float(get_pct(len(methods_in_class),
                                  len(covered_methods_in_class))),
                    float(get_pct(len(methods_in_class),
                                  len(pseudo_tested_methods_in_class))),
                    int(len(statements_in_class)),
                    int(len(covered_statements_in_class)),
                    int(len(statements_in_class) - len(covered_statements_in_class)),
                    int(len(covered_statements_in_class) - len(pseudo_tested_statements_in_class)),
                    int(len(pseudo_tested_statements_in_class)),
                    int(len(pseudo_tested_statements_in_required_methods_in_class)),
                    float(get_pct(len(statements_in_class),
                                  len(covered_statements_in_class))),
                    float(get_pct(len(statements_in_class),
                                  len(pseudo_tested_statements_in_class))),

                    len(pit_mutants),
                    len(list(filter(is_killed_mutant, pit_mutants))),
                    get_pct(len(pit_mutants), len(list(filter(is_killed_mutant, pit_mutants))))
                ]
            )

# Setup
with open("output-data/2-method-summary-data.csv", "w") as c:
    csv_writer = csv.writer(
        c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow(
        [
            r"Subject Name",
            r"Class Name",
            r"Method Name",  # use full package identity
            r"Method Classification",
            r"# Tests Covering",
            r"Statements #",
            r"Statements # cov",
            r"Statements # required",
            r"Statements # pseudo",
            r"Statements % covered",
            r"Statements % pseudo",
            r"# PIT mutants",
            r"# PIT mutants killed",
            r"% PIT mutants killed"
        ]
    )

subject: Subject
for subject in subjects_list:
    print(subject.subject_id)
    subject_class: JavaClass
    for subject_class_key in subject.classes.keys():
        subject_class = subject.classes[subject_class_key]
        method: CoverageElement
        for method in subject_class.get_methods():
            child_elements = method.set_child_elements(subject_class.get_statements())
            covered_child_elements = list(filter(is_covered, method.child_elements))
            required_child_elements = list(filter(is_required, method.child_elements))
            pseudo_tested_child_elements = list(filter(is_pseudo_tested, method.child_elements))
            pit_mutants = method.pit_mutants
            with open("output-data/2-method-summary-data.csv", "a") as c:
                csv_writer = csv.writer(
                    c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                csv_writer.writerow(
                    [
                        subject.subject_id,
                        subject_class_key,
                        method.subtype.strip() + '.' + method.index.strip(),
                        method.classification,
                        len(method.tests_covering),
                        len(child_elements),
                        len(covered_child_elements),
                        len(required_child_elements),
                        len(pseudo_tested_child_elements),
                        get_pct(len(child_elements), len(covered_child_elements)),
                        get_pct(len(child_elements), len(pseudo_tested_child_elements)),
                        len(method.pit_mutants),
                        len(list(filter(mutant_is_killed, pit_mutants))),
                        get_pct(len(pit_mutants), len(list(filter(mutant_is_killed, pit_mutants))))
                    ]
                )


from model.utils.calculate import get_pct
from model.utils.check import mutant_is_killed
from model.coverage_element import CoverageElement
from model.java_class import JavaClass
from model.subject import Subject
import csv

# Setup
with open("output-data/3-statement-summary-data.csv", "w") as c:
    csv_writer = csv.writer(
        c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerow(
        [
            r"Subject Name",
            r"Class Name",
            r"Statement Type",  # use full package identity
            r"Statement ID",  # use full package identity
            r"Statement Classification",
            r"# Tests Covering",
            r"# PIT mutants",
            r"# PIT mutants killed",
            r"% PIT mutants killed"
        ]
    )

subject: Subject
for subject in subjects_list:
    print(subject.subject_id)
    subject_class: JavaClass
    for subject_class_key in subject.classes.keys():
        subject_class = subject.classes[subject_class_key]
        statement: CoverageElement
        for statement in subject_class.get_statements():
            pit_mutants = statement.pit_mutants
            with open("output-data/3-statement-summary-data.csv", "a") as c:
                csv_writer = csv.writer(
                    c, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                csv_writer.writerow(
                    [
                        subject.subject_id,
                        subject_class_key,
                        statement.subtype.strip(),
                        statement.index.strip(),
                        statement.classification,
                        len(statement.tests_covering),
                        len(statement.pit_mutants),
                        len(list(filter(mutant_is_killed, pit_mutants))),
                        get_pct(len(pit_mutants), len(list(filter(mutant_is_killed, pit_mutants))))
                    ]
                )

print('COMPLETE')
