# Bird-Species-Observation-Analysis
A data-driven project focused on analyzing bird species observations from ecological survey datasets. This analysis aims to uncover patterns in bird populations, migration trends, and regional biodiversity using Python Mysql and data visualization tools.
Features
      1.Cleaning and preprocessing bird observation data

      2.Statistical summaries of species count and diversity

      3.Visualizations of bird sightings over time and regions

      4.Filtering by species, location, season, or observer effort

      5.Insights into rare species and migration hotspots

Tools & Technologies
    *Python (Pandas, NumPy, Matplotlib, Seaborn)

    *Jupyter Notebooks

    *Streamlit (optional for interactive dashboards)

    *CSV/Excel observation datasets (e.g., eBird, local surveys)

DATASET
  1. Admin_Unit_Code: The code for the administrative unit (e.g., "ANTI") where the observation was conducted.
  2. Sub_Unit_Code: The sub-unit within the administrative unit for further classification.
  3. Site_Name: The name of the specific observation site within the unit.
  4. Plot_Name: A unique identifier for the specific plot where observations were recorded.
  5. Location_Type: The habitat type of the observation area (e.g., "Forest").
  6. Year: The year in which the observation took place.
  7. Date: The exact date of the observation.
  8. Start_Time: The start time of the observation session.
  9. End_Time: The end time of the observation session.
  10. Observer: The individual who conducted the observation.
  11. Visit: The count of visits made to the same observation site or plot.
  12. Interval_Length: The duration of the observation interval (e.g., "0-2.5 min").
  13. ID_Method: The method used to identify the species (e.g., "Singing," "Calling," "Visualization").
  14. Distance: The distance of the observed species from the observer (e.g., "<= 50 Meters").
  15. Flyover_Observed: Indicates whether the bird was observed flying overhead (TRUE/FALSE).
  16. Sex: The sex of the observed bird (e.g., Male, Female, Undetermined).
  17. Common_Name: The common name of the observed bird species (e.g., "Eastern Towhee").
  18. Scientific_Name: The scientific name of the observed bird species (e.g., Pipilo erythrophthalmus).
  19. AcceptedTSN: The Taxonomic Serial Number for the observed species.
  20. NPSTaxonCode: A unique code assigned to the taxon of the species.
  21. AOU_Code: The American Ornithological Union code for the species.
  22. PIF_Watchlist_Status: Indicates whether the species is on the Partners in Flight Watchlist (e.g., "TRUE" for at-risk species).
  23. Regional_Stewardship_Status: Denotes the conservation priority within the region (TRUE/FALSE).
  24. Temperature: The temperature recorded at the time of observation (in degrees).
  25. Humidity: The humidity percentage recorded at the time of observation.
  26. Sky: The sky condition during the observation (e.g., "Cloudy/Overcast").
  27. Wind: The wind condition (e.g., "Calm (< 1 mph) smoke rises vertically").
  28. Disturbance: Notes any disturbances that could affect the observation (e.g., "No effect on count").
  29. Initial_Three_Min_Cnt: The count of the species observed in the first three minutes of the session.
