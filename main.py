import pandas as pd
import random

#create dfs from the two input csvs
#1st one is the curated list of hymns, with topics manually entered and weird hymns removed
hymn_data = pd.read_csv("hymn-list.csv")
hymn_list_df = pd.DataFrame(hymn_data)

#2nd input is the annual calendar, with optional seasonal topics entered in
calendar_data = pd.read_csv("hymn-calendar.csv")
hymn_calendar_df = pd.DataFrame(calendar_data)

#since not all sundays have a given topic, add in "general" to clear out the nan fields
hymn_calendar_df.Topic = hymn_calendar_df.Topic.fillna('general')

#turn both dfs into lists of dictionaries, because that's easier for me to manipulate
hymn_dict_list = hymn_list_df.to_dict('records')
hymn_calendar_list = hymn_calendar_df.to_dict('records')

#here i filter out songs that should only be used in certain parts of the meeting
sacrament_hymns = [x for x in hymn_dict_list if 'sacrament' in x['topic']]
closing_hymns_only = [x for x in hymn_dict_list if 'closing' in x['topic']]

#Function 1: randomly select a song for the sacrament (ie, communion) portion of the meeting and return a string w
# the hymn's # & name
def random_sacrament_song():
    random_sacrament_song = random.choice(sacrament_hymns)
    random_sacrament_song_value = f"{random_sacrament_song['number']}: {random_sacrament_song['hymn']}"
    return random_sacrament_song_value

#Function 2: randomly select an opening song based on assigned topic (if any). I had to make this a separate function from the next one
# to be able to filter out songs that are exclusively for the end of the meeting. Weirdly, we don't seem to have many opening-exclusive songs...
def random_op_song(row):
    assigned_topic = hymn_calendar_list[row]['Topic']
    topical_hymns = [x for x in hymn_dict_list if assigned_topic in x['topic']]
    random_op_song_pick = random.choice(topical_hymns)
    if random_op_song_pick in closing_hymns_only:
        random_op_song(row)
    else:
        random_op_song_value = f"{random_op_song_pick['number']}: {random_op_song_pick['hymn']}"
        return random_op_song_value

#Function 3: Pick a closing song that *can* come from the closing-songs-only, but doesn't have to, since there are only a handful
def random_cl_song(row):
    assigned_topic = hymn_calendar_list[row]['Topic']
    topical_hymns = [x for x in hymn_dict_list if assigned_topic in x['topic']]
    random_cl_song_pick = random.choice(topical_hymns)
    random_cl_song_value = f"{random_cl_song_pick['number']}: {random_cl_song_pick['hymn']}"
    return random_cl_song_value

#4 Function 4: This is admittedly sloppy, and I'd prefer to fit all of this into the for loop, but I couldn't figure out another way
#to make sure that we don't sing the same opening & closing songs in one service.
def full_song_picker(n):
    hymn_calendar_df.at[n, 'opening'] = random_op_song(n)
    hymn_calendar_df.at[n, 'sacrament'] = random_sacrament_song()
    hymn_calendar_df.at[n, 'closing'] = random_cl_song(n)
    if hymn_calendar_df.at[n, 'opening'] == hymn_calendar_df.at[n, 'closing']:
        full_song_picker(n)
    else:
        return

#le program. I wanted this to iterate based on the rows in the df, but couldn't figure it out. There aren't very many weeks in a year, so this worked.
#I'd like a more elegant, Pythonic solution in the future, though.
for n in range(0,50):
    full_song_picker(n)
hymn_calendar_df.to_csv("2024_hymn_calendar_v2.csv")