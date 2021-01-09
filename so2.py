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

    def inv(self, Jr=False, Jl=False):
        if Jr or Jl:
            J = -1
            return SO2(self.arr.T), J
        else:
            return SO2(self.arr.T)

    def rota(self, v, Jr=False, Jl=False):
        assert v.size == 2
        if Jr:
            J = self.R @ G @ v
            return self.R @ v, J
        elif Jl:
            J = G @ self.R @ v
            return self.R @ v, J
        else:
            return self.R @ v

    def rotp(self, v):
        assert v.size == 2
        return self.inv().arr @ v

    def boxplusr(self, w):
        return self * SO2.Exp(w)

    def boxminusr(self, R2):
        assert isinstance(R2, SO2)
        return SO2.Log(R2.inv() * self)

    def boxplusl(self, w):
        return SO2.Exp(w) * self

    def boxminusl(self, R):
        assert isinstance(R, SO2)
        return SO2.Log(self * R.inv())

    def compose(self, R, Jr=False, Jl=False, Jr2=False, Jl2=False):
        res = self * R
        if Jr or Jr2:
            return res, R.inv().Adj
        elif Jl or Jl2:
            return res, 1.0
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
    def exp(cls, theta_x, Jr=False, Jl=False):
        assert theta_x.shape == (2,2)
        theta = theta_x[1,0]
        if Jr:
            return cls.fromAngle(theta), 1.0
        if Jl:
            return cls.fromAngle(theta), 1.0
        return cls.fromAngle(theta)

    @classmethod
    def Exp(cls, theta, Jr=False, Jl=False):
        logR = cls.hat(theta)
        if Jr:
            R, J = cls.exp(logR, Jr)
            return R, J
        if Jl:
            R, J = cls.exp(logR, Jl)
            return R, J
        return cls.exp(logR)

    @staticmethod
    def Identity():
        return SO2(np.eye(2))

    @staticmethod
    def log(R, Jr=False, Jl=False):
        assert isinstance(R, SO2)
        theta = np.arctan2(R.arr[1,0], R.arr[0,0])
        if Jr:
            return G * theta, 1.0
        if Jl:
            return G * theta, 1.0
        return G * theta

    @classmethod
    def Log(cls, R, Jr=False, Jl=False):
        if Jr:
            logR, J = cls.log(R, Jr)
            return logR, J
        if Jl:
            logR, J = cls.log(R,Jl)
            return logR, J
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
