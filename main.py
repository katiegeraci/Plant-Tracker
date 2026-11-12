
hide_debug_information()
set_website_title("Plant Tracker")
set_website_framed(False)


from bakery import assert_equal
from drafter import *
from dataclasses import dataclass


# -------------------------
# Dataclasses
# -------------------------

@dataclass
class Plant:
    name: str
    sunlight: str
    water_frequency: int
    is_watered: bool
    additional_information: str


@dataclass
class State:
    plants: list[Plant]
    selected_plant: int
    watered_plants: list[Plant]
    favorite_plant: Plant | None


# -------------------------
# Home Page
# -------------------------

# This route is treated as the index and a typical route function.
@route("index")
def go_home(state: State) -> Page:
    '''
    This is the home page of the website where the user starts.
    It displays their number of plants, number of watered
    plants, and favorite plant.
    
    Args:
        state (State): The state of the website
    Returns:
        The initial page of the website.
    '''
    content = [
        Header("Welcome to the Plant Tracker"),
        Header("Watered Plants:", 2),
        str(len(state.watered_plants)),
        Header("My Plants:", 2),
        str(len(state.plants)),
        Header("Favorite Plant:", 2)
    ]

    if state.favorite_plant is None:
        content.append("No favorite plant.")
    else:
        content.append(state.favorite_plant.name)
# .extend is used to display a list of things in content rather than one.
    content.extend([
        "\n",
        Button("View Plants", "go_view_plants"),
        Button("Water Plants", "go_water_plants")
    ])

    return Page(state, content)

assert_equal(go_home(State(plants=[], selected_plant=-1,
                           watered_plants=[], favorite_plant=None)),
    Page(State(plants=[], selected_plant=-1, watered_plants=[],
               favorite_plant=None), [
        Header('Welcome to the Plant Tracker'),
        Header('Watered Plants:', 2),
        '0',
        Header('My Plants:', 2),
        '0',
        Header('Favorite Plant:', 2),
        'No favorite plant.',
        '\n',
        Button('View Plants', 'go_view_plants'),
        Button('Water Plants', 'go_water_plants'),
    ]))

# Register go_home under both the required starting address
# and the requested go_home address.
add_route("go_home", go_home)
# add_route() makes go_home our index but also a route
# function that can be called by buttons.

# -------------------------
# View Plants Page
# -------------------------

@route
def go_view_plants(state: State) -> Page:
    '''
    The page for the user to observe all of their inputed plants.
    
    Args:
        state (State): The state of the website.
    Returns:
        The page displaying all of the names of the user's plants.
    '''
    content = [
        Header("My Plants:", 2),
        Header("Select Favorite", 2)
    ]

    if len(state.plants) == 0:
        content.append("You have no plants.")
    else:
        for index, plant in enumerate(state.plants):
            content.extend([
                plant.name,
                Button(
                    "View Details",
                    "go_plant_details",
                    [Argument("plant_index", index)]
                    # Argument() sets index in this function
                    # as an argument for the go_plant_details
                    # function under the name plant_index
                ),
                "\n",
                RelatedCheckBox(
                    "favorite_choices",
                    str(index),
                    state.favorite_plant is plant
                ),
                "\n"
            ])

        content.append(Button("Set Favorite", "select_favorite"))
# .extend is used to display a list of things in content rather than one.
    content.extend([
        "\n",
        Button("Go Home", "go_home"),
        Button("Add Plant", "go_add")
    ])

    return Page(state, content)

assert_equal(go_view_plants(State(plants=[], selected_plant=-1,
    watered_plants=[], favorite_plant=None)),
    Page(State(plants=[], selected_plant=-1, watered_plants=[],
               favorite_plant=None), [
        Header('My Plants:', 2),
        Header('Select Favorite', 2),
        'You have no plants.',
        '\n',
        Button('Go Home', 'go_home'),
        Button('Add Plant', 'go_add'),
    ]))

# -------------------------
# Add Plant Page
# -------------------------

