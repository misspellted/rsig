import pygame
import sys
import threading
import time
import timeit

from random import randint, shuffle

class RedColorModifier:
    def __init__(this, color=pygame.Color("black")):
        this.color = color

    def modifyColor(this, value):
        this.color.r = value
        return this.color

class GreenColorModifier:
    def __init__(this, color=pygame.Color("black")):
        this.color = color

    def modifyColor(this, value):
        this.color.g = value
        return this.color

class BlueColorModifier:
    def __init__(this, color=pygame.Color("black")):
        this.color = color

    def modifyColor(this, value):
        this.color.b = value
        return this.color

class WhiteColorModifier:
    def modifyColor(this, value):
        return pygame.Color(value, value, value)

class PygameEventHandler:
    def __init__(this, raiseNotImplementedErrors):
        this.raiseNotImplementedErrors = raiseNotImplementedErrors

    def onQuit(this):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onActiveEvent(this, gain, state):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onKeyDown(this, unicode, key, mod):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onKeyUp(this, key, mod):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onMouseMotion(this, pos, rel, buttons):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onMouseButtonDown(this, pos, button):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onMouseButtonUp(this, pos, button):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onJoystickAxisMotion(this, joy, axis, value):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onJoystickBallMotion(this, joy, ball, rel):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onJoystickHatMotion(this, joy, hat, value):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onJoystickButtonDown(this, joy, button):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onJoystickButtonUp(this, joy, button):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onVideoResize(this, size, w, h):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onVideoExpose(this):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onUserEvent(this, code):
        if this.raiseNotImplementedErrors:
            raise NotImplementedError()

    def onEvent(this, event):
        eventType = event.type
        if eventType == pygame.QUIT:
            this.onQuit()
        elif eventType == pygame.ACTIVEEVENT:
            this.onActiveEvent(event.gain, event.state)
        elif eventType == pygame.KEYDOWN:
            this.onKeyDown(event.unicode, event.key, event.mod)
        elif eventType == pygame.KEYUP:
            this.onKeyUp(event.key, event.mod)
        elif eventType == pygame.MOUSEMOTION:
            this.onMouseMotion(event.pos, event.rel, event.buttons)
        elif eventType == pygame.MOUSEBUTTONDOWN:
            this.onMouseButtonDown(event.pos, event.button)
        elif eventType == pygame.MOUSEBUTTONUP:
            this.onMouseButtonUp(event.pos, event.button)
        elif eventType == pygame.JOYAXISMOTION:
            this.onJoystickAxisMotion(event.joy, event.axis, event.value)
        elif eventType == pygame.JOYBALLMOTION:
            this.onJoystickBallMotion(event.joy, event.ball, event.rel)
        elif eventType == pygame.JOYHATMOTION:
            this.onJoystickHatMotion(event.joy, event.hat, event.value)
        elif eventType == pygame.JOYBUTTONDOWN:
            this.onJoystickButtonDown(event.joy, event.button)
        elif eventType == pygame.JOYBUTTONUP:
            this.onJoystickButtonUp(event.joy, event.button)
        elif eventType == pygame.VIDEORESIZE:
            this.onVideoResize(event.size, event.w, event.h)
        elif eventType == pygame.VIDEOEXPOSE:
            this.onVideoExpose()
        elif eventType == pygame.USEREVENT:
            this.onUserEvent(event.code)

class PygameProgram(PygameEventHandler):
    def __init__(this):
        pygame.init()
        this.displayInfo = None
        this.display = None
        this.terminating = False
        PygameEventHandler.__init__(this, False)

    def refreshDisplayInfo(this):
        this.displayInfo = pygame.display.Info()

    def setWindowedCaption(this, caption):
        if caption is not None:
            pygame.display.set_caption(caption)

    def getDisplaySurface(this):
        return this.display

    def setWindowedParameters(this, length, height, caption=None, flags=0, depth=0):
        this.display = pygame.display.set_mode((length, height), flags, depth)
        this.setWindowedCaption(caption)

    def refreshDisplay(this):
        if this.display is not None:
            pygame.display.flip()

    def onQuit(this):
        print "Quitting..."
        this.terminating = True

    def onActiveEvent(this, gain, state):
        print "Window activity: gain:", gain, "| state:", state

    def onKeyDown(this, unicode, key, mod):
        print "Key pressed: unicode:", unicode, "| key:", key, "| mod: ", mod, "}"

    def onKeyUp(this, key, mod):
        print "Key released: key:", key, "| mod: ", mod, "}"

    def onMouseMotion(this, pos, rel, buttons):
        print "Mouse moved: pos:", pos, "| rel:", rel, "| buttons: ", buttons, "}"

    def onMouseButtonDown(this, pos, button):
        print "Mouse button pressed: pos:", pos, "| button: ", button, "}"

    def onMouseButtonUp(this, pos, button):
        print "Mouse button released: pos:", pos, "| button: ", button, "}"

    def onVideoResize(this, size, w, h):
        print "Display resized: size:", size, " | w:", w, " | h:", h

    def onVideoExpose(this):
        print "Display exposed (?)"

    def onUserEvent(this, code):
        print "User event: code:", code

    def run(this):
        while not this.terminating:
            for event in pygame.event.get():
                this.onEvent(event)
                if this.terminating:
                    pygame.quit()
                    sys.exit()
            this.refreshDisplay()

