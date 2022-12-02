class RemoteControlTransition(MonitoredTransition):
    def __init__(self, next_state = None ):
        super().__init__(next_state)

class RemoteControlCondition(ValueCondition):
    def __init__(self, initial_value, expected_value, robot, inverse = False):
        super().__init__(initial_value, expected_value, inverse)
        self.robot = robot

    def _compare(self):
        longuest_string = 20 # longueur arbitraire, ne sert que pour l'affichage
        print(f'\r{self.robot.remote_control.get_remote_code()}', sep='', end=' ' * longuest_string)
        return self.expected_value == self.robot.remote_control.get_remote_code()
    
class ManualControlStateMachine(FiniteStateMachine):
    def __init__(self, robot):
        self.robot = robot
            
        ''' LES STATE'''
        stop_state = MonitoredState()
        forward_state = MonitoredState()
        backward_state = MonitoredState()    
        rotate_right_state = MonitoredState()
        rotate_left_state = MonitoredState()
        
        ''' STOP STATE'''
        def phare_off():
            self.robot.ledBlinkers.turn_off_0(SideBlinker.Side.BOTH)
            print("phare off")
        
        stop_condition_0 = RemoteControlCondition("", "right", self.robot)
        stop_condition_1 = RemoteControlCondition("", "up", self.robot)
        stop_condition_2 = RemoteControlCondition("", "left", self.robot)
        stop_condition_3 = RemoteControlCondition("", "down",  self.robot)
        
        stop_transition_0 = RemoteControlTransition()
        stop_transition_1 = RemoteControlTransition() 
        stop_transition_2 = RemoteControlTransition()
        stop_transition_3 = RemoteControlTransition()    
        
        stop_transition_0.condition = stop_condition_0
        stop_transition_1.condition = stop_condition_1
        stop_transition_2.condition = stop_condition_2
        stop_transition_3.condition = stop_condition_3
        
        stop_transition_0.next_state = rotate_right_state
        stop_transition_1.next_state = forward_state
        stop_transition_2.next_state = rotate_left_state
        stop_transition_3.next_state = backward_state
        
        stop_state.add_transition(stop_transition_0)
        stop_state.add_transition(stop_transition_1)        
        stop_state.add_transition(stop_transition_2)
        stop_state.add_transition(stop_transition_3)
        stop_state.add_in_state_action(self.robot.robot.stop) 
        stop_state.add_entering_action(phare_off)
        
        ''' FORWARD STATE''' 
        
        def phare_blink_both_forward():
            self.robot.ledBlinkers.blink1(SideBlinker.Side.BOTH, cycle_duration=1.0, percent_on= 0.25, begin_on = True)
        def phare_blink_both_backward():
            self.robot.ledBlinkers.blink1(SideBlinker.Side.BOTH, cycle_duration=1.0, percent_on= 0.75, begin_on = True)
        
        forward_condition_0 = RemoteControlCondition("up", "", self.robot)
        forward_transition_0 = RemoteControlTransition()
        forward_transition_0.condition = forward_condition_0
        forward_transition_0.next_state = stop_state
        forward_state.add_transition(forward_transition_0)
        forward_state.add_in_state_action(self.robot.robot.forward)
        forward_state.add_entering_action(phare_blink_both_forward)
          

        ''' BACKWARD STATE'''
        backward_condition_0 = RemoteControlCondition("down", "", self.robot)
        backward_transition_0 = RemoteControlTransition()
        backward_transition_0.condition = backward_condition_0
        backward_transition_0.next_state = stop_state
        backward_state.add_transition(backward_transition_0)
        backward_state.add_in_state_action(self.robot.robot.backward)
        backward_state.add_entering_action(phare_blink_both_backward)

        ''' ROTATE RIGHT STATE'''
        def phare_rotate_right():
            self.robot.ledBlinkers.blink1(SideBlinker.Side.RIGHT, cycle_duration=1.0, percent_on= 0.50, begin_on = True)                
        
        rotate_right_condition_0 = RemoteControlCondition("right", "", self.robot)
        rotate_right_transition_0 = RemoteControlTransition()
        rotate_right_transition_0.condition = rotate_right_condition_0
        rotate_right_transition_0.next_state = stop_state
        rotate_right_state.add_transition(rotate_right_transition_0)
        rotate_right_state.add_in_state_action(self.robot.robot.right)
        rotate_right_state.add_entering_action(phare_rotate_right)
        
        ''' ROTATE LEFT STATE'''
        def phare_rotate_left():
            self.robot.ledBlinkers.blink1(SideBlinker.Side.LEFT, cycle_duration=1.0, percent_on= 0.50, begin_on = True)                
        
        rotate_left_condition_0 = RemoteControlCondition("left", "", self.robot)
        rotate_left_transition_0 = RemoteControlTransition()
        rotate_left_transition_0.condition = rotate_left_condition_0
        rotate_left_transition_0.next_state = stop_state
        rotate_left_state.add_transition(rotate_left_transition_0)
        rotate_left_state.add_in_state_action(self.robot.robot.left)
        rotate_left_state.add_entering_action(phare_rotate_left)

        ''' LAYOUT '''
        self.layout = FiniteStateMachine.Layout([stop_state, forward_state, backward_state, rotate_right_state, rotate_left_state], stop_state)
        super().__init__(self.layout)
      
    
