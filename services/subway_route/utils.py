class StationNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def get_station_id_by_name(name, stations):
    try:
        return next(x["id"] for x in stations.values() if x["name"] == name)
    except StopIteration:
        raise StationNotFound(f"Station '{name}' not found")


def get_station_pos(station_id, line, stations):
    i = stations[station_id]["lines"].index(line)
    return stations[station_id]["positions"][i]


def get_direction(from_station, to_station, line, stations, lines):
    from_pos = get_station_pos(from_station, line, stations)
    to_pos = get_station_pos(to_station, line, stations)

    if from_pos > to_pos:
        return lines[line]["min_station"]

    if from_pos < to_pos:
        return lines[line]["max_station"]


def infer_line(a, b, current_line, stations):
    lines_a = stations[a]["lines"]
    lines_b = stations[b]["lines"]

    common = set(lines_a).intersection(lines_b)
    if current_line in common:
        return current_line

    if not common:
        return lines_b[0]

    return next(iter(common))
