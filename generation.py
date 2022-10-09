# coding:utf-8
import rhinoscriptsyntax as rs
import random
        
#################################################
# Axis class
#################################################
class Axis(object):
    def __init__(
            self, 
            parentEP, 
            parentAxises, 
            angleXZ, 
            angleXY
            ):
        self.parentEP = parentEP
        self.parentAxises = parentAxises
        self.angleXZ = angleXZ
        self.angleXY = angleXY
                
        self.axises = []
        self.setAxis()
            
    def setAxis(self):
        # XZ
        newAxises1 = []
        for axis in self.parentAxises:
            newAxis = rs.VectorRotate(axis, self.angleXZ, self.parentAxises[1])
            newAxises1.append(newAxis)
        # XY
        newAxises2 = []
        for axis in newAxises1:
            newAxis = rs.VectorRotate(axis, self.angleXY, self.parentAxises[2])
            newAxises2.append(newAxis)
                
        self.axises = newAxises2
            
    def draw(self):
        guids = [] 
        # x
        x = rs.VectorAdd(self.parentEP,self.axises[0])
        guid = rs.AddLine(self.parentEP, x)
        guids.append(guid)
                
        # y
        y = rs.VectorAdd(self.parentEP,self.axises[1])
        guid = rs.AddLine(self.parentEP, y)
        guids.append(guid)
                
        # z
        z = rs.VectorAdd(self.parentEP,self.axises[2])
        guid = rs.AddLine(self.parentEP, z)
        guids.append(guid)
                
        return guids
                
#################################################
# Branch class
#################################################
class Branch(object):
    def __init__(
            self, 
            maxN,
            n,
            no,
            parentEP, 
            parentLength, 
            parentAxises,
            angleXZ,
            angleXY,
            scale
            ):
        self.maxN = maxN
        self.n = n
        self.no = no
        self.parentEP = parentEP
        self.parentLength = parentLength
        self.parentAxises = parentAxises
        self.angleXZ = angleXZ
        self.angleXY = angleXY
        self.scale = scale
        
        self.sP = []
        self.eP = []
        self.length = []
        self.axis = None
        
        self.setAxis()
        self.setBranch()
            
    def setAxis(self):
        self.axis = Axis(
                    self.parentEP, 
                    self.parentAxises, 
                    self.angleXZ, 
                    self.angleXY
                    ) 
            
    def setBranch(self):
        vec = rs.VectorCrossProduct(self.axis.axises[0], self.axis.axises[1])
        vec = rs.VectorUnitize(vec)
        vec = rs.VectorScale(vec, self.parentLength * self.scale)
        
        self.sP = self.parentEP
        self.eP = rs.VectorAdd(vec, self.parentEP)
        
        self.length = rs.Distance(self.sP, self.eP)
        
    def draw(self):
        guid = rs.AddLine(self.sP, self.eP)
        return guid
    
    def drawLeaf(self):
        if(self.n!=self.maxN):return None
        r = 300
        # plane = rs.
        plane = rs.PlaneFromNormal(self.eP,self.axis.axises[2], self.axis.axises[1])
        guid = rs.AddCircle(plane,r)
        guid = rs.AddPlanarSrf(guid)[0]
        return guid
            
                
                
#################################################
# Tree class
#################################################
class Tree(object):
    def __init__(self, maxN, angleXZGene):
        self.maxN = maxN
        self.angleXZGene = angleXZGene
        self.angleXYGene = 90
        self.scaleGene = 0.9
        self.branches = []
        self.minScale = 0.8
        self.maxScale = 1.0
        self.minXZAngle = 0
        self.maxXZAngle = 45
        self.minXYAngle = 0
        self.maxXYAngle = 90
        
        # parent
        parentEP = [0,0,0]
        parentLength = 2000
        parentAxises = [
            [300,0,0],
            [0,300,0],
            [0,0,300]
        ]
                
        # child
        n = 0
        no = 0
        angleXZ = 0
        angleXY = 0
        scale = 1
        branch = Branch(
            self.maxN,
            n,
            no,
            parentEP, 
            parentLength, 
            parentAxises,
            angleXZ,
            angleXY,
            scale
        )
        self.branches.append(branch)
        
        # recursion
        no = self.makeChildBranch(branch,n+1,no+1)
        
    def makeChildBranch(self,branch,n,no):
        # end condition
        if(n>self.maxN):
            return no
        
        # left branch
        parentEP = branch.eP
        parentLength = branch.length
        parentAxises = branch.axis.axises
        angleXZ = (self.maxXZAngle-self.minXZAngle)*self.angleXZGene[no]+self.minXZAngle
        angleXY = 90
        scale = 0.9
        leftBranch = Branch(
            self.maxN,
            n,
            no,
            parentEP, 
            parentLength, 
            parentAxises,
            angleXZ,
            angleXY,
            scale
        )
        self.branches.append(leftBranch)
        no = self.makeChildBranch(leftBranch, n+1, no+1)
                
        # right branch
        parentEP = branch.eP
        parentLength = branch.length
        parentAxises = branch.axis.axises
        angleXZ = (self.maxXZAngle-self.minXZAngle)*self.angleXZGene[no]+self.minXZAngle
        angleXY = -90
        scale = 0.9
        rightbranch = Branch(
            self.maxN,
            n,
            no,
            parentEP, 
            parentLength, 
            parentAxises,
            angleXZ,
            angleXY,
            scale
        )
        self.branches.append(rightbranch)
        no = self.makeChildBranch(rightbranch, n+1, no+1)
                
        return no
        
##############################################
# instance
##############################################
tree = Tree(maxN,angleXZGene)
        
##############################################
# draw
##############################################
allBranch = []
allText = []
allNoPt = []
allLeaf = []
rs.EnableRedraw(False)
for branch in tree.branches: 
#     # axis
#    guids = branch.axis.draw()
#    allGuids.extend(guids)
    
    # text
    no = branch.no
    n = branch.n
    str = "n = {}\nno = {}".format(n,no)
    allText.append(str)
    noPt = rs.VectorAdd(branch.sP, branch.eP)
    noPt = rs.VectorScale(noPt,0.5)
    allNoPt.append(noPt)
    
    # branch
    guid = branch.draw()
    allBranch.append(guid)

    # leaf
    guid = branch.drawLeaf()
    if(guid!=None):
        allLeaf.append(guid)
rs.EnableRedraw(True)
        
