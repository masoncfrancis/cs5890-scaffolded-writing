from typing import Dict, Any
from typing import Dict, Any
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from shared_utils import set_weighted_score_data
import scaffolded_writing.dp_utils as sw_du
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.dp_utils import concat_into_production_rule
from scaffolded_writing.student_submission import StudentSubmission
from scaffolded_writing.constraint_based_grader import Constraint


COMES_TO_NET_CFG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

    FUNCTION_DECLARATION -> "the subproblem" | {concat_into_production_rule(
        ["DP", "Memo", "MaxProfit"],
        ["(i)", "(i,j)"]
    )}

    FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "that can be obtained" SITUATION

    EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
    OUTPUT_NOUN -> "answer" | "profit"
    SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION \
               | NUM_TRIALS_RESTRICTION SUBARRAY_RESTRICTION

    MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

    SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
    SUBARRAY -> "the rest of the trials" | "Trials 1 through n" \
              | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
    PREFIX_SUBPROBLEM -> "Trials 1 through i"
    SUFFIX_SUBPROBLEM -> "Trials i through n"
    DOUBLE_ENDED_SUBPROBLEM -> "Trials i through j"

    NUM_TRIALS_RESTRICTION -> "by accepting" COMPARISON_OPERATOR COMPARISON_RHS "trials"
    COMPARISON_OPERATOR -> "at least" | "at most" | "exactly"
    COMPARISON_RHS -> "i" | "j"

    EPSILON ->
""")

COMES_TO_NET_CFG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Hit a" SHOT_TYPE
    SHOT_TYPE -> "forehand" | "backhand"
""")

class CorrectSideConstraint(Constraint[StudentSubmission]):
    # def __init__(self):
    #     pass

    def is_satisfied(self, submission: StudentSubmission):
        return False

    def get_feedback(self, submission: StudentSubmission):
        return 'If you run around the ball to hit a forehand, you will be too far out of position if they volley to your forehand side.'


def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = COMES_TO_NET_CFG.to_json_string()


def grade(data: Dict[str, Any]) -> None:
    grader = IncrementalConstraintGrader(StudentSubmission, COMES_TO_NET_CFG)

    grader.add_constraint(CorrectSideConstraint(), 1)

    # grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
    # grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("profit", "maximum"), 0.1)
    # grader.add_constraint(sw_du.DescriptiveFunctionName("MaxProfit"), 0.15)
    # grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n"]), 0.25)
    # grader.add_constraint(sw_du.DecoupledParametersConstraint(
    #         SUBARRAY="the index of a trial",
    #         COMPARISON_RHS="the number of trials accepted",
    #     ), 0.3)
    # grader.add_constraint(ArrayReducesConstraint("SUBARRAY"), 0.5)
    # grader.add_constraint(NoPrefixSubproblems(), 0.6)
    # grader.add_constraint(sw_du.NoIrrelevantRestrictions("NUM_TRIALS_RESTRICTION"), 0.7)
    # grader.add_constraint(sw_du.NoDoubleEndedParameterization())



    grader.grade_question(data, "subproblem_definition")
    set_weighted_score_data(data)

statement = "Your oppenent approaches the net with a forehand down the line. What is your next move?"