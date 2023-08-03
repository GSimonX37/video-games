import time


class ProgressBar:
    def __init__(self):
        self.current: int = 0
        self.maximum: int = 0
        self.bars: int = 0
        self.percents: float = 0.0
        self.speed: float | None = None
        self.previous_time: int | None = None
        self.time_left: int | None = None

    def step(self):
        if self.previous_time:
            self.speed = 60 / (time.time() - self.previous_time)
        if self.speed:
            self.time_left = (self.maximum - self.current) // self.speed
        self.previous_time = time.time()
        self.current += 1
        self.percents = 100 / self.maximum * self.current
        self.bars = int(self.percents)

    def set(self, current: int, maximum: int):
        self.current = current
        self.maximum = maximum
        self.percents = 100 / maximum * current
        self.bars = int(self.percents)
        self.speed = None
        # self.previous_time = time.time()
        self.time_left = None

    def for_print(self, name: str):
        hours = int(self.time_left // 60) if self.time_left else 0
        minutes = int(self.time_left % 60) if self.time_left else 0

        return (f'{name + ":":10}'
                f'{self.speed if self.speed else 0.0:<4.2f} p/m '
                f'|{chr(0x2588) * self.bars:100}| - '
                f'{self.percents:6.2f}% '
                f'({self.current} of {self.maximum}) - '
                f'{hours:02}h {minutes:02}m.')


class ProgressManager:
    def __init__(self):
        self.current_release: str | None = None
        self.progress: dict[str: list[int, int]] = {}
        self.finished: dict[str: list[int, int]] = {}
        self.release_progress_bar = ProgressBar()
        self.overall_progress_bar = ProgressBar()

    def set_progress(self, progress: dict[str: list[int, int]]):
        self.progress = progress
        self.finished = {release: [current_page - 1, last_page]
                         for release, (current_page, last_page) in progress.items()}
        for (release, (current, last)) in self.finished.items():
            if current != last:
                self.current_release = release
                break
        self.release_progress_bar.set(*self.finished[self.current_release])
        self.overall_progress_bar.set(sum([current_page for (current_page, last_page) in self.finished.values()]),
                                      sum([last_page for (current_page, last_page) in self.finished.values()]))

    def step(self):
        self.finished[self.current_release][0] += 1
        self.release_progress_bar.step()
        self.overall_progress_bar.step()

        if self.progress[self.current_release][0] != self.progress[self.current_release][1]:
            self.progress[self.current_release][0] += 1
        else:
            for (release, (current, last)) in self.progress.items():
                if current != last:
                    self.current_release = release
                    self.release_progress_bar.set(self.finished[self.current_release][0],
                                                  self.finished[self.current_release][1])
                    break

    def for_print(self) -> str:
        releases, total_current, total_last = '', 0, 0
        for release, (current_page, last_page) in self.finished.items():
            releases += f'{release:20} {current_page:5} of {last_page:5};\n'

        total_current = sum([current_page for (current_page, last_page) in self.finished.values()])
        total_last = sum([last_page for (current_page, last_page) in self.finished.values()])
        releases += f'{"total":20} {total_current:5} of {total_last:5}.'

        return (f'{releases}\n'
                f'{self.release_progress_bar.for_print("release")}\n'
                f'{self.overall_progress_bar.for_print("overall")}')
