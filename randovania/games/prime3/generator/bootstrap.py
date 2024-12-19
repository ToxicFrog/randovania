from __future__ import annotations

from typing import TYPE_CHECKING

from randovania.games.prime3.layout.corruption_configuration import CorruptionConfiguration
from randovania.resolver.bootstrap import Bootstrap
from randovania.resolver.energy_tank_damage_state import EnergyTankDamageState

if TYPE_CHECKING:
    from randovania.game_description.game_description import GameDescription
    from randovania.layout.base.base_configuration import BaseConfiguration
    from randovania.resolver.damage_state import DamageState


class CorruptionBootstrap(Bootstrap):
    def create_damage_state(self, game: GameDescription, configuration: BaseConfiguration) -> DamageState:
        assert isinstance(configuration, CorruptionConfiguration)
        return EnergyTankDamageState(
            configuration.energy_per_tank - 1,
            configuration.energy_per_tank,
            game.resource_database,
            game.region_list,
        )
