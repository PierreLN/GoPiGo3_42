import easygopigo3 as gpg

class LedBlinkers(SideBlinker):
    def __init__(self, state_generator: Blinker.StateGenerator, robot):
        super().__init__(state_generator)
        self.robot=robot
        print(self.robot)
    
    def track(self):
        if self.is_on(SideBlinker.Side.LEFT):
            self.robot.led_on(1)
        else:
            self.robot.led_off(1)
        if self.is_on(SideBlinker.Side.RIGHT):
            self.robot.led_on(0)
        else:
            self.robot.led_off(0)
        return super().track()

class EyeBlinkers(SideBlinker):
    def __init__(self, state_generator: Blinker.StateGenerator, robot):
        super().__init__(state_generator)
        self.robot = robot
        color = (0,0,255) # Blue
        self.robot.set_right_eye_color(color)
        self.robot.set_left_eye_color(color)
        
    def track(self):
        if self.is_on(SideBlinker.Side.LEFT):
            self.robot.open_left_eye()
        else:
            self.robot.close_left_eye()
        if self.is_on(SideBlinker.Side.RIGHT):
            self.robot.open_right_eye()
        else:
            self.robot.close_right_eye()
        return super().track()
    
    def set_left_eye_color(self, color):
        self.robot.set_left_eye_color(color) 
        
    def set_right_eye_color(self, color):
        self.robot.set_right_eye_color(color)
    
class Robot():
    def __init__(self) -> None:
        self.robot = gpg.EasyGoPiGo3()
        self.ledBlinkers = LedBlinkers(TextStateGenerator("Entering", "Exiting"), self.robot)
        self.eyeBlinkers = EyeBlinkers(TextStateGenerator("Entering", "Exiting"), self.robot)       
        
        self.remote_control_port = 'AD1'
        self.remote_control = self.robot.init_remote(port=self.remote_control_port)