Ev Trip Planner

Kody Sanchez

Senior Project Spring 2019
Utah State University

Advisor: Dr. Nicholas Flann

Abstract:
    This project uses value itertation to create an optimal charging schedule for an Electric Vehical trip. 
The goal is to automate trip scheduling for EV users and show that long distance trips are acheivable with 
the current network. 

Summary of Modules:
    webservice -  This model is a simple flask webserve that uses the OSRM routing service to create a 
        ev trip schedule. The input is the same as an API call to the OSRM routing service. 
    trip_scheduler - This is the main module used to create a trip schedule. The high level module takes the
        input parameters which include the vehicle, start and end locations, arrival time, time block precision, 
        data locations, file locations, and other data. Using the input parameters, the scheduler chooses the 
        correct trip builder and environment and runs the trip simulation, outputing a schedule. 

        schedule - The schedule contains information about the simulation, the resulting stops if succesful, and 
            an OSRM route going to each stop unitl the trip ends. 

        action_space - Defines an enum that is the action space of the simulation

        environment - This is the environment that the value iteration algorithm interacts with. It represents
            a route from point A to point B with all possible charging stops in between. The distance, time, and energy
            consumed between each stop are precalculated before the environments construction. The environment only
            determines the reward for an action given a state. The environment class is based off the OpenAI discrete gym.

        optimizer - This module contains the value iteration algorithm. The algorithm takes an environment and a trip, then 
            returns a possible schedule.

        trip_builder - This module is used to construct a trip. There are several methods to build a trip. The main
            method is to use the OSRM service. This builder gets the route from the start point to the end point from OSRM. 
            It then queries the local database to find all the nearest charges to the route. The route is broken up into sections, 
            and the energy, elevation, time, and distance for each section are calulated. This trip builder is the most processor intensive
            and takes the longest to run. 
            The file trip builder is a simpler trip builder that omits OSRM requests and Database calls in favor of loading pre-saved data
            from a file. This was made to allow for easier debugging earlier on, but has not been updated. 
            The distance trip builder and simple trip builder are very simple trip builders that take a simple hardcoded trip
            for the optimizer to solve. These methods are the fastest, but lack depth because there are simple. They are great for debugging 
            and visualizations. 

        visualizations - classes used to visualize the trip data. 

    tests - incomplete unit tests that were meant to test the energy model before it was offloaded to another student. 

    integration_tests - This module contains 2 "tests" for each type of trip builder. They are for running the service
        and debugging the service without running the webservice app.

    data - A folder to store data files in for the file readers to use. 

    temp - A generated location where all visualizations are stored. 
        

How to run:
    These services must be started to run the program on the local computer. 
        -postgres database with the charging locations. 
            Postgres must be installed on the machine and the ev user must be setup before running the db population script. 
            The db user credentials can be found in the trip_builder/charger_context/charger_context.py file. 
            populate_database_from_file can be used to populate data from previously downloaded charger data from 
            open charge maps. I have not included this data because it is too big to commit to the repository. 

        -OSRM: Run on local machine. Can be build from source or installed with docker.
         Start with osrm-routed --port [port] --algorithm=mld utah-latest.osrm
         Make sure to set the port in the Osrm class as well.
         
        -Open-elevation: Run via docker on local machine via "docker start [name of docker]"
            I had to ping the docker server to the IP send API calls to that IP address. 
    
    
    Run the webserver by navigating to the webservice folder and running flask.

Licence: