import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    """ Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs """
    print("Which city do you want to see data from: Chicago, New York or Washington")

    city = input()
    """ To get user input for the city """
    city = city.lower().replace(' ','_')
    """ To convert city name into lower and replace spaces with underscore """
    while city not in CITY_DATA:
        print("The city you chose is %s and it is invalid " % (city))
        break
    print("Your city of choice is %s " % (city))
    print("How would you like to filter your data: month, day or both? Type 'no' if you don't want to apply filters")
    choice_data = ['month','day','both','no']
    data_choice = input()
    """ To get user input for the choice """
    choice = data_choice.lower()
    """ To convert the choice into lower case """
    while choice not in choice_data:
        """ To handle invalid input entered by the user """
        print("Your selection %s is invalid " % (choice))
        break
    if choice == 'month':
        """ If Selected Choice is month """
        print("By which month? January, February, March, April, May, June")
        month = input()
        month = month.lower()
        day = 'all'
    elif choice == 'day':
        print("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday ")
        day = input()
        month = 'all'
    elif choice == 'both':
        """ If the Selected Choice is both """
        print("Which month? January, February, March, April, May, June")
        month = input()
        month = month.lower()
        print("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday ")
        day = input()
    else:
        """ If Selected Choice is none """
        month = 'all'
        day = 'all'

    print('-'*40)
    return city,month,day

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

    df = pd.read_csv(CITY_DATA[city])
    """ To load the selected city csv file """

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    """ To convert start time into standard time """
    df['month'] = df['Start Time'].dt.month
    """ To get the month value from start time """
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    """ To get the day_of_week value from start time """

    if month != 'all':
        """ If selected month is not none in choice then this function will triggers """
        months = ['january','february','march','april','may','june']
        """ List of months """
        month = months.index(month)+1
        """ Find the index of selected month from the list """
        df = df[df['month'] == month]
        """ New DataFrame that contains the old data frame month equals to selected month """

    if day != 'all':
        """ If selected day is not none in choice then this function will triggers """
        df = df[df['day_of_week'] == day.title()]
        """ New DataFrame that contains the old data frame day equals to selected day """

    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    frequent_month = df['Start Time'].dt.month.mode()[0]

    frequent_day = df['Start Time'].dt.weekday_name.mode()[0]

    frequent_hour = df['Start Time'].dt.hour.mode()[0]

    print("The Most Frequent Month is %s " % (frequent_month))
    print("The Most Frequent Day is %s " % (frequent_day))
    print("Most Frequent Hour is %s " % (frequent_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    frequent_start_station = df['Start Station'].mode()[0]

    frequent_end_station = df['End Station'].mode()[0]

    trip_with_counts = df.groupby(['Start Station','End Station']).size().reset_index(name = 'trips')

    sort_trips = trip_with_counts.sort_values('trips', ascending = False)

    start_trip = sort_trips['Start Station'].iloc[0]

    end_trip = sort_trips['End Station'].iloc[0]

    print("Most Frequent Start Station is %s " % (frequent_start_station))
    print("Most Frequent End Station is %s " % (frequent_end_station))
    print("Most popular trip is from %s to %s " % (start_trip,end_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_trip_time = df['Trip Duration'].sum()

    mean_trip_time = df['Trip Duration'].mean()

    print("Total Travel Time is %s in seconds " % (total_trip_time))
    print("Mean Travel Time is %s in seconds " % (mean_trip_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Count's of User Type's ")
    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())
    else:
        print("Sorry the %s User Type data cannot be found " % (city))

        print("Count's of Gender ")

    if 'Gender' in df.columns:

        print(df['Gender'].value_counts())
    else:
        print("Sorry the %s Gender data cannot be found " % (city))


    print("Data regarding Date of Birth")

    if 'Birth Year' in df.columns:

        recent_birth_year = df['Birth Year'].max()

        print("Most Recent Birth Year is %s " % (recent_birth_year))

        early_birth_year = df['Birth Year'].min()

        print("Most Earliest Birth Year is %s " % (early_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]

        print("Most Common Birth Year is %s " % (common_birth_year))

    else:

        print("Sorry the %s Birth Year data is not available " % (city))


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        print("Would you like to see 10 lines of data ? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()

        i = 10
        while display_data != 'yes':
            break
            """ Display 5 lines of raw data for the user"""
        print(df[:i])
        print("Would you like to see 5 more lines of data ? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()
        i = 5
        while display_data != 'yes':
            break
            """ Display 5 lines of raw data for the user"""
        print(df[:i])
        print("Would you like to see 5 more lines of data ? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()
        i = 5
        while display_data != 'yes':
            break
            """ Display 5 lines of raw data for the user"""
        print(df[:i])
        print("Would you like to see 5 more lines of data ? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()
        print("Would you like to see 5 more lines of data ? Enter yes or no ")

        restart = input('\nWould you like to restart?\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
