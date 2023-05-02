from __future__  import annotations
# the `Adapter` pattern is designed to interact with existing code;
# Adapters are used to allow two preexisting objects to work together, even if
# their interfaces are not compatible;
""" the `Adapter` pattern """
# the `Adapter` pattern is similar to a simplified decorator pattern;
# Decorators typically provide the same interface that they replace,
# whereas adapters map between two different interfaces;
class TimeSince:
    """Expects time as six digits, no punctuation."""
    def parse_time(self, time: str) -> tuple[float, float, float]:
        return (
            float(time[0:2]),
            float(time[2:4]),
            float(time[4:]),
        )

    def __init__(self, starting_time: str) -> None:
        self.hr, self.min, self.sec = self.parse_time(starting_time)
        self.start_seconds = ((self.hr * 60) + self.min) * 60 + self.sec

    def interval(self, log_time: str) -> float:
        log_hr, log_min, log_sec = self.parse_time(log_time)
        log_seconds = ((log_hr * 60) + log_min) * 60 + log_sec
        return log_seconds - self.start_seconds
# Log started at 00:01:23
ts = TimeSince("000123")
print(
    ts.interval("020304")
)
data = [
    ("000123", "INFO", "Gila Flats 1959-08-20"),
    ("000142", "INFO", "test block 15"),
    ("004201", "ERROR", "intrinsic field chamber door locked"),
    ("004210.11", "INFO", "generator power active"),
    ("004232.33", "WARNING", "extra mass detected")
]
#
class LogProcessor:
    def __init__(
        self,
        log_entries: list[tuple[str, str, str]]
    ) -> None:
        self.log_entries = log_entries
        self.time_convert = IntervalAdapter()

    def report(self) -> None:
        first_time, first_sev, first_msg = self.log_entries[0]
        for log_time, severity, message in self.log_entries:
            if severity == "ERROR":
                first_time = log_time
            interval = self.time_convert.time_offset(first_time, log_time)
            print(f"{interval:8.2f} | {severity:7s} {message}")


class IntervalAdapter:
    def __init__(self) -> None:
        self.ts: Optional[TimeSince] = None

    def time_offset(self, start: str, now: str) -> float:
        if self.ts is None:
            self.ts = TimeSince(start)
        else:
            h_m_s = self.ts.parse_time(start)
            if h_m_s != (self.ts.hr, self.ts.min, self.ts.sec):
                self.ts = TimeSince(start)
        return self.ts.interval(now)
#
log_proc = LogProcessor(data)
print(
    log_proc.report()
)
#
