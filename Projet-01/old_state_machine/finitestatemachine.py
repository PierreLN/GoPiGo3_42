from enum import Enum
from time import perf_counter
from typing import *

# from transition import Transition
# from state import State

class FiniteStateMachine():

    class OperationState(Enum):
        UNITIALIZED = 0
        IDLE = 1
        RUNNING = 2
        TERMINAL_REACHED = 3

    # infrastucture statique des etat-transitions
    # comme feu de circulation (vert->jaune->rouge  ==> layout)
    class Layout():
        def __init__(self, states: List[State], initial_state: State) -> None: 
            self.__states = states
            self.__initial_state = initial_state

        @property
        def is_valid(self) -> bool:
            return self.__initial_state is not None

        @property
        def initial_state(self) -> State:
            return self.__initial_state

        @initial_state.setter
        def initial_state(self, value: State) -> None:
            self.__initial_state = value

        def add_state(self, state: State) -> None:
            self.__states.append(state)

        def add_states(self, statelist: List[State]) -> None:
            for state in statelist:
                self.__states.append(state)

    def __init__(self, layout: FiniteStateMachine.Layout, uninitialized: bool = True) -> None:
        # raise exception
        if self.__layout is not Layout:
            raise TypeError('Layout not initialised') 
        else:
            self.__layout: Layout = layout
        self.__current_applicative_state: State = self.__layout.initial_state
        self.__current_operational_state: OperationState = uninitialized


    # l'action e cours de l'engin de resolution
    @property
    def current_operational_state(self) -> OperationState:
        return self.__current_operational_state

    # l'etat courant de la partie applicative
    @property
    def current_applicative_state(self) -> State:
        return self.__current_applicative_state

    def transit_by(self, transition: Transition) -> Transition:
        return transition

    def transit_to(self, state: int) -> State:
        return state

    def track(self) -> bool:
        # logique de fait un pas de calcul et validation de transition et appel de fonctions
        if self.__current_operational_state == OperationState.TERMINAL_REACHED:
            return False
        else:
            return True
    
    def reset(self) -> OperationState:
        if self.__current_operational_state == OperationState.RUNNING:
            self.stop()
        self.__current_operational_state = OperationState.IDLE
        return self.__current_operational_state

    def start(self, reset: bool = True, time_budget: float = None) -> OperationState:
        timer_start = perf_counter()
        while reset is True:
            # comteur de temps en seconde
            timer_total = perf_counter() - timer_start
            if not self.track() or timer_total > time_budget:
                print(timer_total)
                return 

    def stop(self) -> OperationState:
        if self.__current_operational_state == OperationState.RUNNING:
            self.__current_operational_state = OperationState.IDLE
        return self.__current_operational_state

if __name__ == '__main__':

    layout = FiniteStateMachine.Layout('la liste', 0)
    fsm = FiniteStateMachine(layout, 1, OperationState.UNITIALIZED)

    '''
        # simulation a partir du depart
        print(f'1er -> {fsm.current_operational_state}')
        fsm.reset()
        print(f'2e -> {fsm.current_operational_state}')
        fsm.start(time_budget= 3)
        print(fsm.track())
    '''

    # simulation a partir de la fin
    fsm2 = FiniteStateMachine(layout, 1, OperationState.TERMINAL_REACHED)

    print(f'1er -> {fsm2.current_operational_state}')
    fsm2.reset()
    print(f'2e -> {fsm2.current_operational_state}')

