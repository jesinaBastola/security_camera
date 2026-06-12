import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
from src.tracker import CentroidTracker
from src.categoriser import ObjectCategoriser
from src.logger import MotionLogger

def test_config():
    print("Testing Config...", end=" ")
    assert Config.MIN_CONTOUR_AREA == 1500
    assert Config.OUTPUT_DIR == "security_clips"
    print("PASS")

def test_tracker_empty():
    print("Testing Tracker (empty)...", end=" ")
    t = CentroidTracker()
    assert t.update([]) == {}
    print("PASS")

def test_tracker_new():
    print("Testing Tracker (new object)...", end=" ")
    t = CentroidTracker()
    r = t.update([(100,100,50,80)])
    assert 0 in r and r[0] == (125,140)
    print("PASS")

def test_tracker_disappears():
    print("Testing Tracker (disappears)...", end=" ")
    t = CentroidTracker(max_disappeared=2)
    t.update([(100,100,50,50)])
    t.update([]); t.update([]); t.update([])
    assert len(t.objects) == 0
    print("PASS")

def test_categoriser_small():
    print("Testing Categoriser (small)...", end=" ")
    c = np.array([[[0,0]],[[30,0]],[[30,30]],[[0,30]]],dtype=np.int32)
    label, _ = ObjectCategoriser.categorise(c)
    assert label == "Small Object"
    print("PASS")

def test_categoriser_person():
    print("Testing Categoriser (person)...", end=" ")
    c = np.array([[[0,0]],[[100,0]],[[100,100]],[[0,100]]],dtype=np.int32)
    label, _ = ObjectCategoriser.categorise(c)
    assert label == "Person-Sized"
    print("PASS")

def test_categoriser_large():
    print("Testing Categoriser (large)...", end=" ")
    c = np.array([[[0,0]],[[250,0]],[[250,250]],[[0,250]]],dtype=np.int32)
    label, _ = ObjectCategoriser.categorise(c)
    assert label == "Large Object"
    print("PASS")

def test_logger():
    print("Testing Logger...", end=" ")
    Config.LOG_FILE = "test_log.csv"
    if os.path.exists("test_log.csv"): os.remove("test_log.csv")
    lg = MotionLogger()
    lg.log_event("MOTION_START", 2, "clip.avi")
    assert lg.total_events == 1
    os.remove("test_log.csv")
    Config.LOG_FILE = "motion_log.csv"
    print("PASS")

if __name__ == "__main__":
    print("\n" + "="*45)
    print("  CSY3058 -- Test Suite")
    print("="*45 + "\n")
    passed = 0
    for test in [test_config, test_tracker_empty, test_tracker_new,
                 test_tracker_disappears, test_categoriser_small,
                 test_categoriser_person, test_categoriser_large, test_logger]:
        try:
            test(); passed += 1
        except Exception as e:
            print(f"FAIL: {e}")
    print(f"\n  {passed}/8 tests passed!")
    print("="*45)