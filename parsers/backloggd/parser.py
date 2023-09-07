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
        self.releases: dict[str, str] = {
            'main': 'main_game',
            'dlc': 'dlc_addon',
            'expansion': 'expansion',
            'bundle': 'bundle',
            'standalone_expansion': 'standalone_expansion',
            'mod': 'mod',
            'episode': 'episode',
            'season': 'season',
            'remake': 'remake',
            'remaster': 'remaster',
            'expanded': 'expanded_game',
            'port': 'port',
            'fork': 'fork',
            'pack': 'pack',
            'update': 'game_update'
        }

    async def connect(self):
        print('Parser: server connection...', flush=True)

        if (status := await self.network_manager.connect()) == 200:
            print(f'Parser: connecting to the server successfully.', flush=True)
        else:
            print(f'Parser: connection to server failed (code {status}).', flush=True)

        return status

    async def run(self):
        await self.print_status()

        for release, (current, last) in self.progress_manager.progress.items():
            for page in range(current, last + 1):

                link_page = self.network_manager.get_link_page(release)
                links_to_games = await self.get_links_to_games(link_page, page)
                games = await self.get_games_data(links_to_games, release)

                self.file_manager.write_data([game.for_csv() for game in games])

                self.progress_manager.step()
                await self.print_status()
                await self.save_checkpoint()

    async def setting(self, data_file_name: str, mode: str, checkpoint_file_name: str = 'checkpoint.json',
                      releases: list | str = None, pages: list = None,
                      delay: [int, int] = (5, 10)):
        await self.file_manager_setting(data_file_name, mode, checkpoint_file_name)
        await self.progress_manager_setting(releases, pages)
        await self.network_manager_setting(delay)

    async def file_manager_setting(self, data_file_name: str, mode: str, checkpoint_file_name: str = 'checkpoint.json'):
        await self.file_manager.set_data_file_name(data_file_name, mode)
        await self.file_manager.set_configuration_file_name(checkpoint_file_name)

    async def progress_manager_setting(self, releases: list | str = None, pages: list = None):
        progress = {}

        if releases or pages:
            if releases:
                if isinstance(releases, list):
                    progress = {release: [None, None] for release in releases}
                elif isinstance(releases, str):
                    progress = {releases: [None, None]}
            else:
                progress = {release: [None, None] for release in self.releases}

            if pages:
                empty = []

                if all([isinstance(page, list) for page in pages]):
                    for release, (first_page, last_page) in zip(progress, pages):
                        progress[release][0] = first_page
                        if last_page:
                            progress[release][1] = last_page
                        else:
                            empty.append(release)

                    if empty:
                        last_pages = await self.get_last_page_numbers((*empty,))

                        i = 0
                        for release in progress:
                            if not progress[release][1]:
                                progress[release][1] = last_pages[i]
                                i += 1

                elif isinstance(pages, list):
                    first_page, last_page = pages

                    if last_page:
                        for release in progress:
                            progress[release][0], progress[release][1] = first_page, last_page
                    else:
                        last_pages = await self.get_last_page_numbers((*progress.keys(),))

                        for release, last_page in zip(progress, last_pages):
                            progress[release][0], progress[release][1] = first_page, last_page
            else:
                last_pages = await self.get_last_page_numbers((*progress.keys(),))

                for release, last_page in zip(progress, last_pages):
                    progress[release] = [1, last_page]

        else:
            last_pages = await self.get_last_page_numbers((*self.releases.keys(),))
            progress = {release: [1, last_page] for release, last_page in zip(self.releases.keys(), last_pages)}

        self.progress_manager.set_progress(progress)

    async def network_manager_setting(self, delay: tuple[int, int] = (5, 10)):
        await self.network_manager.set_delay(delay)

    async def get_last_page_numbers(self, releases: tuple[str]) -> tuple[int]:
        print('Parser: getting data on the number of pages with video games...', flush=True)
        tasks = []

        for release in releases:
            release = self.network_manager.releases[release]
            link = self.network_manager.url + f'/games/lib/release:asc/release_year:released;category:{release}'
            tasks.append(asyncio.create_task(self.get_last_page_number(link)))

        numbers_of_pages = await asyncio.gather(*tasks)

        if all(numbers_of_pages):
            print('Parser: received data on the number of game pages.', flush=True)
        else:
            print('Parser: failed to get game page count data.', flush=True)

        return numbers_of_pages

    async def get_last_page_number(self, link: str) -> None | int:
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

    async def get_games_data(self, links_to_games: list[str], release: str):

        tasks = []

        for link_to_games in links_to_games:
            tasks.append(asyncio.create_task(self.get_game_data(link_to_games, release)))

        games = await asyncio.gather(*tasks)

        return games

    async def get_game_data(self, link_to_game: str, release: str) -> Game:
        status, number_attempts = None, 0
        game = Game(release)

        while status != 200:
            if number_attempts > 5 and status != 429:
                return game

            response = await self.network_manager.get(link_to_game)
            status = response['status']

            await self.print_status()
            number_attempts += 1

            if status == 200:
                text = response['body']
                soup = BeautifulSoup(text, 'html.parser')
                soup = soup.find('div', class_='row', id='game-profile')
                await game.basic_data_parsing(soup)

                status, link_to_statistic = None, link_to_game.replace('games', 'logs') + 'plays/'
                while status != 200:
                    if number_attempts > 5 and status != 429:
                        return game

                    response = await self.network_manager.get(link_to_statistic)
                    status = response['status']

                    await self.print_status()
                    number_attempts += 1

                    if status == 200:
                        text = response['body']
                        soup = BeautifulSoup(text, 'html.parser')
                        await game.get_statistic(soup)

        return game

    async def close_connection(self):
        await self.network_manager.session.close()

    async def save_checkpoint(self):
        settings = self.progress_manager.for_json() | self.network_manager.for_json()
        self.file_manager.write_checkpoint(settings)

    async def load_checkpoint(self, checkpoint_file_name: str):
        settings = self.file_manager.load_checkpoint(checkpoint_file_name)
        await self.file_manager_setting(settings['data_file_name'], 'a', checkpoint_file_name)
        await self.progress_manager_setting([*settings['progress'].keys()], [*settings['progress'].values()])

    async def print_status(self):
        os.system('cls')

        print(f'File manager:\n'
              f'{self.file_manager.for_print()}\n\n'
              f'Network manager:\n'
              f'{self.network_manager.for_print()}\n\n'
              f'Progress manager:\n'
              f'{self.progress_manager.for_print()}')
