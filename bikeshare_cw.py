# BikeShare Project Udacity
# Christof Wittig
# Sep 9, 2019

import time
import pandas as pd
import numpy as np

# This is my first refactoring!
# This is my second refactoring!

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('-'*80)

    # get user input for city (chicago, new york city, washington)
    city = user_choice("city", list(CITY_DATA.keys()))

    # get user input for month (all, january, february, ... , june)
    month = user_choice("month", ['all'] + months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = user_choice("day", ['all'] + days)

    print('-'*80)
    print("\nAnalyzing data for [%s], [%s], [%s]....." % (city, month, day))
    print('-'*80)
    return city, month, day


def user_choice(name, choices):
    """
    Prompts user to choose a "name" from a list of string "choices"
    """
    while True:
        print('\nChoose a ' + name + ' from ' + str(dict(enumerate(choices))).title().replace("\'",""))
        choice = input('Your selection (0-{}): '.format(len(choices) - 1))
        try:
            choice = int(choice)
            if choice >= 0 and choice < len(choices):
                choice = choices[choice]
                print("\nGreat! You chose for " + name + ": " + choice.title())
                break
            else:
                print("Entry not valid, try again!")
        except ValueError:
            print("Please enter a number, try again!")
    return choice


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the weekdays list to get the corresponding int
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:      ', months[popular_month - 1].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day:        ', days[popular_day].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: ', popular_hour, "h")

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', popular_start.title())

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Common End Station:   ', popular_end.title())

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + "  To: " + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most Common Trip:           From: ', popular_trip.title())

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel time: {:0,.0f} secs'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel time:  {:0,.1f} secs".format(mean_travel_time))

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print('Counts of user types:\n', user_types)
        print()
    else:
        print('No user type data available for this city')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Counts of gender:\n', gender)
        print()
    else:
        print('No gender data available for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birthyear_earliest = df['Birth Year'].min()
        birthyear_recent = df['Birth Year'].max()
        birthyear_common = df['Birth Year'].mode()[0]
        print('Earliest Birth Year   : ', int(birthyear_earliest))
        print('Most Recent Birth Year: ', int(birthyear_recent))
        print('Most Common Birth Year: ', int(birthyear_common))
    else:
        print('No birth year data available for this city')

    print("\nThis took %.4f seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Show sample data in increments of 5
        prompt = "\nTo browse the first 5 records, please enter \'y\': "
        pointer = 0
        while True:
            browse = input(prompt)
            if browse.lower() != 'y':
                break
            print(df[pointer:(pointer + 5)].to_string())
            pointer += 5
            prompt = prompt.replace('first','next')

        prompt = "\nTo analyze a different data set, please enter \'y\': "
        restart = input(prompt)
        if restart.lower() != 'y':
            print('\nThank you and good bye!\n')
            break


if __name__ == "__main__":
	main()
