## CVI Dash Dashboard 

Repository for developing the Dash implementation of our COVID-19 Community Vulnerability Index dashboard.

![Image of Map App](https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Visual%20Map%2007.07.png)

# Updates:
**Visual components:**
- Choropleth map of 3 primary scores (COVID severity, economic harm, and mobile health)
- Choropleth maps of all underlying variables in the base dataset (listed here)
- Bar graph of 10 counties with highest COVID case counts
- Select which scores and/or underlying variables they want the map to display

**Users can :**
- Adjust display area of the map
- Hover over a county on the map to see key statistics (county and state name, scores)
- Select a specific state and/or county (zoom to the location and display information)
- Choose multiple indicators to visualize at the same time

# Next steps:
- Legends for all choropleth maps
- List of highest scoring counties for each metric (can be a single list widget where you select which score to show)
- Side bar prominently displaying brief descriptions of each scores (including variables used to construct them) and instructions on how to use the dashboard)
- Users can see demographic information of a county on the hoverboard
- Users can find their current location and display score information
- Integrate all features described above into a single Dash dashboard instance that can be hosted elsewhere
- Host on a website

# Possible next steps
- Create our own CSS stylesheets for the website
