import math
pi = 3.14149265
class Point:
    """ Point class represents and manipulates x,y coords. """
    def __init__(self,x0,y0):
        """ Create a new point at the origin """
        self.x = x0
        self.y = y0

    def __repr__(self):
    	return("Point(%r, %r)" % ( (self.x), (self.y)))
	    
	 

    def addpoints(self, point1):

        xsum = self.x + point1.x
        ysum = self.y + point1.y
        ans = Point(xsum,ysum)
        return ans
    def findlength(self,otherpoint):
        return((((self.x - otherpoint.x)**2 + (self.y - otherpoint.y)**2 )**0.5))
class Pentagon:
    
    def __init__(self, A,point1, angle1,angle2):

        self.sideLengths = A
        self.P51 = point1
        self.P12 = Point(point1.x + A[0],0)
        self.P23 = 0
        self.P34 = 0
        self.P45 = 0

        self.theta51 = angle1  *0.0174533 # Converts deg to rad
        self.theta12 = angle2 * 0.0174533

    def __repr__(self):
    	print([self.P51, self.P12, self.P23, self.P34, self.P45])

    

    def findpointer(self):

        sideLengths = self.sideLengths
        P51 = self.P51
        P12 = self.P12
        theta51 = self.theta51
        theta12 = self.theta12

        
        P23 = Point(P12.x + sideLengths[1]* math.cos(pi - theta12),P12.y + sideLengths[1]* math.sin(pi - theta12))
        P45 = Point(P51.x - sideLengths[4]* math.cos(pi - theta51),P51.y + sideLengths[4]* math.sin(pi - theta51))
        self.P23 = P23
        self.P45 = P45
        #L53 = sideLengths[0] + sideLengths[4]*math.cos(pi - theta51) + sideLengths[1]* math.cos(pi - theta12)
        L53 = P23.findlength(P45)
        self.L53 =L53
        #print(P23.x - P45.x)
        #print(L53)
        #print((P23.x - P45.x)/L53)
        angle_Offset = -math.acos((P23.x - P45.x)/L53)
        #print(angle_Offset)
        
        theta34 = math.acos((L53**2 - sideLengths[3] **2 - sideLengths[2]**2)/(-2 * sideLengths[3] * sideLengths[2]))
        theta452 = angle_Offset + math.acos((sideLengths[2]**2 - sideLengths[3]**2 - L53**2)/(-2*sideLengths[3]*L53))
        theta232 = (math.acos((sideLengths[3]**2 - sideLengths[2]**2 - L53**2)/(-2*sideLengths[2]*L53)) - angle_Offset)
        P34 = Point(P45.x + sideLengths[3]*math.cos(theta452), P45.y + sideLengths[3]*math.sin(theta452))
        
       #print([P51,P12,P23,P34,P45])
        #print([theta51/.0174533,theta12/0.0174533,theta232/0.0174533,theta34/0.0174533,theta452/0.0174533])
        #print(P45)
        #print(theta452/0.0174533)
        return P34
        
    def findangles(self, A, endpoint):
        
        sideLengths = A
        P34 = endpoint
        P51 = Point(0,0)
        P12 = Point(A[0],0)

        L1 = P51.findlength(P34)
        L2 = P12.findlength(P34)


    	
        theta122 = math.acos((L1**2 - sideLengths[0]**2 - L2**2)/(-2*L2*sideLengths[0]))
        theta512 = math.acos((L2**2 - sideLengths[0]**2 - L1**2)/(-2*sideLengths[0]*L1))
        theta511 = math.acos((sideLengths[3]**2 - sideLengths[4]**2 - L1**2)/(-2*L1*sideLengths[4]))
        theta121 = math.acos((sideLengths[2]**2 - sideLengths[1]**2 - L2**2)/(-2*sideLengths[1]*L2))

        theta12 = theta122 + theta121
        theta51 = theta512 + theta511

        newPent = Pentagon(A,P51,theta51,theta12)

        return [theta51/0.0174533,theta12/0.0174533]




a = Point(0,0)
d = Point(0.49,1.55)
test = Pentagon([6.75,6,5.625,5.625,5.875],a,130,90)

print(test.findpointer())

newangles = test.findangles([6.75,6,5.625,5.625,5.875],Point(4,8))
print(newangles)
#test = Pentagon([1,1,1,1,1],a , newangles[0],newangles[1])

#print(test.findpointer())




