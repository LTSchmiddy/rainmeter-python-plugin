# This class isn't meant to do anything. It simply provides a type definition
# for the native Rainmeter type to aid with autocompletion.

# Could also be used as a wrapper class for Rainmeter But, since they has the
# same structure, not much point.


class RainmeterW:
    def __init__(self, rm):
        self.rm = rm

    @property
    def LOG_ERROR(self) -> int:
        return self.rm.LOG_ERROR

    @property
    def LOG_WARNING(self) -> int:
        return self.rm.LOG_WARNING

    @property
    def LOG_NOTICE(self) -> int:
        return self.rm.LOG_NOTICE

    @property
    def LOG_DEBUG(self) -> int:
        return self.rm.LOG_DEBUG

    def RmReadString(
        self, option: str, default: str, replaceMeasures: bool = False
    ) -> str:
        return self.rm.RmReadString(option, default, replaceMeasures)

    def RmReadPath(self, option: str, default: str) -> str:
        return self.rm.RmReadPath(option, default)

    def RmReadDouble(self, option: str, default: float) -> float:
        return self.rm.RmReadPath(option, default)

    def RmReadInt(self, option: str, default: int) -> int:
        return self.rm.RmReadPath(option, default)

    def RmGetMeasureName(self):
        return self.rm.RmGetMeasureName()

    def RmExecute(self, commandStr: str):
        return self.rm.RmExecute(commandStr)

    def RmLog(self, level: int, message: str):
        return self.rm.RmLog(level, message)
