import csv
import os
from datetime import datetime
from src.config import Config

class MotionLogger:
    def __init__(self):
        self.log_path    = Config.LOG_FILE
        self.event_count = 0
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["Event","Timestamp","Objects Detected","Clip File"])

    def log_event(self, event_type, num_objects=0, clip_file=""):
        self.event_count += 1
        with open(self.log_path, "a", newline="") as f:
            csv.writer(f).writerow(
                [event_type, datetime.now().isoformat(), num_objects, clip_file])

    @property
    def total_events(self):
        return self.event_count