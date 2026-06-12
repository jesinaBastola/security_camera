import math
import numpy as np
from collections import OrderedDict
from src.config import Config

class CentroidTracker:
    def __init__(self, max_disappeared=Config.MAX_DISAPPEARED):
        self.next_id     = 0
        self.objects     = OrderedDict()
        self.disappeared = OrderedDict()
        self.max_dis     = max_disappeared

    def _get_centroid(self, box):
        x, y, w, h = box
        return (int(x + w / 2), int(y + h / 2))

    def _register(self, centroid):
        self.objects[self.next_id] = centroid
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def _deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, bounding_boxes):
        if not bounding_boxes:
            for oid in list(self.disappeared.keys()):
                self.disappeared[oid] += 1
                if self.disappeared[oid] > self.max_dis:
                    self._deregister(oid)
            return self.objects

        new_centroids = [self._get_centroid(b) for b in bounding_boxes]

        if not self.objects:
            for centroid in new_centroids:
                self._register(centroid)
        else:
            existing_ids       = list(self.objects.keys())
            existing_centroids = list(self.objects.values())
            D = np.array([[math.dist(e, n) for n in new_centroids]
                          for e in existing_centroids])
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            matched_rows, matched_cols = set(), set()
            for row, col in zip(rows, cols):
                if row in matched_rows or col in matched_cols:
                    continue
                oid = existing_ids[row]
                self.objects[oid] = new_centroids[col]
                self.disappeared[oid] = 0
                matched_rows.add(row)
                matched_cols.add(col)
            for row in set(range(len(existing_ids))) - matched_rows:
                oid = existing_ids[row]
                self.disappeared[oid] += 1
                if self.disappeared[oid] > self.max_dis:
                    self._deregister(oid)
            for col in set(range(len(new_centroids))) - matched_cols:
                self._register(new_centroids[col])

        return self.objects