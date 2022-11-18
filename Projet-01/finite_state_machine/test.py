from level_one import *
from level_two import *


# Liste de Callable (Actions)
def print_0():
    print("CALLABLE 000")


def print_1():
    print("CALLABLE 001")


def print_2():
    print("CALLABLE 002")


def print_3():
    print("CALLABLE 003")


def print_4():
    print("CALLABLE 004")


def print_5():
    print("CALLABLE 005")


def print_6():
    print("CALLABLE 006")


def print_7():
    print("CALLABLE 007")


def print_8():
    print("CALLABLE 008")


def print_9():
    print("CALLABLE 009")


def print_10():
    print("CALLABLE 010")


def print_11():
    print("CALLABLE 011")


def print_12():
    print("CALLABLE 012")


def print_13():
    print("CALLABLE 013")


def print_14():
    print("CALLABLE 014")


def print_15():
    print("CALLABLE 015")


'''
FONCTIONNEL
    Test #1 :
    Deux ActionState avec une ActionTransition
    Le deuxième state est terminal donc termine le programme
'''


def test_one():
    # Création de la transition
    condition_000 = AlwaysTrueCondition()
    transition_000 = ActionTransition()
    transition_000.condition = condition_000

    # Création des states
    params_000 = State.Parameters()
    # params_000.do_in_state_action_when_entering = True
    # params_000.do_in_state_action_when_exiting = True
    m_state_000 = ActionState(params_000)

    params_001 = State.Parameters()
    params_001.terminal = True
    m_state_001 = ActionState(params_001)

    # Ajout des actions aux states et à la transition
    m_state_000.add_entering_action(print_1)
    m_state_000.add_in_state_action(print_2)
    m_state_000.add_exiting_action(print_3)
    transition_000.add_transiting_action(print_4)
    transition_000.add_transiting_action(print_5)
    m_state_001.add_entering_action(print_6)
    m_state_001.add_in_state_action(print_7)
    m_state_001.add_exiting_action(print_8)

    # Ajout du next_state à la transition
    transition_000.next_state = m_state_001
    # Ajout de la transition au state initial
    m_state_000.add_transition(transition_000)

    # Création de la liste de states pour le layout
    state_list = list()
    state_list.append(m_state_000)
    state_list.append(m_state_001)

    # Création du layout
    layout = FiniteStateMachine.Layout(state_list, m_state_000)
    fsm = FiniteStateMachine(layout)

    # Exécution de la machine d'états
    print(fsm.current_operational_state)  # Current Operational State est soit UNITIALIZED OU IDLE
    fsm.reset()  # Current Operational State est IDLE
    print(fsm.current_operational_state)
    fsm.start(time_budget=0.1)  # Current Operational State devient RUNNING
    print(fsm.current_operational_state)  # Current Operational State est devenu TERMINAL_REACHED


'''
FONCTIONNEL
    Test #2 :
    Deux ActionState avec deux ActionTransition dotées de conditions AlwaysTrueCondition
    Une loop infinie entre les deux states
'''


def test_two():
    # Création des transitions
    condition_000 = AlwaysTrueCondition()
    transition_000 = ActionTransition()
    transition_000.condition = condition_000

    condition_001 = AlwaysTrueCondition()
    transition_001 = ActionTransition()
    transition_001.condition = condition_001

    # Création des states
    params_000 = State.Parameters()
    # params_000.do_in_state_action_when_entering = True
    params_000.do_in_state_action_when_exiting = True
    m_state_000 = ActionState(params_000)
    params_001 = State.Parameters()
    # params_001.do_in_state_action_when_entering = True
    params_001.do_in_state_action_when_exiting = True
    m_state_001 = ActionState(params_001)

    # Ajout des actions aux states et aux transitions
    m_state_000.add_entering_action(print_1)
    m_state_000.add_in_state_action(print_2)
    m_state_000.add_exiting_action(print_3)
    transition_000.add_transiting_action(print_4)
    transition_000.add_transiting_action(print_5)
    m_state_001.add_entering_action(print_6)
    m_state_001.add_in_state_action(print_7)
    m_state_001.add_exiting_action(print_8)
    transition_001.add_transiting_action(print_9)

    # Ajout des next_state aux transitions
    transition_000.next_state = m_state_001
    transition_001.next_state = m_state_000
    # Ajout des transitions aux states
    m_state_000.add_transition(transition_000)
    m_state_001.add_transition(transition_001)

    # Création de la liste de states pour le layout
    state_list = list()
    state_list.append(m_state_000)
    state_list.append(m_state_001)

    # Création du layout
    layout = FiniteStateMachine.Layout(state_list, m_state_000)
    fsm = FiniteStateMachine(layout)

    # Exécution de la machine d'états
    print(fsm.current_operational_state)  # Current Operational State est soit UNITIALIZED OU IDLE
    fsm.reset()  # Current Operational State est IDLE
    print(fsm.current_operational_state)
    fsm.start(time_budget=0.1)  # Current Operational State devient RUNNING
    print(fsm.current_operational_state)  # Current Operational State est devenu TERMINAL_REACHED


