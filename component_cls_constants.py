from collections import namedtuple

# Ivairiu offsetu definai
ContactOffsets = namedtuple('ContactOffsets', ['x1', 'y1', 'x2', 'y2'])
TextOffset = namedtuple('TextOffset', ['x', 'y'])


class EVSConstants():
    ORIGIN_X = 50
    ORIGIN_Y = 50

    CONTACT1_OFFSET = ContactOffsets(-10, 30, -20, 40)
    CONTACT2_OFFSET = ContactOffsets(80, 30, 90, 40)

    CONTACT1_OFFSET.x1

    CONTACT1_LIST_PLACE = 0
    CONTACT2_LIST_PLACE = 1

    TEXT_OFFSET = TextOffset(35, 90)

    DEFAULT_VALUE = 12
    DEFAULT_NAME = "EV"
    DEFAULT_SYMBOL = "V"

    DEFAULT_WIDTH = 70
    DEFAULT_HEIGHT = 70

    DEFAULT_FILL_COLOR = "black"
    DEFAULT_OUTLINE_COLOR = "white"
    DEFAULT_BODY_OUTLINE_WIDTH = 5
    DEFAULT_CONTACT_OUTLINE_WIDTH = 3

    DEFAULT_COMPONENT_FONT = ("Helvetica", 12, 'bold')
    DEFAULT_FONT_COLOR = "white"


class ResistorConstants():
    ORIGIN_X = 50
    ORIGIN_Y = 50

    CONTACT1_OFFSET = ContactOffsets(-10, 15, -20, 25)
    CONTACT2_OFFSET = ContactOffsets(110, 15, 120, 25)

    CONTACT1_LIST_PLACE = 0
    CONTACT2_LIST_PLACE = 1

    TEXT_OFFSET = TextOffset(50, 50)

    DEFAULT_VALUE = 1000
    DEFAULT_NAME = "R"
    DEFAULT_SYMBOL = "Ω"

    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 40

    DEFAULT_FILL_COLOR = "black"
    DEFAULT_OUTLINE_COLOR = "white"
    DEFAULT_BODY_OUTLINE_WIDTH = 5
    DEFAULT_CONTACT_OUTLINE_WIDTH = 3

    DEFAULT_COMPONENT_FONT = ("Helvetica", 12, 'bold')
    DEFAULT_FONT_COLOR = "white"