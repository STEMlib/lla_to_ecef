# Author: Brandon Touchet <touchetbrandon@gmail.com>
#   Date:  January 6, 2021

import pandas as pd
import numpy as np

from scipy.interpolate import interp1d


def load_data(filename):
    """This function reads .csv using pandas

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
    """
    df = pd.read_csv(filename)
    return df


def lla_to_ecef(lat,lon,alt):
    """This function takes in WGS84 latitude, longitude, and altitude 
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
    """    
    # convert lat and long from degrees to radians because numpy expects 
    # radians for trig functions
    deg_2_rads = np.pi/180
    lat = deg_2_rads*lat
    lon = deg_2_rads*lon    
    
    # convert altitude from kilometers to meters
    alt = 1000*alt    
    
    # convert LLA to ECEF with the following equations
    cos_lat = np.cos(lat)
    cos_lon = np.cos(lon)
    sin_lat = np.sin(lat)

    A = 6378137
    B = 6356752.31424518
    H = alt
    E1 = np.sqrt((A**2-B**2)/A**2)
    E2 = E1**2
    N = A/np.sqrt(1-E2*(sin_lat**2))

    X = (N+H)*cos_lat*cos_lon
    Y = (N+H)*cos_lat*np.sin(lon)
    Z = (N*(1-E2)+H)*sin_lat
    
    return X,Y,Z
    

def cal_ecef_velocity(t,x,y,z):
    """This function calculates the velocity vector from ECEF position

    Args:
        t (1D, pandas.core.series.Series): WGS84 time [seconds]
                                           Example: df.time
        x (1D, pandas.core.series.Series): ECEF x-coordinate [meters]
        y (1D, pandas.core.series.Series): ECEF y-coordinate [meters]
        z (1D, pandas.core.series.Series): ECEF z-coordinate [meters]

    Returns:
        v [numpy.ndarray]: ECEF velocity [meters/second]
    """     
    def calc_velocity(time,position):
        """Calculates the velocity from ECEF position components
           (e.g. Vx, Vy, Vz)
        """
        n = len(position)
        v = np.zeros(n)        
        for i in range(1,len(position)):
            v[i] = (position[i]-position[i-1])/(time[i]-time[i-1])
        return v
    
    v_xyz = [] # empty array to append velocity components
    items = [x,y,z] # put positional components into array for looping
    
    for item in items:
        v_xyz.append(calc_velocity(t,item))
    
    # calculate RMS of velocity components
    # velocity = SQRT(Vx**2+Vy**2+Vz**2)
    v = np.sqrt(v_xyz[0]**2+v_xyz[1]**2+v_xyz[2]**2)    
    
    return v
    


def interpolate_src_velocity(time,velocity,time_request): 
    """This function interpolates velocity

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
        print(output) [string]: interpolated velocity for time_request
                          Example: Velocity(time=1532334000seconds) 
                                                = 1389.4745700513633 m/s
        stdout [.txt]: text file with the above output appended
        
    """
    f = interp1d(time, velocity)
    output = '\nVelocity(time=' + str(time_request) + 'seconds) = '+ str(f(time_request).item()) + ' m/s\n'

    file = open('stdout.txt', 'a')
    file.write(output)
    file.close()

    return print(output)


def interpolate_new_velocity(filename,time_request):
    """Function to interpolate new data from file

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
    """
    # import data
    df = load_data(filename)

    # assign variables for LLA-to-ECEF conversion
    lat = df.latitude
    lon = df.longitude
    alt = df.altitude    
    X,Y,Z = lla_to_ecef(lat,lon,alt) # execute LLA-to-ECEF conversion

    # calculate velocity from ECEF positions
    V = cal_ecef_velocity(df.time,X,Y,Z)

    # interpolate velocity for given time
    f = interp1d(df.time, V)
    output = '\nVelocity(time=' + str(time_request) + 'seconds) = '+ str(f(time_request).item()) + ' m/s\n'

    file = open('stdout.txt', 'a')
    file.write(output)
    file.close()

    return print(output)