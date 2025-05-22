from services.subway_route import find_subway_route


def route_to_instructions(route):
    instructions = []
    for i, step in enumerate(route["steps"], 1):
        type = step["type"]

        if type == "embark":
            line = step["line"]
            direction = step["direction"]
            from_station = step["from_station"]["name"]
            to_station = step["to_station"]["name"]
            stops = len(step["via"]) - 1

            instructions.append(
                f"{i}. Embarque na linha {line} no sentido {direction}.\n"
                f"Siga da estação {from_station} até {to_station}, passando por {stops} parada{'s' if stops != 1 else ''}."
            )

        if type == "transfer":
            station = step["at"]["name"]
            from_line = step["from_line"]
            to_line = step["to_line"]

            instructions.append(
                f"{i}. Faça baldeação na estação {station}.\n"
                f"Troque da linha {from_line} para a linha {to_line}."
            )

    duration_min = route["estimated_duration"] // 60
    duration_sec = route["estimated_duration"] % 60
    instructions.append(
        f"Duração estimada da viagem: {duration_min}:{duration_sec:02d} minutos."
    )

    return "\n\n".join(instructions)


def route_handler(con, values):
    from_station = values["from_station"]
    to_station = values["to_station"]

    route = find_subway_route(con, from_station, to_station)
    return route_to_instructions(route)


RESPONSE_HANDLERS = {"route_handler": route_handler}
