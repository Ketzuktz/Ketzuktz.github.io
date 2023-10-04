from enum import Enum


class PhaseStatusEnum(Enum):
    Preparation = "[P0] Preparation"

    Roll = "[P1][R0] Roll"
    # Action Type
    RA_start = "[P1][R1] Start"
    # all continue, but next is player i
    RA_all_continue_1 = "[P1][R2] All continue 1"
    RA_all_continue_2 = "[P1][R3] All continue 2"
    # only continue, but next is player i
    RA_only_continue_1 = "[P1][R4] Only continue 1"
    RA_only_continue_2 = "[P1][R5] Only continue 2"
    # all end
    RA_all_end = "[P1][R6] All end"

    End = "[P1][R7] End"

    VE = "[P2] Victory Evaluation"


class TossType(Enum):
    RANDOM = "Toss Random"
    CONST_1 = "Toss Const 1"
    CONST_2 = "Toss Const 2"
