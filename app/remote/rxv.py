import requests
import xml.etree.ElementTree as ET
from collections import namedtuple

BasicStatus = namedtuple("BasicStatus", "on volume mute input")
MenuStatus = namedtuple("MenuStatus", "ready layer name current_line max_line current_list")

GetParam = 'GetParam'
YamahaCommand = '<YAMAHA_AV cmd="{command}">{payload}</YAMAHA_AV>'
MainZone = '<Main_Zone>{request_text}</Main_Zone>'
BasicStatusGet = '<Basic_Status>GetParam</Basic_Status>'
Input = '<Input><Input_Sel>{input_name}</Input_Sel></Input>'
InputSelItem = '<Input><Input_Sel_Item>{input_name}</Input_Sel_Item></Input>'
VolumeLevel = '<Volume><Lvl>{value}</Lvl></Volume>'
VolumeLevelValue = '<Val>{val}</Val><Exp>{exp}</Exp><Unit>{unit}</Unit>'
MuteState = '<Volume><Mute>{state}</Mute></Volume></Main_Zone>'


class RXV(object):
    CTRL_URL = 'http://192.168.1.218/YamahaRemoteControl/ctrl'

    def _request(self, command, request_text, main_zone=True):
        if main_zone:
            payload = MainZone.format(request_text=request_text)
        else:
            payload = request_text

        request_text = YamahaCommand.format(command=command, payload=payload)
        res = requests.post(
            self.CTRL_URL,
            data=request_text,
            headers={"Content-Type": "text/xml"}
        )
        response = ET.XML(res.content)
        if response.get("RC") != "0":
            raise ReponseException(res.content)
        return response

    @property
    def basic_status(self):
        response = self._request('GET', BasicStatusGet)
        on = response.find("Main_Zone/Basic_Status/Power_Control/Power").text
        inp = response.find("Main_Zone/Basic_Status/Input/Input_Sel").text
        mute = response.find("Main_Zone/Basic_Status/Volume/Mute").text
        volume = response.find("Main_Zone/Basic_Status/Volume/Lvl/Val").text
        volume = int(volume) / 10.0

        status = BasicStatus(on, volume, mute, inp)
        return status

    @property
    def input(self):
        request_text = Input.format(input_name=GetParam)
        response = self._request('GET', request_text)
        return response.find("Main_Zone/Input/Input_Sel").text

    @input.setter
    def input(self, input_name):
        request_text = Input.format(input_name=input_name)
        self._request('PUT', request_text)

    @property
    def volume(self):
        request_text = VolumeLevel.format(value=GetParam)
        response = self._request('GET', request_text)
        vol = response.find('Main_Zone/Volume/Lvl/Val').text
        return float(vol) / 10.0

    @volume.setter
    def volume(self, value):
        value = str(int(value * 10))
        exp = 1
        unit = 'dB'

        volume_val = VolumeLevelValue.format(val=value, exp=exp, unit=unit)
        request_text = VolumeLevel.format(value=volume_val)
        self._request('PUT', request_text)

    @property
    def mute(self):
        response = self._request('GET', BasicStatusGet)
        mute = response.find("Main_Zone/Basic_Status/Volume/Mute").text
        return mute

    @mute.setter
    def mute(self, state):
        request_text = MuteState.format(state=state)
        self._request('PUT', request_text)


class RXVException(Exception):
    pass


class ReponseException(RXVException):
    """Exception raised when yamaha receiver responded with an error code"""
    pass


class MenuUnavailable(RXVException):
    """Menu control unavailable for current input"""
    pass
