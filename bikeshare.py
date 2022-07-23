#this project has already been checked so no need to change Pythong code

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Asks user to specify a city, month, and day to analyze.

    

#    Returns:
#        (str) city - name of the city to analyze
def main():
    go_on = 'y'
    while go_on == 'y':
        city = ''
        while city not in ('chicago', 'new york city', 'washington'):
            city = input('Enter the city of choice ').lower()
            if city == 'chicago' :
                print('you chose Chicago')
            elif city == 'new york city' :
                print('you chose New York City')
            elif city == 'washington' :
                print('you chose Washington')
            else :
                print ("that is not a valid city (try Chicago, Washington or New York City)")

        #        (str) month - name of the month to filter by, or "all" to apply no month filter
        month = ''
        while month not in ('all','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december') :
            month = input('Please choose a month (ex January or all) ').lower()
        #        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        day = ''
        while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday') :
            day = input('Please choose a day of the week (ex Monday or all) ').lower()
        #    return city, month, day    
        print('you chose '+city.capitalize()+'-'+month.capitalize()+'-'+day.capitalize())



        df = pd.read_csv(CITY_DATA[city])

        #if city == 'new york city':
        #    df = pd.read_csv('new_york_city.csv')
        #else:
        #    df = pd.read_csv(city+'.csv')


        #tidying up potential bad inputs of capitals and lowers for month and day
        if month.lower() == 'all':
            month = month.lower()
        else:
            month = month.capitalize()

            if day.lower() == 'all':
                day = day.lower()
            else:
                day = day.capitalize()

        df['dfMonth'] = pd.DatetimeIndex(df['Start Time']).month
        df['dfMonth'] = pd.to_datetime(df['dfMonth'], format='%m').dt.month_name()
        df['day_of_week'] = pd.to_datetime(df['Start Time'])
        df['day_of_week'] = df['day_of_week'].dt.weekday_name
        df['Start_hour'] = pd.to_datetime(df['Start Time']).dt.hour

        # Loads data for the specified city and filters by month and day if applicable.
        if month == 'all' and day == 'all':
            df = df
        elif month == 'all' and day !='all':
            df = df[(df.day_of_week == day)]
        elif month != 'all' and day =='all':
            df = df[(df.dfMonth == month)]
        else:
            df = df[(df.dfMonth == month) & (df.day_of_week == day)]

        #    return df
        print('What does the raw data look like?')
        view_data = 'yes'
        def show_data_5_rows():
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
            start_loc = 0
            while view_data in ('yes','y'):
                print(df.iloc[start_loc:start_loc + 5])
                start_loc += 5
                view_data = input('Do you want to see more?: ').lower()


        show_data_5_rows()        
        
        
        
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()


         # TO DO: display the most common month
        print('Most common month to travel is '+df['dfMonth'].value_counts().idxmax())
         # TO DO: display the most common day of week
        print('Most common day of the week to travel is '+df['day_of_week'].value_counts().idxmax())
        # TO DO: display the most common start hour
        print('Most common hour to start your travel is '+str(df['Start_hour'].value_counts().idxmax()))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

        
        
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()
        # TO DO: display most commonly used start station
        print('Most common start station is '+df['Start Station'].value_counts().idxmax())
        # TO DO: display most commonly used end station
        print('Most common end station is '+df['End Station'].value_counts().idxmax())
        # TO DO: display most frequent combination of start station and end station trip
        df['Comb Station'] = 'From '+ df['Start Station'] + ' to ' +df['End Station']
        print('Most common combination of stations is '+df['Comb Station'].value_counts().idxmax())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

        
        
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()
        # converting str to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        #calculating travel time
        df['travel_time'] = (df['End Time'] - df['Start Time']).dt.total_seconds()/60
            # TO DO: display total travel time
        total_travel_time_min = df['travel_time'].sum()
        print('Total Travel time in selected data is '+str(total_travel_time_min)+' minutes or '+str(total_travel_time_min/60)+' hours or '+ str(total_travel_time_min/1440) + ' days')
            # TO DO: display mean travel time
        mean_travel_time_min = df['travel_time'].mean()
        print('Mean/Average Travel time in selected data is '+str(mean_travel_time_min)+' minutes or '+str(mean_travel_time_min/60)+' hours or '+ str(mean_travel_time_min/1440) + ' days')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

        
        
        print('\nCalculating User Stats...\n')
        start_time = time.time()
        # TO DO: Display counts of user types
        print('there are following User Types in the data')
        print(df.groupby(['User Type']).size().reset_index(name='counts'))
        # TO DO: Display counts of gender
        if 'Gender' not in df:
            print('\nsorry no gender data available for \n'+city)
        else:
            print('there are following genders in the data')
            print(df.groupby(['Gender']).size().reset_index(name='counts'))
        
        #TO DO: Display earliest, most recent, and most common year of birth
        if 'Birth Year' not in df:
            print('\n sorry no Birth Year data available for \n'+city)
        else:
            birth_year_min = df['Birth Year'].min()
            birth_year_max = df['Birth Year'].max()
            birth_year_common = df['Birth Year'].value_counts().idxmax()


            print('Earliest Birth Year is ' + str(birth_year_min) + ', most recent Birth Year is '+ str(birth_year_max) + ', most common Birth Year is '+ str(birth_year_common))
        go_on = input('Do you want to run the script again? y/n ')
    


main()


    

