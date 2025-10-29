import io
import json
import xml.etree.ElementTree as ET

import requests
from loguru import logger
from tqdm import tqdm

from api.scripts.utils.exponential_backoff import ExponentialBackoff

BASE_URL = "https://outervision.com"


def get_data() -> None:
    res = requests.get(f"{BASE_URL}/cpu_v1.17.json")
    if not res.ok:
        raise ConnectionError(res.text)
    cpus = res.json()
    cpus = cpus[1980:]
    with open("./data/cpu.json", "w+", encoding="utf-8") as f:
        json.dump(cpus, f, indent=2)
    for i, dat in enumerate(tqdm(cpus)):
        if i % 20 == 0:
            logger.info("Saving to file")
            with open("./data/cpu.json", "w+", encoding="utf-8") as f:
                json.dump(cpus, f, indent=2)
        res = ExponentialBackoff(
            lambda: requests.get(f"{BASE_URL}/getCpuInfo?cpuID={dat['cpu_id']}"),
            dat["cpu_id"],
        ).run()
        if res is None:
            logger.error(f"Failed to retrieve details for CPUID {dat['cpu_id']}")
            continue
        else:
            buffer = io.BytesIO(res.text.encode())
            buffer.seek(0)
            try:
                data = ET.parse(buffer).getroot().text
            except ET.ParseError:
                logger.error(f"Invalid XML for CPUID {dat['cpu_id']}")
                continue
            try:
                clock_mhz = float(data.split(",")[0])
                clock_ghz = round(clock_mhz / 1000, 1)
                cpus[i]["base_clock_ghz"] = clock_ghz
            except ValueError:
                logger.error(f"Invalid base clock for CPUID {dat['cpu_id']}")
                continue
    with open("./data/cpu.json", "w+", encoding="utf-8") as f:
        json.dump(cpus, f, indent=2)


def clean_data() -> None:
    with open("./data/cpu.json", "r") as f:
        cpus = json.load(f)
    cpus = list(filter(lambda c: "pro" not in c["description"].lower(), cpus))
    cpus = list(filter(lambda c: "epyc" not in c["description"].lower(), cpus))
    with open("./data/cpu.json", "w+", encoding="utf-8") as f:
        json.dump(cpus, f, indent=2)


def parse_data() -> None:
    with open("./data/cpu.json", "r") as f:
        cpus = json.load(f)
    for i, cpu in enumerate(cpus):
        cpus[i] = {
            "manufacturer": cpu["description"].split(" ")[0],
            "product_sku": str.join(" ", cpu["description"].split(" ")[1:]),
            "base_clock_ghz": cpu["base_clock_ghz"],
        }
    with open("./data/cpu.json", "w+", encoding="utf-8") as f:
        json.dump(cpus, f, indent=2)


@logger.catch
def main() -> None:
    get_data()
    clean_data()
    parse_data()


if __name__ == "__main__":
    main()
