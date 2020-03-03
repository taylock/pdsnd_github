import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Possible_cities     = [ "new york city", "chicago", "washington" ]
Possible_months     = [ "january", "february", "march", "april", "may", "june", "all" ]
Possible_days       = [ "monday", "tuesday", "wednesday", "thursday",
                        "friday", "saturday", "sunday", "all" ]
def question_user (options, message):
    answer = ""
    while len(answer) == 0:
        answer = input(message)
        answer = answer.strip().lower()

        if answer in options:
            return answer
        else:
            answer = ""
            print("Please enter one of the provided options above.\n")

def get_filters():
      
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! I am Chris let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = question_user (
            Possible_cities,
            "Please enter city that you would like to explore: 'new york city', 'chicago' or 'washington' > ")
          
    # TO DO: get user input for month (all, january, february, ... , june)
    
    month = question_user (
        Possible_months, 
        "Please enter month that you would like to explore: 'january', 'february', 'march', 'april', 'may', 'june' or 'all' > ")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = question_user (
        Possible_days,
        "Please enter day that you would like to explore: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' or 'all' > ")

    
    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city], index_col = 0)

    df['Start Time'] = pd.to_datetime(df['Start Time'])     # Format "Start Time" to datetime
    df["month"] = df['Start Time'].dt.month                 # Get the weekday 
    df["week_day"] = df['Start Time'].dt.weekday_name       # Get the Month-part 
    df["start_hour"] = df['Start Time'].dt.hour             # Get the Hour-part
    df["start_end"] = df['Start Station'].astype(str) + ' to ' + df['End Station']

    if month != 'all':
        month_index = Possible_months.index(month) + 1      # Get the list-index of the month.
        df = df[df["month"] == month_index ]                # Create filter for month.

    if day != 'all':
        df = df[df["week_day"] == day.title() ]             # Create filter for week day.

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_index = df["month"].mode()[0] - 1
    most_common_month = Possible_months[month_index].title()
    print("Most common month: ", most_common_month)
    
    # TO DO: display the most common day of week
    most_common_day = df["week_day"].mode()[0]
    print("Most common day: ", most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = df["start_hour"].mode()[0]
    print("Most common hour: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_used_start = df['Start Station'].mode()[0]
    print("Most used start: ", most_used_start)

    # TO DO: display most commonly used end station
    most_used_end = df['End Station'].mode()[0]
    print("Most used end: ", most_used_end)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df["start_end"].mode()[0]
    print("Most common used combination concerning start- and end-station: ", 
            most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total time of travel: ", total_travel_time)

    # TO DO: display mean travel time
    average_time = df["Trip Duration"].mean()
    print("The average travel-time: ", '{:06.2f}'.format(average_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Count user types: ", 
            df["User Type"].value_counts())

    # TO DO: Display counts of gender
    if "Gender" in df:
        print("\nCounts of gender")
        print("Male: ", df.query("Gender == 'Male'").Gender.count())
        print("Female: ", df.query("Gender == 'Female'").Gender.count())

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("\nEarliest year of birth: ", '{:.0f}'.format(df["Birth Year"].min()))
        print("Most recent year of birth: ", '{:.0f}'.format(df["Birth Year"].max()))
        print("Most common year of birth: ", '{:.0f}'.format(df["Birth Year"].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # To Display 5 Lines of raw data upon user's request
    
def display_data(df):
    """ Display 5 lines of raw bikeshare data."""
    r_length = df.shape[0]
    
    # repeat from 0 to number of rows in steps of 5
    for i in range(0, r_length, 5):
        yes=input('\nDo you want to view user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() !='yes':
            break
        #get data and convert to json format
        data_row= df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in data_row:
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
