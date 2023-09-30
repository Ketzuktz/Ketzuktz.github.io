from enum import Enum


class PhaseType(Enum):
    Preparation = "Preparation Phase"
    Round = "Round Phase"
    VE = "Victory Evaluation"


class RoundType(Enum):
    Roll = "Roll"

    # Action Type
    # all continue, but next is player i
    RA_all_continue_1 = "All continue 1"
    RA_all_continue_2 = "All continue 2"
    # only continue, but next is player i
    RA_only_continue_1 = "Only continue 1"
    RA_only_continue_2 = "Only continue 2"
    # all end
    RA_all_end = "All end"

    End = "End"


class TossType(Enum):
    RANDOM = "Toss Random"
    CONST_1 = "Toss Const 1"
    CONST_2 = "Toss Const 2"
