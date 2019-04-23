import math



class EnergyConsumptionModel:
    """ Model used to simulate ev battery consumption. 

        Based on this paper: https://www.researchgate.net/publication/294112610_Power-based_electric_vehicle_energy_consumption_model_Model_development_and_validation
    """
    GravitationAcceleration = 9.8066 #[m/s^2]
    AirDensity = 1.2256 #[kg/m^3]
    CR = 1.75
    C1 = 0.0328
    C2 = 4.575

    def ComputerEnergyExpended(self, vehicle, acceleration, velocity, grade, time, distance):
        powerAtWheels = self.ComputePowerToWheels(vehicle, acceleration, velocity, grade)
        power = self.ComputeTractionPowerAtMotor(powerAtWheels, vehicle)

        if acceleration < 0:
            power = self.CalculatePowerWithBraking(power, acceleration)
        net = power + 700 #Electronics
        return (1.0/3600000.0) * (net * time)
    
    def ComputePowerToWheels(self, vehicle, acceleration, velocity, roadGrade):
        """ Equation:
            Pwheels(t) = (ma(a) + mg * cos(theta) * (c_r/1000)(c_1v(t) + c_2) + (1/2) * rho_air * A_f * C_d * v^2(t) + mg*sin(theta)) * v(t)

            Where:
            Pwheels = the power to the vehicles wheels
            m = vehicle mass (m =1521^2kg for Nissan Leaf)
            a(t) = dv(t)/dt (acceleration of vehicle in [m/s]^2) and can be negative
            g = 9.8066 [m/s^2]
            theta = road grade
            c_r = 1.75 - Rolling resistance parameter
            c_1 = 0.0328 - Rolling resistance parameter
            c_2 = 4.575 - Rolling resistance parameter
            p_air = 1.2256 [kg/m^3] air density
            A_f = frontal area of vehicle (2.3316 m^2 for leaf)
            c_d =  drag coefficient of vehicle (0.28 for leaf)
            v(t) speed of vehicle in [m/s]
        """
        powerToWheels = ((vehicle.Mass * acceleration * acceleration) + (vehicle.Mass * self.GravitationAcceleration) * math.cos(roadGrade) \
            * (self.CR / 1000) * (self.C1 * velocity + self.C2) + 0.5 * self.AirDensity * vehicle.FrontalArea * vehicle.DragCoefficient * velocity * velocity \
                + (vehicle.Mass * self.GravitationAcceleration) * math.sin(roadGrade)) * velocity

        return powerToWheels

    def ComputeTractionPowerAtMotor(self, powerAtWheels, vehicle):
        """ Equation:
            Pelectricmotor(t) = Pwheels * 1+ (1 -nu_drivetrain) * 1+ (1 - nu_electricmotor)
        """
        
        powerAtMotor = powerAtWheels * (1.0 + (1.0 - vehicle.DrivelineEfficiency)) * (1.0 + (1.0 - vehicle.MotorEfficiency))
        return powerAtMotor

    def CalculatePowerWithBraking(self, power, acceleration):
        """
            rb = e^(0.00411/a(t))^-1
        """
        exponent = 0.00411/abs(acceleration)
        try:
            rb = math.pow(math.exp(exponent),-1)
        except:
            return power
        return rb * power