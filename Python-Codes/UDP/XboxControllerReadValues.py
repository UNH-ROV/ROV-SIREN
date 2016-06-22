"""
ROV - XboxController Read code
Edited and reworked by Shawn Swist

In actual code start controller with
    XboxCont = XboxController( deadzone = ##, scale = ##, invertYAxis = True)
where ## represent the max value of the triggers/joysticks and the size of the deadzone

Provides all values from the xbox controller into code except left thumb...

Pygame must be downloaded for this code to work and can be downloaded at:
    http://www.pygame.org/download.shtml



Original Code:
#Martin O'Hanlon
#www.stuffaboutcode.com
#A class for reading values from an xbox controller
# uses xboxdrv and pygame
# xboxdrv should already be running
"""




import pygame
from pygame.locals import *
import os, sys
import threading
import time


class XboxController(threading.Thread):

    #internal ids for the xbox controls
    class XboxControls():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 4
        RTHUMBY = 3
        RTRIGGER = 2
        LTRIGGER = 2    # FOR SOME REASON IT IS MAPPING BOTH TRIGGERS TO AXIS 2, LT = +, RT = -
        A = 6
        B = 7
        X = 8
        Y = 9
        LB = 10
        RB = 11
        BACK = 12
        START = 13
        XBOX = 16
        LEFTTHUMB = 14
        RIGHTTHUMB = 15
        DPAD = 17

    #pygame axis constants for the analogue controls of the xbox controller
    class PyGameAxis():
        LTHUMBX = 0
        LTHUMBY = 1
        RTHUMBX = 4     # CHANGED THIS 
        RTHUMBY = 3
        RTRIGGER = 2
        LTRIGGER = 6

    #pygame constants for the buttons of the xbox controller
    class PyGameButtons():
        A = 0
        B = 1
        X = 2
        Y = 3
        LB = 4
        RB = 5
        BACK = 6
        START = 7
        XBOX = 8
        LEFTTHUMB = 9
        RIGHTTHUMB = 10

    #map between pygame axis (analogue stick) ids and xbox control ids
    AXISCONTROLMAP = {PyGameAxis.LTHUMBX: XboxControls.LTHUMBX,
                      PyGameAxis.LTHUMBY: XboxControls.LTHUMBY,
                      PyGameAxis.RTHUMBX: XboxControls.RTHUMBX,
                      PyGameAxis.RTHUMBY: XboxControls.RTHUMBY}
    
    #map between pygame axis (trigger) ids and xbox control ids
    TRIGGERCONTROLMAP = {PyGameAxis.RTRIGGER: XboxControls.RTRIGGER,
                         PyGameAxis.LTRIGGER: XboxControls.LTRIGGER}

    #map between pygame buttons ids and xbox contorl ids
    BUTTONCONTROLMAP = {PyGameButtons.A: XboxControls.A,
                        PyGameButtons.B: XboxControls.B,
                        PyGameButtons.X: XboxControls.X,
                        PyGameButtons.Y: XboxControls.Y,
                        PyGameButtons.LB: XboxControls.LB,
                        PyGameButtons.RB: XboxControls.RB,
                        PyGameButtons.BACK: XboxControls.BACK,
                        PyGameButtons.START: XboxControls.START,
                        PyGameButtons.XBOX: XboxControls.XBOX,
                        PyGameButtons.LEFTTHUMB: XboxControls.RIGHTTHUMB,
                        PyGameButtons.RIGHTTHUMB: XboxControls.LEFTTHUMB}   # CHANGED R/L Thumb buttons...
 #setup xbox controller class
    def __init__(self,
                 controllerCallBack = None,
                 joystickNo = 0,
                 deadzone = 0.1,
                 scale = 1,
                 invertYAxis = False):

        #setup threading
        threading.Thread.__init__(self)
        
        #persist values
        self.running = False
        self.controllerCallBack = controllerCallBack
        self.joystickNo = joystickNo
        self.lowerDeadzone = deadzone * -1
        self.upperDeadzone = deadzone
        self.scale = scale
        self.invertYAxis = invertYAxis
        self.controlCallbacks = {}

        #setup controller properties
        self.controlValues = {self.XboxControls.LTHUMBX:0,
                              self.XboxControls.LTHUMBY:0,
                              self.XboxControls.RTHUMBX:0,
                              self.XboxControls.RTHUMBY:0,
                              self.XboxControls.RTRIGGER:0,
                              self.XboxControls.LTRIGGER:0,
                              self.XboxControls.A:0,
                              self.XboxControls.B:0,
                              self.XboxControls.X:0,
                              self.XboxControls.Y:0,
                              self.XboxControls.LB:0,
                              self.XboxControls.RB:0,
                              self.XboxControls.BACK:0,
                              self.XboxControls.START:0,
                              self.XboxControls.XBOX:0,
                              self.XboxControls.LEFTTHUMB:0,
                              self.XboxControls.RIGHTTHUMB:0,
                              self.XboxControls.DPAD:(0,0)}

        #setup pygame
        self._setupPygame(joystickNo)

    #Create controller properties
    @property
    def LTHUMBX(self):
        return self.controlValues[self.XboxControls.LTHUMBX]

    @property
    def LTHUMBY(self):
        return self.controlValues[self.XboxControls.LTHUMBY]

    @property
    def RTHUMBX(self):
        return self.controlValues[self.XboxControls.RTHUMBX]

    @property
    def RTHUMBY(self):
        return self.controlValues[self.XboxControls.RTHUMBY]

    @property
    def RTRIGGER(self):
        return self.controlValues[self.XboxControls.RTRIGGER]

    @property
    def LTRIGGER(self):
        return self.controlValues[self.XboxControls.LTRIGGER]

    @property
    def A(self):
        return self.controlValues[self.XboxControls.A]

    @property
    def B(self):
        return self.controlValues[self.XboxControls.B]

    @property
    def X(self):
        return self.controlValues[self.XboxControls.X]

    @property
    def Y(self):
        return self.controlValues[self.XboxControls.Y]

    @property
    def LB(self):
        return self.controlValues[self.XboxControls.LB]

    @property
    def RB(self):
        return self.controlValues[self.XboxControls.RB]

    @property
    def BACK(self):
        return self.controlValues[self.XboxControls.BACK]

    @property
    def START(self):
        return self.controlValues[self.XboxControls.START]

    @property
    def XBOX(self):
        return self.controlValues[self.XboxControls.XBOX]

    @property
    def LEFTTHUMB(self):
        return self.controlValues[self.XboxControls.LEFTTHUMB]

    @property
    def RIGHTTHUMB(self):
        return self.controlValues[self.XboxControls.RIGHTTHUMB]

    @property
    def DPAD(self):
        return self.controlValues[self.XboxControls.DPAD]

    #setup pygame
    def _setupPygame(self, joystickNo):
        # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # init pygame
        pygame.init()
        # create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # init the joystick control
        pygame.joystick.init()
        # how many joysticks are there
        #print pygame.joystick.get_count()
        # get the first joystick
        joy = pygame.joystick.Joystick(joystickNo)
        # init that joystick
        joy.init()

    #called by the thread
    def run(self):
        self._start()

    #start the controller
    def _start(self):
        
        self.running = True
        
        #run until the controller is stopped
        while(self.running):
            #react to the pygame events that come from the xbox controller
            for event in pygame.event.get():

                #thumb sticks, trigger buttons                    
                if event.type == JOYAXISMOTION:
                    #is this axis on our xbox controller
                    if event.axis in self.AXISCONTROLMAP:
                        #is this a y axis
                        yAxis = True if (event.axis == self.PyGameAxis.LTHUMBY or event.axis == self.PyGameAxis.RTHUMBY) else False
                        #update the control value
                        self.updateControlValue(self.AXISCONTROLMAP[event.axis],
                                                self._sortOutAxisValue(event.value, yAxis))
                    #is this axis a trigger
                    if event.axis in self.TRIGGERCONTROLMAP:
                        #update the control value
                        self.updateControlValue(self.TRIGGERCONTROLMAP[event.axis],
                                                self._sortOutTriggerValue(event.value))
                        
                #d pad
                elif event.type == JOYHATMOTION:
                    #update control value
                    self.updateControlValue(self.XboxControls.DPAD, event.value)

                #button pressed and unpressed
                elif event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
                    #is this button on our xbox controller
                    if event.button in self.BUTTONCONTROLMAP:
                        #update control value
                        self.updateControlValue(self.BUTTONCONTROLMAP[event.button],
                                                self._sortOutButtonValue(event.type))
        
    #stops the controller
    def stop(self):
        self.running = False

    #updates a specific value in the control dictionary
    def updateControlValue(self, control, value):
        #if the value has changed update it and call the callbacks
        if self.controlValues[control] != value:
            self.controlValues[control] = value
            self.doCallBacks(control, value)
    
    #calls the call backs if necessary
    def doCallBacks(self, control, value):
        #call the general callback
        if self.controllerCallBack != None: self.controllerCallBack(control, value)

        #has a specific callback been setup?
        if control in self.controlCallbacks:
            self.controlCallbacks[control](value)
            
    #used to add a specific callback to a control
    def setupControlCallback(self, control, callbackFunction):
        # add callback to the dictionary
        self.controlCallbacks[control] = callbackFunction
                
    #scales the axis values, applies the deadzone
    def _sortOutAxisValue(self, value, yAxis = False):
        #invert yAxis
        if yAxis and self.invertYAxis: value = value * -1
        #scale the value
        value = value * self.scale
        #apply the deadzone
        if value < self.upperDeadzone and value > self.lowerDeadzone: value = 0
        return value

    #turns the trigger value into something sensible and scales it
    def _sortOutTriggerValue(self, value):
        #trigger goes -1 to 1 (-1 is off, 1 is full on, half is 0) - I want this to be 0 - 1
        
       # value = max(0,(value + 1) / 2)
       # AS THE TRIGGERS ARE MAPPED TOGETHER, I WANT -1 to 1 FOR THE RANGE
       
        #scale the value
        value = value * self.scale
        return value

    #turns the event type (up/down) into a value
    def _sortOutButtonValue(self, eventType):
        #if the button is down its 1, if the button is up its 0
        value = 1 if eventType == JOYBUTTONDOWN else 0
        return value


