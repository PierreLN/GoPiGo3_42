from enum import Enum
from time import perf_counter
from typing import *
from abc import abstractmethod, ABC

""" LEVEL 01 : STATE """


class State:
    """ ÉTAT APPLICATIF COURANT -> DYNAMIQUE """

    def __init__(self, parameters: 'State.Parameters' = 'State.Parameters()'):
        if isinstance(parameters, State.Parameters):
            self.__params: State.Parameters = parameters
        else:
            raise TypeError('Les paramètres passés doivent être de type State.Parameters.')
        self.__transitions: List[Transition] = list()

    """ ACCESSEURS """

    """ State est valide selon 2 critères
    * existe-il au moins 1 transition ?
    * est-ce que chacune des transitions listées est valide ?
    """

    @property
    def is_valid(self) -> bool:
        # critère 001 : ANNULÉ PAR LE PROF
        #if len(self.__transitions) < 1 and not self.is_terminal:
        #    raise Exception("Il faut au moins une transition à un état qui n'est pas terminal.")
        # critère 002
        for t in self.__transitions:
            if not t.is_valid:
                raise Exception("Une des transitions est invalide. Peut-être qu'il manque la condition.")
        return True

    ''' query '''

    @property
    def is_terminal(self) -> bool:
        return self.__params.terminal

    """ Requête en boucle
    * retourne la première Transition effective
    """

    @property
    def is_transiting(self) -> 'Transition':
        for t in self.__transitions:
            if t.is_transiting:
                return t
        return None

    @property
    def params(self) -> 'Parameters':
        return self.__params

    @property
    def transitions(self) -> List['Transition']:
        return self.__transitions

    ''' MÉTHODES '''

    def add_transition(self, t: 'Transition'):
        self.__transitions.append(t)

    """ Exécution opérations connexes et propres à la mise en marche de State ( initialisation de l'état ) 
    * précède/ symbolise une entrée/ transition vers un State spécifié
    """

    def _exec_entering_action(self):
        self._do_entering_action()

        if self.__params.do_in_state_action_when_entering:
            self._exec_in_state_action()

    """ Exécution opérations propres au State actuel """

    def _exec_in_state_action(self):
        self._do_in_state_action()

    """ Exécution opérations connexes et propres à la mise en arrêt de State ( termination de l'état ) 
    * précède une sortie/ transition vers un autre State
    """

    def _exec_exiting_action(self):
        if self.__params.do_in_state_action_when_exiting:
            self._exec_in_state_action()

        self._do_exiting_action()

    def _do_entering_action(self):
        pass

    def _do_in_state_action(self):
        pass

    def _do_exiting_action(self):
        pass

    """ CLASSES INTERNES """

    class Parameters:
        def __init__(self):
            self.terminal: bool = False
            self.do_in_state_action_when_entering: bool = False
            self.do_in_state_action_when_exiting: bool = False


""" LEVEL 01 : TRANSITION """


class Transition(ABC):
    def __init__(self, next_state: 'State' = None) -> None:
        if isinstance(next_state, State) or next_state is None:
            self.__next_state = next_state
        else:
            raise TypeError("Le prochain état doit être de type State.")

    @property
    def is_valid(self) -> bool:
        return self.__next_state is not None

    @property
    def next_state(self) -> 'State':
        return self.__next_state

    @next_state.setter
    def next_state(self, value: 'State') -> None:
        if isinstance(value, State) or value is None:
            self.__next_state = value
        else:
            raise TypeError("Le prochain état doit être de type State.")

    @abstractmethod
    def is_transiting(self):
        pass

    def _exec_transiting_action(self) -> None:
        self._do_transiting_action()

    def _do_transiting_action(self) -> None:
        pass


""" LEVEL 01 : FINITE STATE MACHINE """

