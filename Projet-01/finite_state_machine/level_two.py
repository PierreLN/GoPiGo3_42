from mimetypes import init
from level_one import *
from abc import ABC, abstractmethod
from time import perf_counter
from typing import List


""" LEVEL 02 : STATE """


class ActionState(State):
    """ PERMET LA GÉNÉRATION DE State """

    def __init__(self, parameters: 'State.Parameters' = State.Parameters()):
        if not isinstance(parameters, State.Parameters):
            raise TypeError('Les paramètres passés doivent être de type State.Parameters.')
        super().__init__(parameters)
        ''' créer State par manipulation d'un Callable typé Action lorsque: entering, in_state, exiting, transiting '''
        self.__entering_actions: List[ActionState.Action] = list()
        self.__in_state_actions: List[ActionState.Action] = list()
        self.__exiting_actions: List[ActionState.Action] = list()

    Action = Callable[[], None]

    """ MÉTHODES """

    # @override
    def _do_entering_action(self):
        for action in self.__entering_actions:
            action()

    # @override
    def _do_in_state_action(self):
        for action in self.__in_state_actions:
            action()

    # @override
    def _do_exiting_action(self):
        for action in self.__exiting_actions:
            action()

    def add_entering_action(self, action: 'ActionState.Action'):
        if self.__is_callable_action(action):
            self.__entering_actions.append(action)

    def add_in_state_action(self, action: 'ActionState.Action'):
        if self.__is_callable_action(action):
            self.__in_state_actions.append(action)

    def add_exiting_action(self, action: 'ActionState.Action'):
        if self.__is_callable_action(action):
            self.__exiting_actions.append(action)

    @staticmethod
    def __is_callable_action(action: 'ActionState.Action') -> bool:
        if callable(action):
            return True
        else:
            raise RuntimeError("L'objet 'action' transmis en paramètre n'est pas un Callable.")


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

    def __init__(self, parameters: 'State.Parameters' = State.Parameters()):
        if not isinstance(parameters, State.Parameters):
            raise TypeError('Les paramètres passés doivent être de type State.Parameters.')
        super().__init__(parameters)
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

    @property
    def custom_value(self) -> any:
        return self.custom_value

    """ MUTATEURS """

    @last_entry_time.setter
    def last_entry_time(self, new_entry_time: float):
        if type(new_entry_time) is float:
            self.__counter_last_entry: float = new_entry_time
        else:
            raise TypeError("Le paramètre doit être typé 'float'.")

    @last_exit_time.setter
    def last_exit_time(self, new_exit_time: float):
        if type(new_exit_time) is float:
            self.__counter_last_exit: float = new_exit_time
        else:
            raise TypeError("Le paramètre doit être typé 'float'.")

    @entry_count.setter
    def entry_count(self, new_entry_count: int):
        if type(new_entry_count) is int:
            self.__entry_count: int = new_entry_count
        else:
            raise TypeError("Le paramètre doit être typé 'int'.")

    @custom_value.setter
    def custom_value(self, new_custom_value: any):
        self.custom_value = new_custom_value

    """ MÉTHODES """

    def reset_last_times(self):
        self.last_entry_time: float = 0.
        self.last_exit_time: float = 0.

    def reset_entry_count(self):
        self.entry_count: int = 0

    def _exec_entering_action(self):
        self._do_entering_action()

    def _exec_exiting_action(self):
        self._do_exiting_action


#########################


""" LEVEL 02 : TRANSITION """


class ConditionalTransition(Transition):
    def __init__(self, condition: 'Condition' = None) -> None:
        super().__init__()
        if isinstance(condition, Condition) or condition is None:
            self.__condition = condition
        else:
            raise TypeError("Le type de la condition doit être Condition.")

    @property
    def is_valid(self) -> bool:
        return self.__condition is not None

    @property
    def condition(self) -> 'Condition':
        return self.__condition

    @condition.setter
    def condition(self, value: 'Condition') -> None:
        if isinstance(value, Condition) or value is None:
            self.__condition = value
        else:
            raise TypeError("La condition doit être de type Condition.")

    @property
    def is_transiting(self) -> bool:
        if self.__condition is not None:
            return bool(self.__condition)
        else:
            return True