@route
def go_add(state: State, error: str = "") -> Page:
    '''
    The page where users are able to add a plant.
    It involves TextBoxs and a TextArea for the user to input
    all of the information about this new plant.
    
    Args:
        state (State): The state of the website.
        error (str): The empty string. This is used to check
        and make sure that the user inputed something into
        the boxes.
    Returns:
        The page with TextBoxs and a TextArea for the
        user to input all information about the plant
        they want to add.
    '''
    content = [
        Header("Add Plant", 2)
    ]
    
    if error != "":
        content.append(error)
    # Here, error checks if there is anything inputed in the textboxes.
    # If there is nothing (empty string: ""), it displays an error
    # message to the user.
    # Without this, the website would actauly have an error
    # and not work.
    # .extend is used to display a list of things in content rather than one.
    content.extend([
        "Name:",
        TextBox("name"),
        "\n",
        "Sunlight Needed:",
        TextBox("sunlight"),
        "\n",
        "Watering Frequency Days a Week (0-7):",
        TextBox("water_frequency"),
        "\n",
        "Additional Information:",
        TextArea("additional_information"),
        "\n",
        Button("Add", "add_plant"),
        Button("Back", "go_view_plants")
    ])

    return Page(state, content)

assert_equal(go_add(State(plants=[], selected_plant=-1,
    watered_plants=[], favorite_plant=None)),
    Page(State(plants=[], selected_plant=-1, watered_plants=[],
               favorite_plant=None), [
        Header('Add Plant', 2),
        'Name:',
        TextBox('name'),
        '\n',
        'Sunlight Needed:',
        TextBox('sunlight'),
        '\n',
        'Watering Frequency Days a Week (0-7):',
        TextBox('water_frequency'),
        '\n',
        'Additional Information:',
        TextArea('additional_information'),
        '\n',
        Button('Add', 'add_plant'),
        Button('Back', 'go_view_plants'),
    ]))

# -------------------------
# Plant Details Page
# -------------------------

@route
def go_plant_details(state: State, plant_index: int) -> Page:
    '''
    The page displaying all information about a certain plant.
    
    Args:
        state (State): The state of the website.
        plant_index (int): The index of the plant in the list
        of plants that was selected to see the details of.
    Returns:
        A page with all of the information on the plant that
        was selected by the user to see the details of.
    '''
    state.selected_plant = plant_index

    plant = state.plants[state.selected_plant]

    return Page(state, [
        Header(plant.name),
        "Sunlight Needed:",
        plant.sunlight,
        "\n",
        "Watering Frequency:",
        str(plant.water_frequency) + " days a week",
        "\n",
        "Additional Information:",
        plant.additional_information,
        "\n",
        Button("Edit", "go_edit"),
        Button("Remove", "remove_plant"),
        Button("Back", "go_view_plants")
    ])

