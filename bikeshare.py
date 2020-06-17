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
        (str) month - name of the month to filter by, or "all" to apply no month filter (only January through June (inclusive) are valid month choices)
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)

    print('There are 3 cities to choose from: Chicago, New York City, & Washington')
    city = str(input('Please select one of the 3 cities: ')).lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print('\nSorry, that response is not valid! Please try again.')
        print('\nThere are 3 cities to choose from: Chicago, New York City, & Washington')
        city = str(input('Please select one of the 3 cities: ')).lower()
    # get user input for month (all, january, february, ... , june)
    month = str(input('Please select one of the first six months of the year by typing its full name (e.g. \'January\' not \'Jan\') or type \'All\': ').lower())
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print('\nSorry, that response is not valid! Please try again.')
        month = str(input('Please select one of the first six months of the year by typing its full name (e.g. \'January\' not \'Jan\') or type \'All\': ').lower())

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Please select a day or type \'All\': ').lower())
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('\nSorry, that response is not valid! Please try again.')
        day = str(input('Please select a day or type \'All\': ').lower())

    print('-'*40)
    return city, month, day

# earlier experimenting before try/except fix

#results_check = get_filters()
#city_check = results_check[0]

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month, day, both, or neither.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and/or day (if selected)
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        bool_month = df['month'] == month
        df = df[bool_month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)

        # filter by day of week to create the new dataframe
        bool_day = df['day_of_week'] == day
        df = df[bool_day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # Timing the calculation
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of the Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # view raw data option
    view_raw_data(df)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # Timing the calculation
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(start_station_mode))


    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print('The most common ending station is {}.'.format(end_station_mode))

    # display most frequent combination of start station and end station trip

    combined_station_mode = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('The most common start & end station combination is {}.'.format(combined_station_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # view raw data option
    view_raw_data(df)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # Timing the calculation
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time for all trips was {} seconds.'.format(total_travel_time))
    print('That\'s approximately equal to {} hours'.format(float(total_travel_time)//3600))
    print()
    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average travel time for all trips was {} seconds.'.format(avg_travel_time))
    print('That\'s approximately equal to {} minutes'.format(float(avg_travel_time)//60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # view raw data option
    view_raw_data(df)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Note: Gender and Birth Year data doesn't exist for Washington data set.
    A try/except function pair is used to prevent this from causing issues.
    """

    print('\nCalculating User Stats...\n')
    # Timing the calculation
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print()

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
        print()
    except:
        print('There\'s no gender data for Washington D.C.')
        print()

    # Display earliest, most recent, and most common year of birth
    try:
        birth_earliest = df['Birth Year'].max()
        birth_most_recent = df['Birth Year'].min()
        birth_mode = df['Birth Year'].mode()
        print('The youngest rider was born in {}. The oldest rider was born in {}. The most common rider birth year is {}.'.format(str(birth_earliest)[:4], str(birth_most_recent)[:4], str(birth_mode)[5:9]))
    except:
        print('There\'s no birth year data for Washington D.C.')
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # view raw data option
    view_raw_data(df)


def view_raw_data(x):
    """Gives user option to view raw data, 5 rows at a time """
    counter = 0
    view_data = input('Do you want to view raw data?').lower()
    while view_data == 'yes':
        print(x[counter:(counter + 5)])
        counter += 5
        view_data = input('Do you want to view raw data?')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
