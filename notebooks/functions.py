# As the import of other folders for .ipynbs does not work, we place the function file in the same folder. 

import numpy as np

#*********************************************************************************************

# Scheduled block time 
def create_scheduledblocktime(df):
    df['scheduled_block_time'] = (df['arr_sched_time']-df['dep_sched_time']).dt.total_seconds()/60

# Leg column 
def create_leg(df):
    df['leg'] = df["dep_ap_sched"] + "-" + df["arr_ap_sched"]

# Routing column 
def create_route(df):
    df['route'] = np.where(df["dep_ap_sched"]<df["arr_ap_sched"], 
        df["dep_ap_sched"] + "-" + df["arr_ap_sched"],
        df["arr_ap_sched"] + "-" + df["dep_ap_sched"]
        )

# Ground/Departure delay in minutes
def create_grounddelay(df):
    df['ground_delay'] = (df['m_offblockdt'] - df['dep_sched_time']).dt.total_seconds()/60

# Block time delay in minutes
def create_blockdelay(df):
    df['block_delay'] = (df['block_time'] - (
        (df['arr_sched_time']-df['dep_sched_time']).dt.total_seconds()/60) # this is just scheduled_block_time without adding the column
    )

# Rotational mismatch indicator
def create_rotmismatch(df):
    #df = df.sort_values(by = ['ac_registration_x', 'm_offblockdt']).reset_index(drop = True)
    df['rot_mismatch'] = np.where(
        df['ac_registration_x'].shift(-1).eq(df['ac_registration_x']) == True, # Where the registration is the same as the row above
        ~df['dep_ap_sched'].shift(-1).eq(df['arr_ap_sched']), # Check whether current arr ap is the same as prev. dep ap | Tilde negates the bool value
        False # Set false in case the registrations are not equal, as then a new ac rotation pattern follows
        )


#*********************************************************************************************

# standard function 
def create_standard_columns(df):
    create_scheduledblocktime(df)
    create_leg(df)
    create_route(df)
    create_grounddelay(df)
    create_blockdelay(df)