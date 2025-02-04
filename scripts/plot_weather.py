import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, datetime
import botocore.session
import s3fs

session = botocore.session.get_session()
AWS_SECRET = session.get_credentials().secret_key
AWS_ACCESS_KEY = session.get_credentials().access_key 

s3 = s3fs.S3FileSystem(anon=False, key=AWS_ACCESS_KEY, secret=AWS_SECRET)

today = date.today()
today = date.today()
current_year = datetime.now().year
lake_name = "nj_woodcliff_lake"

lst_ = []
for year_ in range(2010, current_year + 1):
	print(year_)
	df = pd.read_csv(f"s3://cwa-assets/{lake_name}/assets/weather_tab/{lake_name}_gridmet_{year_}.csv", parse_dates=["date"])
	lst_.append(df)

data = pd.concat(lst_)
today = date.today()

data = data.drop_duplicates().reset_index(drop=True)



### CUMSUM WEATHER ###
#path = "./Data/or_detroit_lake_dashboard/proc_dashboard_data/"
# path = "/tmp/nj_woodcliff_lake_dashboard/proc_dashboard_data/"
# pwd = path+"weather_tab/"
#data = pd.read_csv(pwd + "or_detroit_lake_gridmet.csv",parse_dates=["date"])
# data = pd.read_csv(pwd + "nj_woodcliff_lake_gridmet.csv",parse_dates=["date"])


#files = glob.glob("./Data/proc_dashboard_data/weather_tab/*.csv")
#data = pd.read_csv(files[0],parse_dates=["date"])
data["month"] = data["date"].dt.month
data["week"] = data["date"].dt.week
data["year"] = data["date"].dt.year
data['dayofyear'] = data['date'].dt.dayofyear

#! Length of timeseries
T = len(data["year"].unique())

#! assume 1 location
loc = pd.unique(data['lat'])[0]
data = data[data["lat"]==loc]

#! Today
d1 = int(today.strftime("%d/%m/%Y")[-4:])
d2 = d1 - 1

#! Group by week to get the climatology (excluding this year)
climat = data[data["year"]!=d1]
climat = data.groupby(data["dayofyear"]).mean()


################! Plot temp !################
fig, axs = plt.subplots(figsize=(8, 4.5))

sns.lineplot(x="dayofyear", y="Air_Temp_cumsum",hue="year", data=data[data["year"]!=d1],
        palette=sns.color_palette('Greys', as_cmap = True))

# Plot the temperature data for the year 2023 (or any other specific year)
sns.lineplot(x="dayofyear", y="Air_Temp_cumsum", hue="year",
             data=data[data["year"] == d2], palette=['orange'])

cl = sns.lineplot(x="dayofyear", y="Air_Temp_cumsum", 
        data=climat, linewidth=3, color="#FFBF00", label="Average")

nw = sns.lineplot(x="dayofyear", y="Air_Temp_cumsum",hue="year", 
        data=data[data["year"]==d1], palette=['red'], linewidth=3)




plt.legend(frameon=False)
plt.plot(data.iloc[-1]["dayofyear"], data.iloc[-1]["Air_Temp_cumsum"],'r.',ms=20)
plt.xlabel("Time of year")
plt.ylabel("Cumulative temperature (degC)")
tics = np.arange(15,365,30)
labs = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
plt.xticks(tics,labs)

#! Set xlim to now
xmin = 1
xmax = 365
axs.set_xlim(xmin,xmax)

#! Save
plt.tight_layout()
plt.savefig("./Figs/Fig_temp_cumsum.png",dpi=600)




################! Plot temp !################
fig, axs = plt.subplots(figsize=(8, 4.5))

sns.lineplot(x="dayofyear", y="Precip_cumsum",hue="year", data=data[data["year"]!=d1],
        palette=sns.color_palette('Greys', as_cmap = True))

# Plot the temperature data for the year 2023 (or any other specific year)
sns.lineplot(x="dayofyear", y="Precip_cumsum", hue="year",
             data=data[data["year"] == d2], palette=['orange'])

cl = sns.lineplot(x="dayofyear", y="Precip_cumsum", 
        data=climat, linewidth=3, color="#FFBF00", label="Average")

nw = sns.lineplot(x="dayofyear", y="Precip_cumsum",hue="year", 
        data=data[data["year"]==d1], palette=['red'], linewidth=3)

plt.legend(frameon=False)
plt.plot(data.iloc[-1]["dayofyear"], data.iloc[-1]["Precip_cumsum"],'r.',ms=20)
plt.xlabel("Time of year")
plt.ylabel("Cumulative Precipitation (mm)")
tics = np.arange(15,365,30)
labs = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
plt.xticks(tics,labs)

#! Set xlim to now
xmin = 1
xmax = 365
axs.set_xlim(xmin,xmax)

#! Save
plt.tight_layout()
plt.savefig("./Figs/Fig_precip_cumsum.png",dpi=600)








