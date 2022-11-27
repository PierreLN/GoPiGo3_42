from level_three import Blinker, SideBlinker


class Robot():
    def __init__(self) -> None:
        pass




class LedBlinkers(SideBlinker):
    def __init__(self, state_generator: Blinker.StateGenerator):
        super().__init__(state_generator)

        pass

class EyesBlinkers(SideBlinker):
    def __init__(self, state_generator: Blinker.StateGenerator):
        super().__init__(state_generator)

        pass