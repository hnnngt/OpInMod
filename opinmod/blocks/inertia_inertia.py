"""Creating sets, variables, constraints and parts of
the objective function for Inertia objects.

"""

from pyomo.core.base.block import SimpleBlock


class Inertia(SimpleBlock):
    """Inertia block with definitions for standard inertia sources.

    **The following parts of the objective function are created:**

    If :attr:`inertia_costs` are set by the user:
      .. math::
          \sum_{(i,o)} \sum_t source_inertia(i, o, t) \cdot
          sources\_inertia(i, o).moment_of_inertia(t) \cdot
          sources\_inertia(i,o).inertia_costs(t)

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Creates sets, variables and constraints for all sources of inertia.

        Parameters
        ----------
        group

        """
        if group is None:
            return None

        m = self.parent_block()

    def _objective_expression(self):
        """ Objective expression for all standard inertia sources with
        costs for inertia.
        """
        m = self.parent_block()

        inertia_costs = 0

        for i, o in m.SOURCES_INERTIA:
            for t in m.TIMESTEPS:
                inertia_costs += (m.source_inertia[i,o,t] *
                                  m.sources_inertia[i,o].moment_of_inertia[t] *
                                  m.sources_inertia[i,o].inertia_costs[t])

        return inertia_costs
