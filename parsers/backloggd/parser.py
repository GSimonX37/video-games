import asyncio
import os

from bs4 import BeautifulSoup

from game import Game
from managers.file_manager import FileManager
from managers.network_manager.network_manager import NetworkManager
from managers.progress_manager import ProgressManager


class Parser:
    def __init__(self):
        self.file_manager = FileManager()
        self.network_manager = NetworkManager()
        self.progress_manager = ProgressManager()

    async def connect(self):
        print('Server connection...', end=' ', flush=True)

        if (status := await self.network_manager.connect()) == 200:
            print(f'Connecting to the server successfully.', flush=True)
        else:
            print(f'Connection to server failed (code {status}).', flush=True)

        return status

    async def run(self):
        await self.print_status()

        for (release, count_pages) in self.progress_manager.total_pages.items():
            for page in range(1, count_pages + 1):

                link_page = self.network_manager.get_link_page(release)
                links_to_games = await self.get_links_to_games(link_page, page)
                games = await self.get_games_data(links_to_games, release)

                self.file_manager.write([game.for_csv() for game in games])

                self.progress_manager.step()
                await self.print_status()

    async def set_file_name(self, file_name: str):
        await self.file_manager.set_file_name(file_name)

    async def set_delay(self, minimum_delay: list[int, int], delay_delta: int):
        await self.network_manager.set_delay(minimum_delay, delay_delta)

    async def set_number_of_all_pages(self) -> bool:
        print('Getting data on the number of pages with video games...', end=' ', flush=True)
        tasks = []

        for release in self.network_manager.releases.values():
            link = self.network_manager.url + f'/games/lib/release:asc/release_year:released;category:{release}'
            tasks.append(asyncio.create_task(self.get_number_of_pages(link)))

        numbers_of_pages = await asyncio.gather(*tasks)

        if all(numbers_of_pages):
            self.progress_manager.set_total_number_of_pages([*self.network_manager.releases.keys()], numbers_of_pages)
            return True
        else:
            print('Failed to get game page count data.', end='', flush=True)
            return False

    async def get_number_of_pages(self, link: str) -> None | int:
        status, number, number_attempts = None, None, 0

        while status != 200 and number_attempts < 5:
            response = await self.network_manager.get(link)
            status, number_attempts = response['status'], number_attempts + 1

            if status == 200:
                soup = BeautifulSoup(response['body'], 'html.parser')
                number = int(soup.find_all('span', class_='page')[-2].next.text)

        return number

    async def get_links_to_games(self, link: str, page: int) -> list[str]:
        status = None
        links = []

        while status != 200:
            response = await self.network_manager.get(link, params={'page': f'{page}'})
            status = response['status']

            if status == 200:
                text = response['body']
                soup = BeautifulSoup(text, 'html.parser')
                html = soup.find_all('a', class_='cover-link')
                for a in html:
                    name = a['href'].split('/')[2]
                    links.append(f'{self.network_manager.url}/games/{name}/')

                await self.print_status()

        return links

    async def get_game_data(self, link_to_game: str, release: str) -> Game:
        status, number_attempts = None, 0
        game = Game(release)

        while status != 200:
            if number_attempts > 3 and status != 429:
                return game

            response = await self.network_manager.get(link_to_game)
            status = response['status']

            if status == 200:
                text = response['body']
                soup = BeautifulSoup(text, 'html.parser')
                soup = soup.find('div', class_='row', id='game-profile')
                await game.basic_data_parsing(soup)

            await self.print_status()
            number_attempts += 1

        return game

    async def get_games_data(self, links_to_games: list[str], release: str):

        tasks = []

        for link_to_games in links_to_games:
            tasks.append(asyncio.create_task(self.get_game_data(link_to_games, release)))

        games = await asyncio.gather(*tasks)

        return games

    async def close_connection(self):
        await self.network_manager.session.close()

    async def print_status(self):
        os.system('cls')

        print(f'File manager:\n'
              f'{self.file_manager.for_print()}\n\n'
              f'Network manager:\n'
              f'{self.network_manager.for_print()}\n\n'
              f'Progress manager:\n'
              f'{self.progress_manager.for_print()}')
