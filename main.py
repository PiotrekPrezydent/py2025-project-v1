import asyncio
from sensors.sensor_manager import SensorManager
import unittest

CONFIG_PATH = "./configs/sensors_config.json"

async def main():
    manager = SensorManager(CONFIG_PATH)
    manager.start_all()
    manager.start_refresh_loop()

    readings = manager.get_all_readings()
    print("--- Pierwszy odczyt ---")
    for r in readings:
        print(r)

    manager.stop_sensor(1)
    print("Wyłączono sensor o id 1")

    await asyncio.sleep(3)

    readings = manager.get_all_readings()
    print("--- Drugi odczyt ---")
    for r in readings:
        print(r)

    await manager.stop_refresh_loop()

if __name__ == "__main__":
    # Załaduj wszystkie testy z plików testowych
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Dodaj testy z konkretnych plików
    suite.addTests(loader.discover('./tests', pattern='test_sensors.py'))
    suite.addTests(loader.discover('./tests', pattern='test_sensor_manager.py'))

    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("Wszystkie testy przeszły pomyślnie!")
    else:
        print("Niektóre testy zakończyły się niepowodzeniem.")
        exit()
    asyncio.run(main())