import numpy as np

G = np.array([[0, -1], [1, 0]])

class SO2:
    def __init__(self, R):
        assert R.shape == (2,2)
        self.arr = R

    def __mul__(self, R2):
        assert isinstance(R2, SO2)
        return SO2(self.arr @ R2.arr)

    def __str__(self):
        return str(self.R)

    def __repr__(self):
        return str(self.R)

    def inv(self, Jr=None, Jl=None):
        if Jr:
            J = -1
            return SO2(self.arr.T), J * Jr
        elif Jl:
            J = -1
            return SO2(self.arr.T), J * Jl
        else:
            return SO2(self.arr.T)

    def rota(self, v, Jr=None, Jl=None):
        assert v.size == 2
        if Jr:
            J = self.R @ G @ v
            return self.R @ v, J * Jr
        elif Jl:
            J = G @ self.R @ v
            return self.R @ v, J * Jl
        else:
            return self.R @ v

    def rotp(self, v, Jr=None, Jl=None):
        assert v.size == 2
        if Jr:
            R_inv, J = self.inv(Jr=Jr)
            vp, J = R_inv.rota(v, Jr=J)
            return vp, J
        elif Jl:
            R_inv, J = self.inv(Jl=Jl)
            vp, J = R_inv.rota(v, Jl=J)
            return vp, J
        else:
            return self.inv().rota(v)

    # For the boxplus I'm not sure I need the jacobian wrt the first element ever. I can add it later if I need to
    def boxplusr(self, w, Jr=None, Jl=None):
        if Jr:
            R2, J = SO2.Exp(w, Jr=Jr)
            return self.compose(R2, Jr2=J)
        elif Jl:
            R2, J = SO2.Exp(w, Jl=Jl)
            return self.compose(R2, Jl2=J)
        else:
            return self * SO2.Exp(w)

    def boxminusr(self, R2, Jr1=None, Jl1=None, Jr2=None, Jl2=None):
        assert isinstance(R2, SO2)
        if Jr1 is not None:
            dR, J = R2.inv().compose(self, Jr2=Jr1)
            return SO2.Log(dR, Jr=J)
        elif Jl1 is not None:
            dR, J = R2.inv().compose(self, Jl2=Jl1)
            return SO2.Log(dR, Jl=J)
        elif Jr2 is not None:
            R2_inv, J = R2.inv(Jr=Jr2)
            dR, J = R2_inv.compose(self, Jr=J)
            return SO2.Log(dR, Jr=J)
        elif Jl2 is not None:
            R2_inv, J = R2.inv(Jl=Jl2)
            dR, J = R2.inv().compose(self, Jl=J)
            return SO2.Log(dR, Jl=J)
        else:
            return SO2.Log(R2.inv() * self)

    def boxplusl(self, w, Jr=None, Jl=None):
        if Jr is not None:
            R, J = SO2.Exp(w, Jr=Jr)
            return R.compose(self, Jr=J)
        elif Jl is not None:
            R, J = SO2.Exp(w, Jl=Jl)
            return R.compose(self, Jl=J)
        else:
            return SO2.Exp(w) * self

    def boxminusl(self, R, Jr1=None, Jl1=None, Jr2=None, Jl2=None):
        assert isinstance(R, SO2)
        if Jr1 is not None:
            temp, J = self.compose(R.inv(), Jr=Jr1)
            return SO2.Log(temp, Jr=J)
        elif Jl1 is not None:
            temp, J = self.compose(R.inv(), Jl=Jl1)
            return SO2.Log(temp, Jl=J)
        elif Jr2 is not None:
            R_inv, J = R.inv(Jr=Jr2)
            temp, J = self.compose(R_inv, Jr2=J)
            return SO2.Log(temp, Jr=J)
        elif Jl2 is not None:
            R_inv, J = R.inv(Jl=Jl2)
            temp, J = self.compose(R_inv, Jl2=J)
            return SO2.Log(temp, Jl=J)
        else:
            return SO2.Log(self * R.inv())

    def compose(self, R, Jr=None, Jl=None, Jr2=None, Jl2=None):
        res = self * R
        if Jr:
            return res, R.inv().Adj * Jr
        elif Jr2:
            return res, R.inv().Adj * Jr2
        elif Jl:
            return res, 1.0 * Jl
        elif Jl2:
            return res, 1.0 * Jl2
        else:
            return res

    @property
    def R(self):
        return self.arr

    @classmethod
    def fromAngle(cls, theta):
        ct = np.cos(theta)
        st = np.sin(theta)
        R = np.array([[ct, -st], [st, ct]])
        return cls(R)

    @classmethod
    def exp(cls, theta_x, Jr=None, Jl=None):
        assert theta_x.shape == (2,2)
        theta = theta_x[1,0]
        if Jr:
            return cls.fromAngle(theta), 1.0 * Jr
        if Jl:
            return cls.fromAngle(theta), 1.0 * Jl
        return cls.fromAngle(theta)

    @classmethod
    def Exp(cls, theta, Jr=None, Jl=None):
        logR = cls.hat(theta)
        if Jr:
            R, J = cls.exp(logR, Jr=Jr)
            return R, J
        elif Jl:
            R, J = cls.exp(logR, Jl=Jl)
            return R, J
        else:
            return cls.exp(logR)

    @staticmethod
    def Identity():
        return SO2(np.eye(2))

    @staticmethod
    def log(R, Jr=None, Jl=None):
        assert isinstance(R, SO2)
        theta = np.arctan2(R.arr[1,0], R.arr[0,0])
        if Jr:
            return G * theta, 1.0 * Jr
        elif Jl:
            return G * theta, 1.0 * Jl
        else:
            return G * theta

    @classmethod
    def Log(cls, R, Jr=None, Jl=None):
        if Jr:
            logR, J = cls.log(R, Jr)
            return logR, J * Jr
        elif Jl:
            logR, J = cls.log(R,Jl)
            return logR, J * Jl
        else:
            logR = cls.log(R)
            return cls.vee(logR)

    @staticmethod
    def vee(theta_x):
        assert theta_x.shape == (2,2)
        return theta_x[1,0]

    @staticmethod
    def hat(theta):
        return theta * G

    @property
    def Adj(self):
        return 1.0

    @classmethod
    def random(cls):
        theta = np.random.uniform(-np.pi, np.pi)
        return cls.fromAngle(theta)
