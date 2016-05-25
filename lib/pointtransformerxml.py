from pointtransformer import PointTransformer

class PointTransformerXML(PointTransformer):


    def point2text(self, l, id = None):
        i = ""
        if id is not None:
            i = " id='" + id + "'"

        return "<point" + i + " x='" + str(l[0]) + "' y='" + str(l[1]) + "' />"

    def face2text(self, l, id = None):
        i = ""
        if id is not None:
            i = " id='" + id + "'"

        s = "<face" + i + ">"
        if len(l) == 1:
            s += self.point2text(l[0])

        else:
            for pc, point in enumerate(l):
                s += self.point2text(point, str(pc))

        s += "</face>"
        return s

    def img2text(self, l, id = None):
        i = ""
        if id is not None:
            i = " id='" + id + "'"

        s = "<img" + i + ">"
        if len(l) == 1:
            s += self.face2text(l[0])

        else:
            for fc, face in enumerate(l):
                s += self.face2text(face, str(fc))

        s += "</img>"
        return s


    def vid2text(self, l):
        s = "<video>"
        for fc, frame in enumerate(l):
            s += self.img2text(frame, str(fc))

        s += "</video>"

        return s