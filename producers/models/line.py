"""Defines functionality relating to train lines"""
import collections
from enum import IntEnum
import logging

from models import Station, Train


logger = logging.getLogger(__name__)


class Line:
    """Contains Chicago Transit Authority (CTA) Elevated Loop Train ("L") Station Data"""

    colors = IntEnum("colors", "blue green red", start=0)
    num_directions = 2

    def __init__(self, color, station_data, num_trains=10):
        self.color = color
        self.num_trains = num_trains
        self.stations = self._build_line_data(station_data)
        # We must always discount the terminal station at the end of each direction
        self.num_stations = len(self.stations) - 1
        self.trains = self._build_trains()

    def _build_line_data(self, station_df):
        """Constructs all stations on the line"""
        stations = station_df["station_name"].unique()

        station_data = station_df[station_df["station_name"] == stations[0]]
        line = [
            Station(station_data["station_id"].unique()[0], stations[0], self.color)
        ]
        prev_station = line[0]
        for station in stations[1:]:
            station_data = station_df[station_df["station_name"] == station]
            new_station = Station(
                station_data["station_id"].unique()[0],
                station,
                self.color,
                prev_station,
            )
            prev_station.dir_b = new_station
            prev_station = new_station
            line.append(new_station)
        return line

    def _build_trains(self):
        """Constructs and assigns train objects to stations"""
        trains = []
        curr_loc = 0
        b_dir = True
        for train_id in range(self.num_trains):
            tid = str(train_id).zfill(3)
            train = Train(
                f"{self.color.name[0].upper()}L{tid}", Train.status.in_service
            )
            trains.append(train)

            if b_dir:
                self.stations[curr_loc].arrive_b(train, None, None)
            else:
                self.stations[curr_loc].arrive_a(train, None, None)
            curr_loc, b_dir = self._get_next_idx(curr_loc, b_dir)

        return trains

    def run(self, timestamp, time_step):
        """Advances trains between stations in the simulation. Runs turnstiles."""
        self._advance_turnstiles(timestamp, time_step)
        self._advance_trains()

    def close(self):
        """Called to stop the simulation"""
        _ = [station.close() for station in self.stations]

    def _advance_turnstiles(self, timestamp, time_step):
        """Advances the turnstiles in the simulation"""
        _ = [station.turnstile.run(timestamp, time_step) for station in self.stations]

    def _advance_trains(self):
        """Advances trains between stations in the simulation"""
        # Find the first b train
        curr_train, curr_index, b_direction = self._next_train()
        self.stations[curr_index].b_train = None

        trains_advanced = 0
        while trains_advanced < self.num_trains - 1:
            # The train departs the current station
            if b_direction is True:
                self.stations[curr_index].b_train = None
            else:
                self.stations[curr_index].a_train = None

            prev_station = self.stations[curr_index].station_id
            prev_dir = "b" if b_direction else "a"

            # Advance this train to the next station
            curr_index, b_direction = self._get_next_idx(
                curr_index, b_direction, step_size=1
            )
            if b_direction is True:
                self.stations[curr_index].arrive_b(curr_train, prev_station, prev_dir)
            else:
                self.stations[curr_index].arrive_a(curr_train, prev_station, prev_dir)

            # Find the next train to advance
            move = 1 if b_direction else -1
            next_train, curr_index, b_direction = self._next_train(
                curr_index + move, b_direction
            )
            if b_direction is True:
                curr_train = self.stations[curr_index].b_train
            else:
                curr_train = self.stations[curr_index].a_train

            curr_train = next_train
            trains_advanced += 1

        # The last train departs the current station
        if b_direction is True:
            self.stations[curr_index].b_train = None
        else:
            self.stations[curr_index].a_train = None

        # Advance last train to the next station
        prev_station = self.stations[curr_index].station_id
        prev_dir = "b" if b_direction else "a"
        curr_index, b_direction = self._get_next_idx(
            curr_index, b_direction, step_size=1
        )
        if b_direction is True:
            self.stations[curr_index].arrive_b(curr_train, prev_station, prev_dir)
        else:
            self.stations[curr_index].arrive_a(curr_train, prev_station, prev_dir)

    def _next_train(self, start_index=0, b_direction=True, step_size=1):
        """Given a starting index, finds the next train in either direction"""
        if b_direction is True:
            curr_index = self._next_train_b(start_index, step_size)

            if curr_index == -1:
                curr_index = self._next_train_a(len(self.stations) - 1, step_size)
                b_direction = False
        else:
            curr_index = self._next_train_a(start_index, step_size)

            if curr_index == -1:
                curr_index = self._next_train_b(0, step_size)
                b_direction = True

        if b_direction is True:
            return self.stations[curr_index].b_train, curr_index, True
        return self.stations[curr_index].a_train, curr_index, False

    def _next_train_b(self, start_index, step_size):
        """Finds the next train in the b direction, if any"""
        for i in range(start_index, len(self.stations), step_size):
            if self.stations[i].b_train is not None:
                return i
        return -1

    def _next_train_a(self, start_index, step_size):
        """Finds the next train in the a direction, if any"""
        for i in range(start_index, 0, -step_size):
            if self.stations[i].a_train is not None:
                return i
        return -1

    def _get_next_idx(self, curr_index, b_direction, step_size=None):
        """Calculates the next station index. Returns next index and if it is b direction"""
        if step_size is None:
            step_size = int((self.num_stations * Line.num_directions) / self.num_trains)
        if b_direction is True:
            next_index = curr_index + step_size
            if next_index < self.num_stations:
                return next_index, True
            else:
                return self.num_stations - (next_index % self.num_stations), False
        else:
            next_index = curr_index - step_size
            if next_index > 0:
                return next_index, False
            else:
                return abs(next_index), True

    def __str__(self):
        return "\n".join(str(station) for station in self.stations)

    def __repr__(self):
        return str(self)
