import asyncio
import unittest
from sensors.sensor_manager import SensorManager
from logger.logger import Logger 
from datetime import datetime
from network.client import NetworkClient

CONFIG_PATH = "./configs/sensors_config.json"
LOGGER_CONFIG_PATH = "./configs/logger_config.json"  # plik konfig dla loggera

async def main():
    client = NetworkClient()
    client.connect()
    logger = Logger(LOGGER_CONFIG_PATH,client=client)
    logger.start()
    # Inicjalizacja SensorManager z klientem
    manager = SensorManager(CONFIG_PATH, client=client)
    manager.register_callbacks(logger)
    print("➡️  Uruchamiam wszystkie sensory...")
    manager.start_all()

    await asyncio.sleep(3)

    if manager.sensors:
        first_sensor = manager.sensors[0]
        print(f"⛔ Wyłączam sensor: {first_sensor.sensor_id}")
        manager.stop_sensor(first_sensor.sensor_id)
    else:
        print("❗ Brak sensorów do zatrzymania.")

    await asyncio.sleep(1)

    print("⛔ Wyłączam wszystkie sensory...")
    manager.stop_all()
    logger.stop()
    client.close()
    print("✅ Zakończono")

if __name__ == "__main__":
    # Uruchom testy
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.discover('./tests', pattern='test_*.py'))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ Wszystkie testy przeszły pomyślnie!\n")
    else:
        print("\n❌ Niektóre testy zakończyły się niepowodzeniem.\n")
        exit()

    asyncio.run(main())
