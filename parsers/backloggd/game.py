import datetime

from bs4 import BeautifulSoup


class Game:
    def __init__(self, release: str):
        self.name: str | None = None
        self.date: datetime.date | None = None
        self.genres: list | None = None
        self.platforms: list[str] | list = []
        self.developers: list[str] | list = []
        self.rating: float | None = None
        self.votes: list[int] | list = []
        self.release: str = release
        self.reviews: int | None = None
        self.plays: int | None = None
        self.playing: int | None = None
        self.backlogs: int | None = None
        self.wishlists: int | None = None
        self.description: str | None = None

    def __bool__(self):
        return any([getattr(self, attribute) for attribute in self.__dict__ if attribute != 'release'])

    def for_csv(self):
        return [
            self.name,
            self.date,
            self.developers,
            self.rating,
            self.votes,
            self.platforms,
            self.genres,
            self.release,
            self.reviews,
            self.plays,
            self.playing,
            self.backlogs,
            self.wishlists,
            self.description
        ]
