import asyncio

from parser import Parser


async def main():
    parser = Parser()

    if await parser.connect() == 200:
        await parser.configure_file_manager('output.csv')
        await parser.configure_progress_manager()
        await parser.configure_network_manager([5, 10])
        await parser.print_status()

        if not input('Press enter to start...'):
            await parser.run()

    await parser.close_connection()

if __name__ == '__main__':
    asyncio.run(main())
