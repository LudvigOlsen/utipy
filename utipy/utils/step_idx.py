
# TODO Add tests

class StepIdx:

    def __init__(self, start_idx: int = 0) -> None:
        """
        A counter for stepping through some list of tasks.
        Get current, previous and next indices.

        Parameters
        ----------
        start_idx : int
            Starting index.
        """
        self.current = start_idx

    def step(self) -> None:
        """
        Take a step. 
        Increases "current index" by 1.
        """
        self.current += 1

    @property
    def previous(self) -> int:
        """
        Get the index of the previous step.

        Returns
        -------
        int
            Previous index.
        """
        if self.current == 0:
            raise ValueError("`current` was 0 which has no `previous` index.")
        return self.current - 1

    @property
    def next(self) -> int:
        """
        Get the index of the following step.

        Returns
        -------
        int
            Next index.
        """
        return self.current + 1
