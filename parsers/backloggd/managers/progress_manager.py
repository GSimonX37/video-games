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

    def set(self, maximum: int):
        self.current = 0
        self.maximum = maximum
        self.bars = 0
        self.speed = None
        self.previous_time = time.time()
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
        self.current_status: str | None = None
        self.current_pages: dict[str: int] = {}
        self.total_pages: dict[str: int] = {}
        self.releases: list[str] = []
        self.release_progress_bar = ProgressBar()
        self.overall_progress_bar = ProgressBar()

    def set_total_number_of_pages(self, releases: list[str], numbers_of_pages: list[int]):
        self.releases = releases
        self.current_release = releases[0]
        self.total_pages = {release: count_pages for release, count_pages in zip(releases, numbers_of_pages)}
        self.current_pages = {release: 0 for release in releases}

        self.release_progress_bar.set(self.total_pages[self.current_release])
        self.overall_progress_bar.set(sum(self.total_pages.values()))

    def step(self):
        self.current_pages[self.current_release] += 1
        self.release_progress_bar.step()
        self.overall_progress_bar.step()

        if self.current_pages[self.current_release] == self.total_pages[self.current_release]:
            next_index = self.releases.index(self.current_release) + 1
            if next_index < len(self.releases):
                self.current_release = self.releases[next_index]
                self.release_progress_bar.set(self.total_pages[self.current_release])

    def for_print(self) -> str:
        releases = ''
        for (release, current), total in zip(self.current_pages.items(), self.total_pages.values()):
            releases += f'{release:20} {current:5} of {total:5};\n'
        releases += f'{"total":20} {sum(self.current_pages.values()):5} of {sum(self.total_pages.values()):5}.'

        return (f'{releases}\n'
                f'{self.release_progress_bar.for_print("release")}\n'
                f'{self.overall_progress_bar.for_print("overall")}')
