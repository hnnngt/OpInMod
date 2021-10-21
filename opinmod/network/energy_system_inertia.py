## Copyright 2021 Henning Thiesen

## OpInMod is released under the open source MIT License, see
## https://github.com/hnnngt/OpInMod/blob/main/LICENSE

"""OpInMod version of oemof.solph.network.energy_system

Check the oemof.solph documentation for further details
https://github.com/oemof/oemof-solph

"""

from opinmod.network import inertia_inertia
from opinmod.groupings_inertia import GROUPINGS

import oemof.network.energy_system as one
import oemof.solph.network as osn

class EnergySystem(one.EnergySystem):
    """
        A variant of :class:`EnergySystem
        <oemof.solph.network.EnergySystem>` specially tailored to OpInMod.
    """
    def __init__(self, *args, **kwargs):
        """
        """
        self.nominal_grid_frequency = kwargs.get("nominal_grid_frequency")

        self.minimum_system_synchronous_inertia = kwargs.get("minimum_system_synchronous_inertia")

        self.minimum_system_inertia = kwargs.get("minimum_system_inertia")

        self.emulated_inertia_constant = kwargs.get("emulated_inertia_constant")

        self._check_input()

        kwargs['groupings'] = (GROUPINGS + kwargs.get('groupings', []))

        super().__init__(*args, **kwargs)

    def _check_input(self):
        """
        Checks the inputs

        Returns
        -------
        self
        """

        # check, if grid frequency is above 0
        if self.nominal_grid_frequency is None:
            None
        elif self.nominal_grid_frequency <= 0:
            raise ValueError("The nominal grid frequency has to be above 0.")
        else:
            None

        # checks, if minimum inerita is above zero
        if self.minimum_system_synchronous_inertia is None:
            None
        elif self.minimum_system_synchronous_inertia < 0:
            raise ValueError("The minimum system synchronous inertia can not be below zero.")
        else:
            None

        # checks, if minimum inerita is above zero
        if self.minimum_system_inertia is None:
            None
        elif self.minimum_system_inertia < 0:
            raise ValueError("The minimum system inertia can not be below zero.")
        else:
            None

    def flows(self):
        return {
            (source, target): source.outputs[target]
            for source in self.nodes
            for target in source.outputs
            if isinstance(source.outputs[target], osn.Flow)
        }


    def sources_inertia(self):
        return {
            (source, target): source.outputs[target]
            for source in self.nodes
            for target in source.outputs
            if isinstance(source.outputs[target], inertia_inertia.Inertia)
        }
