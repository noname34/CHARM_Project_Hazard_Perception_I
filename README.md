Project name
=============

Basic information
---------------

- **Student** : Kevin Bürgisser - kevin.buergisser@edu.hefr.ch
- **Supervisors** : Pierre Kuonen, Beat Wolf, Jean Hennebert
- **Dates** : 19.02.2020 to 13.05.2020


Overview
--------
Today, cars are nearly autonomous due to advanced driver assistance systems for safe driving which offer numerous features such as cruise control, emergency breaking, traffic signs recognition, etc. This is possible thanks to the use of cameras, sensors and other devices which focus on perceiving the surrounding environment. These features enable the vehicle to take control during potentially unsafe situations and prepare for any corrective measures such as automatic maneuvering to avoid collision, slowdown and breaking.
This project was proposed by Edge Hill University (UK) as part of the project CHARM (Context-aware Human Activity Recognition and Monitoring for intelligent vehicles), an international project regrouping experts from Indian and British leading universities to predict driver distraction. The project aims to better understand hazard perception in the context of autonomous vehicle, propose an approach to detect hazards happening around the vehicle and implement a first prototype.

Usage
--------
1. First download project

2. Get prototype v0 or v1 and launch the script.\
Note: The environment variable IGNORE_3D=True before lauching the scripts!
- Prototype v0: inter-vehicle distance\
Run python script at ps6_hazard_detection/src/features/prototype_v0/main.py\
Then check log alerts at ps6_hazard_detection/reports/alerts/distance_checker v0.csv

- Prototype v1: trajectories prediction\
Run python script at ps6_hazard_detection/src/features/prototype_v1/main.py\
Then check log alerts at ps6_hazard_detection/reports/alerts/trajectories prediction v1.\

Note: The dataset is confidential and I am therefore not able to share it on this repository.


Licence
-------
The MIT License (MIT)
Copyright (c) 2020, kevin bürgisser

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