#generic call back
def controlCallBack(xboxControlId, value):
    print "Control Id = {}, Value = {}".format(xboxControlId, value)
    

#setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
xboxCont = XboxController( deadzone = 10, scale = 50, invertYAxis = True)


def GetValues():
    Rx = xboxCont.RTHUMBX
    Ry = xboxCont.RTHUMBY
    Lx = xboxCont.LTHUMBX
    Ly = xboxCont.LTHUMBY
    Rt = xboxCont.RTRIGGER
    Lt = xboxCont.LTRIGGER
    A = xboxCont.A
    B = xboxCont.B
    X = xboxCont.X
    Y = xboxCont.Y
    Rb = xboxCont.RB
    Lb = xboxCont.LB
    rthumb = xboxCont.RIGHTTHUMB
    lthumb = xboxCont.LEFTTHUMB
    Back = xboxCont.BACK
    Start = xboxCont.START
    dpad = xboxCont.DPAD
    
    # Balance out Rt, Lt ... (0.05 to balance out sigfigs)

    if Rt > -0.05:
        Rt = 0
    elif Rt < 0.05:
        Rt = -Rt

    if Lt < 0:
        Lt = 0
    elif Lt > 0.05:
        Lt = Lt

    return Lx, Ly, Rx, Ry, Lt, Rt, dpad

