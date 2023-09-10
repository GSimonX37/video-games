import datetime

from bs4 import BeautifulSoup


class ParsingManager:
    def __init__(self):
        pass

    async def basic_data_parsing(self, game,  text: str):
        soup = BeautifulSoup(text, 'html.parser')
        soup = soup.find('div', class_='row', id='game-profile')

        game.name = await self.get_name(soup)
        game.date = await self.get_date(soup)
        game.developers = await self.get_companies(soup)
        game.rating = await self.get_rating(soup)
        game.votes = await self.get_votes(soup)
        game.reviews = await self.get_reviews(soup)
        game.platforms = await self.get_platforms(soup)
        game.genres = await self.get_genres(soup)
        game.description = await self.get_description(soup)

    @staticmethod
    async def get_name(soup: BeautifulSoup) -> str | None:
        try:
            name = soup.find('h1', class_='mb-0').text
            return name
        except AttributeError:
            return
        except ValueError:
            return

    @staticmethod
    async def get_date(soup: BeautifulSoup) -> str | None:
        try:
            date = (soup
                    .find('div', class_='col-auto mt-auto pr-0')
                    .find('a')
                    .text)
            date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')
            return date
        except AttributeError:
            return None
        except ValueError:
            return None

    @staticmethod
    async def get_companies(soup: BeautifulSoup) -> list:
        try:
            companies = (soup
                         .find('div', class_='col-auto pl-lg-1 sub-title')
                         .find_all('a'))
            developers = [*map(lambda x: x.text, companies)]
            return developers
        except AttributeError:
            return []
        except ValueError:
            return []

    @staticmethod
    async def get_rating(soup: BeautifulSoup) -> float | None:
        try:
            rating = float(soup
                           .find(class_='side-section')
                           .find('h1', class_='text-center')
                           .text)
            return rating
        except AttributeError:
            return
        except ValueError:
            return

    @staticmethod
    async def get_votes(soup: BeautifulSoup) -> list:
        try:
            votes = (soup
                     .find(class_='side-section')
                     .find('div', id='ratings-bars-height')
                     .find_all('div'))
            votes = [vote['data-tippy-content'].split()[0] for vote in votes[::2]]
            return votes
        except AttributeError:
            return []
        except ValueError:
            return []

    @staticmethod
    async def get_reviews(soup: BeautifulSoup) -> int | None:
        try:
            reviews = soup.find('div', id='center-content')
            reviews = (reviews
                       .find('div', class_='col-5 col-xl-auto pl-1')
                       .find('p')
                       .text)
            reviews = reviews.split()[0]
            reviews = int(float(reviews.replace('K', '')) * 1000) if 'K' in reviews else int(reviews)
        except AttributeError:
            return
        except ValueError:
            return

        if reviews > 5:
            try:
                reviews = soup.find_all('a', class_='small-link')[-1].text
                reviews = int(reviews.split()[-2])
            except IndexError:
                return
            except AttributeError:
                return
            except ValueError:
                return

        return reviews

    @staticmethod
    async def get_platforms(soup: BeautifulSoup) -> list:
        try:
            platforms = (soup
                         .find('div', class_='col-lg-4 mt-1 mt-lg-2 col-12')
                         .find_all('div')[2]
                         .find_all('a'))
            platforms = [*map(lambda x: x.text.strip(), platforms)]
            return platforms
        except AttributeError:
            return []
        except ValueError:
            return []

    @staticmethod
    async def get_genres(soup: BeautifulSoup) -> list:
        try:
            genres = (soup
                      .find('div', class_='col-lg-4 mt-1 mt-lg-2 col-12')
                      .find_all('div')[6]
                      .find_all('a'))
            genres = [*map(lambda x: x.text, genres)]
            return genres
        except AttributeError:
            return []
        except ValueError:
            return []

    @staticmethod
    async def get_description(soup: BeautifulSoup) -> str | None:
        try:
            description = (soup
                           .find('div', id='center-content')
                           .find('div', id='collapseSummary')
                           .findAll('p'))
            description = '\n'.join([x.text for x in description]).replace('\n', ' ')
            return description
        except AttributeError:
            return
        except ValueError:
            return

    @staticmethod
    async def get_statistic(game, text: str) -> None:
        soup = BeautifulSoup(text, 'html.parser')

        try:
            statistic = soup.find('div', id='plays-nav').find_all('a')
            statistic = [*map(lambda x: x.text, statistic)]
            game.plays, game.playing, game.backlogs, game.wishlists = [int(s.split()[1]) for s in statistic]
        except AttributeError:
            return
        except ValueError:
            return

    @staticmethod
    async def get_last_page_number(text: str) -> int:
        soup = BeautifulSoup(text, 'html.parser')
        number = int(soup.find_all('span', class_='page')[-2].next.text)

        return number

    @staticmethod
    async def get_links_to_games(url :str, text: str) -> list:
        links = []

        soup = BeautifulSoup(text, 'html.parser')
        html = soup.find_all('a', class_='cover-link')
        for a in html:
            name = a['href'].split('/')[2]
            links.append(f'{url}/games/{name}/')

        return links
