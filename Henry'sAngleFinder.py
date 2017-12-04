from scipy.optimize import brenth
from math import *
import numpy as np
from time import time

np.set_printoptions(linewidth=200)

#base:
thetaB = radians(38.27)
rB     = 4.0-5.0/16.0

#top:
thetaT = radians(20.45)
rT     = 3.46;

k = np.array([0,0,1,0])

legLen = 12.0 + 5.0/8.0
hornRad = 1

mins =[620,2310,810,2280,540,2260]
maxs =[2080,850,2270,820,2000,800]

def rescale(a, minb, maxb, mina, maxa):
 return (a-minb)/(maxb-minb)*(maxa-mina)+mina

def buildModel(r, theta):
  phi = (2*pi - 3*theta)/3
  model = []
  for i in range(3):
    model.append([r*cos(i*(phi+theta)-theta/2),r*sin(i*(phi+theta)-theta/2),0,1])
    model.append([r*cos(i*(phi+theta)+theta/2),r*sin(i*(phi+theta)+theta/2),0,1])
  return np.transpose(model)

botPts = buildModel(rB, thetaB)
topPts = buildModel(rT, thetaT)

def transform(x,y,z,ux,uy,uz):
  norm = sqrt(ux**2 + uy**2 + uz**2)
  ux /= norm;
  uy /= norm;
  uz /= norm;
  d = sqrt(ux**2 + uz**2)
  mat = [[uz/d,-ux*uy/d,ux,x],[0,d,uy,y],[-ux/d,-uy*uz/d,uz,z],[0,0,0,1]]
  return np.array(mat)

def getTop(x,y,z,ux,uy,uz):
  return transform(x,y,z,ux,uy,uz).dot(topPts)

def ei(n):
  j = botPts[0:3,n]
  j = j/np.linalg.norm(j,,,)
  return np.array([j[1],-j[0],0,0])*(-1)**n


def getLen(theta, n, topPos):
  top = topPos[0:4,n];
  base = botPts[0:4,n];
  ePos = np.add(np.add(base,ei(n)*cos(theta)*hornRad),k*sin(theta)*hornRad)
  return np.linalg.norm(np.subtract(top,ePos))-legLen

def findAngles(x,y,z,ux,uy,uz):
  thetas = [0,0,0,0,0,0]
  topPos = getTop(x,y,z,ux,uy,uz)
  for i in range(6):
    thetas[i] = brenth(getLen, radians(-70), radians(70), disp = True, args =(i,topPos), xtol = 1e-3)
   # thetas[i] = int(round(rescale(thetas[i], radians(-70), radians(70), mins[i], maxs[i])))
  return thetas

if __name__ == '__main__':
  before = time()
  angles = findAngles(0,2,12.43,0,0,0)
  after = time()
  print(after-before)
  print(angles)