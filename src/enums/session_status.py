from enum import Enum

class SessionStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    BROKEN = "broken"
    IN_PROGRESS = "in progress"


@staticmethod
def from_string(label):
    if label == "passed":
        return SessionStatus.PASSED
    elif label == "failed":
        return SessionStatus.FAILED
    elif label == "broken":
        return SessionStatus.BROKEN
    elif label == "in progress":
        return SessionStatus.IN_PROGRESS
    else:
        return None
