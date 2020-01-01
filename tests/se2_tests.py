import unittest
import sys 
sys.path.append("..")
import numpy as np 
from se2 import SE2 

class SE2_Test(unittest.TestCase):
    def testInv(self):
        for i in range(100):
            t = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)
            ct = np.cos(theta)
            st = np.sin(theta)
            R = np.array([[ct, -st], [st, ct]])

            T = SE2(R, t)
            T_inv = T.inv()
            T_inv_true = np.eye(3)
            T_inv_true[:2, :2] = R.T 
            T_inv_true[:2, 2] = -R.T @ t 

            np.testing.assert_allclose(T_inv_true, T_inv.arr)
    
    def testGroupOperator(self):
        for i in range(100):
            t1 = np.random.uniform(-10, 10, size=2)
            theta1 = np.random.uniform(-np.pi, np.pi)
            t2 = np.random.uniform(-10, 10, size=2)
            theta2 = np.random.uniform(-np.pi, np.pi)

            ct1 = np.cos(theta1)
            ct2 = np.cos(theta2)
            st1 = np.sin(theta1)
            st2 = np.sin(theta2)
            R1 = np.array([[ct1, -st1], [st1, ct1]])
            R2 = np.array([[ct2, -st2], [st2, ct2]])
            
            T1 = SE2(R1, t1)
            T2 = SE2(R2, t2)
            T = T1 * T2
            
            R_true = R1 @ R2
            t_true = R1 @ t2 + t1
            T_true = SE2(R_true, t_true)

            np.testing.assert_allclose(T_true.arr, T.arr)
    
    def testLog(self):
        for i in range(100):
            t = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)

            ct = np.cos(theta)
            st = np.sin(theta)
            R = np.array([[ct, -st], [st, ct]])

            T = SE2(R, t)
            logT = SE2.log(T)

            logT_true = np.zeros((3,3)) 
            logT_true[0,1] = -theta
            logT_true[1,0] = theta
            V = 1/theta * np.array([[st, ct - 1], [1 - ct, st]])
            logT_true[:2,2] = np.linalg.inv(V) @ t 
            logT_true[2,2] = 1

            np.testing.assert_allclose(logT_true, logT)

    def testExp(self):
        for i in range(100):
            v = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)

            logT = np.array([[0, -theta, v[0]],
                            [theta, 0, v[1]],
                            [0, 0, 1]])
            
            T = SE2.exp(logT)

            T_true = np.eye(3)
            ct = np.cos(theta)
            st = np.sin(theta)
            T_true[:2,:2] = np.array([[ct, -st], [st, ct]])
            T_true[0,2] = (v[1] * (ct - 1)+ v[0] * st)/theta
            T_true[1,2] = (v[0] * (1 - ct) + v[1] * st)/theta

            np.testing.assert_allclose(T_true, T.arr)
    
    def testVee(self):
        for i in range(100):
            u = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)

            arr_true = np.array([u[0], u[1], theta])
            X = np.array([[0, -theta, u[0]], [theta, 0, u[1]], [0, 0, 1]])
            arr = SE2.vee(X)

            np.testing.assert_allclose(arr_true, arr)
    
    def testHat(self):
        for i in range(100):
            u = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)

            arr = np.array([u[0], u[1], theta])
            X_true = np.array([[0, -theta, u[0]], [theta, 0, u[1]], [0, 0, 0]])
            X = SE2.hat(arr)

            np.testing.assert_allclose(X_true, X)
    
    def testAdjoint(self): 
        for i in range(100):
            t = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)

            ct = np.cos(theta)
            st = np.sin(theta)
            R = np.array([[ct, -st], [st, ct]])
            T = SE2(R, t)
            adj = T.Adj()

            adj_true = np.eye(3)
            adj_true[:2, :2] = R 
            adj_true[0, 2] = t[1]
            adj_true[1, 2] = -t[0]

            np.testing.assert_allclose(adj_true, adj)
    
    def testRotateTangentVector(self):
        for i in range(100):
            t = np.random.uniform(-10, 10, size=2)
            theta = np.random.uniform(-np.pi, np.pi)
            u = np.random.uniform(-1, 1, size=2)
            phi = np.random.uniform(-np.pi, np.pi)
            delta = np.array([u[0], u[1], phi])

            ct = np.cos(theta)
            st = np.sin(theta)
            R = np.array([[ct, -st], [st, ct]])
            T = SE2(R, t)
            
            adj = T.Adj()

            delta_rot = adj @ delta
            delta_rot_true = np.array([0, 0, phi])
            delta_rot_true[:2] = R @ u + phi * np.array([t[1], -t[0]])

            np.testing.assert_allclose(delta_rot_true, delta_rot)

if __name__=="__main__":
    unittest.main()