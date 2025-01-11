from __future__ import annotations

from subprocess import Popen, TimeoutExpired
from typing import TYPE_CHECKING

from randovania.game_connection.builder.prime_connector_builder import PrimeConnectorBuilder
from randovania.game_connection.connector_builder_choice import ConnectorBuilderChoice
from randovania.game_connection.executor.dolphin_executor import DolphinExecutor

if TYPE_CHECKING:
    from randovania.game_connection.executor.memory_operation import MemoryOperationExecutor


class DolphinConnectorBuilder(PrimeConnectorBuilder):
    dolphin_cmd: str
    dolphin_child: Popen

    def __init__(self, dolphin_cmd: str = ""):
        super().__init__()
        self.dolphin_cmd = dolphin_cmd
        self.dolphin_child = None

    @property
    def pretty_text(self) -> str:
        if self.dolphin_cmd:
            return f"{super().pretty_text}: {self.dolphin_cmd}"
        else:
            return f"{super().pretty_text}: (autodetect)"

    @property
    def connector_builder_choice(self) -> ConnectorBuilderChoice:
        return ConnectorBuilderChoice.DOLPHIN

    def start_dolphin(self):
        if not self.dolphin_cmd:
            return

        if self.dolphin_child is None:
            self.logger.info(f"Dolphin not running, attempting to start it: {self.dolphin_cmd}")
            self.dolphin_child = Popen([self.dolphin_cmd], executable=self.dolphin_cmd)

        elif self.dolphin_child.poll() is not None:
            self.logger.info(f"Dolphin has exited, restarting it: {self.dolphin_cmd}")
            self.dolphin_child = Popen([self.dolphin_cmd])

    def stop_dolphin(self):
        if self.dolphin_child is not None:
            self.logger.info("Shutting down child Dolphin process.")
            self.dolphin_child.terminate()
            try:
                self.dolphin_child.terminate()
                self.dolphin_child.wait(timeout=1)
            except TimeoutExpired:
                self.dolphin_child.kill()
            self.dolphin_child = None

    def create_executor(self) -> MemoryOperationExecutor:
        return DolphinExecutor(self.dolphin_cmd)

    def configuration_params(self) -> dict:
        return {
            "dolphin_cmd": self.dolphin_cmd,
        }
