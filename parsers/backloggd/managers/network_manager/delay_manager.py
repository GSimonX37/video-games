import asyncio

from random import uniform


class DelayManager:
    def __init__(self):
        self.current_delay: list[int, int] = [0, 0]
        self.minimum_delay: list[int, int] = [0, 0]
        self.delay_delta: int | None = None

    async def send_response_status(self, status: int):
        if status == 200 and self.current_delay > self.minimum_delay:
            self.current_delay[0] -= self.delay_delta
            self.current_delay[1] -= self.delay_delta
        elif status == 429:
            self.current_delay[0] += self.delay_delta
            self.current_delay[1] += self.delay_delta

    async def delay(self):
        await asyncio.sleep(uniform(*self.current_delay))

    async def set_delay(self, minimum_delay: list[int, int], delay_delta: int):
        self.minimum_delay, self.current_delay = minimum_delay.copy(), minimum_delay.copy()
        self.delay_delta = delay_delta
