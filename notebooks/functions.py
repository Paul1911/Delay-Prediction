# As the import of other folders into the notebooks folder does not work, we place the function file in the same folder. 

import numpy as np
from ast import literal_eval
import pandas as pd


# Scheduled block time 
def create_scheduledblocktime(df):
    df['scheduled_block_time'] = (df['arr_sched_time']-df['dep_sched_time']).dt.total_seconds()/60

# Actual block time
def create_actualblocktime(df):
    df['actual_block_time'] = (df['m_onblockdt'] - df['m_offblockdt']).dt.total_seconds()/60


# Leg column 
def create_leg(df):
    df['leg'] = df["dep_ap_sched"] + "-" + df["arr_ap_sched"]


# Routing column 
def create_route(df):
    df['route'] = np.where(df["dep_ap_sched"]<df["arr_ap_sched"], 
        df["dep_ap_sched"] + "-" + df["arr_ap_sched"],
        df["arr_ap_sched"] + "-" + df["dep_ap_sched"]
        )


# Leg counter column 
def create_leg_no(df):
    df["flt_event_number"] = df.groupby(['dep_sched_date', 'ac_registration_x']).cumcount()+1


# Ground/Departure delay in minutes
def create_grounddelay(df):
    df['ground_delay'] = (df['m_offblockdt'] - df['dep_sched_time']).dt.total_seconds()/60


# Block time delay in minutes
def create_blockdelay(df):
    # block delay as actual block time - scheduled block time 
    df['block_delay'] = (df['actual_block_time'] - (
        (df['arr_sched_time']-df['dep_sched_time']).dt.total_seconds()/60) # this is just scheduled_block_time without adding the column
    )

    # block delay as arrival delay (following Hinnerks definition)
    #df['block_delay'] = (df['m_onblockdt']-df['arr_sched_time']).dt.total_seconds()/60


# Rotational mismatch indicator
def create_rotmismatch(df):
    '''Takes a dataframe and adds a rotation mismatch flag if the arrival airport is not equal to the next departure airport'''
    df['rot_mismatch'] = np.where(
        df['ac_registration_x'].shift(-1).eq(df['ac_registration_x']) == True, # Where the registration is the same as the row below
        ~df['dep_ap_sched'].shift(-1).eq(df['arr_ap_sched']), # Check whether current dep ap is the same as next arr. ap | Tilde negates the bool value
        False # Set false in case the registrations are not equal, as then a new ac rotation pattern follows
    )
    return df


# Crewchange after
def change_check_after(row):
    # If same registration and day
    if (row['ac_registration_x']==row['ac_registration_x-1']) & (row['dep_sched_date']==row['dep_sched_date-1']): 
        if (row['cockpit_crew']!=row['cockpit_crew-1']) & (row['cabin_crew']!=row['cabin_crew-1']):
            change = 'both'
        elif (row['cockpit_crew']!=row['cockpit_crew-1']) & (row['cabin_crew']==row['cabin_crew-1']):
            change = 'cockpit'
        elif (row['cockpit_crew']==row['cockpit_crew-1']) & (row['cabin_crew']!=row['cabin_crew-1']):
            change = 'cabin'
        else:
            change = 'no change'
    else:
        change = 'last flt of day'
    return change

def create_crewchange(df):
    cabin_crew = []
    cockpit_crew = []
    trash_crew = []

    for flight in df['TLC_trans']:
        cabin = []
        cockpit = []
        trash = []
        for crew_member_info in literal_eval(flight):
            if crew_member_info.split('_')[-1] == "cp":
                cockpit.append(crew_member_info.split('_')[0])
            elif crew_member_info.split('_')[-1] == "ca":
                cabin.append(crew_member_info.split('_')[0])
            else:
                print('the horror')
                trash.append(crew_member_info)

        # Alphabetical sorting of lists
        cabin = sorted(cabin, key=str.lower)
        cockpit = sorted(cockpit, key=str.lower)
        trash = sorted(trash, key=str.lower)

        # Appending lists to column list
        cabin_crew.append(cabin)
        #print(cabin)
        cockpit_crew.append(cockpit)
        #print(cockpit)
        trash_crew.append(trash)

    df['cabin_crew'] = pd.Series(cabin_crew, index = df.index)
    df['cockpit_crew'] = pd.Series(cockpit_crew, index = df.index)

    df['ac_registration_x-1'] = df['ac_registration_x'].shift(-1)
    df['dep_sched_date-1'] = df['dep_sched_date'].shift(-1)
    df['cockpit_crew-1'] = df['cockpit_crew'].shift(-1)
    df['cabin_crew-1'] = df['cabin_crew'].shift(-1)



    df['Crewchange'] = df.apply(change_check_after, axis=1)

    df.drop(['ac_registration_x-1','dep_sched_date-1','cockpit_crew-1','cabin_crew-1'], axis=1, inplace = True)

    df.drop(['cockpit_crew','cabin_crew'], axis=1, inplace = True)
    
    return df


