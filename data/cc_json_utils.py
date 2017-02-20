"""
Data structures for manipulating Chip's Challenge (CC) data
Created for the class Programming for Game Designers
"""
BYTE_ORDER = "little"


class CCField:
    """The base field class
    Member vars:
        type_val (int): the type identifier of this class (set to 3)
        byte_val (bytes): the byte data of the field
    """

    def __init__(self, type_val, byte_val):
        self.type_val = type
        self.byte_val = byte_val

    @property
    def byte_data(self):
        return self.byte_val

    def __str__(self):
        return_str = "    Generic Field (type="+self.type_val+")\n"
        return_str += "      data = "+str(self.byte_val)
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.int_type
        json_field["value"] = self.byte_val.decode()
        return json_field


class CCMapTitleField(CCField):
    """A class defining the map title field
    Member vars:
        type_val (int): the type identifier of this class (set to 3)
        title (string): the title, max length 63 characters
    """
    TYPE = 3

    def __init__(self, title):
        if __debug__:
            if len(title) >= 64: raise AssertionError("Map Title must be 63 characters or fewer. Current title is '"+title+"'("+str(len(title))+")")
        self.type_val = CCMapTitleField.TYPE
        self.title = title

    def __str__(self):
        return_str = "    Map Title Field (type=3)\n"
        return_str += "      title = '"+str(self.title)+"'"
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        json_field["title"] = self.title
        return json_field

    @property
    def byte_data(self):
        title_bytes = b""
        title_bytes += self.title.encode("ascii")
        title_bytes += b'\x00'
        return title_bytes


class CCCoordinate:
    """A class defining a single coordinate
    Member vars:
        x (int): x position, a value from 0 to 31
        y (int): y position, a value from 0 to 31
    """

    def __init__(self, x, y):
        if __debug__:
            if (x<0 or x>31) or (y<0 or y>31):
                raise AssertionError("Coordinates: ("+str(x)+", "+str(y)+") out of range. Coordinates must be from 0 to 31")
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    @property
    def json_data(self):
        return {"x":self.x, "y":self.y}


class CCTrapControl:
    """A class defining a single trap control
    Member vars:
        button_coord (CCCoordinate): the location of the brown button
        trap_coord (CCCoordinate): the location of the trap
    """

    def __init__(self, bx, by, tx, ty):
        """Traps are defined by a pairs of coordinates (bx, by, tx, ty)
        Note that all coordinates must be from 0 to 31
        Args:
            bx, by (int, int): the position of the button
            tx, ty (int, int): the position of the trap
        """
        self.button_coord = CCCoordinate(bx, by)
        self.trap_coord = CCCoordinate(tx, ty)

    def __str__(self):
        return "button"+str(self.button_coord)+", trap"+str(self.trap_coord)

    @property
    def json_data(self):
        json_val = {}
        json_val["button_coord"] = self.button_coord.json_data
        json_val["trap_coord"] = self.trap_coord.json_data
        return json_val


class CCTrapControlsField(CCField):
    """A class defining the trap controls field
    Member vars:
        type_val (int) : the type identifier of this class (set to 4)
        traps (list of CCTrapControl): a list of traps for the map
    """
    TYPE = 4

    def __init__(self, traps):
        """A Trap Control Field is defined by a list of traps
        Note that there is a max of 25 traps per level
        Args:
            traps (list of CCTrapControl): the traps
        """
        if __debug__:
            if len(traps) > 25:
                raise AssertionError("Max trap count exceeded. Max trap count is 25. Number of traps passed = "+str(len(traps)))
        self.type_val = CCTrapControlsField.TYPE
        self.traps = traps

    def __str__(self):
        return_str = "    Trap Controls Field (type=4)\n"
        for trap in self.traps:
            return_str += "      trap = "+str(trap)
            if trap != self.traps[-1]:
                return_str += "\n"
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        traps_data = []
        for trap in self.traps:
            traps_data.append(trap.json_data)
        json_field["traps"] = traps_data
        return json_field

    @property
    def byte_data(self):
        byte_value = b""
        for trap in self.traps:
            byte_value += trap.button_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += trap.button_coord.y.to_bytes(2, BYTE_ORDER)
            byte_value += trap.trap_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += trap.trap_coord.y.to_bytes(2, BYTE_ORDER)
            byte_value += b'\x00\x00' #DAT format says to append 0 to the end of the coordinates
        return byte_value


