#!/home/ogawa/workspace/git/script/hrpsyspy
import sys
import socket
import traceback
import math
import time
import java.lang.System

import rtm
import waitInput
import bodyinfo
import OpenHRP

def init(robotHost=None):
    if robotHost != None:
      print 'robot host = '+robotHost
      java.lang.System.setProperty('NS_OPT',
          '-ORBInitRef NameService=corbaloc:iiop:'+robotHost+':2809/NameService')
      rtm.initCORBA()

    print "creating components"
    rtcList = createComps(robotHost)

    print "connecting components"
    connectComps()

    print "activating components"
    #activateComps(rtcList)

    print "initialized successfully"

def activateComps(rtcList):
    rtm.serializeComponents(rtcList)
    for r in rtcList:
        r.start()

def initRTC(module, name):
    ms.load(module)
    return ms.create(module, name)

def createComps(hostname=socket.gethostname()):
    global ms, adm_svc, rh, rh_svc, servo, seq, seq_svc, kf, simulation_mode
    ms = rtm.findRTCmanager(hostname)
    rh = rtm.findRTC("RobotHardware0")
    if rh != None:
        simulation_mode = 0
        rh_svc = OpenHRP.RobotHardwareServiceHelper.narrow(rh.service("service0"))
        servo = rh
        adm = rtm.findRTC("SystemAdmin0")
        if adm != None:
          adm.start()
          adm_svc = OpenHRP.SystemAdminServiceHelper.narrow(adm.service("service0"))
    else:
        simulation_mode = 1
        rh = rtm.findRTC("JVRC")
        servo = rtm.findRTC("creekPdServo0")
  
    seq = initRTC("creekSequencePlayer", "seq")
    seq_svc = OpenHRP.creekSequencePlayerServiceHelper.narrow(seq.service("service0"))

    kf  = initRTC("creekStateEstimator", "kf")

    return [rh, kf]

def connectComps():
    rtm.connectPorts(rh.port("gyrometer"), kf.port("rate"))
    rtm.connectPorts(rh.port("gsensor"),   kf.port("acc"))

    rtm.connectPorts(rh.port("qCur"),   seq.port("qInit"))
    rtm.connectPorts(seq.port("qRef"),  servo.port("qRef"))

def setupLogger():
    print "dummy"

def saveLog(fname='sample'):
    print 'saved'

def goInital():
    seq_svc.setJointAngles(bodyinfo.makeCommandPose(bodyinfo.initialPose), bodyinfo.timeToInitialPose)

def goHalfSitting():
    seq_svc.setJointAngles(bodyinfo.makeCommandPose(bodyinfo.halfsitPose), bodyinfo.timeToHalfsitPose)

def test():
    seq_svc.isEmpty()


if __name__ == '__main__' or __name__ == 'main':
    if len(sys.argv) > 1:
        robotHost = sys.argv[1]
    else:
        robotHost = None
    init(robotHost)
    setupLogger()
    userTest()
