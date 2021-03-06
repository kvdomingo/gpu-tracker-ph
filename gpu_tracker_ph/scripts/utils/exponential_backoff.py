from requests import Response
from time import sleep
from warnings import warn
from typing import Union


class ExponentialBackoff:
    def __init__(self, func: callable, data_id: int, retries: int = 3):
        self.func = func
        self.data_id = data_id
        self.timeout = [2**i for i in range(retries)]

    def run(self) -> Union[Response, None]:
        attempts = 1
        while True:
            if attempts == len(self.timeout):
                return None
            res = self.func()
            if res.ok:
                return res
            else:
                warn(f"ID {self.data_id} timeout at attempt {attempts}, retrying in {self.timeout[attempts - 1]}s...")
                sleep(self.timeout[attempts - 1])
                attempts += 1
