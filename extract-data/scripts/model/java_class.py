import json
import os

from model.mutation import Mutation
from model.utils.check import is_method, is_statement, is_matching_element, mutant_is_in_element
from model.coverage_element import CoverageElement


def _get_pseudo(typeMetricsHashMap):
    pseudo = []
    for metric in typeMetricsHashMap:
        pseudo.extend(typeMetricsHashMap[metric]["coverageGap"])
    return pseudo


class JavaClass:

    def __init__(self, class_json):
        self.file_name = class_json["fileName"]
        self.package_name = class_json["packageName"]
        self.class_name = class_json["className"]
        self.coverage_elements = []
        self.parse_coverage_elements(class_json["coverageElementPositions"])

    def parse_coverage_elements(self, coverage_elements_json):
        for c in coverage_elements_json:
            if str(coverage_elements_json[c]) != "None":
                if not self._element_exists(CoverageElement(c, coverage_elements_json[c])):
                    self.coverage_elements.append(CoverageElement(c, coverage_elements_json[c]))

    def get_methods(self):
        return list(filter(is_method, self.coverage_elements))

    def get_statements(self):
        return set(filter(is_statement, self.coverage_elements))

    def set_classifications(self, subject_id):
        self._parse_class_analysis(subject_id)

    def set_test_coverage(self, subject_id):
        sdl_dir_path = '../project-data/' + subject_id + '/red4j-data/results-sdl/'
        xmt_dir_path = '../project-data/' + subject_id + '/red4j-data/results-xmt/'
        self._parse_results(sdl_dir_path)
        self._parse_results(xmt_dir_path)

    def _parse_class_analysis(self, subject_id):
        sdl_analysis_dir_path = '../project-data/' + subject_id + '/red4j-data/analysis-sdl/'
        xmt_analysis_dir_path = '../project-data/' + subject_id + '/red4j-data/analysis-xmt/'
        file_name = self.package_name.replace('.', '/') + '/' + self.class_name + '.json'
        self._set_element_classification(xmt_analysis_dir_path, file_name)
        self._set_element_classification(sdl_analysis_dir_path, file_name)

    def _set_element_classification(self, dir_path, file_name):
        with open(dir_path + file_name) as json_file:
            c = json.loads(json_file.read())

            for element_str in c["covered"]:
                element: CoverageElement
                for element in self.coverage_elements:
                    if is_matching_element(element, element_str):
                        element.classification = "COVERED"

            for element_str in _get_pseudo(c["typeMetricsHashMap"]):
                element: CoverageElement
                for element in self.coverage_elements:
                    if is_matching_element(element, element_str):
                        element.classification = "PSEUDO-TESTED"

            for element_str in c["effectualCovered"]:
                element: CoverageElement
                for element in self.coverage_elements:
                    if is_matching_element(element,
                                           element_str) and not element.classification == "PSEUDO-TESTED":
                        element.classification = "REQUIRED"

    def add_mutant(self, mutation_obj: Mutation):
        for element in self.coverage_elements:
            element: CoverageElement
            if mutant_is_in_element(element, mutation_obj):
                element.add_mutant(mutation_obj)

    def _element_exists(self, c):
        for existing_element in self.coverage_elements:
            if str(c) == str(existing_element):
                return True
        return False

    def _parse_results(self, dir_path):
        for (dirpath, _, filenames) in os.walk(dir_path):
            for filename in filenames:
                if filename.endswith('.json'):
                    with open(dirpath + '/' + filename) as json_file:
                        data = json.loads(json_file.read())
                        coverage_element: CoverageElement
                        for coverage_element in self.coverage_elements:
                            if data["coverageElementTestOutcomes"].get(
                                    coverage_element.element_info_json_str) is not None:
                                coverage_element.tests_covering.append(filename.removesuffix('.json'))

