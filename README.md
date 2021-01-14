# Overview

This folder contains functions for to convert from LLA coordinate system to ECEF coordinates using Python. Position output checked against [Dept of Oceanography](https://www.oc.nps.edu/oc2902w/coord/llhxyz.htm).

# Requirements
The following packages were used.
```Python
python==3.6.4
numpy==1.19.4
scipy==1.5.1
pandas==1.1.2
```
and the data file must have headers: time,latitude,longitude,altitude. Please see any assumptions within the doc string.

# Quick Start
## Change File Extensions
If the file names have been changed to `.txt` then first change the names as follows. 
```bash
scitech_lab.txt --> scitech_lab.py
test_basic.txt --> test_basic.py
```
## Run Test
To run the test the following package requirements are needed. 

```Python
python==3.6.4
numpy==1.19.4
scipy==1.5.1
pandas==1.1.2
```
However, the test should work with any current versions. To run the test put all files in a common folder. From terminal change directory into said folder. From terminal run `test_basic.py`. Example below for MacOSX.

```bash
$ mkdir folder
$ cd folder
$ python test_basic.py
```

### Virtual Environment

#### MacOX

Virtual environment setup using `virtualenv`.
```bash
$ mkdir folder
$ cd folder
$ virtualenv --python=/usr/local/bin/python3.6 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python test_basic.py
```

# Functions
In the `scitech_lab.py` file there are five functions. 

### [1] load_data(filename)
```python
This function reads .csv using pandas

    Assumptions:
        - file is .csv
        - file has the following column names
            1. time
            2. latitude
            3. longitude
            4. altitude
        - file has LLA input type
        - file has 
            1. Time since Unix epoch [seconds]
            2. WGS84 Latitude [degrees]
            3. WGS84 Longitude [degrees]
            4. WGS84 Altitude [kilometers]

    Args:
        filename [string]: path to .csv file as string
                           Example: 'filename.csv'
                           Example: 'path/to/folder/filename.csv'

    Returns:
        df [pandas DataFrame]: filename is imported and returned as 
                 with         pandas DataFrame
```



### [2] lla_to_ecef(lat,lon,alt)
 ```python
    This function takes in WGS84 latitude, longitude, and altitude 
       from LLA coordinate system and converts to ECEF coordinate system

    Args:
        lat [pandas.core.series.Series]: WGS84 Latitude [degrees]
                                         Example: df.latitude
        lon [pandas.core.series.Series]: WGS84 Longitude [degrees]
                                         Example: df.longitude
        alt [pandas.core.series.Series]: WGS84 Altitude [kilometers]
                                         Example: df.altitude

    Returns:
       X [pandas.core.series.Series]: ECEF x-coordinate [meters]
       Y [pandas.core.series.Series]: ECEF y-coordinate [meters]
       Z [pandas.core.series.Series]: ECEF z-coordinate [meters]
``` 
    

### [3] cal_ecef_velocity(t,x,y,z)
```python
    This function calculates the velocity vector from ECEF position

    Args:
        t (1D, pandas.core.series.Series): WGS84 time [seconds]
                                            Example: df.time
        x (1D, pandas.core.series.Series): ECEF x-coordinate [meters]
        y (1D, pandas.core.series.Series): ECEF y-coordinate [meters]
        z (1D, pandas.core.series.Series): ECEF z-coordinate [meters]

    Returns:
        v [numpy.ndarray]: ECEF velocity [meters/second]
```
             


### [4] interpolate_src_velocity(time,velocity,time_request)
```python
    This function interpolates velocity

    Args:
        time [1D, pandas.core.series.Series]: WGS84 time [seconds]
                                            Example: df.time
        velocity [numpy.ndarray]: ECEF velocity [meters/second]
        time_request ([type]): time requested for interpolation
                               time expected in Unix seconds between    
                               time(start) and time(end)
                               Example: time(start)=1532332859
                               Example: time(end)=1532335359

    Returns:
        print() [string]: interpolated velocity for time_request
                        Example: Velocity(time=1532334000seconds) 
                                                = 1389.4745700513633 m/s
        stdout [.txt]: text file with the above output appended
```



### [5] interpolate_new_velocity(filename,time_request)
```python
Function to interpolate new data from file

Args:
    filename [string]: path to .csv file as string
                    Example: 'filename.csv'
                    Example: 'path/to/folder/filename.csv'
    time_request ([type]): time requested for interpolation
                           time expected in Unix seconds between    
                           time(start) and time(end)
                           Example: time(start)=1532332859
                           Example: time(end)=1532335359

Returns:
    print() [string]: interpolated velocity for time_request
                    Example: Velocity(time=1532334000seconds) 
                                            = 1389.4745700513633 m/s
    stdout [.txt]: text file with the above output appended
```

# Test - Basic

Included is a basic test of the data, which has been renamed to 'lla_data.csv'. 

Change directories into the folder with `test_basic.py` and `scitec_lab.py`. Run the test from the terminal by 

```bash
$ cd folder/with/pyfiles
$ python test_basic.py
```
The output should return the following.

```bash
Testing data import function...

 DataFrame head...
         time  latitude  longitude  altitude
0  1532332859  40.33990  127.51010   0.50000
1  1532332864  40.27902  127.51786  21.28817
2  1532332869  40.21822  127.52562  41.99302
3  1532332874  40.15751  127.53337  62.61454
4  1532332879  40.09687  127.54113  83.15275

 DataFrame describe...
               time    latitude   longitude     altitude
count  5.010000e+02  501.000000  501.000000   501.000000
mean   1.532334e+09   28.486670  129.320156  1732.680972
std    7.238525e+02    5.937824    1.010894   780.198986
min    1.532333e+09   20.000000  127.510100     0.000000
25%    1.532333e+09   23.187490  128.455970  1131.802220
50%    1.532334e+09   27.639970  129.352900  1953.015630
75%    1.532335e+09   33.357440  130.200920  2438.812010
max    1.532335e+09   40.339900  131.000000  2604.104170


Testing LLA to ECEF conversion function...

X ECEF values [meters]: 
 0   -2.964584e+06
1   -2.977429e+06
2   -2.990250e+06
3   -3.003046e+06
4   -3.015819e+06
5   -3.028566e+06
6   -3.041288e+06
7   -3.053985e+06
8   -3.066657e+06
9   -3.079304e+06
dtype: float64

Y ECEF values [meters]: 
 0    3.862111e+06
1    3.877758e+06
2    3.893364e+06
3    3.908930e+06
4    3.924455e+06
5    3.939941e+06
6    3.955384e+06
7    3.970787e+06
8    3.986149e+06
9    4.001469e+06
dtype: float64

Z ECEF values [meters]: 
 0    4.107149e+06
1    4.115433e+06
2    4.123632e+06
3    4.131747e+06
4    4.139776e+06
5    4.147721e+06
6    4.155582e+06
7    4.163360e+06
8    4.171052e+06
9    4.178662e+06
dtype: float64


Testing velocity calculator function...

Velocity ECEF values [meters/second]: 
 [   0.         4374.65790201 4359.6517096  4344.57284567 4329.65298721
 4314.64593199 4299.59338515 4284.60204114 4269.69575387 4254.64606692]


Testing interpolator function...

Velocity(time=1532334000seconds) = 1389.4745700513633 m/s


Velocity(time=1532335268seconds) = 3891.4336413608644 m/s
```

There should also be a text file `stdout.txt` in the same directory with the two above velocity interpolation outputs.

# Usage

to use `scitec_lab.py` in your own `.py` file import the library while in the same folder as follows.

```python
from scitec_lab import *
```

This will import all methods listed above. To test the interpolation method on new file.

```python
from scitec_lab import *

filename = 'path/to/data.csv'
time_request = 1532334000
interpolate_new_velocity(filename,time_request)
```

