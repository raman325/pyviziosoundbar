import logging
from urllib.parse import urlsplit

import requests
import xmltodict

from .cmd_input import GetInputsListCommand, GetCurrentInputCommand, ChangeInputCommand
from .cmd_power import GetPowerStateCommand
from .cmd_remote import EmulateRemoteCommand
from .cmd_settings import GetCurrentAudioCommand
from .discovery import discover
from .protocol import invoke_api, KeyCodes

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_LOGGER = logging.getLogger(__name__)

class DeviceDescription(object):
    def __init__(self, ip, name, model, udn):
        self.ip = ip
        self.name = name
        self.model = model
        self.udn = udn


class VizioSoundBar(object):
    def __init__(self, device_id, ip, name):
        self._ip = ip
        self._name = name
        self._device_id = device_id

    def __invoke_api(self, cmd):
        return invoke_api(self._ip, cmd, _LOGGER)

    def __remote(self, key_code):
        if isinstance(key_code, list) is False:
            key_code = [key_code]
        cmd = EmulateRemoteCommand(key_code)
        result = self.__invoke_api(cmd)
        return result is not None

    def __remote_multiple(self, key_code, num):
        key_codes = []
        for ii in range(0, num):
            key_codes.append(key_code)
        return self.__remote(key_codes)

    @staticmethod
    def discovery():
        results = []
        devices = discover("urn:dial-multiscreen-org:device:dial:1")
        for dev in devices:
            data = xmltodict.parse(requests.get(dev.location, verify=False).text)

            if "root" not in data or "device" not in data["root"]:
                continue

            root = data["root"]["device"]
            manufacturer = root["manufacturer"]
            if manufacturer is None or "VIZIO" != manufacturer:
                continue
            split_url = urlsplit(dev.location)
            device = DeviceDescription(split_url.hostname, root["friendlyName"], root["modelName"], root["UDN"])
            results.append(device)

        return results

    def get_inputs(self):
        return self.__invoke_api(GetInputsListCommand())

    def get_current_input(self):
        return self.__invoke_api(GetCurrentInputCommand())

    def get_power_state(self):
        return self.__invoke_api(GetPowerStateCommand())

    def power_on(self):
        return self.__remote(KeyCodes.POW_ON)

    def power_off(self):
        return self.__remote(KeyCodes.POW_OFF)

    def power_toggle(self):
        return self.__remote(KeyCodes.POW_TOGGLE)

    def vol_up(self, num=1):
        return self.__remote_multiple(KeyCodes.VOL_UP, num)

    def vol_down(self, num=1):
        return self.__remote_multiple(KeyCodes.VOL_DOWN, num)

    def get_current_volume(self):
        return self.__invoke_api(GetCurrentAudioCommand())

    def mute_on(self):
        return self.__remote(KeyCodes.MUTE_ON)

    def mute_off(self):
        return self.__remote(KeyCodes.MUTE_OFF)

    def mute_toggle(self):
        return self.__remote(KeyCodes.MUTE_TOGGLE)

    # def input_next(self):
    #     # HACK: Single call just invoking overlay menu with current input
    #     return self.__remote_multiple(KeyCodes.INPUT_NEXT, 2)

    def play(self):
        return self.__remote(KeyCodes.PLAY)

    def pause(self):
        return self.__remote(KeyCodes.PAUSE)

    # def next_track(self):
    #     return self.__remote(KeyCodes.CH_UP)

    # def previous_track(self):
    #     return self.__remote(KeyCodes.CH_DOWN)

    def remotekey(self, state, num=1):
        if num > 0 and isinstance(num, int):
            return self.__remote_multiple(KeyCodes.__dict__.get(state), num)
        else:
            return False

    def input_switch(self, name):
        cur_input = self.get_current_input()
        if cur_input is None:
            _LOGGER.error("Couldn't detect current input")
            return False
        return self.__invoke_api(ChangeInputCommand(cur_input.id, name))