##
##try:
##    xboxCont.start()
##    while True:
##        Rx = xboxCont.RTHUMBX
##        Ry = xboxCont.RTHUMBY
##        Lx = xboxCont.LTHUMBX
##        Ly = xboxCont.LTHUMBY
##        Rt = xboxCont.RTRIGGER
##        Lt = xboxCont.LTRIGGER
##        A = xboxCont.A
##        B = xboxCont.B
##        X = xboxCont.X
##        Y = xboxCont.Y
##        Rb = xboxCont.RB
##        Lb = xboxCont.LB
##        rthumb = xboxCont.RIGHTTHUMB
##        lthumb = xboxCont.LEFTTHUMB
##        Back = xboxCont.BACK
##        Start = xboxCont.START
##        dpad = xboxCont.DPAD
##
##        # Balance out Rt, Lt ... (0.05 to balance out sigfigs)
##
##        if Rt > -0.05:
##            Rt = 0
##        elif Rt < 0.05:
##            Rt = -Rt
##
##        if Lt < 0:
##            Lt = 0
##        elif Lt > 0.05:
##            Lt = Lt
##
##        print Lx, Ly, Rx, Ry, Lt, Rt
##        time.sleep(.1)
##        
##except KeyboardInterrupt:
##    print "User Cancelled"
##
##except:
##    print "unexpected error"
##
##finally:
##    xboxCont.stop()
##
