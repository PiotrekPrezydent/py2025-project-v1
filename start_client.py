import asyncio
import unittest
from sensors.sensor_manager import SensorManager
from logger.logger import Logger 
from datetime import datetime
from network.client import NetworkClient
from gui.gui import GUI

CONFIG_PATH = "./configs/sensors_config.json"
LOGGER_CONFIG_PATH = "./configs/logger_config.json"  # plik konfig dla loggera

async def main():
    client = NetworkClient()
    client.connect()
    logger = Logger(LOGGER_CONFIG_PATH, client=client)
    logger.start()

    manager = SensorManager(CONFIG_PATH, client=client)
    manager.register_callbacks(logger)
    manager.start_all()

    gui = GUI(manager)
    await gui.async_mainloop()
    print("end")
    client.close()

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
