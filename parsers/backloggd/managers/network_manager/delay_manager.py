import asyncio

from random import uniform


class DelayManager:
    def __init__(self):
        self.request_delay: list[int, int] = [0, 0]

    async def delay(self):
        await asyncio.sleep(uniform(*self.request_delay))

    async def set_delay(self, delay: list[int, int]):
        self.request_delay = delay
