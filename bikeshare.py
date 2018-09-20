import datetime
import time
import pandas as pd
import numpy as np
import calendar

## I like pie

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    city = input('Which city would you like to see the data for - Chicago, New York City, or Washington?:\n')
    while True:
        if city.lower() == 'chicago' or city == 'Chicago' or city == 'c' or city == 'C':
            print("\nThe Windy City it is!\n")
            return 'chicago.csv'
        elif city.lower() == 'new york city' or city == 'New York City' or city == 'n' or city == 'N':
            print("\nThe Big Apple!\n")
            return 'new_york_city.csv'
        elif city.lower() == 'washington' or city == 'washington' or city == 'w' or city == 'W':
            print("\nEl Capital!\n")
            return 'washington.csv'
        else:
            print("\nSorry, that's not a valid city - please try again.")
            return get_city()



def get_month():
    """
    Asks user to specify a month between January and July

    Args:
        none

    Returns:
        (str) month - Which month to analyze the data for. Each month is converted
        into their respective number
    """
    month = input('Which month? January, February, March, April, May, or June?\n').title()
    if month == 'January':
        return '01'
    elif month == 'February':
        return '02'
    elif month == 'March':
        return '03'
    elif month == 'April':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'June':
        return '06'
    else:
        print("\nThat's an invalid month - Please try again.")
        return get_month()


def get_day():
    """ Asks the user which day to pick from.
    Args:
        none
    Returns:
        (str) Gets the day from the data. Each day represents a specific number.
    """
    day = input('\nGreat! Now which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
    if day == 'Monday':
        print("\nGross - Mondays :(\n")
        return 0
    elif day == 'Tuesday':
        print("\nTuesday it is!\n")
        return 1
    elif day == 'Wednesday':
        print("\nHump day!\n")
        return 2
    elif day== 'Thursday':
        print("\nThirsty Thursdays! *chugs*\n")
        return 3
    elif day == 'Friday':
        print("\nIt's finally Friday!\n")
        return 4
    elif day == 'Saturday':
        print("\nSaturdays are the best day of the week!\n")
        return 5
    elif day == 'Sunday':
        print("\nSunday Funday!\n")
        return 6
    else:
        print("\nThat's an invalid day. Please try again.\n")
        return get_day()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Filter by city - month - day
    df = pd.read_csv('{}'.format(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    pop_month = df.groupby('month')['Start Time'].count()
    print("The most common month is: " + calendar.month_name[int(pop_month.sort_values(ascending=False).index[0])])


    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday
    pop_day = df.groupby('day')['Start Time'].count()
    print("The most common day of the week is: " + calendar.day_name[int(pop_day.sort_values(ascending=False).index[0])])

    # display the most common start hour
    pop_hour = int(df['Start Time'].dt.hour.mode())
    if pop_hour == 0:
        am_or_pm = 'AM'
        most_pop_hour = 12
    elif 1 <= pop_hour < 13:
        am_or_pm = 'PM'
        most_pop_hour = pop_hour
    elif 13 <= pop_hour < 24:
        am_or_pm = 'PM'
        most_pop_hour = pop_hour - 12
    print("The most common start hour is: {} {}".format(most_pop_hour, am_or_pm))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode().to_string(index = False)
    print("The most commonly used start station is: {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode().to_string(index = False)
    print("The most commonly used end station is: {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    pd.set_option('max_colwidth',100)
    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' to ')
    popular_combo = df['Trip'].mode().to_string(index = False)
    print("The mose frequent combination of stations is: {}".format(popular_combo))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = round(df['Trip Duration'].sum())
    minute, second = divmod(total_time, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    year, day = divmod(day, 365)
    print("The total travel time is {} years, {} days, {} hours, {} minutes, and {} seconds.".format(year, day, hour, minute, second))

    # display mean travel time
    avg_time = round(df['Trip Duration'].mean())
    minute, second = divmod(avg_time, 60)
    hour, minute = divmod(minute, 60)
    print("The average travel time on a bike is {} hours, {} minutes, and {} seconds.".format(hour, minute, second))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby('User Type')['User Type'].count()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        male = df.query('Gender == "Male"').Gender.count()
        female = df.query('Gender == "Female"').Gender.count()
        print("\n{} total Male users.".format(male))
        print("{} total Female users.\n".format(female))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        early = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode())
        print("Earliest birth year: {}".format(early))
        print("Most recent birth year: {}".format(recent))
        print("Most common birth year: {}".format(common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Displays 5 files of data if the user selects yes
    If user says no - it goes to def main(). This program continues
    until the user says no.

    Args:
        df: dataframe of the bikeshare data
    Returns:
        User selects yes - returns 5 lines of data then asks again
        User selects no - moves on """

    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    x = 0
    y = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print("Sorry, I do not understand your input. Please type 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes' or display.lower() == 'y':
        print(df[df.columns[0:-1]].iloc[x:y])
        display_lines = ''
        while display_lines.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False:
                display_lines = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_2 = is_valid(display_lines)
                if valid_input_2 == True:
                    break
                else:
                    print("Sorry, I do not understand your input. Please type "
                          "'yes' or 'no'.")
            if display_lines.lower() == 'yes' or display_lines.lower() == 'y':
                x += 5
                y += 5
                print(df[df.columns[0:-1]].iloc[x:y])
            elif display_lines.lower() == 'no' or display_lines.lower() == 'n':
                break

def main():
    while True:
        city = get_city()
        month = get_month()
        day = get_day()
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
