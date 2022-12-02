class C64Projet1(FiniteStateMachine):
    def __init__(self):
        self.robot = Robot()
        state_000 = MonitoredState()
#         def entering():
#             print("entering")
#         def in_state():
#             print("in state")
#         def exiting():
#             print("exiting")
#         state_000.add_entering_action(entering)
#         state_000.add_in_state_action(in_state)
#         state_000.add_exiting_action(exiting)
        self.layout = FiniteStateMachine.Layout([state_000], state_000)
        super().__init__(self.layout)
    
    def track(self) -> bool:
        self.robot.ledBlinkers.track()
#         longuest_string = 20 # longueur arbitraire, ne sert que pour l'affichage
#         print(f'\r{self.robot.ledBlinkers.is_on(SideBlinker.Side.LEFT)}', sep='', end=' ' * longuest_string)
#         self.eyesBlinker.track()
        return super().track()

'''

projet1 = C64Projet1()
projet1.robot.ledBlinkers.blink1(SideBlinker.Side.LEFT_RECIPROCAL, cycle_duration=3, percent_on= 0.5, begin_on = True)
projet1.start()

'''