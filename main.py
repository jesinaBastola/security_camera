"""
CSY3058 Media Technology - Assessment 1
Smart Security Camera System
Author: Jesina Batola
Student ID: 24812923
"""

import argparse
from src.config import Config
from src.camera import SmartSecurityCamera

def main():
    parser = argparse.ArgumentParser(description="CSY3058 Smart Security Camera")
    parser.add_argument("--source",      default="0",
                        help="'0' for webcam or video filename e.g. warehouse.mp4")
    parser.add_argument("--sensitivity", type=int, default=50)
    parser.add_argument("--min-area",    type=int, default=1500)
    parser.add_argument("--no-window",   action="store_true")
    args = parser.parse_args()
    Config.BG_VAR_THRESHOLD = args.sensitivity
    Config.MIN_CONTOUR_AREA = args.min_area
    camera = SmartSecurityCamera(args.source)
    camera.run(show_window=not args.no_window)

if __name__ == "__main__":
    main()