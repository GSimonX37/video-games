import datetime

from bs4 import BeautifulSoup


class ParsingManager:
    def __init__(self):
        self.successful: dict[str: int] = {
            'name': 0,
            'date': 0,
            'genres': 0,
            'platforms': 0,
            'developers': 0,
            'rating': 0,
            'votes': 0,
            'reviews': 0,
            'plays': 0,
            'playing': 0,
            'backlogs': 0,
            'wishlists': 0,
            'description': 0,
        }

        self.failed: dict[str: int] = {
            'name': 0,
            'date': 0,
            'genres': 0,
            'platforms': 0,
            'developers': 0,
            'rating': 0,
            'votes': 0,
            'reviews': 0,
            'plays': 0,
            'playing': 0,
            'backlogs': 0,
            'wishlists': 0,
            'description': 0,
        }

    async def basic_data_parsing(self, game,  text: str):
        soup = BeautifulSoup(text, 'html.parser')
        soup = soup.find('div', class_='row', id='game-profile')

        game.name = await self.get_name(soup)
        game.date = await self.get_date(soup)
        game.developers = await self.get_developers(soup)
        game.rating = await self.get_rating(soup)
        game.votes = await self.get_votes(soup)
        game.reviews = await self.get_reviews(soup)
        game.platforms = await self.get_platforms(soup)
        game.genres = await self.get_genres(soup)
        game.description = await self.get_description(soup)

    async def get_name(self, soup: BeautifulSoup) -> str | None:
        try:
            name = soup.find('h1', class_='mb-0').text
            self.successful['name'] += 1
            return name
        except AttributeError:
            self.failed['name'] += 1
        except ValueError:
            self.failed['name'] += 1

    async def get_date(self, soup: BeautifulSoup) -> str | None:
        try:
            date = (soup
                    .find('div', class_='col-auto mt-auto pr-0')
                    .find('a')
                    .text)
            date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')

            self.successful['date'] += 1
            return date
        except AttributeError:
            self.failed['date'] += 1
        except ValueError:
            self.failed['date'] += 1

    async def get_developers(self, soup: BeautifulSoup) -> list:
        try:
            companies = (soup
                         .find('div', class_='col-auto pl-lg-1 sub-title')
                         .find_all('a'))
            developers = [*map(lambda x: x.text, companies)]

            self.successful['developers'] += 1
            return developers
        except AttributeError:
            self.failed['developers'] += 1
            return []
        except ValueError:
            self.failed['developers'] += 1
            return []

    async def get_rating(self, soup: BeautifulSoup) -> float | None:
        try:
            rating = float(soup
                           .find(class_='side-section')
                           .find('h1', class_='text-center')
                           .text)

            self.successful['rating'] += 1
            return rating
        except AttributeError:
            self.failed['rating'] += 1
        except ValueError:
            self.failed['rating'] += 1

    async def get_votes(self, soup: BeautifulSoup) -> list:
        try:
            votes = (soup
                     .find(class_='side-section')
                     .find('div', id='ratings-bars-height')
                     .find_all('div'))
            votes = [vote['data-tippy-content'].split()[0] for vote in votes[::2]]

            self.successful['votes'] += 1
            return votes
        except AttributeError:
            self.failed['votes'] += 1
            return []
        except ValueError:
            self.failed['votes'] += 1
            return []

    async def get_reviews(self, soup: BeautifulSoup) -> int | None:
        try:
            reviews = soup.find('div', id='center-content')
            reviews = (reviews
                       .find('div', class_='col-5 col-xl-auto pl-1')
                       .find('p')
                       .text)
            reviews = reviews.split()[0]
            reviews = int(float(reviews.replace('K', '')) * 1000) if 'K' in reviews else int(reviews)

        except AttributeError:
            self.failed['reviews'] += 1
            return
        except ValueError:
            self.failed['reviews'] += 1
            return

        if reviews > 5:
            try:
                reviews = soup.find_all('a', class_='small-link')[-1].text
                reviews = int(reviews.split()[-2])
            except IndexError:
                self.failed['reviews'] += 1
                return
            except AttributeError:
                self.failed['reviews'] += 1
                return
            except ValueError:
                self.failed['reviews'] += 1
                return

        self.successful['reviews'] += 1
        return reviews

    async def get_platforms(self, soup: BeautifulSoup) -> list:
        try:
            platforms = (soup
                         .find('div', class_='col-lg-4 mt-1 mt-lg-2 col-12')
                         .find_all('div')[2]
                         .find_all('a'))
            platforms = [*map(lambda x: x.text.strip(), platforms)]

            self.successful['platforms'] += 1
            return platforms
        except AttributeError:
            self.failed['platforms'] += 1
            return []
        except ValueError:
            self.failed['platforms'] += 1
            return []

    async def get_genres(self, soup: BeautifulSoup) -> list:
        try:
            genres = (soup
                      .find('div', class_='col-lg-4 mt-1 mt-lg-2 col-12')
                      .find_all('div')[6]
                      .find_all('a'))
            genres = [*map(lambda x: x.text, genres)]

            self.successful['genres'] += 1
            return genres
        except AttributeError:
            self.failed['genres'] += 1
            return []
        except ValueError:
            self.failed['genres'] += 1
            return []

    async def get_description(self, soup: BeautifulSoup) -> str | None:
        try:
            description = (soup
                           .find('div', id='center-content')
                           .find('div', id='collapseSummary')
                           .findAll('p'))
            description = '\n'.join([x.text for x in description]).replace('\n', ' ')

            self.successful['description'] += 1
            return description
        except AttributeError:
            self.failed['description'] += 1
            return
        except ValueError:
            self.failed['description'] += 1
            return

    async def get_statistic(self, game, text: str) -> None:
        soup = BeautifulSoup(text, 'html.parser')

        try:
            statistic = soup.find('div', id='plays-nav').find_all('a')
            statistic = [*map(lambda x: x.text, statistic)]
            game.plays, game.playing, game.backlogs, game.wishlists = [int(s.split()[1]) for s in statistic]

            self.successful['plays'] += 1
            self.successful['playing'] += 1
            self.successful['backlogs'] += 1
            self.successful['wishlists'] += 1
        except AttributeError:
            self.failed['plays'] += 1
            self.failed['playing'] += 1
            self.failed['backlogs'] += 1
            self.failed['wishlists'] += 1
            return
        except ValueError:
            self.failed['plays'] += 1
            self.failed['playing'] += 1
            self.failed['backlogs'] += 1
            self.failed['wishlists'] += 1
            return

    @staticmethod
    async def get_last_page_number(text: str) -> int:
        soup = BeautifulSoup(text, 'html.parser')
        number = int(soup.find_all('span', class_='page')[-2].next.text)

        return number

    @staticmethod
    async def get_links_to_games(url: str, text: str) -> list:
        links = []

        soup = BeautifulSoup(text, 'html.parser')
        html = soup.find_all('a', class_='cover-link')
        for a in html:
            name = a['href'].split('/')[2]
            links.append(f'{url}/games/{name}/')

        return links

    def for_print(self):
        result = []
        for (field, successful), failed in zip(self.successful.items(), self.failed.values()):
            total = failed + successful
            result.append(f'{field:20} {successful:5} of {total:5} - {(successful / total) if total else 0:.2%};')

        return '\n'.join(result)
