"""OpInMod version of oemof.solph.Transformer class

Check the oemof.solph documentation for further details
https://github.com/oemof/oemof-solph

"""

import oemof.solph.network as osn

from opinmod.blocks import transformer_inertia


class Transformer(osn.Transformer):
    """A linear Transformer object with n inputs and n outputs.

    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def constraint_group(self):
        return transformer_inertia.Transformer
