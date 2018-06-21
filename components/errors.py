class QrtzError(Exception):
    pass

class QrtzCFGError(QrtzError):
    pass

class QrtzSyscallError(QrtzError):
    pass

class QrtzForwardAnalysisError(QrtzError):
    pass

class QrtzSkipJobNotice(QrtzForwardAnalysisError):
    pass

class QrtzDelayJobNotice(QrtzForwardAnalysisError):
    pass

class QrtzJobMergingFailureNotice(QrtzForwardAnalysisError):
    pass

class QrtzJobWideningFailureNotice(QrtzForwardAnalysisError):
    pass



class SimError(Exception):
    bbl_addr = None
    stmt_idx = None
    ins_addr = None
    executed_instruction_count = None
    guard = None

    def record_state(self, state):
        self.bbl_addr = state.scratch.bbl_addr
        self.stmt_idx = state.scratch.stmt_idx
        self.ins_addr = state.scratch.ins_addr
        self.executed_instruction_count = state.history.recent_instruction_count
        self.gaurd = state.scratch.guard
        return self

class SimStateError(SimError):
    pass

class SimStateOptionsError(SimError):
    pass

class SimEngineError(SimError):
    pass

class SimMemoryError(SimStateError):
    pass

class SimTranslationError(SimEngineError):
    pass

class SimSolverError(SimError):
    pass

class SimValueError(SimSolverError):
    pass

class SimProcedureError(SimEngineError):
    pass

class SimUnsupportedError(SimError):
    pass

class QrtzUnsupportedSyscallError(QrtzSyscallError, SimProcedureError, SimUnsupportedError):
    pass

UnsupportedSyscallError = QrtzUnsupportedSyscallError
