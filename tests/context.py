import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trip_scheduler.trip_builder.vehicle import NissanLeaf
from trip_scheduler.trip_builder.vehicle.energy_model import EnergyConsumptionModel