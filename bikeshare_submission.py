import time
import pandas as pd

CITY_DATA = { 'chicago': r'chicago.csv',
              'new york city': r'new_york_city.csv',
              'washington': r'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please choose a city from Chicago, New York City or Washington: ").lower()
    
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("This city is not included in the data. Please enter the city name from the list above: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input ("Please enter the month during H1 you are interested in. You can also enter all: ").lower()
    
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = input("This month is not included in the data. Please enter a month during H1 using full month name: ").lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the weekday you are interested in. You can also enter all: ").lower()

    while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("This weekday is not included in the data. Please enter a weekday using full name: ").lower()
    
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: {}".format(df['month'].mode().values[0]))

    # display the most common day of week
    print("The most common day is: {}".format(df['day_of_week'].mode().values[0]))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("The most common hour is: {}".format(df['Hour'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: {}".format(df['Start Station'].mode().values[0]))

    # display most commonly used end station
    print("The most commonly used end station is: {}".format(df['End Station'].mode().values[0]))

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + " to " + df['End Station']
    print("The most commonly used route is: {}".format(df['route'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    sum_time = df['Trip Duration'].sum()
    sum_days = sum_time // 86400 # 24 hrs * 3600 seconds
    sum_hours = (sum_time - sum_days * 86400) // 3600
    sum_minutes = (sum_time - sum_days * 86400 - sum_hours * 3600) // 60
    sum_seconds = sum_time % 60
    print("The total travel time is: {} days, {} hours, {} minutes and {} seconds.".format(sum_days, sum_hours, sum_minutes, sum_seconds))
    
    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    avg_days = avg_time // 86400
    avg_hours = (avg_time - avg_days * 86400) // 3600
    avg_minutes = (avg_time - avg_days *86400 - avg_hours * 3600) // 60
    avg_seconds = avg_time % 60
    print("The average travel time is: {} days, {} hours, {} minutes and {} seconds.".format(avg_days, avg_hours, avg_minutes, int(avg_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Below are the counts of user types: ")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print("Below are the counts of gender: ")
        print(df['Gender'].value_counts())
        print()
        
        # Display earliest, most recent, and most common year of birth
        print("The oldest user is born in {}".format(int(df['Birth Year'].min())))
        
        print("The youngest user is born in {}".format(int(df['Birth Year'].max())))
        
        print("The most common birth year is {}".format(int(df['Birth Year'].mode().values[0])))
        
    else:
        print()
        print("There is no data on gender nor birth year for Washington.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Further questions on whether to display raw data based on user input"""

    start_pos = 0
    end_pos = 5
    
    display_question1 = input("Would you like to see the raw data?: ").lower()
    
    if display_question1 == 'yes':
        while end_pos <= df.shape[0] - 1:
            print(df.sample(5))
            start_pos += 5
            end_pos += 5
            
            display_question2 = input("Would you like to continue?: ").lower()
            if display_question2 == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()