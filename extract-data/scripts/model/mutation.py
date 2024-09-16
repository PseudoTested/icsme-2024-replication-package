# mutation.py

class Mutation:
    def __init__(self, detected, status, number_of_tests_run, source_file, mutated_class, mutated_method,
                 method_description, line_number, mutator, index, block, killing_test, description):
        self.detected = detected
        self.status = status
        self.number_of_tests_run = number_of_tests_run
        self.source_file = source_file
        self.mutated_class = mutated_class
        self.mutated_method = mutated_method
        self.method_description = method_description
        self.line_number = line_number
        self.mutator = mutator
        self.index = index
        self.block = block
        self.killing_test = killing_test
        self.description = description

    def __str__(self):
        return f"Mutation detected: {self.detected}, status: {self.status}, numberOfTestsRun: {self.number_of_tests_run}"
