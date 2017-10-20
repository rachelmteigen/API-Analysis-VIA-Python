
# coding: utf-8

# In[229]:

import matplotlib.pyplot as plt
import requests as req
import pandas as pd
import json
import openweathermapy
import csv
api_key = "25bc90a1196e6f153eece0bc0b0fc9eb"
#api_key = "924783bda048569443e49dd6a03e5591"


# In[230]:

cities_pd = pd.read_csv("worldcities.csv")

# Preview the data
cities_pd.head()


# In[258]:

# # Counter

equator = equator[equator["Latitude"]
                              .astype(int) <= 30]
equator = cities_pd.sample(n=500)
equator.head()


# In[259]:

# # Counter

row_count = 1
# Generating 500 Unique Cities Names with Latitude and Longitude
for index, row in equator.iterrows():
    
    # Create endpoint URL
    #API call: api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}
    target_url = "http://api.openweathermap.org/data/2.5/weather?&units=imperial&lat=%s&lon=%s&appid=%s" % (row["Latitude"], row["Longitude"], api_key)
    city_name = req.get(target_url).json()
    
    
    
    # Print log to ensure loop is working correctly
    print("City #" + str(row_count))  
    print(city_name["name"])
    print(target_url)
    row_count += 1


# In[262]:

# Add columns for Temperature, Humidity, Cloudiness and Wind Speed

equator["Temperature"] = ""
equator["Humidity"] = ""
equator["Cloudiness"] = ""
equator["Wind Speed"] = ""
equator.head()


# In[264]:

# Filling in the Data for Columns Above
for index, row in equator.iterrows():
    lat = row["Latitude"]
    lng = row["Longitude"]
    
    #print(lat, lng, api_key)
    target_url = "http://api.openweathermap.org/data/2.5/weather?&units=imperial&lat=%s&lon=%s&appid=%s" % (row["Latitude"], row["Longitude"], api_key)
    #target_url = target_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&types=%s&rankby=distance&keyword=%s&key=%s" % (lat, lng, api_key)
    name_address = req.get(target_url).json()
    #print(json.dumps(name_address, indent=4, sort_keys=True))
    
    # Since some data may be missing we incorporate a try-except to skip any that are missing a data point.
    try:
        equator.set_value(index, "Temperature", name_address["main"]["temp"])
        equator.set_value(index, "Humidity", name_address["main"]["humidity"])
        equator.set_value(index, "Cloudiness", name_address["clouds"]["all"])
        equator.set_value(index, "Wind Speed", name_address["wind"]["speed"])
    
    except:
        print("Missing field... skipping.")


# In[265]:

# Save Data to csv
equator.to_csv("Equator_Output.csv")

# Visualize to confirm airport data appears
equator.head()


# In[270]:

# Build a scatter plot for each data type
plt.scatter(equator["Humidity"], 
            equator["Latitude"],
            s=100, edgecolor="black", c="slateblue", linewidths=1, marker="o", 
            alpha=0.8)

# Incorporate the other graph properties
plt.title("Latitude vs. Humidity %")
plt.ylabel("Latitude")
plt.xlabel("Humidity %")
plt.grid(True)

# Save the figure
#plt.savefig("output_analysis/Latitude_Humidity.png")

# Show plot
plt.show()


# In[267]:

# Build a scatter plot for each data type
plt.scatter(equator["Temperature"], 
            equator["Latitude"],
            s=100, edgecolor="black", linewidths=1, c="red", marker="o", 
            alpha=0.8)

# Incorporate the other graph properties
plt.title("Temperature vs. Latitude")
plt.ylabel("Latitude")
plt.xlabel("Temperature")
plt.grid(True)

# Save the figure
plt.savefig("Latitude_Temperature.png")

# Show plot
plt.show()


# In[269]:

# Build a scatter plot for each data type
plt.scatter(equator["Cloudiness"], 
            equator["Latitude"],
            s=100, edgecolor="black", linewidths=1, c="deeppink", marker="o", 
            alpha=0.8)

# Incorporate the other graph properties
plt.title("Cloudiness % vs. Latitude")
plt.ylabel("Latitude")
plt.xlabel("Cloudiness %")
plt.grid(True)

# Save the figure
plt.savefig("Cloudiness_Latitude.png")

# Show plot
plt.show()


# In[268]:

# Build a scatter plot for each data type
plt.scatter(equator["Wind Speed"], 
            equator["Latitude"],
             s=100, edgecolor="black", linewidths=1, c="indigo", marker="o", 
            alpha=0.8)

# Incorporate the other graph properties
plt.title("Wind Speed MPH vs. Latitude")
plt.ylabel("Latitude")
plt.xlabel("Wind Speed MPH")
plt.grid(True)

# Save the figure
plt.savefig("Wind Speed_Latitude.png")


# Show plot
plt.show()


# In[ ]:

# 3 Observations!
# 1) Obiviously, it is hot at the equator marked by Lat 0° but it is even more hot at Lat 30°. 
#This is where most of the world's deserts are located with some exceptions. Temperature spikes at 30°.
# 2) This leads to point #2 regarding humdidity back to Lat 30°: it's arid in deserts not humid. 
# 3) Observation more than 88% of cities are north Lat 0°. 
# 4) Wind speed is also less at Lat 30°

