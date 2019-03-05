import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
import numpy as np
import os
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

def RoundUp(value):
    return int(Decimal(value).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

class Visualize:
    def __init__(self, numberOfStops, maxTripTime, maxBattery, expectedTripTime):
        self.NumberOfStops = numberOfStops
        self.MaxTripTime = maxTripTime
        self.MaxBattery = maxBattery
        self.ExpectedTripTime = expectedTripTime

        if not os.path.exists("temp"):
            os.mkdir('temp/')

        if not os.path.exists("temp/graphs"):
            os.mkdir('temp/graphs/')


    def VisualizeRewards(self, drivingRewards, chargingRewards):
        fig, axes = plt.subplots(self.NumberOfStops , 2, figsize=(10,10))

        minVal = min(drivingRewards.min(), chargingRewards.min())
        maxVal = max(drivingRewards.max() + 1, chargingRewards.max() + 1)
        tickLabels = np.arange(minVal, maxVal + 1, 1)
        cmap = self.cmap_discretize('jet', tickLabels.size)
        # Make plot with vertical (default) colorbar
        for stop in range(self.NumberOfStops ):
            for action in range(2):
                if action == 0:
                    rewards = drivingRewards[stop]
                else:
                    rewards = chargingRewards[stop]

                ax = axes[stop, action]
                im = ax.imshow(rewards, vmin=minVal, vmax=maxVal, interpolation='nearest', cmap=cmap)
                ax.set_title('Reward for {0} at stop {1}.'.format("Driving" if action == 0 else "Charging", stop), fontsize=8)
                ax.set_yticks(np.arange(self.MaxTripTime))
                ax.set_yticklabels(range(self.MaxTripTime))
                ax.set_xticks(np.arange(self.MaxBattery))
                ax.set_xticklabels(range(self.MaxBattery))
                
        
        fig.subplots_adjust(right=0.79, hspace=0.34)
        
        mappable = cm.ScalarMappable(cmap=cmap)
        mappable.set_array([])
        mappable.set_clim(0.5, tickLabels.size + 0.5)
        cax = fig.add_axes([0.78, 0.11, 0.01, 0.85])
        colorbar = plt.colorbar(mappable, cax=cax)
        colorbar.set_ticks(range(tickLabels.size))
        colorbar.set_ticklabels(tickLabels)
        colorbar.set_label('Rewards')

        fig.text(0.5, 0.96, 'Rewards for given state', ha='center', va='center')
        fig.text(0.5, 0.04, 'Battery Level (kwh)' , ha='center', va='center')
        fig.text(0.06, 0.5, 'Time in {0} minute intervals'.format(15), ha='center', va='center', rotation='vertical')
        
    
        #plt.show()
        fig.savefig('temp/graphs/' + str(datetime.now().date()) + str(datetime.now().time()).replace(':', '.') + '_Rewards.png', dpi=fig.dpi)
    
    def cmap_discretize(self, cmap, N):
        """Return a discrete colormap from the continuous colormap cmap.

            cmap: colormap instance, eg. cm.jet. 
            N: number of colors.

        Example
            x = resize(arange(100), (5,100))
            djet = cmap_discretize(cm.jet, 5)
            imshow(x, cmap=djet)
        """

        if type(cmap) == str:
            cmap = plt.get_cmap(cmap)
        colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
        colors_rgba = cmap(colors_i)
        indices = np.linspace(0, 1., N+1)
        cdict = {}
        for ki,key in enumerate(('red','green','blue')):
            cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki])
                        for i in xrange(N+1) ]
        # Return colormap object.
        return mcolors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)
        
    def VisualizeValueTable(self, values):
        fig, axes = plt.subplots(self.NumberOfStops, figsize=(10,10))

        minVal = values.min()
        maxVal = values.max()
        tickLabels = np.arange(minVal, maxVal + 1, 1)
        cmap = self.cmap_discretize('jet', tickLabels.size)

        # Make plot with vertical (default) colorbar
        for stop in range(self.NumberOfStops ):
            value = values[stop]
            ax = axes[stop]
            im = ax.imshow(value, vmin=minVal, vmax=maxVal, interpolation='nearest', cmap=cmap)
            ax.set_title('Value at stop {0}.'.format(stop), fontsize=8)
            ax.set_xticks(np.arange(self.MaxBattery))
            ax.set_yticks(np.arange(self.MaxTripTime))
        
        fig.subplots_adjust(right=0.79, hspace=0.34)
        
        mappable = cm.ScalarMappable(cmap=cmap)
        mappable.set_array([])
        mappable.set_clim(0.5, tickLabels.size + 0.5)
        cax = fig.add_axes([0.78, 0.11, 0.01, 0.85])
        colorbar = plt.colorbar(mappable, cax=cax)
        colorbar.set_ticks(range(tickLabels.size))
        colorbar.set_ticklabels(tickLabels)
        colorbar.set_label('Expected Value')

        fig.text(0.5, 0.96, 'Expected Value for given state', ha='center', va='center')
        fig.text(0.5, 0.04, 'Battery Level (kwh)', ha='center', va='center')
        fig.text(0.06, 0.5, 'Time in {0} minute intervals'.format(15) , ha='center', va='center', rotation='vertical')
        
    
        #plt.show()

        fig.savefig('temp/graphs/' + str(datetime.now().date()) + str(datetime.now().time()).replace(':', '.')   + '_VTable.png', dpi=fig.dpi)

    def VisualizePolicy(self, policy):
        fig, axes = plt.subplots(self.NumberOfStops, figsize=(10,10))

        minVal = 0
        maxVal = 1
        tickLabels = np.arange(minVal, maxVal + 1, 1)
        cmap = self.cmap_discretize('jet', tickLabels.size)

        # Make plot with vertical (default) colorbar
        for stop in range(self.NumberOfStops ):
            value = policy[stop]
            ax = axes[stop]
            im = ax.imshow(value, vmin=minVal, vmax=maxVal, interpolation='nearest', cmap=cmap)
            ax.set_title('Policy at stop {0}.'.format(stop), fontsize=8)
            ax.set_xticks(range(0,  self.MaxBattery, 1))
            ax.set_xticklabels(range(0,  self.MaxBattery, 1))
            ax.set_yticks(range(0, self.MaxTripTime, 1))
            ax.set_yticklabels(range(0, self.MaxTripTime, 1))
        
        fig.subplots_adjust(right=0.79, hspace=0.34)
        
        mappable = cm.ScalarMappable(cmap=cmap)
        mappable.set_array([])
        mappable.set_clim(0.5, tickLabels.size + 0.5)
        cax = fig.add_axes([0.78, 0.11, 0.01, 0.85])
        colorbar = plt.colorbar(mappable, cax=cax)
        colorbar.set_ticks(range(tickLabels.size))
        colorbar.set_ticklabels(['Drive', 'Charge'])
        colorbar.set_label('Action')

        fig.text(0.5, 0.96, 'Action for given state', ha='center', va='center')
        fig.text(0.5, 0.04, 'Battery Level (kwh)' , ha='center', va='center')
        fig.text(0.06, 0.5, 'Time in {0} minute intervals'.format(15) , ha='center', va='center', rotation='vertical')
        
    
        #plt.show()

        fig.savefig('temp/graphs/' + str(datetime.now().date()) + str(datetime.now().time()).replace(':', '.')  + '_Policy.png', dpi=fig.dpi)

    def DisplayEvaluationGraphs(self, tripStats, route, routeName = ""):
        """ Display diagnostic graphs to see if the algorithm is working as expected. 

            Keyword arguments:

            routeName -- The name of the current route to append to figures. 
        """
        batteryInfo = []
        batteryDistance = []
        timeDistance = []

        for stat in tripStats:
            state = stat.State
            action = stat.Action
            batteryInfo.append([state.BatteryLevel, state.TimeBlock])
            if action == 1:
                batteryDistance.append([state.BatteryLevel, 0])
                timeDistance.append([state.TimeBlock, 0])
            else:
                batteryDistance.append([state.BatteryLevel, route[state.StopIndex].DistanceFromPreviousStop])
                timeDistance.append([state.TimeBlock, route[state.StopIndex].DistanceFromPreviousStop])
                

        self.PlotBatteryInfo(batteryInfo, routeName)
        self.PlotBatteryVsDistance(batteryDistance, routeName)
        self.PlotTimeVsDistance(timeDistance, routeName)

    def PlotBatteryVsDistance(self, batteryDistance, routeName):
        """ Plots the battery level as a funtion of battery level and distance. 
        """
        batteryDistance = np.array(batteryDistance)
        distance = batteryDistance[:, 1]
        battery = batteryDistance[:, 0]

        milage = []
        total = 0
        for d in distance:
            total += d
            milage.append(total)

        #plot Here
        figure, batteryAxes = plt.subplots()
        plt.ylim(ymax=self.MaxBattery, ymin=0)
        plt.xlim(xmin=0, xmax=max(milage))
        
        batteryAxes.plot(milage, battery)

        yTickSpacing = RoundUp((max(battery) + 1)/10) if max(battery) + 1 > 10 else 1
        plt.yticks(np.arange(0, max(battery) + 1, yTickSpacing))

        xTickSpacing = RoundUp((max(milage) + 1)/10) if max(milage) + 1 > 10 else 1
        plt.xticks(np.arange(0, max(milage) + 1, xTickSpacing))

        labels = batteryAxes.get_xticklabels()
        plt.setp(labels, horizontalalignment='right')
        batteryAxes.set(xlabel='Distance (km)', ylabel='Battery Charge (kwh)', title=routeName + ': Battery Charge vs Distance')

        #plt.show()
        figure.savefig('temp/graphs/' + str(datetime.now().date()) + str(datetime.now().time()).replace(':', '.')  + '_BatteryVsDistance.png', dpi=figure.dpi)

    def PlotTimeVsDistance(self, timeDistance, routeName):
        """ Plots the time as a funtion of distance. 
        """ 
        timeDistance = np.array(timeDistance)
        distance = timeDistance[:, 1]
        milage = []
        total = 0
        for d in distance:
            total += d
            milage.append(total)

        time = timeDistance[:, 0]

        #plot Here
        figure, axes = plt.subplots()
       


        # Horizantal Time
        plt.xlim(xmax=self.MaxTripTime, xmin=0)
        plt.ylim(ymin=0)
        axes.plot(time, milage)
        xTickSpacing = RoundUp((self.MaxTripTime + 1)/10) if self.MaxTripTime + 1 > 10 else 1
        plt.xticks(np.arange(0, self.MaxTripTime + 1, xTickSpacing))
        yTickSpacing = RoundUp((max(milage) + 1)/10) if max(milage) + 1 > 10 else 1
        plt.yticks(np.arange(0, max(milage) + 1, yTickSpacing))
        labels = axes.get_xticklabels()
        plt.setp(labels, horizontalalignment='right')
        axes.set(xlabel='Time (15 minute intervals)', ylabel='Distance (km)', title=routeName + ': Distance vs Time')


        figure.savefig('temp/graphs/' + str(datetime.now().date()) + str(datetime.now().time()).replace(':', '.')  + '_TimeVsDistance.png', dpi=figure.dpi)

    def PlotBatteryInfo(self, batteryInfo, routeName):
        """ Plots the battery level as a funtion of battery level and time. 
        """
        batteryInfo = np.array(batteryInfo)
        expectedTime = self.ExpectedTripTime

        #plot Here
        figure, batteryAxes = plt.subplots()
        plt.ylim(ymax=self.MaxBattery, ymin=0)
        plt.xlim(xmax=self.MaxTripTime,xmin=0)
        time = batteryInfo[:, 1]
        battery = batteryInfo[:, 0]
        batteryAxes.plot(time, battery)
        batteryAxes.axvline(expectedTime, linestyle='--')

        yTickSpacing = RoundUp((max(battery)) + 1/ 10) if max(battery) + 1 > 10 else 1
        plt.yticks(np.arange(0, max(battery) + 1, yTickSpacing))
        xTickSpacing = RoundUp((self.MaxTripTime + 1))/10 if self.MaxTripTime + 1 > 10 else 1
        plt.xticks(np.arange(0, self.MaxTripTime + 1, xTickSpacing))

        labels = batteryAxes.get_xticklabels()
        plt.setp(labels, horizontalalignment='right')
        batteryAxes.set(xlabel='Time (15 minute intervals)', ylabel='Battery Charge (kwh)', title=routeName + ': Battery Charge vs Time')
        
        #plt.show()
        figure.savefig('temp/graphs/' + str(datetime.now().date()) + str(datetime.now().time()).replace(':', '.')  + '_BatteryVsTime.png', dpi=figure.dpi)