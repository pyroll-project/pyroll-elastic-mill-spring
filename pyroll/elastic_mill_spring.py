import logging
from pyroll.core import RollPass, Hook, root_hooks

VERSION = "2.0.0"

log = logging.getLogger(__name__)

RollPass.stand_stiffness = Hook[float]()
"""Stiffness of the roll stand of the current roll pass."""

RollPass.gap_offset = Hook[float]()
"""Offset between set and real roll gap."""


@RollPass.stand_stiffness
def stand_stiffness(self: RollPass):
    raise ValueError("You must provide a roll_stand_stiffness to use the pyroll-elastic-mill-spring plugin.")


@RollPass.gap_offset
def gap_offset(self: RollPass):
    """Calculates the roll gap offset."""

    if not self.has_set_or_cached("roll_force"):
        offset = 0
    else:
        offset = self.roll_force / self.stand_stiffness
        log.info(f"Calculated a roll gap offset of {offset * 1e3:.2f} mm!")

    return offset


@RollPass.gap
def gap(self: RollPass):
    if not hasattr(self, "nominal_gap"):
        self.nominal_gap = self.gap

    gap = self.nominal_gap + self.gap_offset
    return gap


root_hooks.add(RollPass.gap)
