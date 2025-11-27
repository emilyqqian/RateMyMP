from enum import Enum


class MotionClassification(str, Enum):
    SUBSTANTIVE = "substantive"
    SUBSIDIARY = "subsidiary"
    PRIVILEGED = "privileged"
    INCIDENTAL = "incidental"


class VoteChoice(str, Enum):
    YEA = "yea"
    NAY = "nay"
    ABSTAIN = "abstain"
