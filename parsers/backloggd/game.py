import datetime

from bs4 import BeautifulSoup


class Game:
    def __init__(self, release: str):
        self.name: str | None = None
        self.date: datetime.date | None = None
        self.genres: list | None = None
        self.platforms: list | None = None
        self.developers: list | None = None
        self.rating: float | None = None
        self.release: str = release
        self.main: str | None = None
        self.reviews: int | None = None
        self.plays: int | None = None
        self.playing: int | None = None
        self.backlogs: int | None = None
        self.wishlists: int | None = None
        self.description: str | None = None

    async def basic_data_parsing(self, soup):
        await self.get_name(soup)
        await self.get_date(soup)
        await self.get_companies(soup)
        await self.get_rating(soup)
        await self.get_reviews(soup)
        await self.get_platform(soup)
        await self.get_genres(soup)
        await self.get_description(soup)
        self.main = await self.get_release(soup) if self.release != 'main' else self.name

    async def get_name(self, soup: BeautifulSoup):
        try:
            name = soup.find('h1', class_='mb-0').text
            self.name = name
        except AttributeError:
            return
        except ValueError:
            return

    async def get_date(self, soup: BeautifulSoup):
        try:
            date = (soup
                    .find('div', class_='col-auto mt-auto pr-0')
                    .find('a')
                    .text)
            self.date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')
        except AttributeError:
            return None
        except ValueError:
            return None

    async def get_companies(self, soup: BeautifulSoup):
        try:
            companies = (soup
                         .find('div', class_='col-auto pl-lg-1 sub-title')
                         .find_all('a'))
            self.developers = [*map(lambda x: x.text, companies)]
        except AttributeError:
            self.developers = []
        except ValueError:
            self.developers = []

    async def get_rating(self, soup: BeautifulSoup):
        try:
            self.rating = float(soup
                                .find(class_='side-section')
                                .find('h1', class_='text-center')
                                .text)
        except AttributeError:
            return
        except ValueError:
            return

    async def get_reviews(self, soup: BeautifulSoup):
        try:
            reviews = soup.find('div', id='center-content')
            reviews = (reviews
                       .find('div', class_='col-5 col-xl-auto pl-1')
                       .find('p')
                       .text)
            reviews = reviews.split()[0]
            self.reviews = int(float(reviews.replace('K', '')) * 1000) if 'K' in reviews else int(reviews)
        except AttributeError:
            return
        except ValueError:
            return

        if self.reviews > 5:
            try:
                reviews = soup.find_all('a', class_='small-link')[-1].text
                self.reviews = int(reviews.split()[-2])
            except IndexError:
                return
            except AttributeError:
                return
            except ValueError:
                return

    async def get_platform(self, soup: BeautifulSoup):
        try:
            platforms = (soup
                         .find('div', class_='col-lg-4 mt-1 mt-lg-2 col-12')
                         .find_all('div')[2]
                         .find_all('a'))
            self.platforms = [*map(lambda x: x.text.strip(), platforms)]
        except AttributeError:
            self.platforms = []
        except ValueError:
            self.platforms = []

    async def get_genres(self, soup: BeautifulSoup):
        try:
            genres = (soup
                      .find('div', class_='col-lg-4 mt-1 mt-lg-2 col-12')
                      .find_all('div')[6]
                      .find_all('a'))
            self.genres = [*map(lambda x: x.text, genres)]
        except AttributeError:
            self.genres = []
        except ValueError:
            self.genres = []

    async def get_description(self, soup: BeautifulSoup):
        try:
            description = (soup
                           .find('div', id='center-content')
                           .find('div', id='collapseSummary')
                           .findAll('p'))
            self.description = '\n'.join([x.text for x in description]).replace('\n', ' ')
        except AttributeError:
            return
        except ValueError:
            return

    async def get_release(self, soup: BeautifulSoup):
        try:
            self.release = (soup
                            .find('div', id='center-content')
                            .find('p', class_='mb-2 game-parent-category')
                            .find('a')
                            .text)
        except AttributeError:
            return
        except ValueError:
            return

    def for_csv(self):
        return [
            self.name,
            self.date,
            self.developers,
            self.rating,
            self.platforms,
            self.genres,
            self.release,
            self.main,
            self.reviews,
            self.plays,
            self.playing,
            self.backlogs,
            self.wishlists,
            self.description
        ]
