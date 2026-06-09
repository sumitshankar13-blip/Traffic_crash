import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
#making connection to mysql database
engine=create_engine('mysql+pymysql://root:Sumit123%40%40@localhost:3306/ccrashtable') 
 # Ensure this matches the database created in Phase 1
st.title("Traffic Crash Analytics & Safety Intelligence Platform")
option =st.selectbox('select Assembly', [
    '1.Find the top 5 most dangerous combinations of weather and crash type based on total crashes',
    '2.Identify the top 10 streets with the highest number of crashes and their corresponding severity scores',
    '3.Find the percentage of crashes that resulted in injuries for each crash type. ',
    '4.Determine the peak crash hour for each month.',
    '5.Identify the top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18). ',
    '6.Compare average number of injuries in daylight vs darkness conditions. ',
    '7.Find which traffic control device type has the highest average injuries per crash. ',
    '8.Identify the top 5 locations (latitude/longitude) with the highest crash frequency. ',
    '9.Find the top 5 streets with the highest injury rate, considering only streets with more than 100 crashes. ',
    '10.For each year, identify the most common crash type. ',
    '11.Find the day of the week with the highest average crashes per hour. ',
    '12.Identify high-risk time slots: Group hours into buckets (Morning, Afternoon, Evening, Night) Find which bucket has the highest injury crashes',
    '13.Find the top 3 contributing causes for each crash type. (Use window functions like ROW_NUMBER() or RANK())',
    '14.Calculate the year-over-year growth rate of crashes.(Use LAG() window function)',
    '15. Identify hotspot zones:Group nearby locations (round latitude & longitude to 2 decimal places)Find top 10 zones with highest crashes.'

])
st.write('You selected:', option)


qry_1 ="""   SELECT 
            WEATHER_CONDITION, FIRST_CRASH_TYPE, COUNT(*) AS TotalCrashes 
            FROM CrashTable 
            GROUP BY 1, 2 
            ORDER BY TotalCrashes DESC 
            LIMIT 5;"""
if option == "1.Find the top 5 most dangerous combinations of weather and crash type based on total crashes":
    df = pd.read_sql(qry_1, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: This analysis shows the highest-risk scenarios,
              such as 'Clear/Rear End' crashes being the most frequent,
              suggesting the need for awareness campaigns targeting following distance even in good weather.**_''')
    st.subheader("Top 5 Most Dangerous Weather and Crash Type Combinations")
    fig=px.bar(df, y='TotalCrashes', x='WEATHER_CONDITION', color='FIRST_CRASH_TYPE',barmode='group',
               title='Top 5 Most Dangerous Weather and Crash Type Combinations',
               labels={'TotalCrashes': 'Total Crashes','WEATHER_CONDITION': 'Weather Condition'})
    st.plotly_chart(fig)



qry_2 ="""  SELECT STREET_NAME, SUM(INJURIES_TOTAL) AS TotalInjuries 
            FROM CrashTable 
            GROUP BY STREET_NAME 
            ORDER BY TotalInjuries DESC 
            LIMIT 10;"""
if option == "2.Identify the top 10 streets with the highest number of crashes and their corresponding severity scores":
    df = pd.read_sql(qry_2, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Highlighting these streets is crucial for urban planning to redesign
              or increase patrol presence in these critical injury zones.**_''')


qry_3 ="""      
            SELECT
            FIRST_CRASH_TYPE,
            (CAST(SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) AS REAL) * 100.0) / COUNT(*) AS InjuryCrashPercentage
            FROM CrashTable
            GROUP BY FIRST_CRASH_TYPE
            ORDER BY InjuryCrashPercentage DESC;"""
if option == "3.Find the percentage of crashes that resulted in injuries for each crash type. ":
    df = pd.read_sql(qry_3, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Crash types with the highest injury percentages (e.g., Head-On collisions) 
             should be prioritized for injury prevention studies and improved vehicle safety standards.**_''')


qry_4 ="""      
            WITH MonthlyCrashes AS (
                SELECT
                    CRASH_MONTH,
                    CRASH_HOUR,
                    COUNT(CRASH_RECORD_ID) AS TotalCrashes
                FROM CrashTable
                GROUP BY CRASH_MONTH, CRASH_HOUR
            ),
            RankedCrashes AS (
                SELECT
                    CRASH_MONTH,
                    CRASH_HOUR,
                    TotalCrashes,
                    RANK() OVER (PARTITION BY CRASH_MONTH ORDER BY TotalCrashes DESC) AS hour_rank
                FROM MonthlyCrashes
            )
            SELECT
                CRASH_MONTH,
                CRASH_HOUR AS PeakCrashHour,
                TotalCrashes
            FROM RankedCrashes
            WHERE hour_rank = 1
            ORDER BY CRASH_MONTH;"""
if option == "4.Determine the peak crash hour for each month.":
    df = pd.read_sql(qry_4, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: This seasonal time analysis helps police and emergency services 
             allocate resources and manage traffic during the busiest hours of specific months,
              anticipating changing patternsh,**_''')
    

