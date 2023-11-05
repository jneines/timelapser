#!/usr/bin/env python3
import datetime as dt
from zoneinfo import ZoneInfo
import json

from astral import LocationInfo
from astral.sun import sun
from dateparser import parse

from loguru import logger

from timelapser.paths import program_dir


class ProgramError(Exception):
    pass


def check_mandatory(program, options):
    for option in options:
        if option not in program.keys():
            raise ProgramError(f"Mandatory option '{option}' missing in program.")


def check_one_of(program, options):
    one_available = False
    for option in options:
        if option in program.keys():
            one_available |= True
    if not one_available:
        raise ProgramError(
            f"At least one of the options in '{options}' must be set in the program."
        )


def _load_fuzzy_program(program):
    check_mandatory(program, ["timezone", "start_ts"])
    check_one_of(program, ["end_ts", "duration"])

    parser_settings = {
        "TIMEZONE": program["timezone"],
        "RETURN_AS_TIMEZONE_AWARE": True,
    }

    program["start_ts"] = parse(program["start_ts"], settings=parser_settings)
    if "duration" in program.keys():
        program["end_ts"] = program["start_ts"] + dt.timedelta(
            seconds=program["duration"]
        )
    else:
        program["end_ts"] = parse(program["end_ts"], settings=parser_settings)
    return program


def _load_solar_program(self, program):
    check_mandatory(program, ["timezone", "latitude", "longitude"])

    tz = ZoneInfo(program["timezone"])

    location = LocationInfo(
        name="Here",
        timezone=tz,
        latitude=program["latitude"],
        longitude=program["longitude"],
    )

    now = dt.datetime.now(tz)

    s = sun(location.observer, date=now.date(), tzinfo=location.timezone)

    time_margin = dt.timedelta(seconds=program["time_margin"])

    program["start_ts"] = s["sunrise"] - time_margin
    program["end_ts"] = s["sunset"] + time_margin

    return program


def _load_base_program(self, program):
    return program


_program_mapper = {
    "fuzzy": _load_fuzzy_program,
    "solar": _load_solar_program,
    "base": _load_base_program,
}


def load_program(program_name):
    # program with sane default settings
    program = {
        "timezone": "Europe/Berlin",
        "time_margin": 0,
    }
    with (program_dir / f"{program_name}.json").open("r") as fd:
        _program = json.loads(fd.read())
        program.update(_program)

        return _program_mapper[_program["name"]](program)
