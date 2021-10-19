"""Modules for providing a convenient data structure for OpInMod results.

Check the oemof.solph documentation for further details
https://github.com/oemof/oemof-solph

"""

import oemof.solph.processing as osp
import pandas as pd

def results(om):
    result_dict =  osp.results(om)
    for (ores,ires) in result_dict:
        for (oin, iin) in om.sources_inertia:
            if om.sources_inertia[oin,iin].provision_type == 'synchronous_generator' and oin == ores and ires == iin:
                result_dict[ores, ires]['sequences']['inertia_constant'] = om.sources_inertia[oin,iin].inertia_constant
                result_dict[ores, ires]['sequences']['apparent_power'] = om.sources_inertia[oin,iin].apparent_power
            elif om.sources_inertia[oin,iin].provision_type == 'synchronous_storage' and oin == ores and ires == iin:
                result_dict[ores, ires]['sequences']['inertia_constant'] = om.sources_inertia[oin,iin].inertia_constant
                result_dict[ores, ires]['sequences']['apparent_power'] = om.sources_inertia[oin,iin].apparent_power
            elif om.sources_inertia[oin,iin].provision_type == 'none' and oin == ores and ires == iin:
                result_dict[ores, ires]['sequences']['inertia_constant'] = om.sources_inertia[oin,iin].inertia_constant
                result_dict[ores, ires]['sequences']['apparent_power'] = om.sources_inertia[oin,iin].apparent_power
            elif om.sources_inertia[oin,iin].provision_type == 'synthetic_wind' and oin == ores and ires == iin:
                for t in om.TIMESTEPS:
                    if t == 0:
                        result_dict[ores, ires]['sequences']['inertia_constant'] = None
                        result_dict[ores, ires]['sequences']['apparent_power'] = None
                        result_dict[ores, ires]['sequences'].iloc[t, 1] = om.sources_inertia[oin,iin].inertia_constant[t]
                        result_dict[ores, ires]['sequences'].iloc[t, 2] = om.sources_inertia[oin,iin].apparent_power
                    else:
                        result_dict[ores, ires]['sequences'].iloc[t, 1] = om.sources_inertia[oin,iin].inertia_constant[t]
                        result_dict[ores, ires]['sequences'].iloc[t, 2] = om.sources_inertia[oin,iin].apparent_power
                result_dict[ores, ires]['sequences']['inertia_constant'] = pd.to_numeric(result_dict[ores, ires]['sequences']['inertia_constant'])
                result_dict[ores, ires]['sequences']['apparent_power'] = pd.to_numeric(result_dict[ores, ires]['sequences']['apparent_power'])
            elif om.sources_inertia[oin,iin].provision_type == 'synthetic_storage' and oin == ores and ires == iin:
                result_dict[ores, ires]['sequences']['inertia_constant'] = om.sources_inertia[oin,iin].inertia_constant
                result_dict[ores, ires]['sequences']['apparent_power'] = om.sources_inertia[oin,iin].apparent_power
            else:
                None

    return result_dict