class RobotState(MonitoredState):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        
    
class ManualControlState(RobotState):
    def __init__(self, robot, manual_control_state_machine):
        super().__init__(robot)
        self.fsm = manual_control_state_machine
      
    
class C64Projet1(FiniteStateMachine):
    def __init__(self):
        self.robot = Robot()
        
        ''' TELECOMMANDE '''
        def read_input_home():
            home_state.custom_value = self.robot.remote_control.get_remote_code()
            
        ''' STATE '''
        home_state = MonitoredState()
        self.manual_control_fsm = ManualControlStateMachine(self.robot)
        manual_control_state = ManualControlState(self.robot, self.manual_control_fsm)
        
        ''' HOME '''
        home_state.custom_value = ""
        home_condition_0 = RemoteControlCondition("", "1", self.robot)
        home_transition_0 = RemoteControlTransition()
        home_transition_0.condition = home_condition_0
        home_transition_0.next_state = manual_control_state
        home_state.add_transition(home_transition_0)

        
        ''' MANUAL CONTROL '''
        def gyrophare_tache_1():
            self.robot.eyeBlinkers.blink1(SideBlinker.Side.LEFT_RECIPROCAL, cycle_duration=1.0, percent_on= 0.5, begin_on = True)
            self.robot.eyeBlinkers.set_right_eye_color((255,0,0)) # rouge
            self.robot.eyeBlinkers.set_left_eye_color((0,0,255)) # bleu
            print("gyro active")
            
        def gyrophare_turn_off_both():
            self.robot.eyeBlinkers.turn_off_0(SideBlinker.Side.BOTH)
            print("gyro off")

        manual_control_condition_0 = RemoteControlCondition("1", "ok", self.robot)
        manual_control_transition_0 = RemoteControlTransition()
        manual_control_transition_0.condition = manual_control_condition_0
        manual_control_transition_0.next_state = home_state
        manual_control_state.add_transition(manual_control_transition_0)
        manual_control_state.add_entering_action(self.manual_control_fsm.reset)
        manual_control_state.add_entering_action(gyrophare_tache_1)
        manual_control_state.add_in_state_action(self.manual_control_fsm.track)
        manual_control_state.add_exiting_action(self.robot.robot.stop)
        manual_control_state.add_exiting_action(gyrophare_turn_off_both)
        
        ''' LAYOUT '''
        self.layout = FiniteStateMachine.Layout([home_state, manual_control_state], home_state)
        super().__init__(self.layout)
    
    def track(self) -> bool:
        self.robot.ledBlinkers.track()
        self.robot.eyeBlinkers.track()

        
#         longuest_string = 20 # longueur arbitraire, ne sert que pour l'affichage
#         print(f'\r{self.robot.ledBlinkers.is_on(SideBlinker.Side.LEFT)}', sep='', end=' ' * longuest_string)
#         self.eyesBlinker.track()
        return super().track()  