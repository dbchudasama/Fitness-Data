# Databricks notebook source
#Reading the file and converting it as a dict. 
import pandas as pd
import xmltodict
with open("/dbfs/mnt/adls/2021/export.xml", "r") as xml_file:
  input_data = xmltodict.parse(xml_file.read())
    
#Records list for general health data & imported as Pandas Data Frame
records_list = input_data['HealthData']['Record']
df_records = pd.DataFrame(records_list)

#Workout list for workout data
workouts_list = input_data['HealthData']['Workout']
df_workouts = pd.DataFrame(workouts_list)

# COMMAND ----------

df_workouts.head()

# COMMAND ----------

#Convert selected columns to numeric so we can do calcuations
# convert just columns "..." and "..."
df_workouts[["@duration", "@totalDistance", "@totalEnergyBurned"]] = df_workouts[["@duration", "@totalDistance", "@totalEnergyBurned"]].apply(pd.to_numeric)
df_workouts.dtypes

#convert dates to actual datetime
format = '%Y-%m-%d %H:%M:%S %z'

df_workouts['@creationDate'] = pd.to_datetime(df_workouts['@creationDate'],format=format)

df_workouts['@startDate'] = pd.to_datetime(df_workouts['@startDate'], format=format)

df_workouts['@endDate'] = pd.to_datetime(df_workouts['@endDate'],format=format)

df_workouts.dtypes

# COMMAND ----------

df_workouts.head()

# COMMAND ----------

#drop unnecessary columns (all rows and column 1 to 12)
df_workouts = df_workouts.iloc[:,0:12]
df_workouts.head()

#Remove HKWorkoutActivityTypeWalking and HKWorkoutActivityTypeSnowSports
#df_workouts=df_workouts[df_workouts['@workoutActivityType'] == 'HKWorkoutActivityTypeRunning']
#df_workouts=df_workouts[df_workouts['@workoutActivityType'] != 'HKWorkoutActivityTypeSnowSports']

# COMMAND ----------

df_workouts.head()

# COMMAND ----------

#Rename Activity Types
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeRunning", "Running")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeHighIntensityIntervalTraining", "HIIT")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeTraditionalStrengthTraining", "Strength")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeWalking", "Walking")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeCoreTraining", "Core")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeCycling", "Cycling")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeYoga", "Yoga")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeOther", "Other")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeDance", "Dance")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeGolf", "Golf")
df_workouts["@workoutActivityType"]= df_workouts["@workoutActivityType"].replace("HKWorkoutActivityTypeCrossTraining", "Cross Training")

df_workouts.head()

# COMMAND ----------

#save as csv 
finalADS = df_workouts.to_csv(r'/dbfs/mnt/adls/2021/workoutData2.csv', header=True) 
