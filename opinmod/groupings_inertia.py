## Copyright 2021 Henning Thiesen

## OpInMod is released under the open source MIT License, see
## https://github.com/hnnngt/OpInMod/blob/main/LICENSE

"""OpInMod version of oemof.solph.groupings

Groupings needed on an energy system for it to work with OpInMod.

"""
from opinmod.blocks import inertia_inertia

import oemof.network.groupings as ong
import oemof.solph.blocks as osb
from oemof.solph.groupings import investment_flow_grouping, nonconvex_flow_grouping, constraint_grouping

def _inertia_grouping(stf):
    """Grouping function for class inertia.

    """
    if hasattr(stf[2], 'inertia_constant'):
        return True
    else:
        return False

inertia_grouping = ong.FlowsWithNodes(
    constant_key=inertia_inertia.Inertia,
    filter=_inertia_grouping)

def _flow_grouping(stf):
    """Grouping function for class flow.

    """
    if hasattr(stf[2], 'nominal_value'):
        return True
    else:
        return False

standard_flow_grouping = ong.FlowsWithNodes(
    constant_key=osb.Flow,
    filter=_flow_grouping)

GROUPINGS = [constraint_grouping, investment_flow_grouping,
             standard_flow_grouping, nonconvex_flow_grouping,
             inertia_grouping]
