from typing import Dict, Any, List, Tuple, Optional
from typing import Dict, Any
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

PROBLEM_CONFIG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Hit a" SHOT_TYPE
    SHOT_TYPE -> "forehand" | "backhand"
""")

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, PROBLEM_CONFIG)

    if submission.does_path_exist("SHOT_TYPE", "backhand"):
        return False, 'If you run around the ball to hit a forehand, you will be too far out of position if they volley to your forehand side.'

    return True, None

statement = "Your oppenent approaches the net with a forehand down the line. What is your next move?"

