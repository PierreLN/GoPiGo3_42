from enum import Enum
from level_one import FiniteStateMachine, State
from level_two import StateEntryDurationCondition, ConditionalTransition, MonitoredState, StateValueCondition
from time import perf_counter, sleep
from typing import Callable


class TextStateGenerator():
    def __init__(self, text_in = '', text_out = ''):
        self.__text_in = text_in
        self.__text_out = text_out

    def __call__(self) -> MonitoredState:
        state = MonitoredState()
        state.add_entering_action(lambda :print(self.__text_in))
        # state.add_in_state_action(lambda: print("in state"))
        state.add_exiting_action(lambda :print(self.__text_out))
        return state

class Blinker(FiniteStateMachine):
    StateGenerator = Callable[[], None]
    
    def __init__(self, state_generator: StateGenerator):
        self.__off = state_generator()
        self.__on = state_generator()

        ''' on_duration (inscription de la Transition; initialement, la duration est 0.0 - définie dans turn_on_1()) '''
        self.__on_duration = state_generator()
        self.t_on_duration = ConditionalTransition(StateEntryDurationCondition(.0, self.__on_duration))
        self.t_on_duration.next_state = self.__off
        self.__on_duration.add_transition(self.t_on_duration)

        ''' off_duration (semblable à on_duration) '''
        self.__off_duration = state_generator()
        self.t_off_duration = ConditionalTransition(StateEntryDurationCondition(.0, self.__off_duration))
        self.t_off_duration.next_state = self.__on
        self.__off_duration.add_transition(self.t_off_duration)
        # initialiser une Transition
        # déterminer le prochain état après la Transition effectuée (le State self.__on est le prochain ici)
        # ne pas oublier de dé-commenter plus bas au moment d'ajouter le State dans la liste du Layout


        ''' blink_1'''
        self.__blink_begin = MonitoredState()
        self.__blink_begin.custom_value = .0
        self.__blink_off = state_generator()
        self.__blink_on = state_generator()

        self.t_blink_begin_0 = ConditionalTransition(StateValueCondition(.0, self.__blink_begin))
        self.t_blink_begin_1 = ConditionalTransition(StateValueCondition(.0, self.__blink_begin))
        self.t_blink_begin_0.next_state = self.__blink_off
        self.t_blink_begin_1.next_state = self.__blink_on
        self.__blink_begin.add_transition(self.t_blink_begin_0)
        self.__blink_begin.add_transition(self.t_blink_begin_1)

        self.t_blink_off = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_off))
        self.t_blink_off.next_state = self.__blink_on
        self.__blink_off.add_transition(self.t_blink_off)

        self.t_blink_on = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_on))
        self.t_blink_on.next_state = self.__blink_off
        self.__blink_on.add_transition(self.t_blink_on)

        ''' blink_4'''
        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_begin.custom_value = .0
        self.__blink_stop_end = MonitoredState()
        self.__blink_stop_end.custom_value = .0
        self.__blink_stop_off = state_generator()
        self.__blink_stop_on = state_generator()

        self.t_blink_stop_begin_0 = ConditionalTransition(StateValueCondition(.0, self.__blink_stop_begin))
        self.t_blink_stop_begin_1 = ConditionalTransition(StateValueCondition(.0, self.__blink_stop_begin))
        self.t_blink_stop_begin_0.next_state = self.__blink_stop_off
        self.t_blink_stop_begin_1.next_state = self.__blink_stop_on
        self.__blink_stop_begin.add_transition(self.t_blink_stop_begin_0)
        self.__blink_stop_begin.add_transition(self.t_blink_stop_begin_1)

        self.t_blink_stop_off = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_stop_off))
        self.t_blink_stop_off.next_state = self.__blink_stop_on
        self.__blink_stop_off.add_transition(self.t_blink_stop_off)

        self.t_blink_stop_on = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_stop_on))
        self.t_blink_stop_on.next_state = self.__blink_stop_off
        self.__blink_stop_on.add_transition(self.t_blink_stop_on)

        # add fin ...

        super().__init__(
            FiniteStateMachine.Layout(
                [
                    self.__off
                    , self.__on
                    , self.__on_duration
                    , self.__off_duration
                    , self.__blink_begin
                    , self.__blink_off
                    , self.__blink_on

                    # , self.blink_stop_begin
                    # , self.blink_stop_off
                    # , self.blink_stop_on
                    # , self.blink_stop_end
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
    def is_on_duration(self) -> bool:
        if self.current_applicative_state is self.__on_duration:
            return True
        return False

    @property
    def is_off(self) -> bool:
        if self.current_applicative_state is self.__off:
            return True
        return False

    @property
    def is_off_duration(self) -> bool:
        if self.current_applicative_state is self.__off_duration:
            return True
        return False

    def turn_on_0(self):
        self.transit_to(self.__on)

    def turn_off_0(self):
        self.transit_to(self.__off)

    def turn_on_1(self, duration: float) -> None:
        self.__on_duration.transitions[0].condition.duration = duration
        self.transit_to(self.__on_duration) 

    def turn_off_1(self, duration: float) -> None:
        self.__off_duration.transitions[0].condition.duration = duration
        self.transit_to(self.__off_duration)        

    def blink1(self, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True) -> None:
        self.__blink_begin.custom_value = percent_on
        self.__blink_off.transitions[0].condition.duration = cycle_duration * self.__blink_begin.custom_value
        self.__blink_on.transitions[0].condition.duration = cycle_duration * self.__blink_begin.custom_value
        if begin_on:
            self.transit_to(self.__blink_on)

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

    def track(self):
        pass


if __name__ == '__main__':
    """ TESTS Blinker """
    var = TextStateGenerator('State enter','State exit')
    
    blinker_000 = Blinker(
        var
    )
    ''' test sur la transition d'un état non spécifié à ON (aucun temps requis) - allumer la machine '''
    # print(blinker_000.is_on)  # initialement, résultat attendu est False puisque état initial est OFF
    # blinker_000.turn_on_0()  # allumer la machine d'états
    # print(blinker_000.is_on)  # résultat attendu est désormais True puisque la machine d'états s'est allumé (ON)
    ''' test sur la transition d'un état non spécifié à OFF (aucun temps requis) - éteindre la machine '''
    # print(blinker_000.is_off)  # résultat attendu est False (étant donné le test précédent)
    # blinker_000.turn_off_0()  # éteindre la machine d'états
    # print(blinker_000.is_off)  # résultat attendu est désormais True puisque la machine d'états s'est éteinte (OFF)

    '''
        Test sur le turn_off(duration)
        On appelle track() après avoir pesé sur turn_off(duration)
        après le temps spécifié, le blinker se met à ON 
        TEST VALIDÉ ET APPROUVÉ PAR JC
    '''
    
    blinker_000.turn_off_0() # off
    print(blinker_000.is_on) # check    
    time_reference = perf_counter()
    time_duration = 5
    blinker_000.turn_off_1(duration= 3.0)
    while perf_counter() - time_reference < time_duration:
        blinker_000.track()
        print(blinker_000.is_off_duration) 
        
    # blinker_000.turn_on_0() # on
    # print(blinker_000.is_on) # check  
    # time_reference = perf_counter()
    # time_duration = 5
    # blinker_000.turn_on_1(duration=3.0)
    # print(blinker_000.is_on) # check  
    # while perf_counter() - time_reference < time_duration:
    #     blinker_000.track()
    #     print(blinker_000.is_on_duration) # check  
    
    
    
    # print("clignotant")
    # blinker_000.blink1(cycle_duration=1, percent_on= 0.5, begin_on= True)
    # print(blinker_000.is_on)