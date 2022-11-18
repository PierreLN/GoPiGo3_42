from typing import List, Callable
from abc import abstractmethod, ABC
# from state import State


class Transition(ABC):
    def __init__(self, next_state: 'State' = None) -> None:
        self.__next_state = next_state
    
    @property
    def is_valid(self) -> bool:
        return self.__next_state is not None

    @property
    def next_state(self) -> 'State':
        return self.__next_state

    @next_state.setter
    def next_state(self, value: 'State') -> None:
        self.__next_state = value

    @abstractmethod
    def is_transiting(self):
        pass

    # TO MODIFY : fill function
    def _exec_transiting_action(self) -> None:
        self._do_transiting_action()

    # TO MODIFY : fill function
    def _do_transiting_action(self) -> None:
        pass


class ConditionalTransition(Transition):
    def __init__(self) -> None:
        super().__init__()

    def is_transiting(self):
        pass


class ActionTransition(ConditionalTransition):
    def __init__(self, next_state: 'State' = None) -> None:
        super().__init__()
        self.next_state = next_state
        self.__transiting_actions: List['ActionTransition.Action'] = list()

    # TO MODIFY : fill function
    def _do_transiting_action(self) -> None:
        for transiting_action in self.__transiting_actions:
            transiting_action.callable()

    def add_transiting_action(self, action: 'ActionTransition.Action') -> None:
        self.__transiting_actions.append(action)

    # Custom data type Action
    class Action():
        def __init__(self, action: Callable) -> None:
            self.__callable = action
        
        @property
        def callable(self) -> Callable:
            return self.__callable


class MonitoredTransition(ActionTransition):
    def __init__(self, next_state:int = None) -> None:
        super().__init__(next_state)
        self.__transit_count: int = 0
        self.__last_transit_time: float = 0
        self.custom_value = None
    
    @property
    def transit_count(self) -> int:
        return self.__transit_count
    
    @property
    def last_transit_time(self) -> float:
        return self.__last_transit_time

    def reset_transit_count(self) -> None:
        self.__transit_count = 0

    def reset_last_transit_time(self) -> None:
        self.__last_transit_time = 0

    # TO MODIFY : fill function
    def _exec_transiting_action(self) -> None:
        self._do_transiting_action()


def print_hello_world():
    print('hello world')


if __name__ == '__main__':
    monitored_t = MonitoredTransition(1)
    print(monitored_t.is_valid)
    action = monitored_t.Action(print_hello_world)
    monitored_t.add_transiting_action(monitored_t.Action(print_hello_world))
    monitored_t._exec_transiting_action()
    print(monitored_t._ActionTransition__transiting_actions)