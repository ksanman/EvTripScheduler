import pandas as pd
import numpy as np
import math

def Energyvalueitialization(VehicleWeight=0,CoefficientofFriction=0.015,FrontArea=0,DragCoefficient=0,RhoAir=1.204):
    global CarWeight,CofofFric,carFrontarea,Cd,AirDensity
    CarWeight=VehicleWeight
    CofofFric=CoefficientofFriction
    carFrontarea=FrontArea
    Cd=DragCoefficient
    AirDensity=RhoAir

def Energy(SpreedLimit=25,Distance=0,Elevation=0):
    G = 9.81
    #change MPH intoMeater per second
    SpreedLimit=SpreedLimit/2.237

    time=(Distance*1000)/SpreedLimit
    #convert elevation into grade
    grade=(Elevation*3.281)/(Distance*1000*3.281)
    teta=math.degrees(math.atan(grade))

    # rolling Resistance
    Fr = CarWeight * G * CofofFric


    Fw = 0.5 * SpreedLimit * SpreedLimit * AirDensity * carFrontarea * Cd


    Fs = CarWeight * G * math.sin(teta)


    F = 0

    TotalPower = (Fr + Fw + Fs + F) * SpreedLimit * time
    TotalPower=TotalPower/(1000*3600)

    return TotalPower



