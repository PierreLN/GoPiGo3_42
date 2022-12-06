    
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

class C64Projet1(FiniteStateMachine):
    def __init__(self):
        self.robot = Robot()
        
        ''' TELECOMMANDE '''
        def read_input_home():
            home_state.custom_value = self.robot.remote_control.get_remote_code()
          
        
        ''' LES STATES '''
        home_state = MonitoredState()

        self.manual_control_fsm = ManualControlStateMachine(self.robot)
        manual_control_state = ManualControlState(self.robot, self.manual_control_fsm)
        
        robot_instantiation_state = MonitoredState()
        robot_instantiation_state.custom_value = True
        robot_instantiation_failed_state = MonitoredState()

        # Params
        params_robot_end_state = State.Parameters()
        params_robot_end_state.terminal = True
        robot_end_state = MonitoredState(params_robot_end_state)
        
        robot_integrity_state = MonitoredState()
        robot_integrity_state.custom_value = True
        robot_integrity_failed_state = MonitoredState()
        robot_integrity_succeeded_state = MonitoredState()
        robot_shut_down_state = MonitoredState()

        '''ROBOT INSTANTIATION STATE'''
        
        def print__instantiation():
            print("INSTANTIATION")
        
        c_robot_instantiation_0 = StateValueCondition(True, robot_instantiation_state)
        c_robot_instantiation_1 = StateValueCondition(False, robot_instantiation_state)
        t_robot_instantiation_0 = ConditionalTransition(c_robot_instantiation_0)
        t_robot_instantiation_1 = ConditionalTransition(c_robot_instantiation_1)
        t_robot_instantiation_0.next_state = robot_integrity_state
        t_robot_instantiation_1.next_state = robot_instantiation_failed_state
        robot_instantiation_state.add_transition(t_robot_instantiation_0)
        robot_instantiation_state.add_transition(t_robot_instantiation_1)
        robot_instantiation_state.add_entering_action(print__instantiation)


        '''ROBOT INSTANTIATION FAILED STATE'''

        def print_error_msg_instantiation():
            print("INSTANTIATION FAILED")

        c_robot_instantiation_failed = AlwaysTrueCondition()
        t_robot_instantiation_failed = ConditionalTransition(c_robot_instantiation_failed)
        t_robot_instantiation_failed.next_state = robot_end_state
        robot_instantiation_failed_state.add_transition(t_robot_instantiation_failed)
        robot_instantiation_failed_state.add_entering_action(print_error_msg_instantiation)

        '''ROBOT END STATE'''

        def print_msg_end_state():
            print("ENDDING - TERMINAL STATE")

        robot_end_state.add_entering_action(print_msg_end_state)

        '''ROBOT INTEGRITY STATE'''
        c_robot_integrity_0 = StateValueCondition(True, robot_integrity_state)
        c_robot_integrity_1 = StateValueCondition(False, robot_integrity_state)
        t_robot_integrity_0 = ConditionalTransition(c_robot_integrity_0)
        t_robot_integrity_1 = ConditionalTransition(c_robot_integrity_1)
        t_robot_integrity_0.next_state = robot_integrity_succeeded_state
        t_robot_integrity_1.next_state = robot_integrity_failed_state
        robot_integrity_state.add_transition(t_robot_integrity_0)
        robot_integrity_state.add_transition(t_robot_integrity_1)

        '''ROBOT INTEGRITY FAILED'''

        def print_integrity_failed_msg():
            print("INTEGRITY FAILED")

        c_robot_integrity_failed = StateEntryDurationCondition(5.0, robot_integrity_failed_state)
        t_robot_integrity_failed = ConditionalTransition(c_robot_integrity_failed)
        t_robot_integrity_failed.next_state = robot_shut_down_state
        robot_integrity_failed_state.add_transition(t_robot_integrity_failed)
        robot_integrity_failed_state.add_entering_action(print_integrity_failed_msg)
        # clignote ici


        '''ROBOT SHUTDOWN STATE'''

        def print_shut_down_msg():
            print("SHUTTING DOWN")

        c_robot_shut_down = StateEntryDurationCondition(3.0, robot_shut_down_state)
        t_robot_shut_down = ConditionalTransition(c_robot_shut_down)
        t_robot_shut_down.next_state = robot_end_state
        robot_shut_down_state.add_transition(t_robot_shut_down)
        robot_shut_down_state.add_entering_action(print_shut_down_msg)
        # clignote ici

        '''ROBOT INTEGRITY SUCCEEDED STATE'''

        def print_integrity_succeeded_msg():
            print("INTEGRITY SUCCEEDED")

        c_robot_integrity_succeeded = StateEntryDurationCondition(3.0, robot_integrity_succeeded_state)
        t_robot_integrity_succeeded = ConditionalTransition(c_robot_integrity_succeeded)
        t_robot_integrity_succeeded.next_state = home_state
        robot_integrity_succeeded_state.add_transition(t_robot_integrity_succeeded)
        robot_integrity_succeeded_state.add_entering_action(print_integrity_succeeded_msg)
        # clignote ici

        
        ''' HOME '''
        def print_home_state():
            print("home state")
            
        home_state.custom_value = ""
        home_condition_0 = RemoteControlCondition("", "1", self.robot)
        home_transition_0 = RemoteControlTransition()
        home_transition_0.condition = home_condition_0
        home_transition_0.next_state = manual_control_state
        home_state.add_transition(home_transition_0)
        home_state.add_entering_action(print_home_state) # a effacer


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
        self.layout = FiniteStateMachine.Layout(
            [robot_instantiation_state, 
             robot_instantiation_failed_state, 
             robot_end_state, 
             robot_integrity_state, 
             robot_integrity_failed_state, 
             robot_integrity_succeeded_state, 
             robot_shut_down_state,
             home_state, 
             manual_control_state], robot_instantiation_state)

        super().__init__(self.layout)
    
    def track(self) -> bool:
        self.robot.ledBlinkers.track()
        self.robot.eyeBlinkers.track()

#         longuest_string = 20 # longueur arbitraire, ne sert que pour l'affichage
#         print(f'\r{self.robot.ledBlinkers.is_on(SideBlinker.Side.LEFT)}', sep='', end=' ' * longuest_string)
#         self.eyesBlinker.track()
        return super().track()