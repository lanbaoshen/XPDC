from .._base import DeviceBase
from ..utils import exec_cmd


class HDCDevice(DeviceBase):
    def __init__(self, *, device_id: str, hdc: str):
        self.device_id = device_id
        self._hdc = hdc

    def cmd(self, cmd: list[str], *, timeout: int = 10) -> str:
        cmd = [self._hdc, '-t', self.device_id] + cmd
        return exec_cmd(cmd, timeout=timeout)

    def shell(self, cmd: list[str], *, timeout: int = 10) -> str:
        cmd = [self._hdc, '-t', self.device_id, 'shell'] + cmd
        return exec_cmd(cmd, timeout=timeout)

    def tap(self, x: int, y: int) -> str:
        return self.shell(['uitest', 'uiInput', 'click', str(x), str(y)])

    def double_tap(self, x: int, y: int) -> str:
        return self.shell(['uitest', 'uiInput', 'doubleClick', str(x), str(y)])

    def long_press(self, x: int, y: int, *, duration_ms: int = 3000) -> str:
        return self.shell(['uitest', 'uiInput', 'longClick', str(x), str(y)])

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, *, duration_ms: int = None) -> str:
        if duration_ms is None:
            dist_sq = (start_x - end_x) ** 2 + (start_y - end_y) ** 2
            duration_ms = int(dist_sq / 1000)
            duration_ms = max(1000, min(duration_ms, 2000))  # Clamp between 1000-2000ms

        return self.shell(
            ['uitest', 'uiInput', 'swipe', str(start_x), str(start_y), str(end_x), str(end_y), str(duration_ms)]
        )

    def back(self) -> str:
        return self.shell(['uitest', 'uiInput', 'keyEvent', 'Back'])

    def home(self) -> str:
        return self.shell(['uitest', 'uiInput', 'keyEvent', 'Home'])

    def launch_app(self, bundle: str, ability: str = 'EntryAbility') -> str:
        return self.shell(['aa', 'start', '-b', bundle, '-a', ability])

    def type_text(self, text: str) -> str:
        return self.shell(['uitest', 'uiInput', 'text', text])

    def clear_text(self) -> str:
        # Ctrl + A
        self.shell(['uitest', 'uiInput', 'keyEvent', '2072', '2017'])
        # Delete
        return self.shell(['uitest', 'uiInput', 'keyEvent', '2055'])
