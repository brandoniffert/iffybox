from time import sleep
import serial
import irtoy
from . import rxv
from . import codes


class Remote:
    SLEEP_DUR = 0.2
    SERIAL_DEVICE = '/dev/cu.usbmodem00000001'

    def __init__(self):
        self.device = serial.Serial(self.SERIAL_DEVICE)
        self.toy = irtoy.IrToy(self.device)
        self.receiver = rxv.RXV()

    def __exit__(self):
        self.device.close()

    def _transmit(self, code):
        self.toy.transmit(code)

    def record(self):
        code = self.toy.receive()
        print(code)

    def send(self, codes):
        if any(isinstance(el, list) for el in codes):
            for code in codes:
                self._transmit(code)
                sleep(self.SLEEP_DUR)
        else:
            self._transmit(codes)

    def tv_toggle_power(self):
        self.send(codes.TV_POWER)

    def tv_toggle_input(self):
        self.send([
            codes.TV_INPUT,
            codes.TV_INPUT,
            codes.TV_EXIT
        ])

    def receiver_mute(self):
        mute_state = self.receiver.mute
        if mute_state == 'Off':
            self.receiver.mute = 'On'
        else:
            self.receiver.mute = 'Off'

    def receiver_vol_up(self):
        current_volume = self.receiver.volume
        self.receiver.volume = current_volume + 1

    def receiver_vol_down(self):
        current_volume = self.receiver.volume
        self.receiver.volume = current_volume - 1

    def receiver_input_tv(self):
        self.receiver.input = 'AV1'

    def receiver_input_ps3(self):
        self.receiver.input = 'HDMI1'

    def receiver_input_mac(self):
        self.receiver.input = 'HDMI2'

    def receiver_input_chromecast(self):
        self.receiver.input = 'HDMI3'
