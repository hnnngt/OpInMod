## Copyright 2021 Henning Thiesen

## OpInMod is released under the open source MIT License, see
## https://github.com/hnnngt/OpInMod/blob/main/LICENSE

"""OpInMod version of oemof.solph.models.Model

OpInMod Optimisation Models.

Check the oemof.solph documentation for further details
https://github.com/oemof/oemof-solph

"""

from opinmod import processing_inertia
from opinmod.wind_inertia import calc_inertia_wind
from .blocks import transformer_inertia
from .blocks import inertia_inertia

import oemof.solph.models as osm
import oemof.solph.blocks as osb

import pyomo.environ as po

import math


class Model(osm.Model):
    """An energy system model for operational optimization.

    Parameters
    ----------
    energysystem : EnergySystem object
        Object that holds the nodes of an OpInMod energy system graph

    **The following basic sets are created**:

    SOURCES_INERTIA:
        A 2 dimensional set with all inertia sources. Index: `(source, target)`

    **The following basic variables are created**:

    source_inertia
        inertia source from source to target indexed by SOURCES_INERTIA and
        TIMESTEPS

    """

    CONSTRAINT_GROUPS = [osb.Bus, transformer_inertia.Transformer,
                         osb.InvestmentFlow, osb.Flow,
                         osb.NonConvexFlow, inertia_inertia.Inertia]

    def __init__(self, energysystem, *args, **kwargs):
        self.es = energysystem
        self.sources_inertia = self.es.sources_inertia()
        super().__init__(energysystem, *args, **kwargs)
        self._flow_inertia_constraint()
        self._inertia_flow_constraint()

        if self.es.minimum_system_synchronous_inertia is not None:
            self._min_synchronous_inertia()
        else:
            None

        if self.es.minimum_system_inertia is not None:
            self._min_inertia()
        else:
            None

    def results(self):
        """Returns a nested dictionary of the results of this optimization

        """
        return processing_inertia.results(self)

    def _add_parent_block_sets(self):

        super()._add_parent_block_sets()
        # pyomo set for all inertia sources in the energy system graph
        self.SOURCES_INERTIA = po.Set(initialize=self.sources_inertia.keys(),
                            ordered=True, dimen=2)

    def _add_parent_block_variables(self):

        self.flow = po.Var(self.FLOWS, self.TIMESTEPS,
                           within=po.Reals)

        for (o, i) in self.FLOWS:
            for (oin, iin) in self.SOURCES_INERTIA:
                if o==oin and self.sources_inertia[oin, iin].provision_type=='synthetic_storage':
                    for t in self.TIMESTEPS:
                        self.flow[o, i, t].setub(
                            self.flows[o, i].nominal_value *
                            (1-self.sources_inertia[oin, iin].inertia_power_share))
                elif self.flows[o, i].nominal_value is not None:
                    if self.flows[o, i].fix[self.TIMESTEPS[1]] is not None:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].value = (
                                self.flows[o, i].fix[t] *
                                self.flows[o, i].nominal_value)
                            self.flow[o, i, t].fix()
                    else:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].setub(
                                self.flows[o, i].max[t] *
                                self.flows[o, i].nominal_value)

                        if not self.flows[o, i].nonconvex:
                            for t in self.TIMESTEPS:
                                self.flow[o, i, t].setlb(
                                    self.flows[o, i].min[t] *
                                    self.flows[o, i].nominal_value)
                        elif (o, i) in self.UNIDIRECTIONAL_FLOWS:
                            for t in self.TIMESTEPS:
                                self.flow[o, i, t].setlb(0)
                else:
                    if (o, i) in self.UNIDIRECTIONAL_FLOWS:
                        for t in self.TIMESTEPS:
                            self.flow[o, i, t].setlb(0)


        self.source_inertia = po.Var(self.SOURCES_INERTIA, self.TIMESTEPS,
                           within=po.Binary)

        for (o,i) in self.SOURCES_INERTIA:
            if self.sources_inertia[o,i].provision_type == 'synthetic_wind':
                self.sources_inertia[o,i].inertia_constant = [0] * len(self.es.timeindex)
                self.sources_inertia[o,i].moment_of_inertia = [0] * len(self.es.timeindex)
                for (ofl,ifl) in self.FLOWS:
                    if ofl == o:
                        for t in self.TIMESTEPS:
                            self.sources_inertia[o,i].inertia_constant[t] = calc_inertia_wind(self.flows[o, ifl].fix[t]) * self.es.emulated_inertia_constant
                            self.sources_inertia[o,i].moment_of_inertia[t] = (self.sources_inertia[o, i].inertia_constant[t]*self.sources_inertia[o, i].apparent_power)/(0.5*4*math.pi**2*50**2)
                            if self.flows[o, ifl].fix[t] > 0:
                                self.source_inertia[o,i,t].value=1
                                self.source_inertia[o,i,t].fix()
                            else:
                                self.source_inertia[o,i,t].value=0
                                self.source_inertia[o,i,t].fix()
            elif self.sources_inertia[o,i].provision_type == 'none':
                self.sources_inertia[o,i].inertia_constant = [0] * len(self.es.timeindex)
                self.sources_inertia[o,i].moment_of_inertia = [0] * len(self.es.timeindex)
                for (ofl,ifl) in self.FLOWS:
                    if ofl == o:
                        for t in self.TIMESTEPS:
                            if self.flows[o,ifl].fix[t] > 0:
                                self.source_inertia[o,i,t].value=1
                                self.source_inertia[o,i,t].fix()
                            else:
                                self.source_inertia[o,i,t].value=0
                                self.source_inertia[o,i,t].fix()


    def _flow_inertia_constraint(self):
        """
        Constraint which regulates the relationship between a
        flow an the provision of inertia. Constraint is relevant
        for provision type 'synchronous generator'. If the unit
        is connected to the energy system, then the units flow
        has to be larger then the minimum stable operation point
        times the nominal power of the unit
        """
        def _flow_inertia_rule(self):
            for t in self.TIMESTEPS:
                for (o, iin) in self.SOURCES_INERTIA:
                    if self.sources_inertia[o, iin].provision_type == 'synchronous_generator':
                        lhs = self.source_inertia[o, iin, t]*(self.sources_inertia[o, iin].apparent_power * self.sources_inertia[o, iin].minimum_stable_operation)
                        for (ofl, ifl) in self.FLOWS:
                            try:
                                rhs = self.flow[o, ifl, t]
                            except:
                                None
                        expr = (lhs <= rhs)
                        self.flow_inetia_constraint.add((o, t), expr)
                    #if expr is not True:
                    #    self.flow_inetia_constraint.add((o, t), expr)

        self.flow_inetia_constraint = po.Constraint([(o, t)
                                                     for t in self.TIMESTEPS
                                                     for (o, iin) in self.SOURCES_INERTIA], noruleinit=True)

        self.flow_inetia_constraint_build = po.BuildAction(rule=_flow_inertia_rule)

    def _inertia_flow_constraint(self):
        """
        Constraint which regulates the relationship between
        a flow an the provision of inertia. If the units flow
        is above zero, then inertia is provided
        """
        def _inertia_flow_rule(self):
            for t in self.TIMESTEPS:
                for (o, iin) in self.SOURCES_INERTIA:
                    if self.sources_inertia[o, iin].provision_type == 'synchronous_generator':
                        lhs = self.source_inertia[o, iin, t]
                        for (ofl, ifl) in self.FLOWS:
                            try:
                                rhs = self.flow[o, ifl, t]/self.sources_inertia[o, iin].apparent_power
                            except:
                                None
                        expr = (lhs >= rhs)
                        self.inertia_flow_constraint.add((o, t), expr)
                    #if expr is not True:
                    #    self.flow_inetia_constraint.add((o, t), expr)


        self.inertia_flow_constraint = po.Constraint([(o, t)
                                                     for t in self.TIMESTEPS
                                                     for (o, iin) in self.SOURCES_INERTIA], noruleinit=True)

        self.inertia_flow_constraint_build = po.BuildAction(rule=_inertia_flow_rule)

    def _min_synchronous_inertia(self):
        """Sets an minimum limit of synchronous power system inertia

        .. math:: \sum_{J\_sync} >= limit

        Parameters
        ----------
        minimum_system_synchronous_inertia: numeric
            Value used to create minimum system synchronous
            inertia constraint

        """

        minSyncInertia = self.es.minimum_system_synchronous_inertia

        # defin min synchronous inertia rule
        def _min_sync_inertia_rule(m):
            for t in self.TIMESTEPS:
                actSyncInertia = sum(self.source_inertia[o, i, t]* self.sources_inertia[o, i].moment_of_inertia[t] for (o, i) in self.SOURCES_INERTIA if self.sources_inertia[o,i].provision_type == 'synchronous_generator' or self.sources_inertia[o,i].provision_type == 'synchronous_storage')
                expr = (actSyncInertia >= minSyncInertia)
                if expr is not True:
                    self.min_synchronous_inertia_constraint.add(t, expr)

        self.min_synchronous_inertia_constraint = po.Constraint(self.TIMESTEPS, noruleinit=True)
        self.min_synchronous_inertia_constraint_build = po.BuildAction(rule=_min_sync_inertia_rule)

    def _min_inertia(self):
        """Sets an minimum limit of synchronous power system inertia

        .. math:: \sum_{J\_sync} >= limit

        Parameters
        ----------
        minimum_system_inertia: numeric
            Value used to create minimum system synchronous
            inertia constraint

        """

        minInertia = self.es.minimum_system_inertia

        # defin min synchronous inertia rule
        def _min_inertia_rule(m):
            for t in self.TIMESTEPS:
                actInertia = sum(self.source_inertia[o, i, t]* self.sources_inertia[o, i].moment_of_inertia[t] for (o, i) in self.SOURCES_INERTIA)
                expr = (actInertia >= minInertia)
                if expr is not True:
                    self.min_inertia_constraint.add(t, expr)

        self.min_inertia_constraint = po.Constraint(self.TIMESTEPS, noruleinit=True)
        self.min_inertia_constraint_build = po.BuildAction(rule=_min_inertia_rule)