qry_5 ="""SELECT
          PRIM_CONTRIBUTORY_CAUSE,
          COUNT(*) AS Total_Crashes
          FROM CrashTable
          WHERE CRASH_HOUR >= 18
          GROUP BY PRIM_CONTRIBUTORY_CAUSE
          ORDER BY Total_Crashes DESC
          LIMIT 5;"""
if option == "5.Identify the top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18). ":
    df = pd.read_sql(qry_5, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Knowing the top causes after dark (e.g., 'Failure to Reduce Speed')
              allows for targeted night-time enforcement and increased driver vigilance awareness.**_''')


qry_6 ="""SELECT
          CASE
          WHEN LIGHTING_CONDITION = 'DAYLIGHT' THEN 'Daylight'
          WHEN LIGHTING_CONDITION LIKE 'DARKNESS%%' THEN 'Darkness'
          ELSE 'Other/Unknown'
          END AS Lighting_Condition_Group,
          AVG(INJURIES_TOTAL) AS Average_Injuries
          FROM CrashTable
          GROUP BY 1
          HAVING Lighting_Condition_Group IN ('Daylight', 'Darkness');"""
if option == "6.Compare average number of injuries in daylight vs darkness conditions. ":
    df = pd.read_sql(qry_6, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: If the average injury count is higher in darkness, 
             it supports policy decisions for better street lighting infrastructure investment.**_'''),



qry_7 ="""SELECT
          TRAFFIC_CONTROL_DEVICE,
          AVG(INJURIES_TOTAL) AS average_Injuries_Per_Crash
          FROM CrashTable
          GROUP BY TRAFFIC_CONTROL_DEVICE
          ORDER BY average_Injuries_Per_Crash DESC
          LIMIT 1;"""
if option == "7.Find which traffic control device type has the highest average injuries per crash. ":
    df = pd.read_sql(qry_7, engine)
    st.dataframe(df)    
    st.write('''_**INSIGHT: Identifying a device type associated with high injury rates suggests a potential flaw
              in its design or placement, necessitating immediate safety review.**_''')



qry_8 ="""SELECT
          LATITUDE,
          LONGITUDE,
          COUNT(*) AS CrashFrequency
          FROM CrashTable
          WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
          GROUP BY LATITUDE, LONGITUDE
          ORDER BY CrashFrequency DESC
          LIMIT 5;"""
if option == "8.Identify the top 5 locations (latitude/longitude) with the highest crash frequency. ":
    df = pd.read_sql(qry_8, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: These specific GPS coordinates are persistent micro-hotspots that need immediate,
              site-specific engineering intervention, such as adding turn lanes or signals.**_''')



qry_9 ="""SELECT
          STREET_NAME,
          (CAST(SUM(INJURIES_TOTAL) AS REAL) / COUNT(*)) AS InjuryRate,
          COUNT(*) AS TotalCrashes
          FROM CrashTable
          GROUP BY STREET_NAME
          HAVING TotalCrashes > 100
          ORDER BY InjuryRate DESC
          LIMIT 5;"""
if option == "9.Find the top 5 streets with the highest injury rate, considering only streets with more than 100 crashes. ":
    df = pd.read_sql(qry_9, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Prioritizing based on injury rate (severity) rather than just volume ensures resources
              address the streets where crashes are most likely to cause harm.**_''')


qry_10 ="""            WITH YearCrashTypeCounts AS (
                SELECT
                    year,
                    FIRST_CRASH_TYPE,
                    COUNT(CRASH_RECORD_ID) AS TypeCount
                FROM CrashTable
                GROUP BY year, FIRST_CRASH_TYPE
            ),
            RankedCrashTypes AS (
                SELECT
                    year,
                    FIRST_CRASH_TYPE,
                    TypeCount,
                    RANK() OVER (PARTITION BY year ORDER BY TypeCount DESC) AS type_rank
                FROM YearCrashTypeCounts
            )
            SELECT
                year,
                FIRST_CRASH_TYPE AS MostCommonCrashType,
                TypeCount
            FROM RankedCrashTypes
            WHERE type_rank = 1
            ORDER BY year;"""
if option == "10.For each year, identify the most common crash type. ":
    df = pd.read_sql(qry_10, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Tracking the dominant crash type annually provides a measure of effectiveness
              for long-term safety campaigns and reveals any emerging trends.**_''')



qry_11 ="""            WITH DailyCounts AS (
                SELECT
                    CRASH_DAY_OF_WEEK,
                    COUNT(*) AS TotalCrashes
                FROM CrashTable
                GROUP BY CRASH_DAY_OF_WEEK
            ),
            TotalDaysObserved AS (
                SELECT
                    CRASH_DAY_OF_WEEK,
                    -- Extracts the date part from CRASH_DATE to count distinct days
                    COUNT(DISTINCT SUBSTR(CRASH_DATE, 1, 10)) AS TotalDays
                FROM CrashTable
                GROUP BY CRASH_DAY_OF_WEEK
            )
            SELECT
                T1.CRASH_DAY_OF_WEEK,
                CAST(T1.TotalCrashes AS REAL) / (T2.TotalDays * 24) AS AverageCrashesPerHour
            FROM DailyCounts T1
            JOIN TotalDaysObserved T2 ON T1.CRASH_DAY_OF_WEEK = T2.CRASH_DAY_OF_WEEK
            ORDER BY AverageCrashesPerHour DESC
            LIMIT 1;"""
if option == "11.Find the day of the week with the highest average crashes per hour. ":
    df = pd.read_sql(qry_11, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Identifying the peak intensity day (e.g., Saturday, Sunday)
              helps police and traffic management focus limited resources for effective weekend coverage.**_''')




