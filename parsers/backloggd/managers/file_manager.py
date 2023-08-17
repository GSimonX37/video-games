import csv
import os
import json


class FileManager:
    def __init__(self):
        self.data_file_name: str | None = ''
        self.settings_file_name: str | None = ''
        self.file_size: int | None = None
        self.number_of_records: int | None = None

    async def set_data_file_name(self, file_name: str, mode: str):
        self.data_file_name = file_name

        if mode == 'w':
            self.create_data_file()
        elif mode == 'a':
            with open(self.data_file_name, 'r', newline='', encoding='utf-8') as csvfile:
                rows = csv.reader(csvfile, delimiter=';')
                self.number_of_records = sum([1 for _ in rows]) - 1

            self.file_size = os.path.getsize(self.data_file_name)

    async def set_configuration_file_name(self, file_name: str | None):
        self.settings_file_name = file_name

    def create_data_file(self):
        with open(self.data_file_name, 'w', newline='', encoding='utf-8') as csvfile:
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

    def write_data(self, records: list[str]):
        with open(self.data_file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            for record in records:
                writer.writerow(record)

        self.file_size = os.path.getsize(self.data_file_name)
        self.number_of_records += len(records)

    def write_checkpoint(self, configuration: dict):
        if self.settings_file_name:
            with open(self.settings_file_name, 'w') as json_file:
                settings = self.for_json() | configuration
                json_file.write(json.dumps(settings, indent=4))

    def for_json(self) -> dict:
        return {'data_file_name': self.data_file_name}

    def for_print(self) -> str:
        return (f'file_name: {self.data_file_name}\n'
                f'size: {self.file_size / 2**20:.2f} MB\n'
                f'records: {self.number_of_records}')
