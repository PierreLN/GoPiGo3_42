from __future__ import annotations
from typing import List, Callable
from transition import Transition


class State:
    """ ÉTAT APPLICATIF COURANT -> DYNAMIQUE """

    def __init__(self):
        self.__params: State.Parameters = self.Parameters()
        self.__transitions: List[Transition] = list()

    """ ACCESSEURS """

    """ State est valide selon 2 critères
    * existe-il au moins 1 transition ?
    * est-ce que chacune des transitions listées est valide ?
    """

    @property
    def is_valid(self) -> bool:
        # critère 001
        if len(self.__transitions) < 1:
            print("IS_NOT_VALID -> NO Transition LISTED")
            return False

        # critère 002
        for t in self.__transitions:
            if t.is_valid:
                continue
            else:
                print("IS_NOT_VALID -> AT LEAST A SINGLE Transition IS INVALID")
                return False

        print("IS_VALID")
        return True

    ''' query '''

    @property
    def is_terminal(self) -> bool:
        print("IS_TERMINAL")
        return True

    """ Requête en boucle
    * retourne la première Transition effective
    """

    @property
    def is_transiting(self) -> Transition:
        # au moins 1 Transition doit être référée depuis self.__transitions
        if len(self.__transitions) < 1:
            raise ValueError("Veuillez ajouter, au minimum, 1 Transition dans le conteneur self.__transitions.")

        search = True
        while search:
            for t in self.__transitions:
                if t.is_transiting:
                    search = False
                    print("IS_TRANSITING")
                    return t

    @property
    def params(self) -> Parameters:
        return self.__params

    @property
    def transitions(self) -> List[Transition]:
        print("UNE LISTE DE Transition")
        return self.__transitions

    ''' MÉTHODES '''

    def add_transition(self, t: Transition) -> bool:
        self.__transitions.append(t)
        print(self.__transitions)
        return True

    """ Exécution opérations connexes et propres lors de la mise en marche de State ( initialisation de l'état ) 
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
            print("EXEC_IN_STATE_ACTION + EXEC_EXITING_ACTION")

        self._do_exiting_action()
        print(" EXEC_EXITING_ACTION ")

    def _do_entering_action(self):  # tâche applicative
        pass

    def _do_in_state_action(self):  # tâche applicative
        pass

    def _do_exiting_action(self):  # tâche applicative
        pass

    """ CLASSES INTERNES """

    class Parameters:
        def __init__(self):
            self.terminal: bool = False
            self.do_in_state_action_when_entering: bool = False
            self.do_in_state_action_when_exiting: bool = False


class ActionState(State):
    """ PERMET LA GÉNÉRATION DE State """

    def __init__(self):  # params : Parameters ?
        super().__init__()
        self.__entering_actions: List[ActionState.Action] = list()
        self.__in_state_actions: List[ActionState.Action] = list()
        self.__exiting_actions: List[ActionState.Action] = list()

    """ MÉTHODES """

    def _do_entering_action(self) -> None:  # override
        for a in self.__entering_actions:
            a()

    def _do_in_state_action(self) -> None:  # override
        for a in self.__in_state_actions:
            a()

    def _do_exiting_action(self) -> None:  # override
        for a in self.__exiting_actions:
            a()

    def add_entering_action(self, action: Action):
        if self.__is_callable_action(action):
            self.__entering_actions.append(action)
            print("ADDED ENTERING ACTION")
            print(self.__entering_actions)

    def add_in_state_action(self, action: Action):
        if self.__is_callable_action(action):
            self.__in_state_actions.append(action)
            print("ADDED IN STATE ACTION")
            print(self.__in_state_actions)

    def add_exiting_action(self, action: Action):
        if self.__is_callable_action(action):
            self.__exiting_actions.append(action)
            print("ADDED EXITING ACTION")
            print(self.__exiting_actions)

    @staticmethod
    def __is_callable_action(action: Action) -> bool:
        if callable(action):
            return True
        else:
            raise RuntimeError("L'objet Action transmis en paramètre n'est pas un callable.")

    """ CLASSES INTERNES """

    class Action:
        """ CRÉATION DE State POSSIBLE PAR Action, LORS D'OPÉRATIONS ( entering, in_state, exiting, transiting ) """

        def __init__(self, action: Callable) -> None:
            self.action = action

        def __call__(self, *args, **kwargs) -> any:
            self.action()


