from time import sleep
import serial
import irtoy
from . import codes


class Remote:
    SLEEP_DUR = 0.3
    SERIAL_DEVICE = '/dev/cu.usbmodem00000001'

    def __init__(self):
        self.device = serial.Serial(self.SERIAL_DEVICE)
        self.toy = irtoy.IrToy(self.device)

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
        self.send(codes.RECEIVER_MUTE)

    def receiver_vol_up(self):
        self.send([
            codes.RECEIVER_VOL_UP,
            codes.RECEIVER_VOL_UP,
            codes.RECEIVER_VOL_UP,
            codes.RECEIVER_VOL_UP,
            codes.RECEIVER_VOL_UP,
            codes.RECEIVER_VOL_UP
        ])

    def receiver_vol_down(self):
        self.send([
            codes.RECEIVER_VOL_DOWN,
            codes.RECEIVER_VOL_DOWN,
            codes.RECEIVER_VOL_DOWN,
            codes.RECEIVER_VOL_DOWN,
            codes.RECEIVER_VOL_DOWN,
            codes.RECEIVER_VOL_DOWN
        ])

    def receiver_input_tv(self):
        self.send(codes.RECEIVER_TV)

    def receiver_input_ps3(self):
        self.send(codes.RECEIVER_HDMI_1)

    def receiver_input_mac(self):
        self.send(codes.RECEIVER_HDMI_2)

    def receiver_input_chromecast(self):
        self.send(codes.RECEIVER_HDMI_3)
