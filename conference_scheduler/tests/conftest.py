import pytest
from conference_scheduler.resources import (
    Person, Room, Slot, Session, EventType, Event, Role, Demand,
    Unavailability
)
from conference_scheduler import scheduler
from conference_scheduler import parameters


@pytest.fixture(scope="module")
def people():
    return {
        'alice': Person(name='Alice', max_chair_sessions=3),
        'bob': Person(name='Bob', max_chair_sessions=3),
        'charlie': Person(name='Charlie')
    }


@pytest.fixture(scope="module")
def event_types():
    return {
        'workshop': EventType(name='workshop'),
        'talk': EventType(name='talk')
    }


@pytest.fixture(scope="module")
def rooms(event_types):
    return (
        Room(
            name='Main Hall',
            capacity=500,
            suitability=[event_types['talk']]),
        Room(
            name='Room 2.32',
            capacity=50,
            suitability=[event_types['workshop']])
    )


@pytest.fixture(scope="module")
def slots(rooms):
    return (
        Slot(room=rooms[0], starts_at='15-Sep-2016 09:30', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 10:00', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 11:30', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 12:00', duration=30),
        Slot(room=rooms[0], starts_at='15-Sep-2016 12:30', duration=30),
        Slot(room=rooms[1], starts_at='15-Sep-2016 09:30', duration=90),
        Slot(room=rooms[1], starts_at='15-Sep-2016 11:30', duration=90)
    )


@pytest.fixture(scope="module")
def sessions(slots):
    return (
        Session(slots=(slots[0], slots[1], slots[2])),
        Session(slots=(slots[3], slots[4])),
    )


@pytest.fixture(scope="module")
def roles():
    return {
        'speaker': Role(name='speaker'),
        'leader': Role(name='leader'),
        'mentor': Role(name='mentor')
    }


@pytest.fixture(scope="module")
def events(event_types, roles, people):
    return (
        Event(
            name='Talk 1',
            event_type=event_types['talk'],
            duration=30,
            roles={roles['speaker']: people['alice']}
        ),
        Event(
            name='Talk 2',
            event_type=event_types['talk'],
            duration=30,
            roles={roles['speaker']: people['bob']}
        ),
        Event(
            name='Workshop 1',
            event_type=event_types['workshop'],
            duration=60,
            roles={roles['leader']: people['charlie']}
        )
    )


@pytest.fixture(scope="module")
def demand(events):
    return (
        Demand(event=events['talk_1'], audience=300),
        Demand(event=events['talk_2'], audience=300),
        Demand(event=events['workshop_1'], audience=30),
    )


@pytest.fixture(scope="module")
def unavailability(people, slots):
    return (
        Unavailability(person=people['alice'], slot=slots[0]),
        Unavailability(person=people['alice'], slot=slots[1]),
        Unavailability(person=people['bob'], slot=slots[2]),
        Unavailability(person=people['bob'], slot=slots[3]),
    )


@pytest.fixture(scope='module')
def shape(events, slots):
    return parameters.Shape(len(events), len(slots))


@pytest.fixture(scope='module')
def X(shape):
    return parameters.variables(shape)


@pytest.fixture(scope='module')
def solution(shape):
    return [item for item in scheduler.solution(shape)]


@pytest.fixture(scope='module')
def schedule(events, slots):
    return [item for item in scheduler.schedule(events, slots)]
