from DHT11.dht11 import DHT11
from MHZ14A.mhz14a import MHZ14A
from Wassersensor.waterlevelsensor import WaterLevelSensor
from datetime import datetime
import time
import mariadb
import sys


def insert_data(cursor, value, sensor, timetuple):
    cursor.execute(
        "INSERT INTO messung (messzeitpunkt, messdaten, fk_sensorId) VALUES (%s, %s, %s)",
        (time.strftime("%Y-%m-%d %H:%M:%S", timetuple), value, sensor))


def get_sensor_data():
    mhz14a = MHZ14A()
    dht11 = DHT11()
    waterlevelsensor = WaterLevelSensor()

    temperature = dht11.get_temperature()
    humidity = dht11.get_humidity()
    co2level = mhz14a.get_co2level()
    water_ingress = waterlevelsensor.detect_water_ingress()

    # timetuple = time.localtime()
    timetuple = datetime.utcnow().timetuple()

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

    insert_data(cur, str(temperature), "1", timetuple)
    insert_data(cur, str(humidity), "2", timetuple)
    if 200 < co2level < 5000:
        insert_data(cur, str(co2level), "3", timetuple)
    insert_data(cur, "1" if water_ingress else "0", "4", timetuple)
    conn.commit()
    conn.close()

    return "{}: Temp: {:.1f} C    Humidity: {}%    CO2: {} ppm    Wateringress: {}".format(
        time.asctime(timetuple),
        temperature, humidity, co2level, water_ingress)


if __name__ == "__main__":
    print(get_sensor_data())
