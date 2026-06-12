import cv2

class Config:
    MIN_CONTOUR_AREA   = 1500
    GAUSSIAN_BLUR      = (21, 21)
    BG_HISTORY         = 500
    BG_VAR_THRESHOLD   = 50
    SIZE_SMALL         = 3000
    SIZE_PERSON        = 30000
    POST_MOTION_FRAMES = 90
    OUTPUT_DIR         = "security_clips"
    LOG_FILE           = "motion_log.csv"
    MAX_DISAPPEARED    = 30
    GREEN  = (0, 200, 80)
    RED    = (0, 0, 220)
    YELLOW = (0, 220, 220)
    WHITE  = (255, 255, 255)
    BLUE   = (200, 100, 0)
    ORANGE = (0, 100, 255)
    FONT   = cv2.FONT_HERSHEY_SIMPLEX