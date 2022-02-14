
# TODO Add documentation and tests
# TODO Allow yielding?

class StepIdx:

    def __init__(self, start_idx=0) -> None:
        self.current = start_idx

    def step(self):
        self.current += 1

    @property
    def previous(self):
        if self.current == 0:
            raise ValueError("`current` was 0 which has no `previous` index.")
        return self.current - 1

    @property
    def next(self):
        return self.current + 1
