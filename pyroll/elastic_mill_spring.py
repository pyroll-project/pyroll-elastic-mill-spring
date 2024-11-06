from pyroll.core import BaseRollPass, Hook, root_hooks

VERSION = "3.0.0"

BaseRollPass.stand_stiffness = Hook[float]()
"""Stiffness of the roll stand of the current roll pass."""


@BaseRollPass.stand_stiffness
def stand_stiffness(self: BaseRollPass):
    raise ValueError("You must provide a roll stand stiffness to use the pyroll-elastic-mill-spring plugin.")


@BaseRollPass.gap
def widened_gap(self: BaseRollPass, cycle):
    if cycle:
        return None

    if not hasattr(self, "nominal_gap"):
        self.nominal_gap = self.gap

    elastic_gap_offset = self.roll_force / self.stand_stiffness
    elastic_gap = self.nominal_gap + elastic_gap_offset
    return elastic_gap


root_hooks.add(BaseRollPass.gap)