assert_equal(go_plant_details(State
    (plants=[Plant(name='Audrey II',
    sunlight='Moderate',
    water_frequency=3,
    is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Willow',
    sunlight='A lot',
    water_frequency=5,
    is_watered=False,
    additional_information='Super cool.')],
    selected_plant=0, watered_plants=[],
    favorite_plant=Plant(name='Audrey II',
    sunlight='Moderate',
    water_frequency=3,
    is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.')), 1),
    Page(State(plants=[Plant(name='Audrey II',
    sunlight='Moderate',
    water_frequency=3,
    is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Willow',
    sunlight='A lot',
    water_frequency=5,
    is_watered=False,
    additional_information='Super cool.')],
    selected_plant=1,
    watered_plants=[],
    favorite_plant=Plant(name='Audrey II',
    sunlight='Moderate',
    water_frequency=3,
    is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.')), [
        Header('Willow'),
        'Sunlight Needed:',
        'A lot',
        '\n',
        'Watering Frequency:',
        '5 days a week',
        '\n',
        'Additional Information:',
        'Super cool.',
        '\n',
        Button('Edit', 'go_edit'),
        Button('Remove', 'remove_plant'),
        Button('Back', 'go_view_plants'),
    ]))

# -------------------------
# Edit Plant Page
# -------------------------

@route
def go_edit(state: State, error: str = "") -> Page:
    '''
    The page where users are able to edit an already existing plant.
    It involves TextBoxs and a TextArea for the user to input
    all of the new information about this plant. It is like the
    go_add function but keeps the already inputed information of the
    plant in the TextBoxs and TextArea for editing.
    
    Args:
        state (State): The state of the website.
        error (str): The empty string. This is used to check
        and make sure that the user inputed something into
        the boxes.
    Returns:
        The page with TextBoxs and a TextArea for the
        user to input all new information about the existing plant
        they want to edit.
    '''
    if state.selected_plant < 0 or state.selected_plant >= len(state.plants):
        return go_view_plants(state)

    plant = state.plants[state.selected_plant]

    content = [
        Header("Edit Plant", 2)
    ]

    if error != "":
        content.append(error)
    # Here, error checks if there is anything inputed in the textboxes.
    # If there is nothing (empty string: ""), it displays an error
    # message to the user.
    # Without this, the website would actauly have an error
    # and not work.
# .extend is used to display a list of things in content rather than one.
    content.extend([
        "Name:",
        TextBox("name", plant.name),
        "\n",
        "Sunlight Needed:",
        TextBox("sunlight", plant.sunlight),
        "\n",
        "Watering Frequency Days a Week (0-7):",
        TextBox("water_frequency", str(plant.water_frequency)),
        "\n",
        "Additional Information:",
        TextArea("additional_information", plant.additional_information),
        "\n",
        Button("Update", "edit_plant"),
        Button("Back", "go_plant_details",
               [Argument("plant_index", state.selected_plant)])
    ])
    # Argument() sets state.selected_plant in this function
    # as an argument in the go_plant_details function
    # under the name plant_index

    return Page(state, content)

assert_equal(go_edit(State
    (plants=[Plant(name='Audrey II', sunlight='Moderate',
    water_frequency=3, is_watered=False,
    additional_information='Getting hungrier by the minute!'),
    Plant(name='Willow', sunlight='A lot', water_frequency=5,
    is_watered=False, additional_information='Super cool.')],
    selected_plant=0, watered_plants=[],
    favorite_plant=Plant(name='Audrey II', sunlight='Moderate',
    water_frequency=3, is_watered=False,
    additional_information='Getting hungrier by the minute!'))),
    Page(State(plants=[Plant(name='Audrey II',
        sunlight='Moderate',
        water_frequency=3,
        is_watered=False,
        additional_information='Getting hungrier by the minute!'),
        Plant(name='Willow',
        sunlight='A lot',
        water_frequency=5,
        is_watered=False,
        additional_information='Super cool.')],
        selected_plant=0,
        watered_plants=[],
        favorite_plant=Plant(name='Audrey II',
        sunlight='Moderate',
        water_frequency=3,
        is_watered=False,
        additional_information='Getting hungrier by the minute!')), [
        Header('Edit Plant', 2),
        'Name:',
        TextBox('name', 'Audrey II'),
        '\n',
        'Sunlight Needed:',
        TextBox('sunlight', 'Moderate'),
        '\n',
        'Watering Frequency Days a Week (0-7):',
        TextBox('water_frequency', '3'),
        '\n',
        'Additional Information:',
        TextArea('additional_information', 'Getting hungrier by the minute!'),
        '\n',
        Button('Update', 'edit_plant'),
        Button('Back', 'go_plant_details',
        arguments=[Argument('plant_index', 0)]),
    ]))

# -------------------------
# Water Plants Page
# -------------------------

@route
def go_water_plants(state: State) -> Page:
    '''
    The page that has all of the plant names and their watering frequency
    with RelatedCheckBoxes for the user to check off if they have been watered.
    
    Args:
        state (State): The state of the website.
    Returns:
        A page displaying each plant name and watering frequency with
        RelatedCheckBoxes for each plant to be selected to indicate if
        that plant has been watered.
    '''
    content = [
        Header("Plants:", 2),
        Header("Watered?", 2)
    ]

    if len(state.plants) == 0:
        content.append("You have no plants.")
    else:
        for index, plant in enumerate(state.plants):
            content.extend([
                plant.name,
                "\n",
                str(plant.water_frequency) + " days a week",
                "\n",
                RelatedCheckBox(
                    "watered_indices",
                    str(index),
                    plant.is_watered
                ),
                "\n"
            ])
# .extend is used to display a list of things in content rather than one.
        content.append(Button("Save Watering", "mark_watered"))

    content.append(Button("Go Home", "go_home"))

    return Page(state, content)

assert_equal(go_water_plants(State(plants=[Plant(name='Audrey II',
    sunlight='Moderate', water_frequency=3, is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Poppy', sunlight='None', water_frequency=2, is_watered=False,
    additional_information='Super fun!')], selected_plant=-1,
    watered_plants=[], favorite_plant=Plant(name='Poppy', sunlight='None',
    water_frequency=2, is_watered=False, additional_information='Super fun!'))),
    Page(State(plants=[Plant(name='Audrey II',
    sunlight='Moderate',
    water_frequency=3,
    is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Poppy',
    sunlight='None',
    water_frequency=2,
    is_watered=False,
    additional_information='Super fun!')],
    selected_plant=-1,
    watered_plants=[],
    favorite_plant=Plant(name='Poppy',
    sunlight='None',
    water_frequency=2,
    is_watered=False,
    additional_information='Super fun!')), [
        Header('Plants:', 2),
        Header('Watered?', 2),
        'Audrey II',
        '\n',
        '3 days a week',
        '\n',
        RelatedCheckBox('watered_indices', '0'),
        '\n',
        'Poppy',
        '\n',
        '2 days a week',
        '\n',
        RelatedCheckBox('watered_indices', '1'),
        '\n',
        Button('Save Watering', 'mark_watered'),
        Button('Go Home', 'go_home'),
    ]))

# -------------------------
# Add Plant Route
# -------------------------

@route
def add_plant(
    state: State,
    name: str,
    sunlight: str,
    water_frequency: str,
    additional_information: str
) -> Page:
    '''
    Adds a plant with inputed information to the user's
    list of plants.
    
    Args:
        state (State): The state of the website.
        name (str): The name of the new plant.
        sunlight (str): The amount of sunlight needed by the new plant.
        water_frequency (str): The amount of days per week (0-7) that
        the new plant needs to be watered.
        additional_information (str): Any additional information about
        the new plant.
    Returns:
        The page returned by go_view_plants with this new plant added
        to that list of plants.
    '''

    # Check that all inputs contain information.
    if (name.strip() == "" or sunlight.strip() == ""
            or water_frequency.strip() == ""
            or additional_information.strip() == ""):
        return go_add(state, "Please fill in every field.")

    # Check that the plant name is not already being used.
    for plant in state.plants:
        if plant.name.lower() == name.strip().lower():
            return go_add(state, "A plant with that name already exists.")

    # Check that the watering frequency is an integer.
    # try first tries to make the inputed water_frequency an integer.
    # If the value is not able to be made into an integer, there
    # will be a ValueError. except makes it so that if the
    # ValueError occurs, it will add a message indicating that
    # the value inputed but be an integer.
    try:
        frequency = int(water_frequency)
    except ValueError:
        return go_add(state, "Watering frequency must be an integer.")

    # Check that the watering frequency is between 0 and 7.
    if frequency < 0 or frequency > 7:
        return go_add(state, "Watering frequency must be between 0 and 7.")

    # Construct and add the new plant.
    new_plant = Plant(
        name.strip(),
        sunlight.strip(),
        frequency,
        False,
        additional_information.strip()
    )

    state.plants.append(new_plant)

    return go_view_plants(state)

assert_equal(add_plant(State(plants=[],
    selected_plant=-1, watered_plants=[],
    favorite_plant=None), 'Audrey II', 'Moderate', '3',
    'Getting hungrier by the minute!'),
    Page(State(plants=[Plant(name='Audrey II',
        sunlight='Moderate',
        water_frequency=3,
        is_watered=False,
        additional_information='Getting hungrier by the minute!')],
          selected_plant=-1,
          watered_plants=[],
          favorite_plant=None), [
        Header('My Plants:', 2),
        Header('Select Favorite', 2),
        'Audrey II',
        Button('View Details', 'go_plant_details',
        arguments=[Argument('plant_index', 0)]),
        '\n',
        RelatedCheckBox('favorite_choices', '0'),
        '\n',
        Button('Set Favorite', 'select_favorite'),
        '\n',
        Button('Go Home', 'go_home'),
        Button('Add Plant', 'go_add'),
    ]))

# -------------------------
# Edit Plant Route
# -------------------------

@route
def edit_plant(
    state: State,
    name: str,
    sunlight: str,
    water_frequency: str,
    additional_information: str
) -> Page:
    '''
    Updates an already existing plant with updated inputed information.
    
    Args:
        state (State): The state of the website.
        name (str): The updated name of the plant.
        sunlight (str): The updated amount of sunlight needed by the plant.
        water_frequency (str): The updated amount of days per week (0-7) that
        the plant needs to be watered.
        additional_information (str): Updated additional information about
        the plant.
    Returns:
        The page returned by go_plant_details displaying all of the updated
        information about that plant.
    '''
    if state.selected_plant < 0 or state.selected_plant >= len(state.plants):
        return go_view_plants(state)

    # Check that all inputs contain information.
    if (name.strip() == "" or sunlight.strip() == ""
            or water_frequency.strip() == ""
            or additional_information.strip() == ""):
        return go_edit(state, "Please fill in every field.")

    # Check that another plant does not have the same name.
    for index, plant in enumerate(state.plants):
        if (index != state.selected_plant
                and plant.name.lower() == name.strip().lower()):
            return go_edit(state, "A plant with that name already exists.")

    # Check that the watering frequency is an integer.
    # Check that the watering frequency is an integer.
    # try first tries to make the inputed water_frequency an integer.
    # If the value is not able to be made into an integer, there
    # will be a ValueError. except makes it so that if the
    # ValueError occurs, it will add a message indicating that
    # the value inputed but be an integer.
    try:
        frequency = int(water_frequency)
    except ValueError:
        return go_edit(state, "Watering frequency must be an integer.")

    # Check that the watering frequency is between 0 and 7.
    if frequency < 0 or frequency > 7:
        return go_edit(state, "Watering frequency must be between 0 and 7.")

    # Update the selected plant.
    plant = state.plants[state.selected_plant]

    plant.name = name.strip()
    plant.sunlight = sunlight.strip()
    plant.water_frequency = frequency
    plant.additional_information = additional_information.strip()

    return go_plant_details(state, state.selected_plant)

assert_equal(edit_plant(State(plants=[Plant(name='Audrey II',
    sunlight='Moderate', water_frequency=3, is_watered=False,
    additional_information='Getting hungrier by the minute!'),
    Plant(name='Willow', sunlight='A lot', water_frequency=5,
    is_watered=False, additional_information='Super cool.')],
    selected_plant=0, watered_plants=[], favorite_plant=Plant(name='Audrey II',
        sunlight='Moderate', water_frequency=3, is_watered=False,
        additional_information='Getting hungrier by the minute!')),
        'Audrey II', 'Moderate', '3', 'Getting hungrier by the minute! Woah.'),
    Page(State(plants=[Plant(name='Audrey II',
    sunlight='Moderate',
    water_frequency=3,
    is_watered=False,
    additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Willow',
    sunlight='A lot',
    water_frequency=5,
    is_watered=False,
    additional_information='Super cool.')],
        selected_plant=0,
        watered_plants=[],
        favorite_plant=Plant(name='Audrey II',
        sunlight='Moderate',
        water_frequency=3,
        is_watered=False,
        additional_information='Getting hungrier by the minute!')), [
        Header('Audrey II'),
        'Sunlight Needed:',
        'Moderate',
        '\n',
        'Watering Frequency:',
        '3 days a week',
        '\n',
        'Additional Information:',
        'Getting hungrier by the minute! Woah.',
        '\n',
        Button('Edit', 'go_edit'),
        Button('Remove', 'remove_plant'),
        Button('Back', 'go_view_plants'),
    ]))

# -------------------------
# Remove Plant Route
# -------------------------

@route
def remove_plant(state: State) -> Page:
    '''
    Removes a plant from the user's list of plants.
    
    Args:
        state (State): The state of the website.
    Returns:
        The page returned by go_view_plants displaying the user's
        list of plants without the removed plant.
    '''
    if state.selected_plant < 0 or state.selected_plant >= len(state.plants):
        return go_view_plants(state)

    plant = state.plants[state.selected_plant]

    # Remove the plant from the main list.
    state.plants.remove(plant)

    # Remove it from the watered plants list.
    state.watered_plants = [
        watered_plant
        for watered_plant in state.watered_plants
        if watered_plant is not plant
    ]

    # Remove it as the favorite if necessary.
    if state.favorite_plant is plant:
        state.favorite_plant = None

    # Reset the selected plant.
    state.selected_plant = -1

    return go_view_plants(state)

assert_equal(remove_plant(State(plants=[Plant(name='Audrey II',
    sunlight='Moderate', water_frequency=3, is_watered=True,
    additional_information='Getting hungrier by the minute! Woah.')],
    selected_plant=0, watered_plants=[], favorite_plant=None)),
    Page(State(plants=[], selected_plant=-1, watered_plants=[], favorite_plant=None), [
        Header('My Plants:', 2),
        Header('Select Favorite', 2),
        'You have no plants.',
        '\n',
        Button('Go Home', 'go_home'),
        Button('Add Plant', 'go_add'),
    ]))

# -------------------------
# Mark Watered Route
# -------------------------

@route
def mark_watered(state: State, watered_indices: list[str]) -> Page:
    '''
    Checks the plants to see if they have been watered and
    updates the State's watered_plants with all of the plants
    who have been watered.
    
    Args:
        state (State): The state of the function.
        watered_indices (list[str]): The indicies of all of the watered plants.
        This is used to check if the index of each plant is in watered_indices to
        determine if it has been watered.
    Returns:
        The page returned by go_water_plants that lists the plants
        and checks with all of the watered plants.
    '''

    # Update the watered status of every plant.
    for index, plant in enumerate(state.plants):
        plant.is_watered = str(index) in watered_indices

    # Update the list of watered plants.
    # Goes through state.plants and adds each plant to
    # state.watered_plants if the plant is watered
    # (plant.is_watered = True).
    state.watered_plants = [
        plant for plant in state.plants
        if plant.is_watered
    ]

    return go_water_plants(state)

assert_equal(mark_watered(State(plants=[Plant(
    name='Audrey II', sunlight='Moderate', water_frequency=3,
    is_watered=True, additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Poppy', sunlight='None', water_frequency=2, is_watered=True,
    additional_information='Super fun!')], selected_plant=0,
    watered_plants=[Plant(name='Audrey II', sunlight='Moderate',
    water_frequency=3, is_watered=True,
    additional_information='Getting hungrier by the minute! Woah.'),
    Plant(name='Poppy', sunlight='None', water_frequency=2, is_watered=True,
    additional_information='Super fun!')], favorite_plant=Plant(name='Poppy',
    sunlight='None', water_frequency=2, is_watered=True,
    additional_information='Super fun!')), ['0', '1']),
    Page(State(plants=[Plant(name='Audrey II',
                        sunlight='Moderate',
                        water_frequency=3,
                        is_watered=True,
                        additional_information='Getting hungrier by the minute! Woah.'),
                  Plant(name='Poppy',
                        sunlight='None',
                        water_frequency=2,
                        is_watered=True,
                        additional_information='Super fun!')],
          selected_plant=0,
          watered_plants=[Plant(name='Audrey II',
                                sunlight='Moderate',
                                water_frequency=3,
                                is_watered=True,
                                additional_information='Getting hungrier by the '
                                                       'minute! Woah.'),
                          Plant(name='Poppy',
                                sunlight='None',
                                water_frequency=2,
                                is_watered=True,
                                additional_information='Super fun!')],
          favorite_plant=Plant(name='Poppy',
                               sunlight='None',
                               water_frequency=2,
                               is_watered=True,
                               additional_information='Super fun!')), [
        Header('Plants:', 2),
        Header('Watered?', 2),
        'Audrey II',
        '\n',
        '3 days a week',
        '\n',
        RelatedCheckBox('watered_indices', '0', True),
        '\n',
        'Poppy',
        '\n',
        '2 days a week',
        '\n',
        RelatedCheckBox('watered_indices', '1', True),
        '\n',
        Button('Save Watering', 'mark_watered'),
        Button('Go Home', 'go_home'),
    ]))

# -------------------------
# Select Favorite Route
# -------------------------

@route
def select_favorite(
    state: State,
    favorite_choices: list[str]
) -> Page:
    '''
    Looks at all of the indices of the plants selected to be favorite and
    sets the earlier plant as the favorite_plant.
    
    Args:
        state (State): The state of the website.
        favorite_choices (list[str]): The list of indices of the plants
        that were selected to be favorite.
    Returns:
        The page returned by go_view_plants with all of the same
        information, just with State's favorite_plant updated to the
        proper selected plant.
    '''

    # Reset the favorite plant.
    state.favorite_plant = None

    # Select the first checked plant, if one exists.
    if len(favorite_choices) > 0:
        favorite_index = int(favorite_choices[0])

        if 0 <= favorite_index < len(state.plants):
            state.favorite_plant = state.plants[favorite_index]

    return go_view_plants(state)

assert_equal(select_favorite(State(
    plants=[Plant(name='Audrey II', sunlight='Moderate',
    water_frequency=3, is_watered=False,
    additional_information='Getting hungrier by the minute!')],
    selected_plant=-1, watered_plants=[], favorite_plant=None), []),
    Page(State(plants=[Plant(name='Audrey II',
                sunlight='Moderate',
                water_frequency=3,
                is_watered=False,
                additional_information='Getting hungrier by the minute!')],
          selected_plant=-1,
          watered_plants=[],
          favorite_plant=None), [
        Header('My Plants:', 2),
        Header('Select Favorite', 2),
        'Audrey II',
        Button('View Details', 'go_plant_details', arguments=[Argument('plant_index', 0)]),
        '\n',
        RelatedCheckBox('favorite_choices', '0'),
        '\n',
        Button('Set Favorite', 'select_favorite'),
        '\n',
        Button('Go Home', 'go_home'),
        Button('Add Plant', 'go_add'),
    ]))

# -------------------------
# Start Website
# -------------------------

start_server(State(
    plants=[],
    selected_plant=-1,
    watered_plants=[],
    favorite_plant=None
))

