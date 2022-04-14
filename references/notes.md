# Findings and next steps
# Datasets
## flight_information

### *NaN Analysis*
- Sched Groundtime and Act Groundtime have a reappearing pattern of NaN (see .ipynb)
--> Hypothesis 1: If Sched Groundtime is NA, Act Groundtime is also NA --> True. Act Groundtime also has more NAs than Sched Groundtime. See H3
--> Hypothesis 2: Last flight of the day has no value for both variables
--> Hypothesis 3: m_onblockdt NAs have values for Sched Groundtime but not for Act Groundtime (to be verified). Those could be cancelled flts
### *Variable Plausability Analysis*
- FNRs are unreliable and cannot be seen as Identifier --> Create Routing Column 

- AC Registration and ac Type are reliable 

- 9.3% Non-Hub Flights --> eventuell rotationanordnung

- Non-Hub flights should theoretically not be included in the Ground Information Dataset: "Each datapoint consists of an inbound (=arriving) flight and an outbound (=departing) flight from our hub “East Carmen)"

- m_onblockdt has missing values --> reconstruct 

- Some Rotational mismatches, slightly higher number for ECLGQX - looks like the rows are in the wrong order

- reason for delay can be dropped as this is filled in after the flight and has no predictive information

- Crew Group: Reencode; B2 and B are the same

- make time stamp out of dep_sched_date, dep_sched_time and arr_sched_date, arr_sched_time

- Sched Groundtime and Act Groundtime have negative values and huge positive outliers

- dep_delay is completely correct


## ground_information

- cleaning_duration has 3 values only 

### *NaN Analysis*

### *Variable Plausability Analysis*

# Quicknotes
- Why do I need the ground data dataset? 
- time of day vs delay - zusammenhang? 
- dow vs delay - zusammenhang?
- Check count of data observations pro route/ac type/registration