class MonitoredState(ActionState):
    """ UTILITAIRE
    * informations supplémentaires :
    - temps d'activité
    - compteurs

    * permet automatisation conditionnelle :
    - transition après un certain temps écoulé
    - transition après un certain nombre d'occurrences
    - transition selon une condition
    """

    def __init__(self):  # params : Parameters ?
        super().__init__()
        self.__counter_last_entry: float = 0.
        self.__counter_last_exit: float = 0.
        self.__entry_count: int = 0
        self.custom_value: any

    """ ACCESSEURS """

    @property
    def last_entry_time(self) -> float:
        return self.__counter_last_entry

    @property
    def last_exit_time(self) -> float:
        return self.__counter_last_exit

    @property
    def entry_count(self) -> int:
        return self.__entry_count

    """ MUTATEURS """

    @last_entry_time.setter
    def last_entry_time(self, new_entry_time: float) -> bool:
        if type(new_entry_time) is float:
            self.__counter_last_entry: float = new_entry_time
            return True
        else:
            raise TypeError("Le paramètre doit être typé 'float'.")

    @last_exit_time.setter
    def last_exit_time(self, new_exit_time: float) -> bool:
        if type(new_exit_time) is float:
            self.__counter_last_exit: float = new_exit_time
            return True
        else:
            raise TypeError("Le paramètre doit être typé 'float'.")

    @entry_count.setter
    def entry_count(self, new_entry_count: int) -> bool:
        if type(new_entry_count) is int:
            self.__entry_count: int = new_entry_count
            return True
        else:
            raise TypeError("Le paramètre doit être typé 'int'.")

    """ MÉTHODES """

    def reset_last_times(self):
        self.last_entry_time: float = 0.
        self.last_exit_time: float = 0.

    def reset_entry_count(self):
        self.entry_count: int = 0

    def _exec_entering_action(self):
        pass

    def _exec_exiting_action(self):
        pass


""" TESTS """
if __name__ == '__main__':
    state = State()
    param_001 = state.params.terminal
    param_002 = state.params.do_in_state_action_when_entering
    param_003 = state.params.do_in_state_action_when_exiting
    print(param_001, param_002, param_003)
    # ajouter une Transition
    state.add_transition(Transition(3))
    transitions = state.transitions
    print(transitions)
    print("is_valid: ", state.is_valid)
    print("is_terminal: ", state.is_terminal)
    print("is_transiting: ", state.is_transiting)

    action_state = ActionState()
    print("_exec_in_state_action from subclass: ", action_state._exec_in_state_action())
    print("_exec_entering_action from subclass: ", action_state._exec_entering_action())
    print("_exec_exiting_action from subclass: ", action_state._exec_exiting_action())


    def print_hello() -> any:
        print("HELLO, WORLD!")


    action_state.add_entering_action(action_state.Action(print_hello))
    action_state.add_exiting_action(action_state.Action(print_hello))
    action_state.add_in_state_action(action_state.Action(print_hello))

    monitor = MonitoredState()
    print(monitor.last_entry_time)
    print(monitor.last_exit_time)
    print(monitor.entry_count)
    monitor.last_entry_time = 3.
    monitor.last_exit_time = 3.
    monitor.entry_count = 3
    print("SET")
    print(monitor.last_entry_time)
    print(monitor.last_exit_time)
    print(monitor.entry_count)
    monitor.reset_last_times()
    monitor.reset_entry_count()
    print("RESET")
    print(monitor.last_entry_time)
    print(monitor.last_exit_time)
    print(monitor.entry_count)

    # Callable ( test )
    action_state._do_entering_action()
    action_state._do_exiting_action()
    action_state._do_in_state_action()
