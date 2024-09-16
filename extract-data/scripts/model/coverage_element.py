import os

from model.utils.calculate import elements_quick_sort


class CoverageElement:

    def __init__(self, element_info_json, position_json):
        self.element_info_json_str = element_info_json
        self.method_mutants = []
        self.start_line = int(position_json["startLine"])
        self.end_line = int(position_json["endLine"])
        self.start_col = int(position_json["startCol"])
        self.end_col = int(position_json["endCol"])
        self.type = str(element_info_json.split("(", 1)[0])
        self.index = None
        self.subtype = None
        self.decision_value = None
        self.classification = "NOT-COVERED"
        self.child_elements = None
        self.tests_covering = []
        self.parent_class = None

        if self.type == "Stmt":
            sub_type, self.index, self.parent_class = element_info_json.split(",")[:3]
            self.subtype = sub_type.split("(", 1)[1].strip()
        if self.type == "Block":
            sub_type, self.index, self.parent_class, mutant = element_info_json.split(",")[:4]
            self.subtype = sub_type.split("(", 1)[1].strip()
            self.method_mutants.append(mutant)
        elif self.type == "Decision":
            value, subtype, self.index, self.parent_class = element_info_json.split(",")[:4]
            self.decision_value = value.split("(", 1)[1]
            self.subtype = subtype.strip()

        self.pit_mutants = []
        self.identifier = ""

    def __str__(self):
        return '(' + self.type + self.subtype + ':' + self.index.strip() + ':' + self.classification + ')'

    def set_classification(self, classification):
        self.classification = classification

    def add_mutant(self, mutation_obj):
        self.pit_mutants.append(mutation_obj)

    def get_mutants(self):
        return self.pit_mutants

    def set_child_elements(self, elements):
        self.child_elements = []
        element: CoverageElement
        for element in elements:
            if element.parent_class == self.parent_class and self._is_child(element):
                self.child_elements.append(element)
        return self.child_elements

    def _is_child(self, element):
        if self.start_line <= element.start_line <= element.end_line <= self.end_line:
            return True
        if self.start_line == element.start_line and self.start_col <= element.start_col:
            if self.end_line > element.end_line:
                return True
            elif self.end_line == element.end_line and self.end_col > element.end_col:
                return True

        if self.end_line == element.end_line and self.end_col >= element.end_col:
            if self.start_line < element.start_line:
                return True
            elif self.start_line == element.start_line and self.start_col < element.start_col:
                return True
        return False

    def sort_child_elements(self):
        return elements_quick_sort(self.child_elements)

    def set_identifier(self, method_identifier):
        self.identifier = method_identifier
