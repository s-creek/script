import math

modelName = "JVRC"

timeToHalfsitPose = 3.0 # [sec]
halfsitPose = [ -30, 0, 0, 58, 0, -28,
                -30, 0, 0, 58, 0, -28,
                 0, 0, 0,
                 0, 0, 0,
                 10, -5, 0, -30, 0, 0, 0,
                 0, 0, 0, 0, 0, 0,
                 10,  5, 0, -30, 0, 0, 0,
                 0, 0, 0, 0, 0, 0 ]

timeToInitialPose = 3.0 # [sec]
initialPose = [0] * 44


# this is for compatibility between different robots
def makeCommandPose(pose):
    return [jv*math.pi/180.0 for jv in pose]
