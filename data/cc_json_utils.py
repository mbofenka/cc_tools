
import json

CC_DAT_HEADER_CODE = b'\xAC\xAA\x02\x00'
RLE_CODE_INT = 255
BYTE_ORDER = "little"
READ_ADDRESS = 0

class CCDataFile:
    """A class defining the data of dat file
    Member vars:
        levels (list of CCLevels): the levels of this dat file
    """

    def __init__(self):
        self.levels = []

    def __str__(self):
        return_str = ""
        return_str += "Level Pack:\n"
        for level in self.levels:
            return_str += str(level)

        return return_str

    @property
    def level_count(self):
        return len(self.levels)

    def add_level(self, level):
        self.levels.append(level)

def calculate_option_field_byte_size(field):
    """Returns the size of a given field if converted to binary form
    Note: The total byte count of field entry is the type (1 byte) + size (1 byte) and size of the data in byte form
    Args:
        field (CCField)
    """
    byte_data = field.byte_data
    return len(byte_data) + 2

def write_layer_to_dat(layer, writer):
    """Writes the given layer in binary form to the given writer
    Note: while the DAT file format supports run length encoding, this function does not implement it
    Args:
        layer (list of ints): the layer to write
        writer (BufferedWriter): the active writer in binary write mode
    """
    byte_size = len(layer)
    writer.write(byte_size.to_bytes(2, BYTE_ORDER))
    for val in layer:
        if type(val) is int:
            byte_val = val.to_bytes(1, BYTE_ORDER)
        else:
            byte_val = val
        writer.write(byte_val)

def calculate_total_optional_field_byte_size(optional_fields):
    """Returns the total size of all the given optional fields if converted to binary form
    Note: The total byte count of field entry is the type (1 byte) + size (1 byte) and size of the data in byte form
    Args:
        optional_fields (list of CCFields)
    """
    optional_fields_size = 0
    for field in optional_fields:
        optional_fields_size += calculate_option_field_byte_size(field)
    return optional_fields_size

def calculate_level_byte_size(level):
    """Returns the total size of the given level if converted to binary form
    The total byte count of level entry is:
    size (2) + level number (2) + time (2) + chip count (2) +
    map detail (2) + layer1 size (2) + number of bytes in layer1 + layer2 size (2) + number of bytes in layer2 +
    size of optional fields
    Args:
        level (CCLevel)
    """
    optional_fields_size = calculate_total_optional_field_byte_size(level.optional_fields)
    upper_layer_size = len(level.upper_layer)
    lower_layer_size = len(level.lower_layer)
    return 14 + upper_layer_size + lower_layer_size + optional_fields_size

def write_field_to_dat(field, writer):
    """Writes the given field in binary form to the given writer
    Args:
        field (CCField): the field to write
        writer (BufferedWriter): the active writer in binary write mode
    """
    byte_data = field.byte_data
    writer.write(field.type_val.to_bytes(1, BYTE_ORDER))
    writer.write(len(byte_data).to_bytes(1, BYTE_ORDER))
    writer.write(byte_data)

def write_level_to_dat(level, writer):
    """Writes the given level in binary form to the given writer
    Args:
        level (CCLevel): the level to write
        writer (BufferedWriter): the active writer in binary write mode
    """
    level_bytes = calculate_level_byte_size(level)
    writer.write(level_bytes.to_bytes(2, BYTE_ORDER))
    writer.write(level.level_number.to_bytes(2, BYTE_ORDER))
    writer.write(level.time.to_bytes(2, BYTE_ORDER))
    writer.write(level.num_chips.to_bytes(2, BYTE_ORDER))
    writer.write(b'\x01\x00')  # Write the "map detail" which is always a 2 byte number set to 1
    write_layer_to_dat(level.upper_layer, writer)
    write_layer_to_dat(level.lower_layer, writer)
    total_field_byte_size = calculate_total_optional_field_byte_size(level.optional_fields)
    writer.write(total_field_byte_size.to_bytes(2, BYTE_ORDER))
    for field in level.optional_fields:
        write_field_to_dat(field, writer)

def make_cc_data_from_json(input_json):
    with open(input_json, "rt") as jsonFile:
        d = dict()
        d = json.dumps(jsonFile)
    jsonFile.write(CC_DAT_HEADER_CODE)
    jsonFile.write(len(d["levels"]).to_bytes(2, BYTE_ORDER))
    for level in d["levels"]:
        write_level_to_dat(level, d)


make_cc_data_from_json("level.json")

