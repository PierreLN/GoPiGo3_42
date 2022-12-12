from level_three import Blinker, SideBlinker, TextStateGenerator
# from gopigo3 import GoPiGo3
import easygopigo3 as gpg

class LedBlinkers(SideBlinker):
    def __init__(self, state_generator: Blinker.StateGenerator, robot:EasyGoPiGo3):
        super().__init__(state_generator)
        self.robot=robot
        print(self.robot)
    
    def track(self):
        if self.is_on(SideBlinker.Side.LEFT):
            self.robot.led_on(0)
            print("true")
        else:
            self.robot.led_off(0)
            print("false")
        if self.is_on(SideBlinker.Side.RIGHT):
            self.robot.led_on(1)
        else:
            self.robot.led_off(1)
        return super().track()

class EyesBlinkers(SideBlinker):
    def __init__(self, state_generator: Blinker.StateGenerator, robot:EasyGoPiGo3):
        super().__init__(state_generator)
        self.robot = robot

class Robot():
    def __init__(self) -> None:
        self.robot = gpg.EasyGoPiGo3()
        self.ledBlinkers = LedBlinkers(TextStateGenerator("Entering", "Exiting"), self.robot)
        self.eyesBlinker = EyesBlinkers(TextStateGenerator("Entering", "Exiting"), self.robot)       
