from model.coverage_element import CoverageElement
from model.mutation import Mutation


def is_method(coverage_element: CoverageElement):
    if coverage_element.type == "Block" and coverage_element.subtype == "METHOD":
        return True
    return False


def is_statement(coverage_element: CoverageElement):
    if coverage_element.type == "Stmt" or coverage_element.type == "Decision":
        return True
    return False


def is_matching_element(existing_ce: CoverageElement, json_ce: str):
    json_ce_type = str(json_ce.split("(", 1)[0])
    index = ""
    subtype = ""
    decision_value = None
    if json_ce_type == "Stmt":
        sub_type, index, _ = json_ce.split(",")[:3]
        subtype = sub_type.split("(", 1)[1].strip()
    elif json_ce_type == "Block":
        sub_type, index, parent_class = json_ce.split(",")[:3]
        subtype = sub_type.split("(", 1)[1].strip()
    elif json_ce_type == "Decision":
        value, subtype, index, _ = json_ce.split(",")[:4]
        decision_value = value.split("(", 1)[1]
        subtype = subtype.strip()

    if str(existing_ce.type) == json_ce_type and str(existing_ce.subtype) == subtype and str(
            existing_ce.index) == index:
        if decision_value is None:
            return True
        elif str(existing_ce.decision_value) == decision_value:
            return True

    return False


def is_covered(coverage_element: CoverageElement):
    return True if coverage_element.classification != "NOT-COVERED" else False


def is_pseudo_tested(coverage_element: CoverageElement):
    return True if coverage_element.classification == "PSEUDO-TESTED" or coverage_element.classification == "PiR" else False


def is_required(coverage_element: CoverageElement):
    return True if coverage_element.classification == "REQUIRED" else False


def get_pseudo_tested_children(method: CoverageElement):
    pseudo_tested_children = set()

    if is_required(method) and method.child_elements is not None:
        for child_element in method.child_elements:
            if is_pseudo_tested(child_element):
                child_element.classification = "PiR"
                pseudo_tested_children.add(child_element)
    return pseudo_tested_children


def mutant_is_in_element(c_e: CoverageElement, mutant: Mutation):
    if c_e.start_line <= mutant.line_number <= c_e.end_line:
        if c_e.type == "Stmt" or c_e.type == "Block":
            return True
        elif (c_e.type == "Decision" and mutant.mutator == ("org.pitest.mutationtest.engine.gregor.mutators"
                                                            ".NegateConditionalsMutator") or mutant.mutator ==
              "org.pitest.mutationtest.engine.gregor.mutators.ConditionalsBoundaryMutator"):
            return True

    return False


def is_killed_mutant(mutant: Mutation):
    return mutant.status == "KILLED"


def mutant_is_killed(mutant: Mutation):
    return mutant.status == "KILLED"
