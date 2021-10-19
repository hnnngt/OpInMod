"""
This module is designed to hold components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.
"""

from .generic_storage import GenericStorage

from oemof.solph.components.extraction_turbine_chp import ExtractionTurbineCHP  # noqa: F401
from oemof.solph.components.generic_chp import GenericCHP  # noqa: F401
from oemof.solph.components.offset_transformer import OffsetTransformer  # noqa: F401