class CCCloningMachineControl:
    """A class defining a single cloning machine control
    Member vars:
        button_coord (CCCoordinate): the location of the red button
        machine_coord (CCCoordinate): the location of the cloning machine
    """

    def __init__(self, bx, by, tx, ty):
        """Cloning Machines are defined by a pairs of coordinates (bx, by, tx, ty)
        Note that all coordinates must be from 0 to 31
        Args:
            bx, by (int, int): the position of the button
            tx, ty (int, int): the position of the machine
        """
        self.button_coord = CCCoordinate(bx, by)
        self.machine_coord = CCCoordinate(tx, ty)

    def __str__(self):
        return "button"+str(self.button_coord)+", machine"+str(self.machine_coord)

    @property
    def json_data(self):
        json_val = {}
        json_val["button_coord"] = self.button_coord.json_data
        json_val["machine_coord"] = self.machine_coord.json_data
        return json_val


class CCCloningMachineControlsField(CCField):
    """A class defining the cloning machine controls field
    Member vars:
        type_val (int) : the type identifier of this class (set to 5)
        machine (list of CCCloningMachineControl): a list of cloning machines for the map
    """
    TYPE = 5

    def __init__(self, machines):
        """A cloning machine control field is defined by a list of machines
        Note that there is a max of 31 machines per level
        Args:
            machines (list of CCCloningMachineControl): the machines
        """
        if __debug__:
            if len(machines) > 31:
                raise AssertionError("Max cloning machine count of 31 exceeded. Number of cloning machines passed = "+str(len(machines)))
        self.type_val = CCCloningMachineControlsField.TYPE
        self.machines = machines

    def __str__(self):
        return_str = "    Cloning Machine Controls Field (type=5)\n"
        for machine in self.machines:
            return_str += "      machine = "+str(machine)
            if machine != self.machines[-1]:
                return_str += "\n"
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        machine_data = []
        for machine in self.machines:
            machine_data.append(machine.json_data)
        json_field["machines"] = machine_data
        return json_field

    @property
    def byte_data(self):
        byte_value = b""
        for machine in self.machines:
            byte_value += machine.button_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += machine.button_coord.y.to_bytes(2, BYTE_ORDER)
            byte_value += machine.machine_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += machine.machine_coord.y.to_bytes(2, BYTE_ORDER)
        return byte_value


class CCEncodedPasswordField(CCField):
    """A class defining an encoded password
    Member vars:
        type_val (int): the type identifier of this class (set to 6)
        password (list of ints): a password encoded as a list of ints from 4 to 9 ints in length
    """
    TYPE = 6

    def __init__(self, password):
        """Initializes an encoded password
        Args:
            password (list of ints) : the integer values of an encoded password
        """
        if __debug__:
            if len(password) > 9 or len(password) < 4:
                raise AssertionError("Encoded password must be from 4 to 9 characters in length. Password passed is '"+str(password)+"'")
        self.type_val = CCEncodedPasswordField.TYPE
        self.password = password

    def __str__(self):
        return_str = "    Encoded Password Field (type=6)\n"
        return_str += "      password = "+str(self.password)
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        json_field["password"] = self.password
        return json_field

    @property
    def byte_data(self):
        password_bytes = b""
        for i in self.password:
            password_bytes += i.to_bytes(1, BYTE_ORDER)
        password_bytes += b'\x00'
        return password_bytes


class CCMapHintField(CCField):
    """A class defining a hint
    Member vars:
        type_val (int): the type identifier of this class (set to 7)
        hint (string): the hint for the level max length 127 characters
    """
    TYPE = 7

    def __init__(self, hint):
        if __debug__:
            if len(hint) > 127 or len(hint) < 0:
                raise AssertionError("Hint must be from 0 to 127 characters in length. Hint passed is '"+hint+"'")
        self.type_val = CCMapHintField.TYPE
        self.hint = hint

    def __str__(self):
        return_str = "    Map Hint Field (type=7)\n"
        return_str += "      hint = '"+str(self.hint)+"'"
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        json_field["hint"] = self.hint
        return json_field

    @property
    def byte_data(self):
        hint_bytes = b""
        hint_bytes += self.hint.encode("ascii")
        hint_bytes += b'\x00'
        return hint_bytes


