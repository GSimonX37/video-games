import csv
import os


class FileManager:
    def __init__(self):
        self.file_name: str | None = ''
        self.file_size: int | None = None
        self.number_of_records: int | None = None

    async def set_file_name(self, file_name: str = ''):
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = input('File manager: enter the full name of the file to save the data: ')

        try:
            file_size = os.path.getsize(self.file_name)
            print(f'File manager: a file named {self.file_name} already exists ({file_size / 2**10:.2f} KB).')

            if input('File manager: press "Enter" to continue writing to this file '
                     'or type "rewrite" to erase all data in the file: ') == 'rewrite':
                self.create_file()
            else:
                with open(self.file_name, 'r', newline='', encoding='utf-8') as csvfile:
                    rows = csv.reader(csvfile, delimiter=';')
                    self.number_of_records = sum([1 for _ in rows]) - 1

                self.file_size = os.path.getsize(self.file_name)
        except WindowsError:
            self.create_file()

    def create_file(self):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([
                "name",
                "date",
                "developers",
                "rating",
                "platforms",
                "genres",
                "category",
                "main",
                "reviews",
                "plays",
                "playing",
                "backlogs",
                "wishlists",
                "description"])

        self.file_size, self.number_of_records = 0, 0

    def write(self, records: list[str]):
        with open(self.file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            for record in records:
                writer.writerow(record)

        self.file_size = os.path.getsize(self.file_name)
        self.number_of_records += len(records)

    def for_print(self) -> str:
        return (f'file_name: {self.file_name}\n'
                f'size: {self.file_size / 2**20:.2f} MB\n'
                f'records: {self.number_of_records}')
