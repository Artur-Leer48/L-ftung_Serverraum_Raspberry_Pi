from threading import Lock

from config import TEMP_SCHWELLE


_lock = Lock()
_state = {
    "temperatur": None,
    "temperatur_fahrenheit": None,
    "taupunkt": None,
    "luftfeuchte": None,
    "luftdruck": None,
    "luefter_aktiv": False,
    "temp_schwelle": TEMP_SCHWELLE,
}


def update_measurement(
    temperatur,
    temperatur_fahrenheit,
    taupunkt,
    luftfeuchte,
    luftdruck,
    luefter_aktiv,
):
    with _lock:
        _state.update(
            {
                "temperatur": temperatur,
                "temperatur_fahrenheit": temperatur_fahrenheit,
                "taupunkt": taupunkt,
                "luftfeuchte": luftfeuchte,
                "luftdruck": luftdruck,
                "luefter_aktiv": luefter_aktiv,
            }
        )


def get_state():
    with _lock:
        return _state.copy()


def get_temp_schwelle():
    with _lock:
        return _state["temp_schwelle"]


def set_temp_schwelle(temp_schwelle):
    with _lock:
        _state["temp_schwelle"] = temp_schwelle
