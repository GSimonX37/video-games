import csv
import os


class FileManager:
    def __init__(self):
        self.file_name: str | None = ''
        self.file_size: int | None = None
        self.number_of_records: int | None = None

    async def set_file_name(self, file_name: str, mode: str):
        self.file_name = file_name

        if mode == 'w':
            self.create_file()
        elif mode == 'a':
            with open(self.file_name, 'r', newline='', encoding='utf-8') as csvfile:
                rows = csv.reader(csvfile, delimiter=';')
                self.number_of_records = sum([1 for _ in rows]) - 1

            self.file_size = os.path.getsize(self.file_name)

    def create_file(self):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([
                "name",
                "date",
                "developers",
                "rating",
                "votes",
                "platforms",
                "genres",
                "category",
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
