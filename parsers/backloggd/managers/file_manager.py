import csv
import os
import json


class FileManager:
    def __init__(self):
        self.data_file_name: str | None = ''
        self.checkpoint_file_name: str | None = ''
        self.file_size: int | None = None
        self.number_of_records: int | None = None

    async def setting(self, data_file_name: str, mode: str, checkpoint_file_name: str | None):
        self.data_file_name = data_file_name
        self.checkpoint_file_name = checkpoint_file_name

        if mode == 'w':
            self.create_data_file()
        elif mode == 'a':
            with open(self.data_file_name, 'r', newline='', encoding='utf-8') as csvfile:
                rows = csv.reader(csvfile, delimiter=';')
                self.number_of_records = sum([1 for _ in rows]) - 1

            self.file_size = os.path.getsize(self.data_file_name)

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

    def write_checkpoint(self, checkpoint: dict):
        if self.checkpoint_file_name:
            with open(self.checkpoint_file_name, 'w') as json_file:
                checkpoint = self.for_json() | checkpoint
                json_file.write(json.dumps(checkpoint, indent=4))

    @staticmethod
    def load_checkpoint(checkpoint_file_name: str) -> dict:
        with open(checkpoint_file_name, 'r') as json_file:
            return json.loads(json_file.read())

    def for_json(self) -> dict:
        return {'data_file_name': self.data_file_name}

    def for_print(self) -> str:
        return (f'file_name: {self.data_file_name}\n'
                f'size: {self.file_size / 2**20:.2f} MB\n'
                f'records: {self.number_of_records}')
