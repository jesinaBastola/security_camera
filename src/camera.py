"""
=============================================================================
camera.py -- Main Camera System Controller
CSY3058 Media Technology -- Smart Security Camera System

Fixed:
  - Video resized to 1280x720 for better performance
  - Window size is now nice and manageable
  - Runs much faster on 4K video files
=============================================================================
"""

import cv2
import os
import time

from src.config import Config
from src.motion_detector import MotionDetector
from src.tracker import CentroidTracker
from src.annotator import Annotator
from src.recorder import ClipRecorder
from src.logger import MotionLogger

# Display resolution -- change these if you want bigger or smaller window
DISPLAY_WIDTH  = 1280
DISPLAY_HEIGHT = 720


class SmartSecurityCamera:
    """
    Main orchestrator for the Smart Security Camera System.

    Supports two video input modes:
      - Live webcam:  --source 0
      - Video file:   --source warehouse.mp4

    Both modes use exactly the same detection pipeline.
    Video is resized to 1280x720 for performance and display.
    """

    def __init__(self, source):
        self.source = source
        self.detector = MotionDetector()
        self.tracker  = CentroidTracker()
        self.logger   = MotionLogger()

        print("\n" + "="*55)
        print("  CSY3058 -- Smart Security Camera System")
        print("  University of Northampton")
        print("="*55)

    def _open_video_source(self):
        """Open the video source -- webcam or video file."""
        src = 0 if self.source == "0" else self.source
        cap = cv2.VideoCapture(src)

        if not cap.isOpened():
            raise IOError(
                f"\n[ERROR] Cannot open video source: '{self.source}'\n"
                f"\n  If using webcam:     python main.py --source 0"
                f"\n  If using video file: python main.py --source warehouse.mp4"
                f"\n  Make sure the video file is in the security_camera folder!\n"
            )

        fps    = cap.get(cv2.CAP_PROP_FPS) or 25.0
        orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Use fixed display resolution for performance
        width  = DISPLAY_WIDTH
        height = DISPLAY_HEIGHT

        if self.source == "0":
            source_label = "Live Webcam"
        else:
            source_label = os.path.basename(self.source)

        print(f"\n  Source         : {source_label}")
        print(f"  Original Size  : {orig_w} x {orig_h}")
        print(f"  Display Size   : {width} x {height} (resized for performance)")
        print(f"  FPS            : {fps:.1f}")
        print(f"  Clips          : ./{Config.OUTPUT_DIR}/")
        print(f"  Log            : ./{Config.LOG_FILE}")
        print(f"\n  Press Q to quit")
        print("="*55 + "\n")

        return cap, fps, (width, height), source_label

    def run(self, show_window=True):
        """Main processing loop."""
        cap, fps, frame_size, source_label = self._open_video_source()
        recorder = ClipRecorder(fps, frame_size)

        frame_number = 0
        fps_timer    = time.time()
        display_fps  = fps

        while True:
            # Read next frame
            success, frame = cap.read()
            if not success:
                print("\n[INFO] End of video stream.")
                break

            # Resize frame to display resolution
            # This makes processing MUCH faster for 4K videos
            frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

            frame_number += 1

            # Calculate FPS every 30 frames
            if frame_number % 30 == 0:
                elapsed     = time.time() - fps_timer
                display_fps = 30 / elapsed if elapsed > 0 else fps
                fps_timer   = time.time()

            # STEP 1: Detect motion
            motion_detected, contours, mask = self.detector.detect(frame)

            # STEP 2: Track objects
            bounding_boxes  = [cv2.boundingRect(c) for c in contours]
            tracked_objects = self.tracker.update(bounding_boxes)

            # STEP 3: Annotate frame
            annotated_frame = Annotator.annotate(
                frame, contours, tracked_objects,
                motion_detected, frame_number,
                display_fps, self.logger.total_events,
                source_label
            )

            # STEP 4: Record if motion detected
            if motion_detected:
                if not recorder.recording:
                    recorder.start_recording()
                    self.logger.log_event(
                        "MOTION_START",
                        len(contours),
                        recorder.clip_path
                    )
                else:
                    recorder.post_count = 0
                recorder.write_frame(annotated_frame)

            elif recorder.recording:
                recorder.write_frame(annotated_frame)
                if not recorder.is_post_buffer_active():
                    self.logger.log_event("MOTION_END", 0, recorder.clip_path)
                    recorder.stop_recording()

            # STEP 5: Display windows
            if show_window:
                cv2.imshow("CSY3058 Smart Security Camera", annotated_frame)
                cv2.imshow("Motion Mask (MOG2 Output)", mask)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("\n[INFO] Quit by user.")
                    break

        # Cleanup
        if recorder.recording:
            recorder.stop_recording()

        cap.release()

        if show_window:
            cv2.destroyAllWindows()

        print(f"\n{'='*55}")
        print(f"  Session Complete!")
        print(f"  Total events logged : {self.logger.total_events}")
        print(f"  Clips saved in      : ./{Config.OUTPUT_DIR}/")
        print(f"  Audit log           : ./{Config.LOG_FILE}")
        print(f"{'='*55}\n")