from pocketfurnace.math.vector.Vector3 import Vector3


class RayTraceResult:
    bb = None
    hit_face = None
    hit_vector = None

    def __init__(self, bb, hitFace: int, hitVector: Vector3):
        self.bb = bb
        self.hit_face = hitFace
        self.hit_vector = hitVector

    def get_bounding_box(self):
        return self.bb

    def get_hit_face(self) -> int:
        return self.hit_face

    def get_hit_vector(self) -> Vector3:
        return self.hit_vector
