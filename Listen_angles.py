from scipy.optimize import brenth
from math import *
import numpy as np
from time import time
from random import *
from pickle import dump
from keras.models import load_model
x_model = load_model('x_net.h5')
y_model = load_model('y_net.h5')
z_model = load_model('z_net.h5')
a_model = load_model('a_net.h5')
b_model = load_model('b_net.h5')
c_model = load_model('c_net.h5')
models = [x_model, y_model, z_model, a_model, b_model, c_model]


np.set_printoptions(linewidth=200)

#base:
thetaB = radians(38.278) #angle of the base
rB     = 2.4

#top:
thetaT = radians(40.31)
rT     = 2.13;

k = np.array([0,0,1,0])

legLen = 4.849 #inches
hornRad = 45 / 25.4

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
  # j is the component vectors here
  j = botPts[0:3,n]
  # print(n)
  # normalizes unit vector
  j = j/np.linalg.norm(j)#*radians(90)
  if (n%2 == 0):
    theta = np.radians(9.15)
  else:
       theta = np.radians(-9.15)
  c, s = np.cos(theta), np.sin(theta)
  R = np.array([[c, -s, 0], [s, c,0], [0,0,1]])
  # print('before', j)
  #print(R)
  j = R.dot(j.T)

  # print('after', j)
  # TODO: add rotational matrix to rotate j, in the form [i, j, k]
  # print (np.array([j[1],-j[0],0,0])*(-1)**n)
  #print(np.array([j[1],-j[0],0,0])*(-1)**n)
  j = np.array([j[1],-j[0],0,0])*(-1)**n
  # print('return', j)
  return j


def getLen(theta, n, topPos):
  top = topPos[0:4,n];
  base = botPts[0:4,n];
  ePos = np.add(np.add(base,ei(n)*cos(theta)*hornRad),k*sin(theta)*hornRad)
  return np.linalg.norm(np.subtract(top,ePos))-legLen

def findAngles(x,y,z,ux,uy,uz):
  thetas = [0,0,0,0,0,0]
  topPos = getTop(x,y,z,ux,uy,uz)
  for i in range(6):
      try:
          thetas[i] = brenth(getLen, radians(-70), radians(70), disp = True, args =(i,topPos), xtol = 1e-3)
          thetas[i] = degrees(thetas[i])
      except ValueError:
         return("out of range!")


#    thetas[i] = int(round(rescale(thetas[i], radians(-70), radians(70), mins[i], maxs[i])))
  return thetas

def findPosition(angles):
    angles_array = np.array([angles])
    return [models[i].predict(angles_array) for i in range(len(models))]


if __name__ == '__main__':
    csv_data = []
    count = 0
    n = 10000
    t = 10
  
    for i in range(n):
      before = time()
      x = random()*4.5-2.25
      y = random()*4.5-2.25
      z = legLen + random()*hornRad*0.75
      a = np.sin(radians(random()*2*t-t))
      b = np.sin(radians(random()*2*t-t))
      c = np.cos(radians(random()*2*t-t))
      angles = findAngles(x,y,z,a,b,c)
      after = time()
    #  print(after-before)
      if (len(angles) == 6):
          count = count + 1
    # print(str(float(count)/n) + "angles")


    # f = open("LUT.txt", "wb")
    # dump(csv_data, f)
    # f.close

