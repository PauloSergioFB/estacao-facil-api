from collections import defaultdict

import database.core as db
from serializers.subway import line_serializer


def get_stations(con):
    stmt = """
    SELECT
        s.station_id,
        s.station_name,
        l.line_name,
        ls.position
    FROM
        ef_line_station ls
        LEFT JOIN ef_station      s ON ( ls.station_id = s.station_id )
        LEFT JOIN ef_line         l ON ( ls.line_id = l.line_id )
    """
    db_stations = db.select_all(con, stmt)

    stations = defaultdict(
        lambda: {"id": int(), "name": str(), "lines": list(), "positions": list()}
    )
    for id, station_name, line_name, pos in db_stations:
        stations[id]["id"] = id
        stations[id]["name"] = station_name
        stations[id]["lines"].append(line_name)
        stations[id]["positions"].append(pos)

    return stations


def get_subway_connections(con):
    stmt = """
    SELECT
        origin_station_id,
        destination_station_id,
        trip_duration
    FROM
        ef_connection_stations
    """
    return db.select_all(con, stmt)


def get_lines(con):
    stmt = """
    SELECT
        l.line_name,
        s_min.station_name AS min_station,
        s_max.station_name AS max_station
    FROM
        ef_line         l
        LEFT JOIN ef_line_station ls_min ON ( ls_min.line_id = l.line_id )
        LEFT JOIN ef_station      s_min ON ( s_min.station_id = ls_min.station_id )
        LEFT JOIN ef_line_station ls_max ON ( ls_max.line_id = l.line_id )
        LEFT JOIN ef_station      s_max ON ( s_max.station_id = ls_max.station_id )
    WHERE
        ls_min.position = (SELECT MIN(position) FROM ef_line_station WHERE line_id = l.line_id)
        AND ls_max.position = (SELECT MAX(position) FROM ef_line_station WHERE line_id = l.line_id)
    """
    db_lines = db.select_all(con, stmt, serializer=line_serializer)

    lines = {db_line["name"]: db_line for db_line in db_lines}
    return lines
