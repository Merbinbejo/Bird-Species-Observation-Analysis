USE bird_monitoring_data_db;
SELECT*FROM forest;
SELECT DISTINCT(Admin_Unit_Code) FROM forest;
SELECT DISTINCT(Site_Name) FROM forest
ORDER BY Site_Name ASC;
SELECT DISTINCT(Plot_Name) FROM forest;
SELECT DISTINCT(Common_Name),day,month,Location_Type
FROM forest
WHERE month=5 and day<10
UNION
SELECT DISTINCT(Common_Name),day,month,Location_Type
FROM grassland
WHERE month=5 and day<10
ORDER BY Location_Type ASC;

SELECT COUNT(DISTINCT Common_Name) AS "Total Number Of Species Observer in forest"
FROM grassland;

SELECT Observer, COUNT(Common_Name) AS Observation_Count
FROM forest
GROUP BY Observer
ORDER BY Observation_Count DESC;

SELECT Location_type,Humidity FROM forest
LIMIT 5
UNION
SELECT Location_type,Humidity FROM grassland
LIMIT 5;

SHOW COLUMNS FROM forest;

SELECT Common_Name,
       COUNT(*) AS Risk,
       Location_Type AS Location
FROM grassland
WHERE PIF_Watchlist_Status = TRUE
GROUP BY Common_Name, Location_Type

UNION

SELECT Common_Name,
       COUNT(*) AS Risk,
       Location_Type AS Location
FROM forest
WHERE PIF_Watchlist_Status = TRUE
GROUP BY Common_Name, Location_Type

ORDER BY Risk DESC;

SELECT Common_Name,
       COUNT(*) AS Risk
FROM forest
WHERE PIF_Watchlist_Status = TRUE
GROUP BY Common_Name;

SELECT Common_Name,
       COUNT(*) AS Count
FROM grassland
GROUP BY Common_Name
ORDER BY  Count DESC;