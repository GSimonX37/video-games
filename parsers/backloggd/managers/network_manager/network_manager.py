import aiohttp

from .delay_manager import DelayManager


class NetworkManager:
    def __init__(self):
        self.delay_manager = DelayManager()

        self.url: str = 'https://www.backloggd.com'
        self.session: aiohttp.ClientSession | None = None
        self.incoming_traffic_size: int | None = 0
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 "
                          "(KHTML, like Gecko) "
                          "Chrome/113.0.0.0 Safari/537.36"
        }
        self.statuses = {
            "successful": 0,
            "failed": {}
        }
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

    async def connect(self) -> int:
        self.session = aiohttp.ClientSession(headers=self.header)
        async with self.session.get(self.url) as response:
            if response.status == 200:
                self.incoming_traffic_size = 0

            return response.status

    async def setting(self, normal_delay: tuple[int, int], increased_delay: tuple[int, int], threshold: int):
        await self.delay_manager.setting(normal_delay, increased_delay, threshold)

    async def get(self, link: str, params: dict = None):
        await self.delay_manager.delay()

        async with self.session.get(link, params=params) as response:
            await self.delay_manager.request_status(response.status)

            if response.status == 200:
                self.statuses["successful"] += 1
            else:
                if response.status in self.statuses["failed"]:
                    self.statuses["failed"][response.status] += 1
                else:
                    self.statuses["failed"][response.status] = 1

            if response.status != 404:
                self.incoming_traffic_size += int(response.headers['Content-Length'])
                return {'status': response.status, 'body': await response.text()}
            else:
                return {'status': response.status, 'body': ''}

    def get_link_page(self, release: str):
        return f'{self.url}/games/lib/release:asc/release_year:released;category:{self.releases[release]}'

    def for_json(self) -> dict:
        return {'request_delay': self.delay_manager.request_delay}

    def for_print(self) -> str:
        failed = ''
        for (status, count) in self.statuses["failed"].items():
            failed += f'{" "*4}- {status:<6} {count:8};\n'

        return (f'incoming traffic size: {self.incoming_traffic_size / 2**20:.2f} MB;\n'
                f'{self.delay_manager.for_print()};\n'
                f'{"successful":10} {self.statuses["successful"]:10};\n'
                f'{"failed":10} {sum(self.statuses["failed"].values()):10};\n'
                f'{failed}'
                f'{"total":10} {self.statuses["successful"] + sum(self.statuses["failed"].values()):10}.')
