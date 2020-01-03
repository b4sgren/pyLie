import unittest
import sys 
sys.path.append('..')
from so2 import SO2
import numpy as np

from IPython.core.debugger import Pdb

class SO2Test(unittest.TestCase):

    def testExp(self):
        for i in range(100):
            theta = np.random.uniform(-np.pi, np.pi)
            logR = np.array([[0, -theta], [theta, 0]])
            R = SO2.exp(logR)
            R_true = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
            np.testing.assert_allclose(R_true, R.arr)

    def testLog(self):
        for i in range(100):
            theta = np.random.uniform(-np.pi, np.pi)
            R = SO2.fromAngle(theta)
            logR_true = np.array([[0, -theta], [theta, 0]])
            logR = SO2.log(R)
            np.testing.assert_allclose(logR_true, logR)

    def testHat(self):
        for i in range(100):
            theta = np.random.uniform(-np.pi, np.pi)
            logR_true = np.array([[0, -theta], [theta, 0]])
            logR = SO2.hat(theta)
            np.testing.assert_allclose(logR_true, logR)

    def testVee(self):
        for i in range(100):
            theta_true = np.random.uniform(-np.pi, np.pi)
            R = SO2.fromAngle(theta_true)
            theta = SO2.vee(SO2.log(R))
            self.assertAlmostEqual(theta, theta_true)
    
    def testMul(self):
        for i in range(100):
            theta1 = np.random.uniform(-np.pi, np.pi)
            theta2 = np.random.uniform(-np.pi, np.pi)
            R1 = SO2.fromAngle(theta1)
            R2 = SO2.fromAngle(theta2)
            R = R1 * R2
            theta_true = theta1 + theta2
            if theta_true > np.pi:
                theta_true -= 2 * np.pi 
            if theta_true < -np.pi:
                theta_true += 2 * np.pi
            R_true = np.array([[np.cos(theta_true), np.sin(theta_true)], [-np.sin(theta_true), np.cos(theta_true)]])
            np.testing.assert_allclose(R_true, R.arr)
        
        for i in range(100):
            theta = np.random.uniform(-np.pi, np.pi)
            R = SO2.fromAngle(theta)

            pt = np.random.uniform(-5, 5, size=2)
            rot_pt = R * pt

            x_true = np.cos(theta) * pt[0] + np.sin(theta) * pt[1]
            y_true = -np.sin(theta) * pt[0] + np.cos(theta) * pt[1]
            rot_pt_true = np.array([x_true, y_true])

            np.testing.assert_allclose(rot_pt_true, rot_pt)

    def testInv(self):
        for i in range(100):
            theta = np.random.uniform(-np.pi, np.pi)
            R = SO2.fromAngle(theta)
            mat = R.arr 

            R_inv_true = np.linalg.inv(mat)
            R_inv = R.inv()

            np.testing.assert_allclose(R_inv_true, R_inv.arr)

if __name__=="__main__":
    unittest.main()