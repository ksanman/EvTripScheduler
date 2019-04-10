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

How to run:
    These services must be started to run the program on the local computer. 
        -postgres database with the charging locations. 
        -OSRM: Run on local machine. Start with osrm-routed --port [port] --algorithm=mld utah-latest.osrm
        -open-elevation: Run via docker on local machine. docker start [name of docker]
        -OSRM-Frontend run on local server: npm start in directory. *Upload with changed leaflet code.
    Run the program by navigating to the webservice folder and running flask.

Licence: