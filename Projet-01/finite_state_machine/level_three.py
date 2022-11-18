from enum import Enum
from typing import Callable
from level_one import FiniteStateMachine, State
from level_two \
    import \
    StateEntryDurationCondition, ConditionalTransition, MonitoredState, \
    MonitoredTransition, AlwaysTrueCondition, ActionTransition, NoneCondition, \
    StateValueCondition


def generate_State():  # StateGenerator
    """ with default parameters set """
    return State(State.Parameters())


class Blinker(FiniteStateMachine):
    StateGenerator = Callable[[], State]

    def __init__(
            self
            , off_state_generator: StateGenerator
            , on_state_generator: StateGenerator
    ):
        """ CONSTRUIRE LA MACHINE D'ÉTATS """

        ''' OFF : la machine est éteinte ( état initial ) '''
        self.__off = off_state_generator()
        self.__off.add_transition(ConditionalTransition(NoneCondition()))

        ''' ON : la machine est allumé '''
        self.__on = on_state_generator()
        self.__on.add_transition(ConditionalTransition(NoneCondition()))

        ''' OFF DURATION : la machine passe à OFF après une durée de temps déterminé '''
        self.__off_duration = off_state_generator()
        t_off_duration = ConditionalTransition(StateEntryDurationCondition(.0, MonitoredState()))
        t_off_duration.next_state = self.__off
        self.__off_duration.add_transition(t_off_duration)

        ''' ON DURATION : la machine passe à ON après une durée de temps déterminé '''
        self.__on_duration = on_state_generator()
        t_on_duration = ConditionalTransition(StateEntryDurationCondition(.0, MonitoredState()))
        t_on_duration.next_state = self.__on
        self.__on_duration.add_transition(t_on_duration)

        ''' BLINK OFF : la machine ne clignote pas  '''
        self.__blink_off = off_state_generator()
        ''' BLINK ON : la machine clignote '''
        self.__blink_on = on_state_generator()
        ''' init. BLINK OFF ( définition et ajout de transition ) '''
        t_blink_off = ConditionalTransition(StateEntryDurationCondition(0., MonitoredState()))
        t_blink_off.next_state = self.__blink_on
        self.__blink_off.add_transition(t_blink_off)
        ''' init. BLINK ON ( définition et ajout de transition ) '''
        t_blink_on = ConditionalTransition(StateEntryDurationCondition(0, MonitoredState()))
        t_blink_on.next_state = self.__blink_off
        self.__blink_on.add_transition(t_blink_on)
        ''' BLINK BEGIN : la machine débute la fonction de clignotement '''
        self.__blink_begin = MonitoredState()
        self.__blink_begin.add_transition(ConditionalTransition(StateValueCondition(9, self.__blink_begin)))

        super().__init__(
            FiniteStateMachine.Layout(
                [
                    self.__off
                    , self.__on
                    , self.__off_duration
                    , self.__on_duration
                ]
                , self.__off
            )
        )

    @property
    def is_on(self) -> bool:
        if self.current_applicative_state is self.__on:
            return True
        return False

    @property
    def is_off(self) -> bool:
        if self.current_applicative_state is self.__off:
            return True
        return False

    def turn_on_0(self):
        self.transit_to(self.__on)

    def turn_off_0(self):
        self.transit_to(self.__off)

    def turn_on_1(self, duration: float):
        self.__on_duration.transitions[0].condition.duration = duration
        while not self.__on_duration.transitions[0].condition:
            print("EN ATTENTE D'ÉTEINTE À ALLUMÉE.")
        self.turn_on_0()

    # VERSION 000
    def turn_off_1(self, duration: float) -> None:
        self.__off_duration.transitions[0].condition.duration = duration
        while not self.__off_duration.transitions[0].condition:
            print("EN ATTENTE D'ALLUMÉE À ÉTEINTE.")
        self.turn_off_0()

    # VERSION 001
    def turn_off_1(self, duration: float) -> None:
        self.__off_duration.transitions[0].condition.duration = duration
        self.transit_to(self.__off_duration.transitions[0].next_state)

    def blink1(self, cycle_duration: float = 3.0, percent_on: float = 0.5, begin_on: bool = True) -> None:
        """ intégrer le custom value """
        self.transit_to(self.__blink_on if begin_on else self.__blink_off)
        if begin_on:
            self.__blink_off.transitions[0].condition.duration = cycle_duration * (1 - percent_on)
        else:
            self.__blink_on.transitions[0].condition.duration = cycle_duration * percent_on

    def blink2(self, total_duration: float, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True,
               end_off: bool = True) -> None:
        pass

    def blink3(self, total_duration: float, n_cycles: int, percent_on: float = 0.5, begin_on: bool = True,
               end_off: bool = True) -> None:
        pass

    def blink4(self, n_cycles: int, cycle_duration: float = 1.0, percent_on: float() = 0.5, begin_on: bool = True,
               end_off: bool = True) -> None:

        # blink_stop_begin.custom_value
        # blink_stop_off.transition0.condition.duration
        # blink_stop_off.transition1.condition.duration
        # blink_stop_on.transition0.condition.duration
        # blink_stop_on.transition1.condition.duration
        # blink_stop_end.custom_value
        pass


