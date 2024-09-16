########################################################################################################################
# HELPER METHODS FOR PARSING INPUTS
########################################################################################################################
import json
import os
import xml.etree.ElementTree as ET

from model.java_class import JavaClass
from model.mutation import Mutation


def class_exists():
    pass


def _read_class_file(dirpath, filename):
    with open(dirpath + '/' + filename) as json_file:
        c = json.loads(json_file.read())
        return JavaClass(c)


def walk_classes_dir(dir_path, class_files):
    for (dirpath, _, filenames) in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith('.json'):
                class_object = _read_class_file(dirpath, filename)
                if class_object.package_name + '.' + class_object.class_name not in class_files:
                    class_files[class_object.package_name + '.' + class_object.class_name] = class_object
                else:
                    # add to coverage elements to existing class file
                    with open(dirpath + '/' + filename) as json_file:
                        c = json.loads(json_file.read())
                        class_files[class_object.package_name + '.' + class_object.class_name].parse_coverage_elements(
                            c["coverageElementPositions"])

    return class_files


def parse_class_files(subject_id):
    # SDL
    class_files: dict = walk_classes_dir('../project-data/' + subject_id + '/red4j-data/classes-xmt/', {})
    # XMT
    class_files = walk_classes_dir('../project-data/' + subject_id + '/red4j-data/classes-sdl/', class_files)
    # PIT
    return class_files


def parse_pit_mutations(file_path):
    mutations = []
    with open(file_path) as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for mutation in root:
            # Extract data
            detected = mutation.get('detected')
            status = mutation.get('status')
            number_of_tests_run = mutation.get('numberOfTestsRun')
            source_file = mutation.find('sourceFile').text
            mutated_class = mutation.find('mutatedClass').text
            mutated_method = mutation.find('mutatedMethod').text
            method_description = mutation.find('methodDescription').text
            line_number = int(mutation.find('lineNumber').text)
            mutator = mutation.find('mutator').text
            index = int(mutation.find('indexes/index').text)
            block = mutation.find('blocks/block').text
            killing_test = mutation.find('killingTest').text
            description = mutation.find('description').text

            mutation_obj = Mutation(detected, status, number_of_tests_run, source_file, mutated_class,
                                    mutated_method,
                                    method_description, line_number, mutator, index, block, killing_test,
                                    description)
            mutations.append(mutation_obj)
    return mutations
