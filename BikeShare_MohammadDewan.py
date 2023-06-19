#!/usr/bin/env python
# coding: utf-8

# In[16]:


--import time
--import pandas as pd
--import numpy as np


# In[17]:


# To import the data from the data repository
--chicago='chicago.csv'
--newyorkcity='new_york_city.csv'
--washington='washington.csv'


# In[18]:


# To visualise the data
df = pd.read_csv(chicago)
df.head()


# In[19]:----


# Examine the number of rows and columns in the data set
df.shape


# In[20]:


# To findout the columns names
df.columns


# In[21]:


# To examine the different types of values in each columns
df.info()


# In[22]:


#For duplicat values
df.duplicated().sum()


# In[23]:


# How many missing values
df.isnotnull().sum()


# In[24]:


# Data at a glance
df.describe()


# In[25]:


#Examining the types of customers_1
df['User Type'].value_counts().sum()


# In[26]:


#Examining the customer demographics_1
df['Gender'].value_counts()


# In[27]:


#Examining the customer demographics_2
df['Birth Year'].value_counts().sum()


# In[28]:


df['User Type'].unique().sum()


# In[30]:


# To create a dictionary
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# To validate months and day
month_list =['january','february','march','april','may', 'june', 'all']
weekday_list =['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']


# List for month and day
months= ['january','february','march','april','may', 'june', 'all']
days= ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
        
    # for selecting city (chicago, new york city, washington).
    city = check_user_input("would you like to see the data for chicago, new york or washington?\n", 'c')
    
    # for selecting month (january, february, ... , june or none)
    month = check_user_input("\n Which month would you like to consider? (January, February, March, April, May, June)? Type 'None' for no month filter\n", 'm')
   
    # for selecting day of week (monday, tuesday, ... sunday or none)
    day = check_user_input("\n Which day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'None' for no day filter \n", 'd')
    
    print('-'*40)
    return city, month, day

# Function to validate user input (This format was taken from www.datainsightonline.com/post/sxploring-us-bikeshare-data-project)
def check_user_input(user_input, input_type):
    while True:
        input_user_entered=input(user_input).lower()
        try:
            if input_user_entered in ['chicago','new york city','washington'] and input_type=='c':
                break
            elif input_user_entered in month_list and input_type == 'm':
                break
            elif input_user_entered in weekday_list and input_type == 'd':
                break
            else:
                if input_type == 'c':
                    print('invalid input!, please enter either chicago, new york city, or washington')
                if input_type =='m':
                    print('invalid input!, please enter january, february, march, april, may, or june')
                if input_type =='d':
                    print('invalid input!, please enter a day')
        except ValueError:
            print('sorry, your input is wrong, please enter a valid input')
    return input_user_entered



def load_data(city, month, day):
 
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Loading and converting data file into data frame
    df = pd.read_csv(CITY_DATA[city])
    
    #Converting start time colunm to datetime (www.gitlab.com/tomjose1792/BikeShare-Project-Python)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #Extract month, day and hour (This format was taken from www.datainsightonline.com/post/sxploring-us-bikeshare-data-project)
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour
    
    # filter by month if applicable (This format was taken from www.datainsightonline.com/post/sxploring-us-bikeshare-data-project)
    if month != 'all':
        months =['january', 'february', 'march', 'april', 'may', 'june']
        month =months.index(month) + 1
        
    # To create a new dataframe for month filter
    df = df[df['month'] == month]
    
    
    # filter by day of week if applicable 
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df
    
    
# Define most frequent travel time calculators
def time_stats(df):
    """ Display statistics of the most frequent times of travel"""
    
    print('\ncalculating the most frequent times of travel')
    start_time = time.time()
    
    # Most common month of travel
    most_common_month = df['month'].mode()[0]
    print('most common month is: ', most_common_month)
    
    # Most common day of travel
    most_common_day = df['day_of_week'].mode()[0]
    print('most common day is: ', most_common_day)
    
    # Most common start hour of travel
    most_common_hour = df['hour'].mode()[0]
    print('most common start hour is: ', most_common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
# Stats on most popular stations between travel (This format was taken from www.datainsightonline.com/post/sxploring-us-bikeshare-data-project)
def station_stats(df):
    """ Display statistics on the most popular stations and trip"""
    
    print('\ncalculating the most popular station and trips...\n')
    start_time = time.time()
    
    # The most commonly used starting station
    most_common_start_station = df['Start Station'].mode()[0]
    print('most common start station is: ', most_common_start_station)
    
    # The most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('most common end station is: ', most_common_end_station)
    
    # Display the most commpnly used start and end stations
    # Instead of using mode, we will use group and then result will be sorted to decending order
    combination_group=df.groupby(['Start Station','End Station'])
    most_frequent_combination_station =combination_group.size().sort_values(ascending =False).head(1)
    print('most frequent start_end station is: ', most_frequent_combination_station)
    
    print('\nthis took %s second.' %(time.time()- start_time))
    
# For total and average trip duration
def trip_duration_stats(df):
    """ Display statistics on the total and average trip duration"""
    
    print('\ncalculating trip duration')
    start_time = time.time()
    
    # For total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time is: ', total_travel_time)
    
    # For mean travel time
    mean_travel_time =df['Trip Duration'].mean()
    print('mean travel time is :', mean_travel_time)
    
    print('\nthis took %s second.' %(time.time()- start_time))
    
    
# To display statistics of Bikeshare users
def user_stats(df, city):
    """ Display statistics of Bikeshare users"""
    
    print('\ncalculating user stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    print('user type are : ', df['User Type'].value_counts())
    
    # As the columns Gender and Birth Year are not in washington data, we ensure that the city is not washington.
    if city != 'washington':
        print('\n Counts of Gender: \n', df['Gender'].value_counts())
        
        # Earliest, most common, and most recent year of birth
        earliest_year =df['Birth Year'].min()
        print('earliest year is :', earliest_year)
        
        most_recent_year =df['Birth Year'].max()
        print('most recent year is :', most_recent_year)
        
        most_common_year =df['Birth Year'].mode()[0]
        print('most common year is :', most_common_year)
        
    print('\nthis took %s second.' %(time.time()- start_time))
    print('-'*40)
    
# To view raw data
def ask_more_data(df):
    more_data =input("would you like to examine 5 more rows of data: Enter yes or no?"). lower()
    start_loc = 0
    while more_data == 'yes':
        print(df.iloc[0:5])
        start_loc += 5
        more_data = input("would you like to view 5 rows of data? enter yes or no?").lower()
    return df

                
# For main outputs
def main():
    while True:
        city, month, day = get_filters()
        df =load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        ask_more_data(df)
        restart =input('\n would you like to restart: please enter "y" for yes, "n" for no.\n').lower()
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()


# In[ ]:




