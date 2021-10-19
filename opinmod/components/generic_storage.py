"""OpInMod version of oemof.solph.components.generic_storage.GenericStorage

GenericStorage and associated individual constraints (blocks) and groupings.

Check the oemof.solph documentation for further details
https://github.com/oemof/oemof-solph

"""

from oemof.network import network
from pyomo.core.base.block import SimpleBlock
from pyomo.environ import Binary
from pyomo.environ import Constraint
from pyomo.environ import Expression
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph import network as solph_network
from oemof.solph.options import Investment
from oemof.solph.plumbing import sequence as solph_sequence

import oemof.solph.network as osn
from oemof.solph.components import generic_storage as oscg

class GenericStorage(oscg.GenericStorage):
    """Component `GenericStorage` to model with basic characteristics of storages.

    The GenericStorage is designed for one input and one output of type `flow`.
    Two outputs, on of type `flow` and one of type `inertia` are allowed.

    """

    def __init__(
        self, *args, max_storage_level=1, min_storage_level=0, **kwargs
    ):
        super().__init__(*args, **kwargs)

    def _check_number_of_flows(self):
        msg = "Only one {0} flow allowed in the GenericStorage {1}."
        solph_network.check_node_object_for_missing_attribute(self, "inputs")
        solph_network.check_node_object_for_missing_attribute(self, "outputs")
        if len(self.inputs) > 1:
            raise AttributeError(msg.format("input", self.label))
        cntFlow = 0
        for i in self.outputs:
            if isinstance(self.outputs[i], osn.Flow):
                cntFlow += 1
        if cntFlow > 1:
            raise AttributeError(msg.format("input", self.label))
