from typing import List

from model.java_class import JavaClass
from model.utils.calculate import count_json_files
from model.utils.parse import parse_class_files, parse_pit_mutations


class Subject:
    def __init__(self, subject_id):
        self.mutations = None
        self.subject_id = subject_id
        self.classes = parse_class_files(subject_id)
        self.parse_analysis()
        self.parse_results()
        self.test_count = self.get_test_count()
        self.assertions_count = self.get_assertion_count()
        self.hash_code = self.get_short_hash()


    def parse_analysis(self):
        c: JavaClass
        for c in self.classes:
            self.classes[c].set_classifications(self.subject_id)

    def parse_results(self):
        c: JavaClass
        for c in self.classes:
            self.classes[c].set_test_coverage(self.subject_id)

    def parse_pit_mutants(self):
        file_path = '../project-data/' + self.subject_id + '/gregor.xml'
        self.mutations: List = parse_pit_mutations(file_path)
        for mutation in self.mutations:
            current_class: JavaClass = self.classes.get(mutation.mutated_class)
            if current_class is not None:
                current_class.add_mutant(mutation)

    def get_methods(self):
        methods = []
        for c in self.classes:
            methods.extend(self.classes[c].get_methods())
        return methods

    def get_statements(self):
        statements = []
        for c in self.classes:
            statements.extend(self.classes[c].get_statements())
        return statements

    def get_mutants(self):
        return self.mutations

    def get_test_count(self):
        return count_json_files('../project-data/' + self.subject_id + '/red4j-data/results-sdl/')

    def get_assertion_count(self):
        with open('../project-data/' + self.subject_id + '/assertions_count.txt', "r") as count_txt:
            count = count_txt.read().strip()
            return count

    def get_short_hash(self):
        with open('../project-data/' + self.subject_id + '/hash_code.txt', "r") as short_hash_txt:
            short_hash = short_hash_txt.read().strip()
            return short_hash
