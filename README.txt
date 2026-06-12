CSY3058 Media Technology -- Smart Security Camera System
=========================================================
University of Northampton | Assessment 1 (AS1)
Author: [Your Full Name] | Student ID: [Your Student ID]


FOLDER STRUCTURE
----------------
security_camera/
|
|-- main.py                  Run this file to start the system
|-- requirements.txt         Libraries needed
|-- motion_log.csv           Created automatically when you run
|
|-- src/
|   |-- config.py            All settings (sensitivity, colours, paths)
|   |-- motion_detector.py   Detects motion using MOG2
|   |-- tracker.py           Tracks objects with unique IDs
|   |-- categoriser.py       Classifies objects by size
|   |-- annotator.py         Draws boxes and alerts on frames
|   |-- recorder.py          Saves video clips
|   |-- logger.py            Writes CSV event log
|   |-- camera.py            Main controller (coordinates everything)
|
|-- security_clips/          Saved motion clips (created automatically)
|
|-- tests/
    |-- test_all.py          Run all tests


HOW TO INSTALL
--------------
1. Open Command Prompt or VS Code Terminal
2. Go to the security_camera folder:
   cd Desktop\security_camera

3. Install libraries:
   pip install -r requirements.txt


HOW TO RUN
----------
Live webcam:
   python main.py --source 0

Video file (put video in this folder first):
   python main.py --source warehouse.mp4

More sensitive detection:
   python main.py --source 0 --sensitivity 30

Less sensitive (fewer false alarms):
   python main.py --source 0 --sensitivity 80

Run without display window:
   python main.py --source warehouse.mp4 --no-window


HOW TO TEST
-----------
   python tests/test_all.py


WHAT HAPPENS WHEN YOU RUN IT
-----------------------------
1. Two windows open:
   - Main window: camera feed with status banner
   - Mask window: black/white motion detection view

2. When motion is detected:
   - Top banner turns RED with alert message
   - Coloured boxes appear around moving objects
   - Blue ID numbers track each object
   - Recording starts automatically

3. When motion stops:
   - Records 3 more seconds then stops
   - Saves .avi clip to security_clips/ folder
   - Writes event to motion_log.csv

4. Press Q to quit


OUTPUT FILES
------------
security_clips/motion_YYYYMMDD_HHMMSS.avi  -- Video clips of motion events
motion_log.csv                              -- Spreadsheet log of all events
