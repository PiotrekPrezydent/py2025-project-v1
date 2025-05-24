import asyncio
from sensors.sensor_manager import SensorManager
CONFIG_PATH = "./configs/sensors_config.json"

async def main():
    manager = SensorManager(CONFIG_PATH)
    manager.start_all()
    await manager.log_all_readings(interval=1)

if __name__ == "__main__":
    asyncio.run(main())