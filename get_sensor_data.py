from DHT11.dht11 import DHT11
from MHZ14A.mhz14a import MHZ14A
import time
import mariadb
import sys


def insert_data(cursor, value, sensor, timestamp):
    cursor.execute(
        "INSERT INTO messung (messzeitpunkt, messdaten, fk_sensorId) VALUES (%s, %s, %s)",
        (timestamp, value, sensor))


def get_sensor_data():
    mhz14a = MHZ14A()
    dht11 = DHT11()

    temperature = dht11.get_temperature()
    humidity = dht11.get_humidity()
    co2level = mhz14a.get_co2level()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="klimostat"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()

    insert_data(cur, str(temperature), "1", timestamp)
    insert_data(cur, str(humidity), "2", timestamp)
    insert_data(cur, str(co2level), "3", timestamp)
    conn.commit()
    conn.close()

    return "{}: Temp: {:.1f} C    Humidity: {}%    CO2: {} ppm".format(time.asctime(time.localtime(time.time())),
                                                                       temperature, humidity, co2level)


if __name__ == "__main__":
    print(get_sensor_data())
