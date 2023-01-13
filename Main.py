import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit_folium import folium_static
import folium
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

st.set_page_config(
    page_title="Laundry Data Visualization"
)

def dfMonthCount(df, colName):
    resDF = pd.DataFrame()
    for c in df[colName].unique():
        tmpSeries = df[df[colName] == c].groupby("MonthYear").size()
        tmpDF = pd.DataFrame(tmpSeries)
        tmpDF.reset_index(inplace=True)
        tmpDF["Type"] = c
        tmpDF.rename(columns={0:"Count", "MonthYear":"Date"}, inplace=True)
        resDF = pd.concat([resDF, tmpDF], ignore_index=True)  
    
    return resDF

df = pd.read_csv("visualize_data.csv")
df['Datetime'] = pd.to_datetime(df['Formatted_Date'] + ' ' + df['Time'])
df["MonthYear"] = pd.to_datetime(df["Datetime"].apply(lambda x : x.strftime("%Y-%m")))
df["FormattedMonthYear"] = df["Datetime"].apply(lambda x : x.strftime("%B, %Y"))

st.title("Laundry Data Visualization ")


### LINEPLOT BEGIN
st.header("Lineplot Visualization")

#Total Customer and Avg Spent Row
col1, col2 = st.columns(2)

#Total Customer in Month Column
col1.subheader("Total Customers by month")
dfTotalCustMonth = pd.DataFrame(df.groupby("MonthYear").size()).reset_index()
dfTotalCustMonth.rename(columns={0:"Count"}, inplace=True)
dfTotalCustMonth["MY_Str"] = dfTotalCustMonth["MonthYear"].apply(lambda x: x.strftime("%Y-%m"))

chart = alt.Chart(dfTotalCustMonth).mark_line().encode(
    x = alt.X("MY_Str", title="Month"),
    y = alt.Y("Count", title="Total Customers"),
).interactive()
col1.altair_chart(chart, use_container_width=True)

#Average Total Spent in Month Column
col2.subheader("Mean Total Spent by month")

dfAvgSpentMonth = df.groupby("MonthYear").mean().reset_index()
dfAvgSpentMonth["MY_Str"] = dfAvgSpentMonth["MonthYear"].apply(lambda x: x.strftime("%Y-%m"))

chart = alt.Chart(dfAvgSpentMonth).mark_line().encode(
    x = alt.X("MY_Str", title="Month"),
    y = alt.Y("TotalSpent_RM", title="Average Total Spent (RM)"),
).interactive()
col2.altair_chart(chart, use_container_width=True)


#Dryer and Washer Row
col1, col2 = st.columns(2)

#Washer in Month Column
col1.subheader("Washer No. Usage by month")

dfWasherMonth = dfMonthCount(df, "Washer_No")
dfWasherMonth["Type"] = dfWasherMonth["Type"].astype("category")
dfWasherMonth["MY_Str"] = dfWasherMonth["Date"].apply(lambda x: x.strftime("%Y-%m"))

chart = alt.Chart(dfWasherMonth).mark_line().encode(
    x = alt.X("MY_Str", title="Month"),
    y = alt.Y("Count", title="Washer Count"),
    color=alt.Color("Type", title="Washer No. ")
).interactive()
col1.altair_chart(chart, use_container_width=True)

#Dryer in Month Column
col2.subheader("Dryer No. Usage by month")

dfDryerMonth = dfMonthCount(df, "Dryer_No")
dfDryerMonth["Type"] = dfDryerMonth["Type"].astype("category")
dfDryerMonth["MY_Str"] = dfDryerMonth["Date"].apply(lambda x: x.strftime("%Y-%m"))

chart = alt.Chart(dfDryerMonth).mark_line().encode(
    x = alt.X("MY_Str", title="Month"),
    y = alt.Y("Count", title="Dryer Count"),
    color=alt.Color("Type", title="Dryer No. ")
).interactive()
col2.altair_chart(chart, use_container_width=True)


st.markdown("""---""")
### LINEPLOT END

### MAP PLOT BEGIN
selectMonth = st.selectbox("Please pick a month: ", ["All"] + list(df["FormattedMonthYear"].unique()))

headerStr = "Total Spent by city "
if selectMonth != "All":
    headerStr += "on " + selectMonth
    dfPivot = df[df["FormattedMonthYear"] == selectMonth]
else:
    dfPivot = df
st.header(headerStr)

dfPivotCityMean = dfPivot.groupby("City").mean()
dfPivotCitySum = dfPivot.groupby("City").sum()

southWest = (df["latitude"].min(), df["longitude"].min())
northEast = (df["latitude"].max(), df["longitude"].max())

m = folium.Map()
m.fit_bounds([southWest, northEast])

choropleth = folium.Choropleth(
    geo_data="geojson.json",
    data = dfPivotCitySum.reset_index(),
    columns = ["City", "TotalSpent_RM"],
    key_on='feature.properties.name',
    fill_color = 'BuPu',
    fill_opacity = 0.8,
    nan_fill_color="#edf3f5",
    nan_fill_opacity=0.5,
    line_opacity = 0.2,
    legend_name = 'Total Spent (RM)', 
    highlight = True
).add_to(m)


totalCountData = []
for row in choropleth.geojson.data["features"]:
    tmp = dict()

    rPRef = row["properties"]
    loc = rPRef["name"]
    tmp["City"] = loc

    if not loc in dfPivot["City"].unique():
        tmp["Total Customers"] = 0
        tmp["Average Total Spent"] = "RM0"
        tmp["Total Spent"] = "RM0"
    else:
        tmp["Total Customers"] = len(dfPivot[dfPivot["City"] == loc])

        val = dfPivotCityMean.loc[loc, "TotalSpent_RM"]
        tmp["Average Total Spent"] = "RM" + str(round(val, 4))

        val = dfPivotCitySum.loc[loc, "TotalSpent_RM"]
        tmp["Total Spent"] = "RM" + str(round(val, 4))

    rPRef.update(tmp)
    totalCountData.append(tmp)

folium.GeoJsonTooltip(
    ['City', 'Total Customers', 'Average Total Spent', 'Total Spent']
    ).add_to(choropleth.geojson)

mappu = folium_static(m)

fileName = "TotalSpent" 
if selectMonth != "All":
    fileName += selectMonth.replace(", ", "")
csv = pd.DataFrame(totalCountData).to_csv(index=False).encode('utf-8')

st.download_button(
   "Export Total Spent Data to CSV",
   csv,
   fileName + ".csv",
   "text/csv",
   key='download-csv'
)

### MAP PLOT END


