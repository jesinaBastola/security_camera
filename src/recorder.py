import cv2
import os
from datetime import datetime
from src.config import Config

class ClipRecorder:
    def __init__(self, fps, frame_size):
        self.fps        = max(fps, 15.0)
        self.frame_size = frame_size
        self.writer     = None
        self.clip_path  = None
        self.recording  = False
        self.post_count = 0
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    def start_recording(self):
        if self.recording:
            return
        timestamp      = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.clip_path = os.path.join(Config.OUTPUT_DIR, f"motion_{timestamp}.avi")
        fourcc         = cv2.VideoWriter_fourcc(*"XVID")
        self.writer    = cv2.VideoWriter(
            self.clip_path, fourcc, self.fps, self.frame_size)
        self.recording  = True
        self.post_count = 0
        print(f"  [REC START] Saving --> {self.clip_path}")

    def write_frame(self, frame):
        if self.writer:
            self.writer.write(frame)

    def is_post_buffer_active(self):
        self.post_count += 1
        return self.post_count < Config.POST_MOTION_FRAMES

    def stop_recording(self):
        if self.writer:
            self.writer.release()
            self.writer = None
            print(f"  [REC SAVED] Clip --> {self.clip_path}")
        self.recording  = False
        self.post_count = 0