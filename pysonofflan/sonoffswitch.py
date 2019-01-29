import logging

from pysonofflan import SonoffDevice

_LOGGER = logging.getLogger(__name__)


class SonoffSwitch(SonoffDevice):
    """Representation of a Sonoff Smart Switch/Plug/Wall Switch in LAN Mode.

    Usage example when used as library:
    p = SonoffSwitch("192.168.1.105")
    # print the device ID
    print(p.device_id)
    # change state of plug
    p.state = "ON"
    p.state = "OFF"
    # query and print current state of plug
    print(p.state)

    Errors reported by the device are raised as Exceptions,
    and should be handled by the user of the library.
    """
    # switch states
    SWITCH_STATE_ON = 'ON'
    SWITCH_STATE_OFF = 'OFF'
    SWITCH_STATE_UNKNOWN = 'UNKNOWN'

    def __init__(self,
                 host: str,
                 end_after_first_update: bool = False,
                 context: str = None) -> None:
        SonoffDevice.__init__(self, host, end_after_first_update, context)

    @property
    async def state(self) -> str:
        """
        Retrieve the switch state

        :returns: one of
                  SWITCH_STATE_ON
                  SWITCH_STATE_OFF
                  SWITCH_STATE_UNKNOWN
        :rtype: str
        """
        state = self.params['switch']

        if state == "off":
            return SonoffSwitch.SWITCH_STATE_OFF
        elif state == "on":
            return SonoffSwitch.SWITCH_STATE_ON
        else:
            _LOGGER.warning("Unknown state %s returned.", state)
            return SonoffSwitch.SWITCH_STATE_UNKNOWN

    @state.setter
    async def state(self, value: str):
        """
        Set the new switch state

        :param value: one of
                    SWITCH_STATE_ON
                    SWITCH_STATE_OFF
        :raises ValueError: on invalid state

        """
        if not isinstance(value, str):
            raise ValueError("State must be str, not of %s.", type(value))
        elif value.upper() == SonoffSwitch.SWITCH_STATE_ON:
            await self.turn_on()
        elif value.upper() == SonoffSwitch.SWITCH_STATE_OFF:
            await self.turn_off()
        else:
            raise ValueError("State %s is not valid.", value)

    @property
    def is_on(self) -> bool:
        """
        Returns whether device is on.
        :return: True if device is on, False otherwise
        """
        if 'switch' in self.params:
            return self.params['switch'] == "on"

        return False

    def turn_on(self):
        """
        Turn the switch on.
        """
        _LOGGER.info("Switch turn_on called.")

        self.loop.run_until_complete(
            self.client.send(
                self.client.get_update_payload(
                    self.device_id,
                    {"switch": "on"}
                )
            )
        )

    def turn_off(self):
        """
        Turn the switch off.
        """
        _LOGGER.info("Switch turn_off called.")

        self.loop.run_until_complete(
            self.client.send(
                self.client.get_update_payload(
                    self.device_id,
                    {"switch": "off"}
                )
            )
        )
