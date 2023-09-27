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

statement = 'Assume you are a right-handed tennis player.' + \
    'A right-handed oppenent approaches the net with a forehand down the line. What is your next move?'

PROBLEM_CONFIG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Hit a" SHOT
    SHOT -> SHOT_TYPE SHOT_LOCATION SHOT_SPIN
    SHOT_TYPE -> "forehand" | "backhand"
    SHOT_LOCATION -> "lob" | "down the line" | "cross-court" | EPSILON
    SHOT_SPIN -> "slice" | "with topspin" | EPSILON
    EPSILON ->
""")

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, PROBLEM_CONFIG)

    if submission.does_path_exist("SHOT_LOCATION", "cross-court"):
        return False, 'If you hit cross-court, your oppenent can volley down the line' + \
            ' on your forehand side faster than you can get there.'

    if submission.does_path_exist("SHOT_TYPE", "forehand") and \
        not submission.does_path_exist('SHOT_LOCATION', 'lob'):
        return False, 'If you run around the ball to hit a forehand, ' + \
            'you will be too far out of position if they volley to your forehand side.'

    if submission.does_path_exist("SHOT_TYPE", "backhand") and \
        submission.does_path_exist('SHOT_LOCATION', 'EPSILON'):
        return False, 'A backhand may be a good choice, but where will you hit it?'

    return True, None


