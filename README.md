## CVI Dash Dashboard 

Repository for developing the Dash implementation of our COVID-19 Community Vulnerability Index dashboard.

![Image of Map App](/App&#32;Visualization/Complete&#32;App&#32;08.06.png)

Full Design Mock-up of the app can be found [here](https://github.com/community-insight-impact/dash_cvi_dashboard/blob/master/App%20Visualization/Dash%20Design%20Mock%20Ups%20CVI%20Dashboard.pdf)

# Updates:
**Visual components:**
- Choropleth map of 3 primary scores (COVID severity, economic harm, and mobile health)
- Choropleth maps of all underlying variables in the base dataset (listed here)
- Bar graph of 10 counties with highest COVID case counts
- Select which scores and/or underlying variables they want the map to display
- Legends for all choropleth maps

**Users can :**
- Adjust display area of the map
- Hover over a county on the map to see key statistics (county and state name, scores)
- Select a specific state and/or county (zoom to the location and display information)
- Choose multiple indicators to visualize at the same time
- List of highest scoring counties for each metric (can be a single list widget where you select which score to show)
- Side bar prominently displaying brief descriptions of each scores (including variables used to construct them) and instructions on how to use the dashboard)

# Next steps:
- Users can see demographic information of a county on the hoverboard
- Users can find their current location and display score information
- Integrate all features described above into a single Dash dashboard instance that can be hosted elsewhere
- Host on a website

# Possible next steps
- Create our own CSS stylesheets for the website
