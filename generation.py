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
        self.children = []
        
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
    
    def getSrfPts(self, axisNo):
        pts = []
        scaleW = 0.2
        # pt0
        vec = rs.VectorUnitize(self.axis.axises[axisNo])
        vec = rs.VectorScale(vec, self.length*scaleW/2)
        pt0 = rs.VectorAdd(self.sP, -vec)
        pts.append(pt0)
        # pt1
        pt1 = rs.VectorAdd(self.sP, vec)
        pts.append(pt1)
        # pt2
        vec = rs.VectorUnitize(self.axis.axises[axisNo])
        vec = rs.VectorScale(vec, self.length*self.scale*scaleW/2)
        pt2 = rs.VectorAdd(self.eP, vec)
        pts.append(pt2)
        # pt3
        pt3 = rs.VectorAdd(self.eP, -vec)
        pts.append(pt3)
        return pts

    def drawSrf(self):
        guids = []
        if(len(self.children)==0):
            newPts = []
            myPts = self.getSrfPts(1)
            newPts.append(myPts[0])
            newPts.append(myPts[1])
            newPts.append(myPts[2])
            newPts.append(myPts[3])
            newPts.append(myPts[0])
            guid = rs.AddPolyline(newPts)
            guid = rs.AddPlanarSrf(guid)
            guids.extend(guid)
        else:
            newPts = []
            myPts = self.getSrfPts(1)
            childrenRPts = self.children[0].getSrfPts(0)
            childrenLPts = self.children[1].getSrfPts(0)
            # pt0
            newPts.append(myPts[0])
            # pt1
            newPts.append(myPts[1])
            # pt2
            line0 = rs.AddLine(myPts[1], myPts[2])
            line1 = rs.AddLine(childrenRPts[1], childrenRPts[2])
            intersectPts = rs.LineLineIntersection(line0, line1)
            newPts.append(intersectPts[0])
            # pt3
            newPts.append(childrenRPts[2])
            # pt4
            newPts.append(childrenRPts[3])
            # pt5
            line0 = rs.AddLine(childrenRPts[3], childrenRPts[0])
            line1 = rs.AddLine(childrenLPts[3], childrenLPts[0])
            intersectPts = rs.LineLineIntersection(line0, line1)
            newPts.append(intersectPts[0])
            # pt6
            newPts.append(childrenLPts[3])
            # pt7
            newPts.append(childrenLPts[2])
            # pt8
            line0 = rs.AddLine(myPts[0], myPts[3])
            line1 = rs.AddLine(childrenLPts[2], childrenLPts[1])
            intersectPts = rs.LineLineIntersection(line0, line1)
            newPts.append(intersectPts[0])
            # pt9
            newPts.append(myPts[0])
            # guid
            guid = rs.AddPolyline(newPts)
            guid = rs.AddPlanarSrf(guid)
            guids.extend(guid)
        if(self.n == 0):
            newPts = []
            myPts = self.getSrfPts(0)
            childrenRPts = self.children[0].getSrfPts(1)
            childrenLPts = self.children[1].getSrfPts(1)
            newPts.append(myPts[0])
            newPts.append(myPts[1])
            newPts.append(childrenRPts[0])
            newPts.append(childrenLPts[0])
            newPts.append(myPts[0])
            guid = rs.AddPolyline(newPts)
            guid = rs.AddPlanarSrf(guid)
            guids.extend(guid)
        # return
        return guids
            
                
                
#################################################
# Tree class
#################################################
class Tree(object):
    def __init__(self, maxN, angleXZGene):
        self.maxN = maxN
        self.angleXZGene = angleXZGene
        self.minXZAngle = 5
        self.maxXZAngle = 75
        self.angleXY = 90
        self.scale = 0.8
        self.branches = []

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
        angleXY = self.angleXY
        scale = self.scale
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
        branch.children.append(leftBranch)
        no = self.makeChildBranch(leftBranch, n+1, no+1)
                
        # right branch
        parentEP = branch.eP
        parentLength = branch.length
        parentAxises = branch.axis.axises
        angleXZ = (self.maxXZAngle-self.minXZAngle)*self.angleXZGene[no]+self.minXZAngle
        angleXY = -self.angleXY
        scale = self.scale
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
        branch.children.append(rightbranch)
        no = self.makeChildBranch(rightbranch, n+1, no+1)
                
        return no
        
##############################################
# instance
##############################################
tree = Tree(maxN,angleXZGene)
        
##############################################
# draw
##############################################
allAxis = []
allBranch = []
allText = []
allNoPt = []
allLeaf = []
allBranchSrf = []
allBranchUnrollSrf = []
rs.EnableRedraw(False)
for branch in tree.branches: 
    # axis
    # guids = branch.axis.draw()
    # allAxis.extend(guids)
    
    # text
    str = "n = {}\n".format(branch.n)
    str += "no = {}\n".format(branch.no)
    str += "angleXZ = {}\n".format(branch.angleXZ)
    str += "angleXY = {}\n".format(branch.angleXY)
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
    
    # srf
    guid = branch.drawSrf()
    if(guid!=None):
        allBranchSrf.extend(guid)
        
rs.EnableRedraw(True)
        
