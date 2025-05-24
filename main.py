import asyncio
from sensors.sensor_manager import SensorManager
import unittest

CONFIG_PATH = "./configs/sensors_config.json"

async def main():
    manager = SensorManager(CONFIG_PATH)
    manager.start_all()
    await manager.log_all_readings(interval=1)

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