import asyncio

from random import uniform


class DelayManager:
    def __init__(self):
        self.request_delay: dict[str: tuple[int, int]] = {'normal': (0, 0),
                                                          'enlarged': (0, 0)}
        self.delay_type: str = 'normal'
        self.successful_statuses: int = 0
        self.threshold: int = 30

    async def delay(self):
        await asyncio.sleep(uniform(*self.request_delay[self.delay_type]))

    async def setting(self, normal_delay: tuple[int, int], enlarged_delay: tuple[int, int], threshold: int):
        self.request_delay['normal'] = normal_delay
        self.request_delay['enlarged'] = enlarged_delay
        self.threshold = threshold

    async def request_status(self, status):
        if status == 429:
            self.delay_type = 'enlarged'
        elif status == 200 and self.delay_type == 'enlarged':
            self.successful_statuses += 1

            if self.successful_statuses >= self.threshold:
                self.delay_type = 'normal'
                self.threshold = 0

    def for_print(self):
        return f'delay: {self.request_delay[self.delay_type][0]} to {self.request_delay[self.delay_type][1]}'
