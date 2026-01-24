from enum import Enum

class FailureType(Enum):
    NONE = "none"
    CORRUPTION_DETECTED = "corruption_detected" # Checksum/ECC detected failure
    SILENT_CORRUPTION = "silent_corruption" # Checksum passed but content wrong
    MISSING_DATA = "missing_data" # Index mismatch or truncation
    SYSTEM_ERROR = "system_error" # I/O, OOM, Constraint failure

class DNAStorageError(RuntimeError):
    def __init__(self, message, failure_type=FailureType.SYSTEM_ERROR):
        super().__init__(message)
        self.failure_type = failure_type
