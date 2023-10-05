###############################################################################
#### DO NOT EDIT THIS SECTION
###############################################################################
from typing import Dict, Any, List, Tuple, Optional
from shared_utils import set_weighted_score_data
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.student_submission import StudentSubmission
from shared_utils import grade_question_parameterized

def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = PROBLEM_CONFIG.to_json_string()

def grade(data: Dict[str, Any]) -> None:
    grade_question_parameterized(data, "subproblem_definition", grade_statement)
    set_weighted_score_data(data)

###############################################################################
#### DO NOT EDIT ABOVE HERE, ONLY EDIT BELOW
###############################################################################

statement = "You want to purchase a motorcycle for getting around Logan." + \
    "What engine size, motorcycle type, and manufacturer should you choose for fuel efficiency, reliability, and safety?"

PROBLEM_CONFIG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Purchase a" BIKE
    BIKE -> MANUFACTURER BODY_TYPE "that is" ENGINE_SIZE
    MANUFACTURER -> "Honda" | "Kawasaki" | "Harley-Davidson" | "KTM"
    BODY_TYPE -> "sport bike" | "cruiser" | EPSILON
    ENGINE_SIZE -> "125 cc" | "300 cc" | "600 cc" | "1000 cc" | EPSILON
    EPSILON ->
""")

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, PROBLEM_CONFIG)

    if submission.does_path_exist("STRUCTURE_TYPE", "array"):
        return False, 'Using an array will make checking for duplicates very inefficient.'

    if submission.does_path_exist("STRUCTURE_TYPE", "linked list"):
        return False, 'Using a linked list will make checking for duplicates very inefficient.'

    if submission.does_path_exist("STRUCTURE_TYPE", "binary search tree"):
        return False, 'A binary search tree would be fairly time efficient, but there is a better option.'

    if submission.does_path_exist("STRUCTURE_TYPE", "array"):
        return False, 'Using an array will make checking for duplicates very inefficient.'

    if submission.does_path_exist("STRUCTURE_TYPE", "hash map") and \
        not submission.does_path_exist("REASON", "for efficient"):
        return False, 'You must give a reason why you want to use that structure.'

    if submission.does_path_exist("STRUCTURE_TYPE", "hash map") and \
        submission.does_path_exist("OPERATION", "memory usage"):
        return False, 'Sorry, hash maps are not very memory efficient!'

    if submission.does_path_exist("STRUCTURE_TYPE", "hash map") and \
        submission.does_path_exist("OPERATION", "deletion"):
        return False, 'Hash maps do allow for efficient deletion, but that is not relevant to the question.'

    return True, None


