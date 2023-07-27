import csv
import os


class FileManager:
    def __init__(self):
        self.file_name: str | None = ''
        self.file_size: int | None = None
        self.number_of_records: int | None = None

    async def set_file_name(self):
        # file_name = input('Enter the full name of the file to save the data: ')
        self.file_name = r'output.csv'
        self.file_size, self.number_of_records = 0, 0

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
