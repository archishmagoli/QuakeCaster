# QuakeCaster Earthquake Simulator Project
## Background + About the Lab Experiment
The **QuakeCaster** is an interactive laboratory model that simulates **earthquakes** and **plate-boundary faults.** Current faculty members at Georgia Tech have historically used the model as a way to demonstrate in real-time the impact of earthquakes and strike-slip faults on the stability of the Earth's crust. 
- 🔴 **The Problem:** There was *constant human error* resulting from cranking a fishing reel (or winch), which was needed to pull the mass that, when slipped on the ground, would simulate the faults.
- 🟢 **Our Solution:** In order to *optimize the lab* for students and **gather useful data**, we decided to automate this lab setup and create a new model using **Arduino boards** and an interactive GUI created using Python's `tkinter` library.

[Here is our in-class presentation](https://docs.google.com/presentation/d/1PdBOjfu7RH4z4XNIv7g74CdangAlTY7koaaqGK-brsM/edit?usp=sharing), detailing our previous work and MVP result. 

I decided to **take this project further**, adding new enhancements to further enhance the usability of this model within the classroom. You can check out the new tools being added to the project in the **Features** section below!

## User Setup
- Clone this repository and run `bipolarDataSender\bipolarDataSender.exe` to start the GUI. From there, you have the required information to complete the lab.

## Developer Setup
- Install the following software: 
  - [Arduino IDE](https://www.arduino.cc/en/software) - required for Arduino + hardware integration.
  - Python (version `3.10.*` or above).
  - `tkinter` library (instructions [here](https://www.geeksforgeeks.org/how-to-install-tkinter-in-windows/)): required for GUI manipulation.
  - `matplotlib` library: required for data visualization.
  - `serial` library: required for sending and receiving serial input/output with the force sensor.
    - (`matplotlib` and `serial` can be installed through `pip` on the command line.)

## Main Features
- Ability to customize motor speed and direction of rotation.
- Live updation of force vs. time graph, based on values sent from the Vernier force sensor.
  - Additional user-facing controls for recording force vs. time graph data, including:
    - Pausing/resuming live updation.
    - Restarting data recording.
- Data export to CSV/Excel formats.

## Graphical User Interface (GUI)
<img width="674" alt="image" src="https://github.com/archishmagoli/QuakeCaster/blob/main/GUI%20-%20Final%20Product.png">

## Contributors
- ***Archie Goli (August 2022 - Present)***
- Reiden Webber (August 2022 - December 2022)
- Hayden Narey (August 2022 - December 2022)
