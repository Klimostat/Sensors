from get_sensor_data import get_sensor_data
import time

if __name__ == "__main__":
    while True:
        print(get_sensor_data())
        time.sleep(10)
