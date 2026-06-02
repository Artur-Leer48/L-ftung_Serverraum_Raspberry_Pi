from math import log


def celsius_to_fahrenheit(temperatur_celsius):
    return temperatur_celsius * 9 / 5 + 32


def calculate_dew_point(temperatur_celsius, luftfeuchte):
    magnus_a = 17.62
    magnus_b = 243.12
    relative_luftfeuchte = luftfeuchte / 100
    gamma = log(relative_luftfeuchte) + (
        magnus_a * temperatur_celsius
    ) / (magnus_b + temperatur_celsius)

    return (magnus_b * gamma) / (magnus_a - gamma)
