import asyncio
import unittest
from sensors.sensor_manager import SensorManager

CONFIG_PATH = "./configs/sensors_config.json"


async def main():
    manager = SensorManager(CONFIG_PATH)
    manager.start_all()
    while True:
        manager.log_all_sensors()
        print()
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Załaduj wszystkie testy z plików testowych
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Dodaj testy z katalogu ./tests
    suite.addTests(loader.discover('./tests', pattern='test_*.py'))

    # Uruchom testy
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ Wszystkie testy przeszły pomyślnie!\n")
    else:
        print("\n❌ Niektóre testy zakończyły się niepowodzeniem.\n")
        exit()

    asyncio.run(main())
