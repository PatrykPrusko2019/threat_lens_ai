from enum import Enum

class AlertStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    FALSE_POSITIVE = "false_positive"


class Severity(str, Enum):
    LoW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"    