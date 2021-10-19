"""OpInMod version of oemof.solph.blocks.transformer.Transformer

Creating sets, variables, constraints and parts of
the objective function for Transformer objects.

Check the oemof.solph documentation for further details
https://github.com/oemof/oemof-solph

"""

from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core.base.block import SimpleBlock


class Transformer(SimpleBlock):
    """Block for the linear relation of nodes with type

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the linear constraint for the class:`Transformer`
        block with nodes op type `Flow`.


        """
        if group is None:
            return None

        m = self.parent_block()

        in_flows = {n: [i for i in n.inputs.keys()] for n in group}
        out_flows = {n: [o for o in n.outputs.keys() if o.balanced is True] for n in group}

        self.relation = Constraint(
            [(n, i, o, t)
             for t in m.TIMESTEPS
             for n in group
             for o in out_flows[n]
             for i in in_flows[n]], noruleinit=True)

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    for o in out_flows[n]:
                        for i in in_flows[n]:
                            try:
                                lhs = (m.flow[i, n, t] /
                                       n.conversion_factors[i][t])
                                rhs = (m.flow[n, o, t] /
                                       n.conversion_factors[o][t])
                            except ValueError:
                                raise ValueError(
                                    "Error in constraint creation",
                                    "source: {0}, target: {1}".format(
                                        n.label, o.label))
                            block.relation.add((n, i, o, t), (lhs == rhs))

        self.relation_build = BuildAction(rule=_input_output_relation)
