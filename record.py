# coding:utf-8
from operator import attrgetter



class Record():
    def __init__(self, fitness, angleXZGene):
        self.fitness = fitness
        self.angleXZGene = angleXZGene

records = []
for i in range(len(fitnesses)):
    record = Record(fitnesses[i], angleXZs[i*127:(i+1)*127])
    records.append(record)
records = sorted(records, key=attrgetter('fitness'), reverse=True)
if(no<len(records)):
    fitness = records[no].fitness
    angleXZGene = records[no].angleXZGene

    print("recordNum = {}".format(len(records)))
    print("fitness = {}".format(fitness))
    print("angleXZGeneNum = {}".format(len(angleXZGene)))
    print("angleXZGene = {}".format(angleXZGene))
    
# #####################################################################
# # camera
# #####################################################################
# view = rs.CurrentView()
# beta = -90 + emblems[0].frameCount
# cameraX = l * math.sin(math.radians(alpha)) * math.cos(math.radians(beta))
# cameraY = l * math.sin(math.radians(alpha)) * math.sin(math.radians(beta))
# cameraZ = l * math.cos(math.radians(alpha))
# camera = [cameraX, cameraY, cameraZ]
# target = [0, 0, 0]
# rs.ViewCameraTarget(view, camera, target)
    