##HERE FOR REFERNECE, BUT NOT SUPPORTED
##MAKE SURE YOU USE CCEncodedPasswordField for PASSWORDS
class CCPasswordField(CCField):
    """A class defining an unencoded password
    Member vars:
        type_val (int): the type identifier of this class (set to 8)
        password (string): the password string, length from 4 to 9 characters
    """
    TYPE = 8
    password = ""

    def __init__(self, password):
        if __debug__:
            if len(password) > 9 or len(password) < 4:
                raise AssertionError("Password must be from 4 to 9 characters in length. Password passed is '"+password+"'")
        self.type_val = CCPasswordField.TYPE
        self.password = password

    def __str__(self):
        return_str = "    Password Field (type=8)\n"
        return_str += "      password = '"+str(self.password)+"'"
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        json_field["password"] = self.password
        return json_field

    @property
    def byte_data(self):
        password_bytes = b""
        password_bytes += self.password.encode("ascii")
        password_bytes + b'\x00'
        return password_bytes


class CCMonsterMovementField(CCField):
    """A class defining the monsters that move in a given level
    Member vars:
        type_val (int): the type identifier of this class (set to 10)
        monsters (list of CCCoordinate): the coordinates of each monster
    """
    TYPE = 10

    def __init__(self, monsters):
        if __debug__:
            if len(monsters) > 128:
                raise AssertionError("Max monster count of 128 exceeded. Number of monsters passed = "+str(len(monsters)))
        self.type_val = CCMonsterMovementField.TYPE
        self.monsters = monsters

    def __str__(self):
        return_str = "    Monster Movement Field (type=10)\n"
        for monster in self.monsters:
            return_str += "      monster = "+str(monster)
            if monster != self.monsters[-1]:
                return_str += "\n"
        return return_str

    @property
    def json_data(self):
        json_field = {}
        json_field["type"] = self.type_val
        monster_data = []
        for monster in self.monsters:
            monster_data.append(monster.json_data)
        json_field["monsters"] = monster_data
        return json_field

    @property
    def byte_data(self):
        byte_value = b""
        for monster in self.monsters:
            byte_value += monster.x.to_bytes(1, BYTE_ORDER)
            byte_value += monster.y.to_bytes(1, BYTE_ORDER)
        return byte_value


class CCLevel:
    """A class defining the data of a single level
    Member vars:
        level_number (int): the sequence number for this level. it corresponds to it's order in the list of levels
        time (int): the time limit in seconds for the level. 0 means no time limit
        num_chips (int): the number of computer chips to be collected in the level
            Layers: Chip's Challenge maps are 32x32 grids in 2 layers: upper and lower
            A single map layer is stored as an array of 1024 ints
        upper_layer (int list): the layer data for the upper (main) layer
        lower_layer (int list): the lower layer data. this allows for objects to be placed under other objects
        optional_fields (list of CCField types): the fields that augment the data of this level. all levels have a title and a password
    """
    def __init__(self):
        self.level_number = -1
        self.time = -1
        self.num_chips = -1
        self.upper_layer = []
        self.lower_layer = []
        self.optional_fields = []

    def __str__(self):
        return_str = ""
        return_str += "  Level #"+str(self.level_number)+"\n"
        return_str += "    Time Limit = "+str(self.time)+"\n"
        return_str += "    Chip Count = "+str(self.num_chips)+"\n"
        for field in self.optional_fields:
            return_str += str(field) + "\n"
        return_str += "    Upper Layer:\n"
        for r in range(32):
            return_str += "    "
            row = self.upper_layer[(r*32):(r*32+32)]
            for v in row:
                return_str += " {0:3d}".format(v)
            return_str += "\n"
        return_str += "    Lower Layer:\n"
        for row in range(32):
            return_str += "    "
            row = self.lower_layer[(r*32):(r*32+32)]
            for v in row:
                return_str += " {0:3d}".format(v)
            return_str += "\n"
        return return_str

    def add_field(self, field):
        self.optional_fields.append(field)


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

CC_DAT_HEADER_CODE = b'\xAC\xAA\x02\x00'
RLE_CODE_INT = 255

READ_ADDRESS = 0