qry_12 ="""            SELECT
                CASE
                    WHEN CRASH_HOUR BETWEEN 0 AND 5 THEN 'Night'
                    WHEN CRASH_HOUR BETWEEN 6 AND 11 THEN 'Morning'
                    WHEN CRASH_HOUR BETWEEN 12 AND 17 THEN 'Afternoon'
                    WHEN CRASH_HOUR BETWEEN 18 AND 23 THEN 'Evening'
                    ELSE 'Unknown'
                END AS TimeSlot,
                SUM(INJURIES_TOTAL) AS TotalInjuries
            FROM CrashTable
            GROUP BY TimeSlot
            ORDER BY TotalInjuries DESC
            LIMIT 1;"""
if option == "12.Identify high-risk time slots: Group hours into buckets (Morning, Afternoon, Evening, Night) Find which bucket has the highest injury crashes":
    df = pd.read_sql(qry_12, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Pinpointing the time bucket with the highest total injuries (e.g., Evening)
              helps EMS and hospitals optimize staffing and preparedness for that high-risk window.**_''')



qry_13 ="""            WITH CauseCounts AS (
                SELECT
                    FIRST_CRASH_TYPE,
                    PRIM_CONTRIBUTORY_CAUSE,
                    COUNT(*) AS CauseFrequency
                FROM CrashTable
                GROUP BY 1, 2
            ),
            RankedCauses AS (
            SELECT
            FIRST_CRASH_TYPE,
            PRIM_CONTRIBUTORY_CAUSE,
            CauseFrequency,
            ROW_NUMBER() OVER (PARTITION BY FIRST_CRASH_TYPE ORDER BY CauseFrequency DESC) AS cause_rank
            FROM CauseCounts
            )
            SELECT
            FIRST_CRASH_TYPE,
            PRIM_CONTRIBUTORY_CAUSE,
            CauseFrequency
            FROM RankedCauses
            WHERE cause_rank <= 3
            ORDER BY FIRST_CRASH_TYPE, CauseFrequency DESC;"""
if option == "13.Find the top 3 contributing causes for each crash type. (Use window functions like ROW_NUMBER() or RANK())":
    df = pd.read_sql(qry_13, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: This detailed breakdown helps safety engineers link specific crash mechanics (type)
              to underlying human behaviors (cause), leading to targeted educational programs.**_''')



qry_14 =""" WITH YearlyCrashes AS (
            SELECT
            year,
            COUNT(*) AS CurrentYearCrashes
            FROM CrashTable
            GROUP BY year
            ),
            LaggedCrashes AS (
            SELECT
            year,
            CurrentYearCrashes,
            LAG(CurrentYearCrashes, 1) OVER (ORDER BY year) AS PreviousYearCrashes
            FROM YearlyCrashes
            )
            SELECT
            year,
            CurrentYearCrashes,
            PreviousYearCrashes,
            (CAST(CurrentYearCrashes AS REAL) - PreviousYearCrashes) * 100.0 / PreviousYearCrashes AS YearOverYearGrowthRate
            FROM LaggedCrashes
            WHERE PreviousYearCrashes IS NOT NULL
            ORDER BY year;"""
if option == "14.Calculate the year-over-year growth rate of crashes.(Use LAG() window function)":
    df = pd.read_sql(qry_14, engine)
    st.dataframe(df)    
    st.write('''_**INSIGHT: A positive growth rate in crashes indicates existing safety measures are failing,
              demanding a review of current traffic policy and intervention strategies.**_''')



qry_15 ="""SELECT
           ROUND(LATITUDE, 2) AS ZoneLatitude,
           ROUND(LONGITUDE, 2) AS ZoneLongitude,
           COUNT(*) AS TotalCrashes
           FROM CrashTable
           WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
           GROUP BY ZoneLatitude, ZoneLongitude
           ORDER BY TotalCrashes DESC
           LIMIT 10;"""
if option == "15. Identify hotspot zones:Group nearby locations (round latitude & longitude to 2 decimal places)Find top 10 zones with highest crashes.":
    df = pd.read_sql(qry_15, engine)
    st.dataframe(df)
    st.write('''_**INSIGHT: Identifying clustered zones by rounding coordinates gives Urban 
             Planning actionable areas for major infrastructure overhauls and safety investments**_''')










