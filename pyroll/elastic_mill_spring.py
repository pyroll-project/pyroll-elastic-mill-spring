import logging
from pyroll.core import RollPass, Hook, root_hooks

VERSION = "2.0.0"

log = logging.getLogger(__name__)

RollPass.roll_stand_stiffness = Hook[float]()
"""Stiffness of the roll stand of the current roll pass."""

RollPass.roll_gap_offset = Hook[float]()
"""Offset between set and real roll gap."""


@RollPass.roll_stand_stiffness
def roll_stand_stiffness(self: RollPass):
    raise ValueError("You must provide a roll_stand_stiffness to use the pyroll-elastic-mill-spring plugin.")


@RollPass.roll_gap_offset
def roll_gap_offset(self: RollPass):
    """Calculates the roll gap offset."""

    if "roll_force" not in self.__dict__:
        roll_gap_offset = 0
    else:
        roll_gap_offset = self.roll_force / self.roll_stand_stiffness
        log.info(f"Calculated a roll gap offset of {roll_gap_offset * 1e3:.2f} mm!")

    return roll_gap_offset


@RollPass.gap
def gap(self: RollPass):
    if not hasattr(self, "_nominal_roll_gap"):
        self._nominal_roll_gap = self.gap

    if self.has_value("roll_gap_offset"):
        gap = self._nominal_roll_gap + self.roll_gap_offset
        return gap


root_hooks.add(RollPass.gap)