class RandomizedSequentialLineGenerator(threading.Thread):
    def __init__(this, length, progressive=False):
        this.length = length
        this.progressive = progressive
        this.onLineDataGeneratedListener = None
        this.paused = False
        threading.Thread.__init__(this)

    def toggleProgressive(this):
        this.progressive = not this.progressive

    def setOnLineDataGeneratedListener(this, listener):
        this.onLineDataGeneratedListener = listener

    def getNextInteger(this, last):
        start = last if this.progressive else 0
        next = randint(start, this.length)
        attempts = 1
        while next != (last + 1):
            next = randint(start, this.length)
            attempts += 1
        return attempts

    def pause(this):
        this.paused = True

    def isPaused(this):
        return this.paused

    def resume(this):
        this.paused = False

    def terminate(this):
        this.terminating = True

    def run(this):
        this.terminating = False
        while not this.terminating:
            if not this.paused:
                attempts = list()
                for index in range(0, this.length):
                    attempts.append(this.getNextInteger(index - 1))
                    if this.terminating:
                        break
                minimum = min(attempts)
                maximum = max(attempts)
                ranged = maximum - minimum
                lineData = list()
                for x in range(0, this.length):
                    lineData.append(int((float(attempts[x] - minimum) / ranged) * 255))
                    if this.terminating:
                        break
                if not this.terminating:
                    if this.onLineDataGeneratedListener is not None:
                        this.onLineDataGeneratedListener(list(lineData))
            else:
                time.sleep(0.01)

class RandomizedSequentialImageGenerator(PygameProgram):
    def __init__(this, length, height, progressive=False):
        if length % 3 != 0:
            raise ValueError("Length should be cleanly divisible by 3, for the RGB panels.")
        PygameProgram.__init__(this)
        this.baseCaption = "Randomized Sequential Image Generator"
        this.panelLength = length / 3
        this.lineLength = height
        this.progressive = progressive
        this.setWindowedParameters(length, height, this.baseCaption, pygame.HWSURFACE or pygame.DOUBLEBUF)
        this.lineGenerator = None
        this.followCursor = True
        this.lock = threading.Lock()
        this.setLastColumn(0)

    def setLastColumn(this, lastColumn):
        this.lastColumn = lastColumn
        # Red (left panel), Green (middle panel), Blue (right panel)
        if this.lastColumn < this.panelLength:
            this.modifier = RedColorModifier()
        elif this.lastColumn < this.panelLength * 2:
            this.modifier = GreenColorModifier()
        else:
            this.modifier = BlueColorModifier()

    def onLineDataGenerated(this, lineData):
        with this.lock:
            lineSurface = pygame.Surface((1, len(lineData)))
            y = 0
            for normalizedValue in lineData:
                lineSurface.set_at((0, y), this.modifier.modifyColor(normalizedValue))
                y += 1
            this.getDisplaySurface().blit(lineSurface, (this.lastColumn, 0))
            if not this.followCursor:
                this.setLastColumn(randint(0, this.panelLength * 3))

    def onQuit(this):
        PygameProgram.onQuit(this)
        if this.lineGenerator is not None:
            this.lineGenerator.terminate()

    def onKeyDown(this, unicode, key, mod):
        if key == pygame.K_f:
            this.followCursor = not this.followCursor
        elif key == pygame.K_h:
            if this.lineGenerator is not None:
                if this.lineGenerator.isPaused():
                    this.lineGenerator.resume()
                else:
                    this.lineGenerator.pause()
        elif key == pygame.K_p:
            if this.lineGenerator is not None:
                this.lineGenerator.toggleProgressive()

    def onMouseMotion(this, pos, rel, buttons):
        if this.followCursor:
            x, y = pos
            this.setLastColumn(x)

    def run(this):
        this.lineGenerator = RandomizedSequentialLineGenerator(this.lineLength, this.progressive)
        this.lineGenerator.setOnLineDataGeneratedListener(this.onLineDataGenerated)
        this.lineGenerator.start()
        PygameProgram.run(this)

def main():
    height = 512
    program = RandomizedSequentialImageGenerator(height * 3, height, False)
    program.run()

if __name__ == "__main__":
    main()
