# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#
from tvb.basic.neotraits.api import Attr, List
from tvb.core.entities.file.simulator.simulation_history_h5 import SimulationHistory
from tvb.core.neotraits.view_model import ViewModel, DataTypeGidAttr
from tvb.datatypes.connectivity import Connectivity
from tvb.datatypes.cortex import Cortex
from tvb.datatypes.local_connectivity import LocalConnectivity
from tvb.datatypes.patterns import SpatioTemporalPattern
from tvb.datatypes.projections import ProjectionSurfaceEEG, ProjectionSurfaceMEG, ProjectionSurfaceSEEG
from tvb.datatypes.region_mapping import RegionMapping
from tvb.datatypes.sensors import SensorsEEG, SensorsMEG, SensorsInternal
from tvb.datatypes.surfaces import CorticalSurface
from tvb.simulator.integrators import HeunDeterministic, Integrator, IntegratorStochastic, HeunStochastic, \
    EulerDeterministic, EulerStochastic, RungeKutta4thOrderDeterministic, Identity, VODE, VODEStochastic, Dopri5, \
    Dopri5Stochastic, Dop853, Dop853Stochastic
from tvb.simulator.monitors import Monitor, EEG, MEG, iEEG, Raw, SubSample, SpatialAverage, GlobalAverage, \
    TemporalAverage, Projection, Bold, BoldRegionROI
from tvb.simulator.noise import Noise, Additive, Multiplicative
from tvb.simulator.simulator import Simulator


class NoiseViewModel(ViewModel, Noise):
    @property
    def linked_has_traits(self):
        return Noise


class AdditiveNoiseViewModel(NoiseViewModel, Additive):
    @property
    def linked_has_traits(self):
        return Additive


class MultiplicativeNoiseViewModel(NoiseViewModel, Multiplicative):
    @property
    def linked_has_traits(self):
        return Multiplicative

    def __init__(self):
        super(MultiplicativeNoiseViewModel, self).__init__()
        self.b = type(self.b)()


class IntegratorViewModel(ViewModel, Integrator):
    @property
    def linked_has_traits(self):
        return Integrator


class IntegratorStochasticViewModel(IntegratorViewModel, IntegratorStochastic):
    noise = Attr(
        field_type=NoiseViewModel,
        label=IntegratorStochastic.noise.label,
        default=AdditiveNoiseViewModel(),
        required=IntegratorStochastic.noise.required,
        doc=IntegratorStochastic.noise.doc
    )

    @property
    def linked_has_traits(self):
        return IntegratorStochastic

    def __init__(self):
        super(IntegratorStochasticViewModel, self).__init__()
        self.noise = type(self.noise)()


class HeunDeterministicViewModel(IntegratorViewModel, HeunDeterministic):
    @property
    def linked_has_traits(self):
        return HeunDeterministic


class HeunStochasticViewModel(IntegratorStochasticViewModel, HeunStochastic):
    @property
    def linked_has_traits(self):
        return HeunStochastic


class EulerDeterministicViewModel(IntegratorViewModel, EulerDeterministic):
    @property
    def linked_has_traits(self):
        return EulerDeterministic


class EulerStochasticViewModel(IntegratorStochasticViewModel, EulerStochastic):
    @property
    def linked_has_traits(self):
        return EulerStochastic


class RungeKutta4thOrderDeterministicViewModel(IntegratorViewModel, RungeKutta4thOrderDeterministic):
    @property
    def linked_has_traits(self):
        return RungeKutta4thOrderDeterministic


class IdentityViewModel(IntegratorViewModel, Identity):
    @property
    def linked_has_traits(self):
        return Identity


class VODEViewModel(IntegratorViewModel, VODE):
    @property
    def linked_has_traits(self):
        return VODE


class VODEStochasticViewModel(IntegratorStochasticViewModel, VODEStochastic):
    @property
    def linked_has_traits(self):
        return VODEStochastic


class Dopri5ViewModel(IntegratorViewModel, Dopri5):
    @property
    def linked_has_traits(self):
        return Dopri5


class Dopri5StochasticViewModel(IntegratorStochasticViewModel, Dopri5Stochastic):
    @property
    def linked_has_traits(self):
        return Dopri5Stochastic


class Dop853ViewModel(IntegratorViewModel, Dop853):
    @property
    def linked_has_traits(self):
        return Dop853


class Dop853StochasticViewModel(IntegratorStochasticViewModel, Dop853Stochastic):
    @property
    def linked_has_traits(self):
        return Dop853Stochastic


class MonitorViewModel(ViewModel, Monitor):
    @property
    def linked_has_traits(self):
        return Monitor


class RawViewModel(MonitorViewModel, Raw):
    @property
    def linked_has_traits(self):
        return Raw


class SubSampleViewModel(MonitorViewModel, SubSample):
    @property
    def linked_has_traits(self):
        return SubSample


class SpatialAverageViewModel(MonitorViewModel, SpatialAverage):
    @property
    def linked_has_traits(self):
        return SpatialAverage