class FiniteStateMachine:
    class OperationState(Enum):
        UNITIALIZED = 0
        IDLE = 1
        RUNNING = 2
        TERMINAL_REACHED = 3

    # infrastucture statique des etat-transitions
    # comme feu de circulation (vert->jaune->rouge  ==> layout)
    class Layout:
        def __init__(self, states: List[State], initial_state: State) -> None:
            self.__states: List[State] = states
            if isinstance(initial_state, State):
                self.__initial_state: State = initial_state
            else:
                raise TypeError('Le paramètre doit être typé "State".')
            self.is_valid

        @property
        def is_valid(self) -> bool:
            if self.__initial_state is None:
                raise Exception('Il faut passer en paramètre un état initial de type State.')
            if self.__initial_state not in self.__states:
                raise Exception("Il faut que l'état initial soit dans la liste des états.")
            for state in self.__states:
                if not state.is_valid:
                    raise Exception("Une des transitions ne possède pas de prochain état.")
            return True

        @property
        def initial_state(self) -> State:
            return self.__initial_state

        @initial_state.setter
        def initial_state(self, value: State) -> None:
            if isinstance(value, State):
                self.__initial_state = value
            else:
                raise TypeError("Le paramètre doit être typé 'float'.")

        def add_state(self, state: State) -> None:
            if isinstance(state, State):
                self.__states.append(state)
            else:
                raise TypeError("L'état doit être de type State.")

        def add_states(self, statelist: List[State]) -> None:
            for state in statelist:
                if isinstance(state, State):
                    self.__states.append(state)
                else:
                    raise TypeError("Les états doivent être de type State")

    # A revoir
    def __init__(self, layout: Layout, uninitialized: bool = True) -> None:
        if isinstance(layout, FiniteStateMachine.Layout):
            self.__layout: FiniteStateMachine.Layout = layout
        else:
            raise TypeError('Layout not initialised')

        self.__current_applicative_state: State = self.__layout.initial_state
        self.__current_operational_state: FiniteStateMachine.OperationState = \
            FiniteStateMachine.OperationState.UNITIALIZED if uninitialized else FiniteStateMachine.OperationState.IDLE

    # l'action en cours de l'engin de resolution
    @property
    def current_operational_state(self) -> OperationState:
        return self.__current_operational_state

    # l'etat courant de la partie applicative
    @property
    def current_applicative_state(self) -> State:
        return self.__current_applicative_state

    def _transit_by(self, transition: Transition):
        self.__current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        self.__current_applicative_state._exec_entering_action()

    def transit_to(self, state: State):
        self.__current_applicative_state = state
        self.current_applicative_state._exec_entering_action()
        
    def track(self) -> bool:
        # logique de fait un pas de calcul et validation de transition et appel de fonctions
        if self.__current_operational_state != FiniteStateMachine.OperationState.TERMINAL_REACHED:
            # Si le state est terminal, on indique qu'on entre en état terminal après avoir exécuté son in_state_action()
            if self.__current_applicative_state.params.terminal:
                self.__current_operational_state = FiniteStateMachine.OperationState.TERMINAL_REACHED
            transition = self.__current_applicative_state.is_transiting
            if transition is not None:
                self._transit_by(transition)
            else:
                self.__current_applicative_state._exec_in_state_action()
            return True
        else:
            return False

    def reset(self) -> OperationState:
        self.__current_operational_state = FiniteStateMachine.OperationState.IDLE
        return self.__current_operational_state

    def start(self, reset: bool = True, time_budget: float = None) -> None:
        timer_start = perf_counter()
        self.__current_operational_state = FiniteStateMachine.OperationState.RUNNING
        self.__current_applicative_state._exec_entering_action()
        while reset is True:
            # comteur de temps en seconde
            timer_total = perf_counter() - timer_start
            # print(self.__current_operational_state)
            if time_budget is not None:
                if not self.track() or timer_total > time_budget:
                    return
            else:
                if not self.track():
                    return

    def stop(self) -> OperationState:
        if self.__current_operational_state == FiniteStateMachine.OperationState.RUNNING:
            self.__current_operational_state = FiniteStateMachine.OperationState.IDLE
        return self.__current_operational_state


### TESTING ###

if __name__ == '__main__':
    # créer Transition

    # créer State ( ajouter transitions liste dans un State )
    # créer Layout ( ajouter les State )
    print(FiniteStateMachine.Layout(list(), None))
    # construire FSM avec Layout