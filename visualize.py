import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
import numpy as np

class Visualize:
    def __init__(self, numberOfStops, maxTripTime, maxBattery, expectedTripTime):
        self.NumberOfStops = numberOfStops
        self.MaxTripTime = maxTripTime
        self.MaxBattery = maxBattery
        self.ExpectedTripTime = expectedTripTime

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
        fig.text(0.5, 0.04, 'Battery Level' , ha='center', va='center')
        fig.text(0.06, 0.5, 'Time in {0} minute intervales'.format(15), ha='center', va='center', rotation='vertical')
        
    
        plt.show()
    
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
        fig.text(0.5, 0.04, 'Battery Level', ha='center', va='center')
        fig.text(0.06, 0.5, 'Time in {0} minute intervales'.format(15) , ha='center', va='center', rotation='vertical')
        
    
        plt.show()

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
        fig.text(0.5, 0.04, 'Battery Level' , ha='center', va='center')
        fig.text(0.06, 0.5, 'Time in {0} minute intervales'.format(15) , ha='center', va='center', rotation='vertical')
        
    
        plt.show()