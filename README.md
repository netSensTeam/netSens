<img src="https://github.com/netSensTeam/netSens/blob/master/netsens_logo1.jpg" alt="netsens_logo"/>

<p align="center">
<a href="https://github.com/netSensTeam/netSens/issues"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg"></a>
<a href="https://github.com/netSensTeam/netSens/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
</p>


# netSens


netSens is a system for collecting, processing and presenting network information for the benefit of online and offline communication network analysis, all in a passive and secretive manner.


* Written in Python and JavaScript.
* Based on open shelf products.
* Generic and modular-oriented development - an infrastructure that allows easy integration of new capabilities within the product and interfaces with external services.
<img src="https://github.com/netSensTeam/netSens/blob/master/netsens.jpg" alt="Screenshot of netsens" width="560"/>

## ⭐️ Features
- Cross-Platform (Linux, Windows)
- Event-oriented Pub / Sub architecture
- Web-based UI
- Agent for online data collection
- Pcap upload system for offline data analysis
- Plugin engine: easy to add new protocols and external service providers

## 💻 Services:
- [MongoDB](https://github.com/mongodb/mongo) server
- [Mosquitto](https://github.com/eclipse/mosquitto) server

## ✨ Python Dependencies:
- [dpkt](https://github.com/kbandla/dpkt)
- [flask](https://github.com/pallets/flask)
- [pymongo](https://github.com/mongodb/mongo-python-driver)
- [paho](https://github.com/eclipse/paho.mqtt.python)

## 🚀 Basic usage:
* Windows:
  - use run_public.bat file to start up the system
* Linux:
  - execute init.py file (in center/scripts) to start up the system
- app will be available on port 8000
- goto localhost:8000
- upload a pcap file on the main page
- explore the created network by going to networks tab. use filter if needed.

## 🤝 Authors
netSens was initially developed as a final project at MTA (The Academic College of Tel Aviv-Yaffo) by:

 **Jacob Roginsky**
- Github: [@cyberj19](https://github.com/cyberj19)

 **Nadya Jurba**
- Github: [@nadya1990](https://github.com/nadya1990)


## 📝 License

Copyright © 2019 [netSens](https://github.com/netSensTeam/netSens).<br />
This project is [MIT](https://github.com/netSensTeam/netSens/blob/master/LICENSE) licensed.

> *"The quieter you become the more you are able to hear"* ~ Ram Dass
