import asyncio

from parser import Parser


async def main():
    parser = Parser()

    if await parser.connect() == 200:
        await parser.file_manager_setting('output.csv', 'w')
        await parser.progress_manager_setting(releases='main', pages=[1, 4])
        await parser.network_manager_setting([5, 10])
        await parser.print_status()

        if not input('Press enter to start...'):
            await parser.run()

    await parser.close_connection()

if __name__ == '__main__':
    asyncio.run(main())
