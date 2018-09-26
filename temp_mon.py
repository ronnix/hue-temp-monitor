"""
Poll Hue Bridge API to get measurements from temperature sensors
"""
import argparse
import time

import requests


def main():
    args = parse_args()
    sensor_ids = find_temperature_sensors(args.host, args.username)
    poll_sensors(args.host, args.username, sensor_ids)


def parse_args():
    parser = argparse.ArgumentParser(description='Monitor temperature sensors.')
    parser.add_argument('--host')
    parser.add_argument('--username')
    return parser.parse_args()


def find_temperature_sensors(host, username):
    url = f"http://{host}/api/{username}/sensors"
    response = requests.get(url)
    return [
        id_
        for id_, data in response.json().items()
        if data["type"] == "ZLLTemperature"
    ]


def poll_sensors(host, username, sensor_ids):
    last_recorded = {}
    while True:
        for sensor_id in sensor_ids:
            data = poll_sensor(host, username, sensor_id)
            if data["lastupdated"] > last_recorded.get(sensor_id, ""):
                print(sensor_id, data['lastupdated'], data['temperature'])
                last_recorded[sensor_id] = data["lastupdated"]
        time.sleep(30)


def poll_sensor(host, username, sensor_id):
    url = f"http://{host}/api/{username}/sensors/{sensor_id}"
    response = requests.get(url)
    return response.json()["state"]


if __name__ == '__main__':
    main()