def do_read(reader, byte_count):
    """Utility read function to enable address tracking and other debugging when reading binary files
    Currently keeps track of the current byte address in the file in the global variable TEMP_ADDRESS
    Args:
        reader (BufferedReader) : reader to read from
        byte_count (int) : number of bytes to read
    """
    global READ_ADDRESS
    to_return = reader.read(byte_count)
    # print("x"+format(TEMP_ADDRESS, '02x')+": "+str(to_return)+" ("+str(int.from_bytes(to_return, cc_data.BYTE_ORDER))+")")
    READ_ADDRESS += byte_count
    return to_return


def get_string_from_bytes(byte_data, encoding="ascii"):
    """Decodes a string from DAT file byte data.
    Note that in byte form these strings are 0 terminated and this 0 is removed
    Args:
        byte_data (bytes) : the binary data to convert to a string
        encoding (string) : optional, the encoding type to use when converting
    """
    string_bytes = byte_data[0:(len(byte_data) - 1)]  # strip off the 0 at the end of the string
    string = string_bytes.decode(encoding)
    return string


def make_field_from_bytes(field_type, field_bytes):
    """Constructs and returns the appropriate cc field
    Args:
        field_type (int) : what type of field to construct
        field_bytes (bytes) : the binary data to be used to create the field
    """
    if field_type == CCMapTitleField.TYPE:
        return CCMapTitleField(get_string_from_bytes(field_bytes))
    elif field_type == CCTrapControlsField.TYPE:
        trap_count = int(len(field_bytes) / 10)
        traps = []
        for t_index in range(trap_count):
            i = t_index * 10
            bx = int.from_bytes(field_bytes[i:(i + 2)], byteorder=BYTE_ORDER)
            by = int.from_bytes(field_bytes[i + 2:(i + 4)], byteorder=BYTE_ORDER)
            tx = int.from_bytes(field_bytes[i + 4:(i + 6)], byteorder=BYTE_ORDER)
            ty = int.from_bytes(field_bytes[i + 6:(i + 8)], byteorder=BYTE_ORDER)
            traps.append(CCTrapControl(bx, by, tx, ty))
        return CCTrapControlsField(traps)
    elif field_type == CCCloningMachineControlsField.TYPE:
        machine_count = int(len(field_bytes) / 8)
        machines = []
        for m_index in range(machine_count):
            i = m_index * 8
            bx = int.from_bytes(field_bytes[i:(i + 2)], byteorder=BYTE_ORDER)
            by = int.from_bytes(field_bytes[i + 2:(i + 4)], byteorder=BYTE_ORDER)
            tx = int.from_bytes(field_bytes[i + 4:(i + 6)], byteorder=BYTE_ORDER)
            ty = int.from_bytes(field_bytes[i + 6:(i + 8)], byteorder=BYTE_ORDER)
            machines.append(CCCloningMachineControl(bx, by, tx, ty))
        return CCCloningMachineControlsField(machines)
    elif field_type == CCEncodedPasswordField.TYPE:
        # passwords are encoded as a list of ints
        password = []
        # A bytes object behaves as a list of integers
        # password data is terminated with a zero, iterate to one short of the end of the array
        for b in field_bytes[0:(len(field_bytes)-1)]:
            password.append(b)
        return CCEncodedPasswordField(password)
    elif field_type == CCMapHintField.TYPE:
        return CCMapHintField(get_string_from_bytes(field_bytes))
    elif field_type == CCPasswordField.TYPE:
        return CCPasswordField(get_string_from_bytes(field_bytes))
    elif field_type == CCMonsterMovementField.TYPE:
        monster_count = int(len(field_bytes) / 2)
        monsters = []
        for m_index in range(monster_count):
            i = m_index * 2
            x = int.from_bytes(field_bytes[i:(i + 1)], byteorder=BYTE_ORDER)
            y = int.from_bytes(field_bytes[i + 1:(i + 2)], byteorder=BYTE_ORDER)
            monsters.append(CCCoordinate(x, y))
        return CCMonsterMovementField(monsters)
    else:
        if __debug__:
            raise AssertionError("Unsupported field type: " + str(field_type))
        return CCField(field_type, field_bytes)


