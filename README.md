# parking-area-monitoring-system

FIT SYS 5380 Final Project is a parking area monitoring system.  This is a simulation to validate its effectiveness.

## Simulation Details

Since the simulation output will be used for the ANOVA process, there will be a series of 3 varying factors over 2 states each.  The following configuration items will have an A and B setup configuration for the 3 changing variables believed to contribute to parking time, which are interarrival rates throughout the day, whether or not the PAMS system is installed, and how parking spaces are distributed among the lots.

Each student car enters the simulation after an exponentially distributed interarrival time that ramps up from the morning, then ramps down after midday.  Alternatively, the interarrival rate is constant all day.

Each student car is assigned an ordered preference of identically-sized (975 spaces each) parking lots they'd like to park in, with a slightly higher chance that preference will be lot 1 (35%), and lower consecutive percentage chances for the rest of the lots, at 30%, 20%, and 15% respectively.  Alternatively, the parking lots will be sized differently, with the most desirable parking lot having the least spaces (260), and the consecutively less-desirable lots having more spaces, 520, 1040, and 2080 total.

If PAMS is active, students will only waste 6 seconds waiting on a full deck (the PAMS system would place a large sign in front of each lot showing remaining parking), and will immediately reroute to their next lot choice, saving any additional queueing time they would've wasted looking for parking in a full lot.

## To do list

- Refactor for better comprehension