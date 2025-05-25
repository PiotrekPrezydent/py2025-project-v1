import asyncio
import unittest
from sensors.sensor_manager import SensorManager
from logger.logger import Logger 
from datetime import datetime

CONFIG_PATH = "./configs/sensors_config.json"
LOGGER_CONFIG_PATH = "./configs/logger_config.json"  # plik konfig dla loggera

async def main():
    logger = Logger(LOGGER_CONFIG_PATH)
    logger.start()
    
    manager = SensorManager(CONFIG_PATH)
    
    # Rejestracja callbacka logowania do każdego sensora
    for sensor in manager.get_all_sensors():
        sensor.register_callback(
            lambda timestamp, sensor_id, name, value, unit, logger=logger: 
                logger.log_reading(timestamp, sensor_id, name, value, unit)
        )
    
    manager.start_all()
    
    try:
        for i in range(5):
            manager.log_all_sensors()  # to wyświetla w konsoli statusy sensorów
            await asyncio.sleep(1)
    finally:
        print("stop")
        manager.stop_all()
        logger.stop()

if __name__ == "__main__":
    # Uruchom testy
    # loader = unittest.TestLoader()
    # suite = unittest.TestSuite()
    # suite.addTests(loader.discover('./tests', pattern='test_*.py'))
    # runner = unittest.TextTestRunner(verbosity=2)
    # result = runner.run(suite)

    # if result.wasSuccessful():
    #     print("\n✅ Wszystkie testy przeszły pomyślnie!\n")
    # else:
    #     print("\n❌ Niektóre testy zakończyły się niepowodzeniem.\n")
    #     exit()

    asyncio.run(main())