# Crewchange before
def change_check_before(row):
    # If same registration and day
    if (row['ac_registration_x']==row['ac_registration_x+1']) & (row['dep_sched_date']==row['dep_sched_date+1']): 
        if (row['cockpit_crew']!=row['cockpit_crew+1']) & (row['cabin_crew']!=row['cabin_crew+1']):
            change = 'both'
        elif (row['cockpit_crew']!=row['cockpit_crew+1']) & (row['cabin_crew']==row['cabin_crew+1']):
            change = 'cockpit'
        elif (row['cockpit_crew']==row['cockpit_crew+1']) & (row['cabin_crew']!=row['cabin_crew+1']):
            change = 'cabin'
        else:
            change = 'no change'
    else:
        change = 'first flt of day'
    return change

def create_crewchange_before(df):
    cabin_crew = []
    cockpit_crew = []
    trash_crew = []

    for flight in df['TLC_trans']:
        cabin = []
        cockpit = []
        trash = []
        for crew_member_info in literal_eval(flight):
            if crew_member_info.split('_')[-1] == "cp":
                cockpit.append(crew_member_info.split('_')[0])
            elif crew_member_info.split('_')[-1] == "ca":
                cabin.append(crew_member_info.split('_')[0])
            else:
                print('the horror')
                trash.append(crew_member_info)
                #print(crew_member_info)

        # Alphabetical sorting of lists
        cabin = sorted(cabin, key=str.lower)
        cockpit = sorted(cockpit, key=str.lower)
        trash = sorted(trash, key=str.lower)

        # Appending lists to column list
        cabin_crew.append(cabin)
        cockpit_crew.append(cockpit)
        trash_crew.append(trash)

    df['cabin_crew'] = pd.Series(cabin_crew, index = df.index)
    df['cockpit_crew'] = pd.Series(cockpit_crew, index = df.index)

    df['ac_registration_x+1'] = df['ac_registration_x'].shift(1)
    df['dep_sched_date+1'] = df['dep_sched_date'].shift(1)
    df['cockpit_crew+1'] = df['cockpit_crew'].shift(1)
    df['cabin_crew+1'] = df['cabin_crew'].shift(1)

    df['Crewchange_before'] = df.apply(change_check_before, axis=1)

    df.drop(['ac_registration_x+1','dep_sched_date+1','cockpit_crew+1','cabin_crew+1'], axis=1, inplace = True)

    df.drop(['cockpit_crew','cabin_crew'], axis=1, inplace = True)

    return df


# Create Groundtimes before the given flight
def create_groundtimes_before(df):
    df['act_groundtime_before'] = np.where(
        (df['ac_registration_x'].shift(1).eq(df['ac_registration_x']) == True)&(df['dep_sched_date'].shift(1).eq(df['dep_sched_date']) == True),
        np.around((df['m_offblockdt']-df['m_onblockdt'].shift(1)).dt.total_seconds()/60, decimals =1),
        df['Act Groundtime'] # unclear what to take here for best result, maybe mingt  *****************************************
    )
    df['sched_groundtime_before'] = np.where(
        (df['ac_registration_x'].shift(1).eq(df['ac_registration_x']) == True)&(df['dep_sched_date'].shift(1).eq(df['dep_sched_date']) == True),
        np.around((df['dep_sched_time']-df['arr_sched_time'].shift(1)).dt.total_seconds()/60, decimals =1),
        df['Sched Groundtime'] # unclear what to take here for best result, maybe mingt *****************************************
    )

# Recalculate Scheduled and Actual Ground time 
def recalc_groundtimes(df):
    df['Act Groundtime'] = np.where(
        (df['ac_registration_x'].shift(-1).eq(df['ac_registration_x']) == True) & (df['Act Groundtime'].isna() == False),
        np.around((df['m_offblockdt'].shift(-1) - df['m_onblockdt']).dt.total_seconds()/60, decimals =1),
        df['Act Groundtime']
    )
    df['Sched Groundtime'] = np.where(
        (df['ac_registration_x'].shift(-1).eq(df['ac_registration_x']) == True) & (df['Sched Groundtime'].isna() == False),
        np.around((df['dep_sched_time'].shift(-1) - df['arr_sched_time']).dt.total_seconds()/60, decimals =1),
        df['Sched Groundtime']
    )

#*********************************************************************************************

# standard function 
def create_standard_columns(df):
    '''This function creates the standard new columns: scheduled block time, grounddelay, blockdelay'''
    create_scheduledblocktime(df)
    create_actualblocktime(df)
    #create_leg(df)
    #create_route(df)
    create_grounddelay(df)
    create_blockdelay(df)