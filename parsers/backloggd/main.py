import asyncio

from parser import Parser


async def main():
    parser = Parser()

    if await parser.connect() == 200:
        parser.get_file_name()
        await parser.get_number_of_all_pages()
        await parser.print_status()

        if not input('Press enter to start...'):
            await parser.run()

    await parser.close_connection()

if __name__ == '__main__':
    asyncio.run(main())
