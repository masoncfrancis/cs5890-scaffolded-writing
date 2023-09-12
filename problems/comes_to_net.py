from typing import Dict, Any, List, Tuple, Optional
from typing import Dict, Any
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from shared_utils import set_weighted_score_data
import scaffolded_writing.dp_utils as sw_du
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.dp_utils import concat_into_production_rule
from scaffolded_writing.student_submission import StudentSubmission
from scaffolded_writing.constraint_based_grader import Constraint
from shared_utils import grade_question_parameterized


COMES_TO_NET_CFG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Hit a" SHOT_TYPE
    SHOT_TYPE -> "forehand" | "backhand"
""")

class CorrectSideConstraint(Constraint[StudentSubmission]):
    def __init__(self):
        pass

    def is_satisfied(self, submission: StudentSubmission):
        return False

    def get_feedback(self, submission: StudentSubmission):
        return 'If you run around the ball to hit a forehand, you will be too far out of position if they volley to your forehand side.'


def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = COMES_TO_NET_CFG.to_json_string()

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, COMES_TO_NET_CFG)

    if submission.does_path_exist("SHOT_TYPE", "backhand"):
        return False, 'If you run around the ball to hit a forehand, you will be too far out of position if they volley to your forehand side.'

    return True, None

# def grade(data: Dict[str, Any]) -> None:
#     grader = IncrementalConstraintGrader(StudentSubmission, COMES_TO_NET_CFG)

#     grader.add_constraint(CorrectSideConstraint(), 1)

#     # grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
#     # grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("profit", "maximum"), 0.1)
#     # grader.add_constraint(sw_du.DescriptiveFunctionName("MaxProfit"), 0.15)
#     # grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n"]), 0.25)
#     # grader.add_constraint(sw_du.DecoupledParametersConstraint(
#     #         SUBARRAY="the index of a trial",
#     #         COMPARISON_RHS="the number of trials accepted",
#     #     ), 0.3)
#     # grader.add_constraint(ArrayReducesConstraint("SUBARRAY"), 0.5)
#     # grader.add_constraint(NoPrefixSubproblems(), 0.6)
#     # grader.add_constraint(sw_du.NoIrrelevantRestrictions("NUM_TRIALS_RESTRICTION"), 0.7)
#     # grader.add_constraint(sw_du.NoDoubleEndedParameterization())



#     grader.grade_question(data, "subproblem_definition")
#     set_weighted_score_data(data)

def grade(data: Dict[str, Any]) -> None:
    grade_question_parameterized(data, "subproblem_definition", grade_statement)
    set_weighted_score_data(data)

statement = "Your oppenent approaches the net with a forehand down the line. What is your next move?"

