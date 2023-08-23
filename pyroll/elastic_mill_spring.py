from pyroll.core import RollPass, Hook, root_hooks

VERSION = "2.1"

RollPass.stand_stiffness = Hook[float]()
"""Stiffness of the roll stand of the current roll pass."""


@RollPass.stand_stiffness
def stand_stiffness(self: RollPass):
    raise ValueError("You must provide a roll stand stiffness to use the pyroll-elastic-mill-spring plugin.")


@RollPass.gap
def widened_gap(self: RollPass, cycle):
    if cycle:
        return None

    if not hasattr(self, "nominal_gap"):
        self.nominal_gap = self.gap

    elastic_gap_offset = self.roll_force / self.stand_stiffness
    elastic_gap = self.nominal_gap + elastic_gap_offset
    return elastic_gap


root_hooks.add(RollPass.gap)
