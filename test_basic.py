from scitech_lab import *

print("\n\nTesting data import function...")
filename = 'lla_data.csv'
df = load_data(filename)
print("\n DataFrame head...")
print(df.head())
print("\n DataFrame describe...")
print(df.describe())


print("\n\nTesting LLA to ECEF conversion function...")
lat = df.latitude
lon = df.longitude
alt = df.altitude
X,Y,Z = lla_to_ecef(lat,lon,alt)
print("\nX ECEF values [meters]: \n",X[:10])
print("\nY ECEF values [meters]: \n",Y[:10])
print("\nZ ECEF values [meters]: \n",Z[:10])


print("\n\nTesting velocity calculator function...")
V = cal_ecef_velocity(df.time,X,Y,Z)
print("\nVelocity ECEF values [meters/second]: \n",V[:10])


print("\n\nTesting interpolator function...")
for item in [1532334000,1532335268]:
    interpolate_src_velocity(df.time,V,item)