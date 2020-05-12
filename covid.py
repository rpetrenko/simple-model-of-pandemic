import random

class Status:
    sick = '+'
    healthy = '0'
    dead = 'x'
    immune = '-'


class Stats:
    def __init__(self, population, recovery_days, dead_days, p_sick_factor, p_dead_factor):
        self.population = population
        self.recovery_days = recovery_days
        self.dead_days = dead_days
        self.sick = 0
        self.dead = 0
        self.healthy = population
        self.immune = 0
        self.p_sick_factor = p_sick_factor
        self.p_dead_factor = p_dead_factor

    def summary(self):
        return "{},{},{},{},{},{:.4f}".format(self.population,
        self.sick, self.dead, self.healthy, self.immune, self.p_sick)

    def summary_header(self):
        return "Pop,Sick,Dead,Healthy,Immune,p_sick"

    @property
    def p_sick(self):
        if self.population == 0:
            # all died
            return 0.0
        else:
            return self.sick / self.population * self.p_sick_factor

    @property
    def p_dead(self):
        return self.p_dead_factor


class Person(object):

    def __init__(self):
        self.status = Status.healthy
        self.sick_days = 0

    def update(self, status):
        self.status = status
        if status == Status.sick:
            self.sick_days += 1


def update_status(people, stats):
    for i, person in enumerate(people):
        if person.status == Status.sick:
            # deal with a sick person
            person.update(Status.sick)
            if person.sick_days == stats.recovery_days:
                # sick person might recover
                person.update(Status.immune)
                person.sick_days = 0
                stats.immune += 1
                stats.sick -= 1
            elif person.sick_days == stats.dead_days:
                # sick person might die
                if random.random() < stats.p_dead:
                    person.update(Status.dead)
                    person.sick_days = 0
                    stats.population -= 1
                    stats.dead += 1
                    stats.sick -= 1
        elif person.status == Status.healthy:
            # deal with a healthy person
            if random.random() < stats.p_sick:
                # make healthy person a sick one 
                stats.healthy -= 1
                person.update(Status.sick)
                stats.sick += 1


def print_people(people):
    line = ""
    for p in people:
        line += p.status
    return line


def run_simulation(
        population,
        recovery_days,
        dead_days,
        p_sick_factor,
        p_dead_factor,
        summary_only   
    ):
    lines = []
    stats = Stats(population, recovery_days, dead_days, p_sick_factor, p_dead_factor)
    people = []
    for _ in range(stats.population):
        person = Person()
        people.append(person)

    # make first one as sick always
    people[0].update(Status.sick)
    stats.healthy -= 1
    stats.sick += 1

    day = 1
    while True:
        if summary_only:
            if day == 1:
                lines.append("day," + stats.summary_header())
            lines.append("{},{}".format(day, stats.summary()))
        else:
            if day == 1:
                lines.append("{},{},{}".format("day", "people_details",stats.summary_header()))
            lines.append("{},{},{}".format(day, print_people(people), stats.summary()))
        if stats.sick:
            update_status(people, stats)
        else:
            break
        day += 1
    return lines


if __name__ == "__main__":
    # number of alive people
    population = 20
    # person might recover on this day
    recovery_days = 14
    # person might die on this day
    dead_days = 5
    # probability to get sick after a contact with infected person
    p_sick_factor = 0.3
    # probability to die after being infected
    p_dead_factor = 0.1
    summary_only = not True

    lines = run_simulation(
        population,
        recovery_days,
        dead_days,
        p_sick_factor,
        p_dead_factor,
        summary_only
    )
    for line in lines:
        print(line)