'''
FONCTIONNEL
    Test #3 :
    Deux ActionState avec une transition dotée d'une TimedCondition
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''


def test_three():
    # Création de la transition
    condition_000 = TimedCondition(5.0)
    transition_000 = ActionTransition()
    transition_000.condition = condition_000

    # Création des states
    params_000 = State.Parameters()
    # params_000.do_in_state_action_when_entering = True
    params_000.do_in_state_action_when_exiting = True
    m_state_000 = ActionState(params_000)
    params_001 = State.Parameters()
    # params_001.do_in_state_action_when_entering = True
    params_001.do_in_state_action_when_exiting = True
    params_001.terminal = True
    m_state_001 = ActionState(params_001)

    # Ajout des actions aux states et à la transition
    m_state_000.add_entering_action(print_1)
    m_state_000.add_in_state_action(print_2)
    m_state_000.add_exiting_action(print_3)
    transition_000.add_transiting_action(print_4)
    transition_000.add_transiting_action(print_5)
    m_state_001.add_entering_action(print_6)
    m_state_001.add_in_state_action(print_7)
    m_state_001.add_exiting_action(print_8)

    # Ajout des next_state aux transitions
    transition_000.next_state = m_state_001
    # Ajout des transitions aux states
    m_state_000.add_transition(transition_000)

    # Création de la liste de states pour le layout
    state_list = list()
    state_list.append(m_state_000)
    state_list.append(m_state_001)

    # Création du layout
    layout = FiniteStateMachine.Layout(state_list, m_state_000)
    fsm = FiniteStateMachine(layout)

    # Exécution de la machine d'états
    print(fsm.current_operational_state)  # Current Operational State est soit UNITIALIZED OU IDLE
    fsm.reset()  # Current Operational State est IDLE
    print(fsm.current_operational_state)
    fsm.start(time_budget=15)  # Current Operational State devient RUNNING
    print(fsm.current_operational_state)  # Current Operational State est devenu TERMINAL_REACHED


'''
VÉRIFIER OU QU'ON CHANGE LA VALUE DE ValueCondition
    Test #4 :
    Deux ActionState avec une transition dotée d'une ValueCondition
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''


def test_four():
    # Création de la transition
    condition_000 = ValueCondition(1, 100)
    transition_000 = ActionTransition()
    transition_000.condition = condition_000

    # Création des states
    params_000 = State.Parameters()
    # params_000.do_in_state_action_when_entering = True
    params_000.do_in_state_action_when_exiting = True
    m_state_000 = ActionState(params_000)
    params_001 = State.Parameters()
    # params_001.do_in_state_action_when_entering = True
    params_001.do_in_state_action_when_exiting = True
    params_001.terminal = True
    m_state_001 = ActionState(params_001)

    # Ajout des actions aux states et à la transition
    m_state_000.add_entering_action(print_1)
    m_state_000.add_in_state_action(print_2)
    m_state_000.add_exiting_action(print_3)
    transition_000.add_transiting_action(print_4)
    transition_000.add_transiting_action(print_5)
    m_state_001.add_entering_action(print_6)
    m_state_001.add_in_state_action(print_7)
    m_state_001.add_exiting_action(print_8)

    # Ajout des next_state aux transitions
    transition_000.next_state = m_state_001
    # Ajout des transitions aux states
    m_state_000.add_transition(transition_000)

    # Création de la liste de states pour le layout
    state_list = list()
    state_list.append(m_state_000)
    state_list.append(m_state_001)

    # Création du layout
    layout = FiniteStateMachine.Layout(state_list, m_state_000)
    fsm = FiniteStateMachine(layout)

    # Exécution de la machine d'états
    print(fsm.current_operational_state)  # Current Operational State est soit UNITIALIZED OU IDLE
    fsm.reset()  # Current Operational State est IDLE
    print(fsm.current_operational_state)
    fsm.start(time_budget=5)  # Current Operational State devient RUNNING
    print(fsm.current_operational_state)  # Current Operational State est devenu TERMINAL_REACHED


'''
---
    Test #5 :
    Deux ActionState avec une transition dotée d'une AllConditions
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''
def test_five():
    pass

'''
---
    Test #6 :
    Deux ActionState avec une transition dotée d'une AnyConditions
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''
def test_six():
    pass


'''
---
    Test #7 :
    Deux ActionState avec une transition dotée d'une NoneConditions
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''
def test_seven():
    pass


'''
---
    Test #8 :
    Deux MonitoredState avec une transition dotée d'une StateEntryDurationCondition
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''
def test_eight():
    pass


'''
---
    Test #9 :
    Deux MonitoredState avec une transition dotée d'une StateEntryCountCondition
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''
def test_nine():
    pass


'''
---
    Test #10 :
    Deux MonitoredState avec une transition dotée d'une StateValueCondition
    La première action est répétée jusqu'à ce que la condition soit remplie puis la deuxième action est exécutée.
'''
def test_ten():
    pass

if __name__ == '__main__':
    # test_one()
    # test_two()
    # test_three()
    test_four()
    # test_five()
    # test_six()
    # test_seven()
    # test_eight()
    # test_nine()
    # test_ten()
