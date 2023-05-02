# NOT FINISHED PROPERLY
from typing import Protocol

from iot.devices import HueLight, SmartBattery, SmartSpeaker
from iot.message import Message, MessageType


class StatusSource(Protocol):
    def check_status(self) -> None:
        ...

class Device(Protocol):
    def send_message(self, message_type: MessageType) -> None:
        ...


def run_program(program: list[Message], devices:)
    print("=====RUNNING PROGRAM=====")
    for msg in program:
        devices[msg.device_id].send_message(msg.)
    print("=====END OF PROGRAM=====")

def check_status(devices: dict[str, StatusSource]) -> None:
    for device in devices.values():
        device.check_status()


class SmartBattery:
    def check_status(self) -> None:
        pritn("Battery online.")

class HueLight:
    pass

class SmartSpeaker:
    def check_status(self) -> None:
        print("Smart Speaker connected.")

    def send_message(self, massage_type: MassageType) -> None:
        pass



def main() -> None:
    devices = {
        "hue_light": HueLight(),
        "speaker": SmartSpeaker(),
    }
    status_sources = devices | {
        "battery": SmartBattery(),
    }

    wake_up_program = [
        Message("hue_light", MessageType.SWITCH_ON),
        Message("speaker", MessageType.SWITCH_ON),
        Message("speaker", MessageType.PLAY_SONG,)
    ]

    # run the program
    run_program(wake_up_program)

    # check the status
    check_status(status_sources)


if __name__ == '__main__':
    main()
