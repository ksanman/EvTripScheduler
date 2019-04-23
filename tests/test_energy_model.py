from context import NissanLeaf, EnergyConsumptionModel

vehicle = NissanLeaf(40,5)
model = EnergyConsumptionModel()
kilometers = 13.0
grade = 0.0
acceleration = 0.0
mps = 22.352 # 50 MPH, 79.2 KPH
time = (kilometers * 1000) / mps

energy = model.ComputerEnergyExpended(vehicle, acceleration, mps, grade, time, kilometers)
print energy