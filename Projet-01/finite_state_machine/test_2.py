class Blinker(FiniteStateMachine):
        def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator):
            self.__off_duration = off_state_generator()
            self.t_off_duration = ConditionalTransition(StateEntryDurationCondition(.0, MonitoredState()))
            self.t_off_duration.next_state = self.__on
            self.__off_duration.add_transition(self.t_off_duration)

        super().__init__(
            FiniteStateMachine.Layout(
                [
                    self.__off_duration
                    # , self.__on_duration

                    # , self.blink_stop_begin
                    # , self.blink_stop_off
                    # , self.blink_stop_on
                    # , self.blink_stop_end
                ]
                , self.__off
            )
        )

        def turn_off_0(self):
            self.transit_to(self.__off)

blinker_000.turn_off_0() # off
print(blinker_000.is_on) # check
blinker_000.turn_off_1(duration= 29999999999999.0)
print(blinker_000.is_on) 