def make_optional_fields_from_dat(reader):
    """Reads all the optional fields in from the active reader
    Note that this assumes the reader is at the optional fields section in the file.
    This code does not error check for invalid data
    Args:
        reader (BufferedReader) : active reader reading a DAT file
    Returns:
        A list of all the constructed optional fields
    """
    fields = []
    total_optional_field_bytes = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    while total_optional_field_bytes > 0:
        field_type = int.from_bytes(do_read(reader, 1), byteorder=BYTE_ORDER)
        byte_count = int.from_bytes(do_read(reader, 1), byteorder=BYTE_ORDER)
        byte_vals = do_read(reader, byte_count)
        fields.append(make_field_from_bytes(field_type, byte_vals))
        total_optional_field_bytes -= (byte_count + 2)
    return fields


def make_layer_from_bytes(layer_bytes):
    """Constructs layer data (a 1024 list of ints) from the given layer_bytes data
    Note: DAT files employ Run Length Encoding which this function is designed to decode
    Args:
        layer_bytes (bytes) : The binary data of a layer read in from the DAT file
    Returns:
        A list of ints initialized with the layer data
    """
    layer_data = []
    index = 0
    while index < len(layer_bytes):
        val = layer_bytes[index]
        index += 1
        # Check for the Run Length Encoding value
        if val == RLE_CODE_INT:
            # If using RLE, the next byte is the number of copies to make
            # and the 2nd byte is the value to repeat
            copies = layer_bytes[index]
            code = layer_bytes[index + 1]
            index += 2
            for i in range(copies):
                layer_data.append(code)
        else:
            layer_data.append(val)
    return layer_data


def make_level_from_dat(reader):
    """Reads all the data to construct a single level from the active reader
    Note that this assumes the reader is at new level section in the file.
    This code does not error check for invalid data
    Args:
        reader (BufferedReader) : active reader reading a DAT file
    Returns:
        A CCLevel object constructed with the read data
    """
    level = CCLevel()
    level.num_bytes = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    level.level_number = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    level.time = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    level.num_chips = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    # Note: Map Detail is not used and is expected to always be 1
    map_detail = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    upper_layer_byte_count = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    upper_layer_bytes = do_read(reader, upper_layer_byte_count)
    lower_layer_byte_count = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
    lower_layer_bytes = do_read(reader, lower_layer_byte_count)
    level.upper_layer = make_layer_from_bytes(upper_layer_bytes)
    level.lower_layer = make_layer_from_bytes(lower_layer_bytes)
    level.optional_fields = make_optional_fields_from_dat(reader)
    return level


def make_cc_data_from_dat(dat_file):
    """Reads a DAT file and constructs a CCDataFile object out of it
    This code assumes a valid DAT file and does not error check for invalid data
    Args:
        dat_file (string) : the filename of the DAT file to read in
    Returns:
        A CCDataFile object constructed with the data from the given file
    """
    data = CCDataFile()
    with open(dat_file, 'rb') as reader:
        header_bytes = do_read(reader, 4)
        if header_bytes != CC_DAT_HEADER_CODE:
            print("ERROR: Invalid header found. Expected " + str(CC_DAT_HEADER_CODE) + ", but found " + header_bytes)
            return
        num_levels = int.from_bytes(do_read(reader, 2), byteorder=BYTE_ORDER)
        for i in range(num_levels):
            level = make_level_from_dat(reader)
            data.levels.append(level)
    return data


def calculate_option_field_byte_size(field):
    """Returns the size of a given field if converted to binary form
    Note: The total byte count of field entry is the type (1 byte) + size (1 byte) and size of the data in byte form
    Args:
        field (CCField)
    """
    byte_data = field.byte_data
    return len(byte_data) + 2


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


def write_cc_data_to_dat(cc_dat, dat_file):
    """Writes the given CC dat in binary form to the file
    Args:
        cc_dat (CCData): the cc data to write
        dat_file (string): the filename of the output file
    """
    with open(dat_file, 'wb') as writer: # Note: DAT files are opened in binary mode
        # Basic DAT file format is: DAT header, total number of levels, level 1, level 2, etc.
        writer.write(CC_DAT_HEADER_CODE)
        writer.write(cc_dat.level_count.to_bytes(2, BYTE_ORDER))
        for level in cc_dat.levels:
            write_level_to_dat(level, writer)