from enum import Enum
from logging import raiseExceptions
from operator import truediv
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
        self.__blink_begin.custom_value = True
        
        self.__blink_off = state_generator()
        self.__blink_on = state_generator()

        self.t_blink_begin_0 = ConditionalTransition(StateValueCondition(True, self.__blink_begin))
        self.t_blink_begin_1 = ConditionalTransition(StateValueCondition(False, self.__blink_begin))
        self.t_blink_begin_0.next_state = self.__blink_on
        self.t_blink_begin_1.next_state = self.__blink_off
        self.__blink_begin.add_transition(self.t_blink_begin_0)
        self.__blink_begin.add_transition(self.t_blink_begin_1)

        self.t_blink_on = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_on))
        self.t_blink_on.next_state = self.__blink_off
        self.__blink_on.add_transition(self.t_blink_on)
        self.t_blink_off = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_off))
        self.t_blink_off.next_state = self.__blink_on
        self.__blink_off.add_transition(self.t_blink_off)


        ''' blink_2, blink_3, blink_4'''
        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_begin.custom_value = True
        self.__blink_stop_end = MonitoredState()
        self.__blink_stop_end.custom_value = True
        
        self.__blink_stop_off = state_generator()
        self.__blink_stop_on = state_generator()

        self.t_blink_stop_begin_0 = ConditionalTransition(StateValueCondition(True, self.__blink_stop_begin))
        self.t_blink_stop_begin_1 = ConditionalTransition(StateValueCondition(False, self.__blink_stop_begin))
        self.t_blink_stop_begin_0.next_state = self.__blink_stop_on
        self.t_blink_stop_begin_1.next_state = self.__blink_stop_off
        self.__blink_stop_begin.add_transition(self.t_blink_stop_begin_0)
        self.__blink_stop_begin.add_transition(self.t_blink_stop_begin_1)
        
        
        self.t_blink_stop_off_0 = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_stop_off))
        self.t_blink_stop_off_0.next_state = self.__blink_stop_on
        self.__blink_stop_off.add_transition(self.t_blink_stop_off_0)
        self.t_blink_stop_off_end = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_stop_begin))
        self.t_blink_stop_off_end.next_state = self.__blink_stop_end
        self.__blink_stop_off.add_transition(self.t_blink_stop_off_end)


        self.t_blink_stop_on_0 = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_stop_on))
        self.t_blink_stop_on_0.next_state = self.__blink_stop_off
        self.__blink_stop_on.add_transition(self.t_blink_stop_on_0)
        self.t_blink_stop_on_end = ConditionalTransition(StateEntryDurationCondition(.0, self.__blink_stop_begin))
        self.t_blink_stop_on_end.next_state = self.__blink_stop_end
        self.__blink_stop_on.add_transition(self.t_blink_stop_on_end)
        
        
        self.t__blink_stop_end_0 = ConditionalTransition(StateValueCondition(False, self.__blink_stop_end))
        self.t__blink_stop_end_1 = ConditionalTransition(StateValueCondition(True, self.__blink_stop_end))
        self.t__blink_stop_end_0.next_state = self.__on
        self.t__blink_stop_end_1.next_state = self.__off
        self.__blink_stop_end.add_transition(self.t__blink_stop_end_0)
        self.__blink_stop_end.add_transition(self.t__blink_stop_end_1)
        

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

                    , self.__blink_stop_begin
                    , self.__blink_stop_off
                    , self.__blink_stop_on
                    , self.__blink_stop_end
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
    def is_on_blink(self) -> bool:
        if self.current_applicative_state is self.__blink_on:
            return True
        return False
    
    @property
    def is_blink_stop_on(self) -> bool:
        if self.current_applicative_state is self.__blink_stop_on:
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
    
    @property
    def is_off_blink(self) -> bool:
        if self.current_applicative_state is self.__blink_off:
            return True
        return False    
    
    @property
    def is_blink_stop_off(self) -> bool:
        if self.current_applicative_state is self.__blink_stop_off:
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
        self.__blink_begin.custom_value = begin_on
        self.__blink_off.transitions[0].condition.duration = cycle_duration - (cycle_duration * percent_on)
        self.__blink_on.transitions[0].condition.duration = cycle_duration * percent_on
        
        self.transit_to(self.__blink_begin)

           
    def blink2(self, total_duration: float, cycle_duration: float = 1.0, percent_on: float = 0.5, begin_on: bool = True,
               end_off: bool = True) -> None:
        
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_stop_off.transitions[0].condition.duration = cycle_duration - (cycle_duration * percent_on)
        self.__blink_stop_on.transitions[0].condition.duration = cycle_duration * percent_on
        
        self.__blink_stop_off.transitions[1].condition.duration = total_duration 
        self.__blink_stop_on.transitions[1].condition.duration = total_duration
        self.__blink_stop_end.custom_value = end_off
        
        self.transit_to(self.__blink_stop_begin)
        

    def blink3(self, total_duration: float, n_cycles: int, percent_on: float = 0.5, begin_on: bool = True,
               end_off: bool = True) -> None:
        if n_cycles != 0:
            cycle_duration = total_duration / float(n_cycles)
        else:
            raise ArithmeticError("Cannot divide by 0")
        
        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_stop_off.transitions[0].condition.duration = cycle_duration - (cycle_duration * percent_on)
        self.__blink_stop_on.transitions[0].condition.duration = cycle_duration * percent_on
        
        self.__blink_stop_off.transitions[1].condition.duration = total_duration 
        self.__blink_stop_on.transitions[1].condition.duration = total_duration
        self.__blink_stop_end.custom_value = end_off
        
        self.transit_to(self.__blink_stop_begin)    
        
    
    def blink4(self, n_cycles: int, cycle_duration: float = 1.0, percent_on: float() = 0.5, begin_on: bool = True,
               end_off: bool = True) -> None:

        total_duration = cycle_duration * n_cycles

        self.__blink_stop_begin.custom_value = begin_on
        self.__blink_stop_off.transitions[0].condition.duration = cycle_duration - (cycle_duration * percent_on)
        self.__blink_stop_on.transitions[0].condition.duration = cycle_duration * percent_on
        self.__blink_stop_off.transitions[1].condition.duration = total_duration
        self.__blink_stop_on.transitions[1].condition.duration = total_duration
        self.__blink_stop_end.custom_value = end_off
        
        self.transit_to(self.__blink_stop_begin)



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
    
    # test fonctionne
    # blinker_000.turn_off_0() # off
    # print(blinker_000.is_on) # check    
    # time_reference = perf_counter()
    # time_duration = 5
    # blinker_000.turn_off_1(duration= 3.0)
    # while perf_counter() - time_reference < time_duration:
    #     blinker_000.track()
    #     print(blinker_000.is_off_duration) 
        
    # blinker_000.turn_on_0() # on
    # print(blinker_000.is_on) # check  
    # time_reference = perf_counter()
    # time_duration = 5
    # blinker_000.turn_on_1(duration=3.0)
    # print(blinker_000.is_on) # check  
    # while perf_counter() - time_reference < time_duration:
    #     blinker_000.track()
    #     print(blinker_000.is_on_duration) # check  
    
    # print("== blink_1 ==")
    # blinker_000.blink1(cycle_duration=1, percent_on= 0.7, begin_on = True)
    # while True:
    #     blinker_000.track()
    #     print(blinker_000.is_on_blink)
        
    # print("== blink_2 ==")
    # time_reference = perf_counter()
    # time_duration = 5
    # blinker_000.blink2(total_duration=3.0, cycle_duration=1.0, percent_on= 0.5, begin_on = True, end_off=True)
    # while perf_counter() - time_reference < time_duration:
    #     blinker_000.track()
    #     print(blinker_000.is_blink_stop_off) 
        
    # print("== blink_3 ==")
    # time_reference = perf_counter()
    # time_duration = 10
    # blinker_000.blink3(total_duration=6.0, n_cycles=10, percent_on= 0.5, begin_on = True, end_off=True)
    # while perf_counter() - time_reference < time_duration:
    #     blinker_000.track()
    #     print(blinker_000.is_blink_stop_off)
        
    print("== blink_4 ==")
    time_reference = perf_counter()
    time_duration = 5.0
    blinker_000.blink4(n_cycles=3.0, cycle_duration=1.0, percent_on= 0.5, begin_on = True, end_off=True)
    while perf_counter() - time_reference < time_duration:
        blinker_000.track()
        print(blinker_000.is_blink_stop_off)