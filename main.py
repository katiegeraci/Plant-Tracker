from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Plant Tracker")
set_website_framed(False)


@dataclass
class State:
    pass


@route
def index(state: State) -> Page:
    return Page(state, ["Welcome to the Plant Tracker!"])

assert_equal(index(State()), Page(State(), ["Welcome to the Plant Tracker!"]))

start_server(State())