class ActionTransition(ConditionalTransition):
    Action = Callable[[], None]

    def __init__(self, next_state: 'State' = None) -> None:
        super().__init__()
        if isinstance(next_state, State) or next_state is None:
            self.__next_state = next_state
        else:
            raise TypeError("Le prochain état doit être de type State.")
        self.__transiting_actions: List['ActionTransition.Action'] = list()

    def _do_transiting_action(self) -> None:
        for transiting_action in self.__transiting_actions:
            transiting_action()

    def add_transiting_action(self, action: 'ActionTransition.Action') -> None:
        if callable(action):
            self.__transiting_actions.append(action)
        else:
            raise TypeError("L'action de transition doit être un Callable.")


class MonitoredTransition(ActionTransition):
    def __init__(self, next_state: 'State' = None) -> None:
        if isinstance(next_state, State) or next_state is None:
            super().__init__(next_state)
        else:
            raise TypeError("Le prochain état doit être de type State.")
        self.__transit_count: int = 0
        self.__last_transit_time: float = 0
        self.custom_value: any

    @property
    def transit_count(self) -> int:
        return self.__transit_count

    @property
    def last_transit_time(self) -> float:
        return self.__last_transit_time

    def reset_transit_count(self) -> None:
        self.__transit_count = 0

    def reset_last_transit_time(self) -> None:
        self.__last_transit_time = 0.0

    def _exec_transiting_action(self) -> None:
        start_time = perf_counter()
        self._do_transiting_action()
        self.__transit_count += 1
        self.__last_transit_time = perf_counter() - start_time


#########################


""" LEVEL 02: CONDITIONS """


class Condition(ABC):
    def __init__(self, inverse: bool = False) -> None:
        if type(inverse) is bool:
            self.__inverse = inverse
        else:
            raise TypeError("La variable inverse doit être de type bool.")

    # @property
    # def inverse(self) -> None:
    #     return self.__inverse
    #
    # @inverse.setter
    # def inverse(self, value: bool) -> bool:
    #     if type(value) is bool:
    #         self.__inverse = value
    #     else:
    #         raise TypeError("Le prochain état doit être de type bool.")

    @abstractmethod
    def _compare(self) -> bool:
        pass

    def __bool__(self) -> bool:
        return self._compare() ^ self.__inverse


class AlwaysTrueCondition(Condition):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self):
        return True


class ValueCondition(Condition):
    def __init__(self, initial_value: any, expected_value: any, inverse: bool = False):
        super().__init__(inverse)
        self.expected_value = expected_value
        self.value = initial_value

    def _compare(self):
        return self.value == self.expected_value


class TimedCondition(Condition):
    def __init__(self, duration: float = 1, time_reference: float = None, inverse: bool = False):
        super().__init__(inverse)
        if type(duration) is float:
            self.__counter_duration = duration
        else:
            raise TypeError("La variable duration doit être de type float.")
        if type(time_reference) is float:
            self.__counter_reference = time_reference
        elif time_reference is None:
            self.__counter_reference = perf_counter()
        else:
            raise TypeError("La variable time_reference doit être de type float ou None.")

    def _compare(self):
        return perf_counter() - self.__counter_reference >= self.__counter_duration

    @property
    def duration(self) -> float:
        return self.__counter_duration

    @duration.setter
    def duration(self, value: float) -> None:
        if type(value) is float:
            self.__counter_duration = value
        else:
            raise TypeError("La variable duration doit être de type float")

    def reset(self):
        self.__counter_reference = perf_counter()


########


# Comment cet objet peut être une liste de conditions ???
# class ConditionList:
#     def __init__(self):
#         pass
ConditionList: List[Condition] = []


class ManyConditions(Condition):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        self._conditions: List[Condition] = ConditionList

    def add_condition(self, condition: Condition):
        if isinstance(condition, Condition):
            self._conditions.append(condition)
        else:
            raise TypeError("La condition doit être de type Condition")

    def add_conditions(self, conditions: ConditionList):
        for condition in conditions:
            if isinstance(condition, Condition):
                self._conditions.append(condition)
            else:
                raise TypeError("Les conditions doivent être de type Condition")


class AllCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        self.__inverse: bool = inverse

    def _compare(self) -> bool:
        return self.__inverse


class NoneCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        return self.__inverse


class AnyCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        return self.__inverse


########


''' MonitoredStateCondition '''


class MonitoredStateCondition(Condition):
    def __init__(self, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(inverse)
        if isinstance(monitored_state, MonitoredState):
            self._monitored_state: MonitoredState = monitored_state
        else:
            raise TypeError("La variable monitored_state doit être de type MonitoredState")

    """ ACCESSEURS """

    @property
    def monitored_state(self) -> MonitoredState:
        return self._monitored_state

    """ MUTATEURS """

    @monitored_state.setter
    def monitored_state(self, new_monitored_state):
        if isinstance(new_monitored_state, MonitoredState):
            self._monitored_state = new_monitored_state
        else:
            raise TypeError(
                "L'argument transmis: new_monitored_state doit être une instance de la classe MonitoredState.")


class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration: float, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(monitored_state, inverse)
        ''' le temps requis à passer dans un certain State avant de déclencher transition vers le prochain State '''
        self.__duration: float = duration
        self.__inverse: bool = inverse
        self._monitored_state.last_entry_time = perf_counter()  # secondes

    """ ACCESSEURS """

    @property
    def duration(self) -> float:
        return self.__duration

    @property
    def perf_counter(self) -> float:
        return perf_counter() - self.__elapsedTime
    """ MUTATEURS """

    @duration.setter
    def duration(self, new_duration: float):
        if not isinstance(new_duration, float):
            raise TypeError("Le paramètre doit être typé 'float'.")
        self.__duration = new_duration

    """ MÉTHODES """

    ''' inverse géré implicitement par magic function __call__ de la classe Condition '''
    ''' condition véritable lorsque temps passé dans un State à quitter dépasse le temps requis avant de transiger '''

    def _compare(self) -> bool:
        return perf_counter() - self._monitored_state.last_entry_time >= self.__duration


class StateEntryCountCondition(MonitoredStateCondition):
    def __init__(
            self
            , expected_count: int
            , monitored_state: MonitoredState
            , auto_reset: bool = True
            , inverse: bool = False
    ):
        super().__init__(monitored_state, inverse)
        if type(auto_reset) is bool:
            self.__auto_reset: bool = auto_reset
        else:
            raise TypeError("La variable auto_reset doit être de type bool")
        ''' référence sur le nombre de fois que l'état à requis une transition ( incrémentation ) '''
        self.__ref_count: int = 0
        ''' compte de requêtes nécessaires avant la transition '''
        if type(expected_count) is int:
            self.__expected_count: int = expected_count
        else:
            raise TypeError("La variable expected_count doit être de type int")

    """ ACCESSEURS """

    @property
    def expected_count(self) -> int:
        return self.__expected_count

    """ MUTATEURS """

    @expected_count.setter
    def expected_count(self, expected_count: int):
        if type(expected_count) is int:
            self.__expected_count = expected_count
        else:
            raise TypeError("Le paramètre doit être typé 'int'.")

    """ MÉTHODES """

    ''' inverse géré implicitement par magic function __call__ de la classe Condition '''
    ''' condition véritable lorsque le nombre de fois que le State sollicite la transition dépasse le nombre '''

    def _compare(self) -> bool:
        self.__ref_count += 1
        return self.__ref_count >= self.__expected_count

    def reset_count(self):
        self.__ref_count = 0


class StateValueCondition(MonitoredStateCondition):
    def __init__(self, expected_value: any, monitored_state: MonitoredState, inverse: bool = False):
        super().__init__(monitored_state, inverse)
        ''' self.__expected_value strictement équivalente à MonitoredState's custom_value propriété '''
        self.__expected_value: any = expected_value

    """ ACCESSEURS """

    @property
    def expected_value(self) -> any:
        return self.__expected_value

    """ MUTATEURS """

    @expected_value.setter
    def expected_value(self, new_expected_value: any):
        self.__expected_value = new_expected_value

    """ MÉTHODES """

    ''' inverse géré implicitement par magic function __call__ de la classe Condition '''
    ''' condition véritable lorsque self.expected_value est strictement équivalent à MonitoredState.custom_value '''

    def _compare(self) -> bool:
        return self.__expected_value == self._monitored_state.custom_value
