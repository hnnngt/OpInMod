## Copyright 2021 Henning Thiesen

## OpInMod is released under the open source MIT License, see
## https://github.com/hnnngt/OpInMod/blob/main/LICENSE

"""OpInMod's class `inertia`

"""

import oemof.network.network as onn
from oemof.solph.plumbing import sequence

import math


class Inertia(onn.Edge):
    """Defines a source of inertia between two nodes

    Keyword arguments are used to set the attributes of the inertia source. Parameters
    which are handled specially are noted below.

    Parameters
    ----------
    inertia_constant: numeric, :math: `H_g`
    apparent_power: numeric, :math: `S_g`
    provision_type: string
    inertia_costs: numeric, :math: `c_{inertia}`
    moment_of_inertia: numeric, :math: `J_g`
    minimum_stable_operation: numeric
    inertia_power_share: numeric

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~opinmod.blocks.inertia_inertia.Inertia`

    """

    def __init__(self, inertia_constant=0, apparent_power=0, provision_type=None, inertia_costs=0, moment_of_inertia=0, minimum_stable_operation=0, inertia_power_share=0):
        super().__init__()
        self.inertia_constant = inertia_constant
        self.apparent_power = apparent_power
        self.provision_type = provision_type
        self.inertia_costs = inertia_costs
        self.moment_of_inertia = moment_of_inertia
        self.minimum_stable_operation = minimum_stable_operation
        self.inertia_power_share = inertia_power_share

        self._check_input()
        self._calculations()
        self._create_sequences()

    def _check_input(self):
        """Function to check validity of input

        """
        # check validity of input value - inertia constant
        if self.inertia_constant is not None and self.inertia_constant < 0:
            raise ValueError("The inertia constant can not be below 0.")
        else:
            None

        # check validity of input value - apparent power
        if self.apparent_power is not None and self.apparent_power < 0:
            raise ValueError("The machines apparent power can not be below 0.")
        else:
            None

        # check validity of input value - provision type
        if self.provision_type is None:
            raise ValueError("Please provide a provision type")
        elif self.provision_type == 'synchronous_generator' or self.provision_type == 'synthetic_wind' or self.provision_type == 'none' or self.provision_type == 'synchronous_storage' or self.provision_type == 'synthetic_storage':
            None
        else:
            raise ValueError("Unknown provision type")

        # check validity of input value - moment of inertia
        if self.moment_of_inertia is not None and self.moment_of_inertia < 0:
            raise ValueError("The machines moment of inertia can not be below 0.")
        else:
            None

        if self.provision_type == 'synthetic_storage' and self.inertia_power_share < 0:
            raise ValueError("The inertia/power share can not be below zero")
        elif self.provision_type == 'synthetic_storage' and self.inertia_power_share > 1:
            raise ValueError("The inertia/power share can not be obove one")
        else:
            None

    def _calculations(self):
        """Function to calculate moment of inertia

        """

        if self.provision_type == 'synchronous_generator' or self.provision_type == 'synchronous_storage':
            self.moment_of_inertia = (self.inertia_constant*self.apparent_power)/(0.5*4*math.pi**2*50**2)
        else:
            None

        if self.provision_type == 'synthetic_storage':
            self.moment_of_inertia = (self.apparent_power*self.inertia_power_share)/(4*math.pi**2*50*2)
            self.inertia_constant = (0.5*self.moment_of_inertia*4*math.pi**2*50**2)/(self.apparent_power)
        else:
            None


    def _create_sequences(self):
        """Function to create sequences

        """
        if len([self.inertia_costs]) == 1:
            self.inertia_costs = sequence(self.inertia_costs)
        else:
            raise ValueError("Check length of attribute 'inertia_costs' ")

        if len([self.moment_of_inertia]) == 1:
            self.moment_of_inertia = sequence(self.moment_of_inertia)
        else:
            raise ValueError("Check length of attribute 'moment_of_inertia' ")

        if self.provision_type == 'synthetic_wind':
            self.inertia_constant = sequence(self.inertia_constant)
        elif self.provision_type == 'synchronous_generator' or self.provision_type == 'synchronous_storage' or self.provision_type == 'synthetic_storage' or self.provision_type == 'none':
            None
        else:
            raise ValueError("Check length of attribute 'inertia_constant' and type of provision")

    def constraint_group(self):
        pass
