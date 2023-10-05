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
    "What engine size, body type, and manufacturer should you choose for fuel efficiency, reliability, and safety?"

PROBLEM_CONFIG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Purchase a" BIKE
    BIKE -> MANUFACTURER "that is a" BODY_TYPE "with an engine size of" ENGINE_SIZE
    MANUFACTURER -> "Honda" | "Kawasaki" | "Harley-Davidson" | "KTM"
    BODY_TYPE -> "sport bike" | "cruiser"
    ENGINE_SIZE -> "125 cc" | "300 cc" | "650 cc" | "1000 cc" | EPSILON
    EPSILON ->
""")

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, PROBLEM_CONFIG)

    if submission.does_path_exist("MANUFACTURER", "Harley-Davidson"):
        return False, 'Harley-Davidsons are not known for their reliability or fuel efficiency.'

    if submission.does_path_exist("MANUFACTURER", "KTM"):
        return False, 'KTMs are not known for their reliability.'

    if submission.does_path_exist("BODY_TYPE", "sport bike"):
        return False, 'Sport bikes are generally considered to be less safe than cruisers'

    if submission.does_path_exist("ENGINE SIZE", "650 cc"):
        return False, 'A 650 cc bike is probably too big to be very fuel efficient, and is one of the less safe options.'

    if submission.does_path_exist("ENGINE SIZE", "1000 cc"):
        return False, 'A 1000 cc bike is way too big to be very fuel efficient, completely unnecessary for just getting around town, and is one of the least safe options available.'

    return True, None