class SideBlinker:
    class Side(Enum):
        LEFT = 0
        RIGHT = 1
        BOTH = 2
        LEFT_RECIPROCAL = 3
        RIGHT_RECIPROCAL = 4

    # def __init__(
    #         self
    #         , left_blinker: Blinker
    #         , right_blinker: Blinker
    #         , left_off_state_generator: Blinker.StateGenerator
    #         , left_on_state_generator: Blinker.StateGenerator
    #         , right_off_state_generator: Blinker.StateGenerator
    #         , right_on_state_generator: Blinker.StateGenerator
    # ):
    #     self.__left_blinker = left_blinker
    #     self.__right_blinker = right_blinker

    ''' MÉTHODES '''

    @property
    def is_off(self, side: Side):
        # if side is SideBlinker.Side.LEFT:
        #     if self.__left_blinker.
        pass
        # if side (ex: left_blinker) is off
        # return True
        # else return False

    def is_on(self, side: Side):
        pass
        # if side (ex: left_blinker) is on
        # return True
        # else return False

    def turn_off_0(self, side: Side):
        pass

    def turn_on_0(self, side: Side):
        # if side is SideBlinker.Side.LEFT:
        #     self.__left_blinker.left_on_state_generator()
        pass

    def turn_off_1(self, side: Side, duration: float):
        pass

    def turn_on_1(self, side: Side, duration: float):
        pass

    """ fonctions blink_x """

    def blink_0(
            self
            , side: Side
            , cycle_duration: float = 1.
            , percent_on: float = .5
            , begin_on: bool = True
    ):
        pass

    def blink_1(
            self
            , side: Side
            , total_duration: float
            , cycle_duration: float = 1.
            , percent_on: float = .5
            , begin_on: bool = True
            , end_off: bool = True
    ):
        pass

    def blink_2(
            self
            , side: Side
            , total_duration: float
            , n_cycles: int
            , percent_on: float = .5
            , begin_on: bool = True
            , end_off: bool = True
    ):
        pass

    def blink_3(
            self
            , side: Side
            , n_cycles: int
            , cycle_duration: float = 1.
            , percent_on: float = .5
            , begin_on: bool = True
            , end_on: bool = True
    ):
        pass

    """ fonctions wink_x """

    def wink_0(
            self
            , side: Side
            , wink_duration: float
            , n_winks: int
            , wait_duration: float
            , percent_on: float = .5
            , wait_off: bool = True
            , begin_on: bool = True
    ):
        pass

    def wink_1(
            self
            , side: Side
            , cycle_duration: float
            , wink_duration: float
            , n_winks: int
            , percent_on: float = .5
            , wait_off: bool = True
            , begin_on: bool = True
    ):
        pass

    def wink_2(
            self
            , side: Side
            , wink_duration: float
            , n_winks: int
            , wait_duration: float
            , n_cycles: int
            , percent_on: float = .5
            , wait_off: bool = True
            , begin_on: bool = True
            , end_off: bool = True
    ):
        pass

    def wink_3(
            self
            , side: Side
            , cycle_duration: float
            , wink_duration: float
            , n_winks: int
            , n_cycles: int
            , percent_on: float = .5
            , wait_off: bool = True
            , begin_on: bool = True
            , end_off: bool = True
    ):
        pass

    def track(self):
        pass


if __name__ == '__main__':
    """ TESTS Blinker """
    blinker = Blinker(
        generate_State
        , generate_State
    )

    print("*** TEST 000 : ALLUMER LA MACHINE ***")
    print(blinker.is_on)  # résultat attendu : False
    blinker.turn_on_0()
    print(blinker.is_on)  # résultat attendu : True

    print("*** TEST 001 : ÉTEINDRE LA MACHINE ***")
    print(blinker.is_off)  # résultat attendu : False ( déjà allumée )
    blinker.turn_off_0()
    print(blinker.is_off)  # résultat attendu : True

    print("*** TEST 002 : ALLUMER LA MACHINE APRÈS UNE DURÉE DE TEMPS DÉTERMINÉ ***")
    print(blinker.is_off)  # résultat attendu : True ( machine éteinte )
    blinker.turn_on_1(6.)
    print("LA MACHINE EST ALLUMÉE.")  # la machine est donc ON

    print("*** TEST 003 : ÉTEINDRE LA MACHINE APRÈS UNE DURÉE DE TEMPS DÉTERMINÉ ***")
    print(blinker.is_on)  # résultat attendu : True ( machine allumée )
    blinker.turn_off_1(6.)
    print("LA MACHINE EST ÉTEINTE.")  # la machine est donc OFF

    print("*** TEST 004 : CYCLE DE CLIGNOTEMENT")
    blinker.turn_on_0()  # allumer la machine d'état
    blinker.blink1(6., .5, True)
    while True:
        if blinker.is_on:
            print("ON")
        elif blinker.is_off:
            print("OFF")