class GlobalAverageViewModel(MonitorViewModel, GlobalAverage):
    @property
    def linked_has_traits(self):
        return GlobalAverage


class TemporalAverageViewModel(MonitorViewModel, TemporalAverage):
    @property
    def linked_has_traits(self):
        return TemporalAverage


class ProjectionViewModel(MonitorViewModel, Projection):
    region_mapping = DataTypeGidAttr(
        linked_datatype=RegionMapping,
        required=True,
        label=Projection.region_mapping.label,
        doc=Projection.region_mapping.doc
    )

    @property
    def linked_has_traits(self):
        return Projection


class EEGViewModel(ProjectionViewModel, EEG):
    projection = DataTypeGidAttr(
        linked_datatype=ProjectionSurfaceEEG,
        label=EEG.projection.label,
        doc=EEG.projection.doc
    )

    sensors = DataTypeGidAttr(
        linked_datatype=SensorsEEG,
        label=EEG.sensors.label,
        doc=EEG.sensors.doc
    )

    @property
    def linked_has_traits(self):
        return EEG


class MEGViewModel(ProjectionViewModel, MEG):
    projection = DataTypeGidAttr(
        linked_datatype=ProjectionSurfaceMEG,
        label=MEG.projection.label,
        doc=MEG.projection.doc
    )

    sensors = DataTypeGidAttr(
        linked_datatype=SensorsMEG,
        label=MEG.sensors.label,
        doc=MEG.sensors.doc
    )

    @property
    def linked_has_traits(self):
        return MEG


class iEEGViewModel(ProjectionViewModel, iEEG):
    projection = DataTypeGidAttr(
        linked_datatype=ProjectionSurfaceSEEG,
        label=iEEG.projection.label,
        doc=iEEG.projection.doc
    )

    sensors = DataTypeGidAttr(
        linked_datatype=SensorsInternal,
        label=iEEG.sensors.label,
        doc=iEEG.sensors.doc
    )

    @property
    def linked_has_traits(self):
        return iEEG


class BoldViewModel(MonitorViewModel, Bold):
    @property
    def linked_has_traits(self):
        return Bold

    def __init__(self):
        super(BoldViewModel, self).__init__()
        self.hrf_kernel = type(self.hrf_kernel)()


class BoldRegionROIViewModel(BoldViewModel, BoldRegionROI):
    @property
    def linked_has_traits(self):
        return BoldRegionROI


class CortexViewModel(ViewModel, Cortex):

    @property
    def linked_has_traits(self):
        return Cortex

    surface_gid = DataTypeGidAttr(
        linked_datatype=CorticalSurface,
        label=Simulator.surface.label,
        default=Simulator.surface.default,
        required=Simulator.surface.required,
        doc=Simulator.surface.doc
    )

    local_connectivity = DataTypeGidAttr(
        linked_datatype=LocalConnectivity,
        required=Cortex.local_connectivity.required,
        label=Cortex.local_connectivity.label,
        doc=Cortex.local_connectivity.doc
    )

    region_mapping_data = DataTypeGidAttr(
        linked_datatype=RegionMapping,
        label=Cortex.region_mapping_data.label,
        doc=Cortex.region_mapping_data.doc
    )


class SimulatorAdapterModel(ViewModel, Simulator):

    @property
    def linked_has_traits(self):
        return Simulator

    #TODO: add get_algorithm_module and get_algorithm_class_name to all modules (for project import)

    @property
    def get_algorithm_module(self):
        return "tvb.adapters.simulator.simulator_adapter"

    @property
    def get_algorithm_class_name(self):
        return "SimulatorAdapter"

    is_main = Attr(
        field_type=bool,
        default=True,
        required=False
    )

    connectivity = DataTypeGidAttr(
        linked_datatype=Connectivity,
        required=Simulator.connectivity.required,
        label=Simulator.connectivity.label,
        doc=Simulator.connectivity.doc
    )

    surface = Attr(
        field_type=CortexViewModel,
        label=Simulator.surface.label,
        default=Simulator.surface.default,
        required=Simulator.surface.required,
        doc=Simulator.surface.doc
    )

    stimulus = DataTypeGidAttr(
        linked_datatype=SpatioTemporalPattern,
        label=Simulator.stimulus.label,
        default=Simulator.stimulus.default,
        required=Simulator.stimulus.required,
        doc=Simulator.stimulus.doc
    )

    history_gid = DataTypeGidAttr(
        linked_datatype=SimulationHistory,
        required=False
    )

    integrator = Attr(
        field_type=IntegratorViewModel,
        label=Simulator.integrator.label,
        default=HeunDeterministicViewModel(),
        required=Simulator.integrator.required,
        doc=Simulator.integrator.doc
    )

    monitors = List(
        of=MonitorViewModel,
        label=Simulator.monitors.label,
        default=(TemporalAverageViewModel(),),
        doc=Simulator.monitors.doc
    )

    def __init__(self):
        super(SimulatorAdapterModel, self).__init__()
        self.coupling = type(self.coupling)()
        self.model = type(self.model)()
        self.integrator = type(self.integrator)()
        self.monitors = (type(self.monitors[0])(),)
