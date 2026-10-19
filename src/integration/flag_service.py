import os
from interfaces.config_protocols import FlagServiceProtocol

class FlagService(FlagServiceProtocol):
    ASSIGNATION_DONE_FLAG = "assignation_done"
    def __init__(self, assignation_file: str):
        self.flags = {}
        self.assignation_file = assignation_file

    def is_asignation_done(self) -> bool:
        if self.ASSIGNATION_DONE_FLAG in self.flags and self.flags[self.ASSIGNATION_DONE_FLAG]:
            return self.flags[self.ASSIGNATION_DONE_FLAG]

        self.flags[self.ASSIGNATION_DONE_FLAG] = self.assignation_file and os.path.isfile(self.assignation_file)
        return self.flags[self.ASSIGNATION_DONE_FLAG]