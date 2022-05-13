class Scheduler(object):

    def __init__(self, busy_percentage = 100.0):
        self.hourly_arrival_rates = []
        self.busy_percentage = busy_percentage / 100.0
        # each value is 1 divided by cars per minute
        self.hourly_arrival_rates.append(1.0 / 3 / self.busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 7 / self.busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 12 / self.busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 18 / self.busy_percentage)
        self.hourly_arrival_rates.append(1.0 / 25 / self.busy_percentage)
        reverse_arrivals = list(reversed(self.hourly_arrival_rates))
        for arrival in reverse_arrivals:
            self.hourly_arrival_rates.append(arrival)
    
    def get(self, current_time):
        interarrival_time = 0
        if current_time <= 60:
            interarrival_time = self.hourly_arrival_rates[0]
        elif current_time <= 120:
            interarrival_time = self.hourly_arrival_rates[1]
        elif current_time <= 180:
            interarrival_time = self.hourly_arrival_rates[2]
        elif current_time <= 240:
            interarrival_time = self.hourly_arrival_rates[3]
        elif current_time <= 300:
            interarrival_time = self.hourly_arrival_rates[4]
        elif current_time <= 360:
            interarrival_time = self.hourly_arrival_rates[5]
        elif current_time <= 420:
            interarrival_time = self.hourly_arrival_rates[6]
        elif current_time <= 480:
            interarrival_time = self.hourly_arrival_rates[7]
        elif current_time <= 540:
            interarrival_time = self.hourly_arrival_rates[8]
        elif current_time <= 600:
            interarrival_time = self.hourly_arrival_rates[9]
        return interarrival_time