import cv2
from datetime import datetime
from src.config import Config
from src.categoriser import ObjectCategoriser

class Annotator:
    @staticmethod
    def annotate(frame, contours, tracked_objects, motion,
                 frame_number, fps, total_events, source_name):
        output = frame.copy()
        height, width = output.shape[:2]
        font = Config.FONT

        if motion:
            cv2.rectangle(output, (0, 0), (width, 48), (0, 0, 180), -1)
            cv2.putText(output,
                "  !! MOTION DETECTED  --  UNAUTHORIZED ACCESS ALERT !!",
                (8, 32), font, 0.68, Config.WHITE, 2)
        else:
            cv2.rectangle(output, (0, 0), (width, 40), (0, 120, 40), -1)
            cv2.putText(output,
                "  Monitoring  --  No Motion Detected",
                (8, 27), font, 0.65, Config.WHITE, 1)

        for contour in contours:
            x, y, box_w, box_h = cv2.boundingRect(contour)
            label, colour = ObjectCategoriser.categorise(contour)
            cv2.rectangle(output, (x, y), (x + box_w, y + box_h), colour, 2)
            area = int(cv2.contourArea(contour))
            cv2.putText(output, f"{label} ({area}px)",
                (x, max(y - 6, 15)), font, 0.45, colour, 1)

        for object_id, (cx, cy) in tracked_objects.items():
            cv2.circle(output, (cx, cy), 5, Config.BLUE, -1)
            cv2.putText(output, f"ID:{object_id}",
                (cx + 8, cy - 8), font, 0.40, Config.BLUE, 1)

        cv2.rectangle(output, (0, height - 42), (width, height), (20, 20, 20), -1)
        timestamp = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        cv2.putText(output, timestamp,           (8,   height-26), font, 0.48, Config.GREEN, 1)
        cv2.putText(output, f"Source:{source_name}", (8, height-10), font, 0.36, Config.GREEN, 1)
        cv2.putText(output, f"Frame:{frame_number}", (270,height-10), font, 0.36, Config.GREEN, 1)
        cv2.putText(output, f"FPS:{fps:.0f}",     (400, height-10), font, 0.36, Config.GREEN, 1)
        cv2.putText(output, f"Events:{total_events}",(470,height-10),font, 0.36, Config.GREEN, 1)
        cv2.putText(output, "Press Q to quit", (width-175, height-10), font, 0.36, (160,160,160), 1)

        return output