from typing import List
import os.path


class DataPart:
    """Extracts data from a string.

    Stores the data to extract a section of a given string and then
    given any data string will extract the given section stored in this
    object's state.


    Variables
    ----------
    self.item_name: str
        The name for the current string section that will be extracted.

    self.lower_index: int
        The lower bound index for the substring that will be extracted

    self.upper_index: int
        The upper bound index for the substring that will be extracted


    Methods
    ----------
    verify_index_order(self) -> None
        Swaps the lower and upper indexes if the lower index is greater
        then the upper index. This ensures that the upper and lower
        indexes are never inverted.

    get_data_string(self, data: str) -> str
        Returns a string containing the item name and the section of
        the data (which is passed in as a parameter) that the current
        DataPart object has stored in its 'lower' and 'upper' index
        values. The string returned is what will end up being printed
        out to the user.
    """

    def __init__(self, name: str, lower_bounds: int, upper_bounds: int) -> None:
        self.item_name: str = name
        self.lower_index: int = lower_bounds
        self.upper_index: int = upper_bounds
        # Verify the upper and lower index values are in fact correct
        # (i.e. not switched), but if they are then switch them so they
        # are correct.
        self.verify_index_order()

    def verify_index_order(self) -> None:

        if self.lower_index > self.upper_index:
            old_lower_index = self.lower_index
            self.lower_index = self.upper_index
            self.upper_index = old_lower_index
            # Indicate to the user that they had their upper and lower
            # bounding index values switched, so that they can correct
            # them.
            print("\nDataPart> Error with given index order on item '{}' it has been".format(self.item_name) +
                  " automatically corrected, but please verify the upper and lower indexes are in the proper order.")

    def get_data_string(self, data: str) -> str:
        # Extract the a part of the data based and merge it with the
        # 'item name' so the user knows what the data is.
        return "{}: {}".format(self.item_name, data[self.lower_index:self.upper_index + 1])

    def __str__(self) -> str:
        return "DataPart - name: '{}', lower_index: '{}', upper_index: '{}'".format(
            self.item_name, self.lower_index, self.upper_index
        )


class FileProcessor:
    """Reads a csv file and turns it's contents into DataPart objects.


    Variables
    ----------
    self.filename: str
        Stores the filename of csv file to be read. This is the name
        that will be used when opening and writing to the file.

    self.file_data: List[DataPart]
        Stores a list of DataPart objects which are created from the
        csv file that is read in. (Converts each 'valid' line in the
        csv file to a DataPart object)


    Methods
    ----------
    load_to_data_parts(self) -> List[DataPart]
        Open the file with the filename stored in the state, if the file
        Doesn't exist, then create a new one with all of the default
        values. Then read each line of the file, and extract the 'valid'
        lines (i.e. not comments, or blank space) and convert each
        'valid' line into a DataPart object, and return a list of those
        objects.

    create_default_file(self) -> None
        Open a new file in write mode (or create it if it doesn't exist)
        using the filename stored in the state and write all of the
        default value lines to the file. This includes csv instructions, and default data values.
    """

    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.file_data: List[DataPart] = self.load_to_data_parts()

    def load_to_data_parts(self) -> List[DataPart]:
        # Make sure that the file exists before trying to access it,
        # and create a new one if it doesn't. This prevents errors when
        # trying to load a file that doesn't exist.
        if not os.path.isfile(self.filename) or not os.path.exists(self.filename):
            print("\nERROR> The filter data file could not be found! A new one will be created with the default values.")
            self.create_default_file()

        with open(self.filename) as f:
            lines = f.readlines()

        # Filter out all of the unwanted lines from the file (i.e.
        # comments and blank space) so that the 'invalid' lines will not
        # be attempted to be converted into a DataPart.
        line_data: List[str] = [i.strip() if i.strip() != "" and i.strip()[0] != ";" else None for i in lines]
        line_data = list(filter(lambda x: x is not None, line_data))

        # Create a data object from the current line if possible, if an
        # expected error it thrown then inform the user of the error and
        # do not make a new DataPart, essentially skipping over the item
        # with the error.
        data_part_data: List[DataPart] = []
        for i in line_data:
            try:
                # csv format: 'name,lower_index,upper_index'
                # from csv Filter Data Format v1.0
                line_parts = i.split(",")
                data_part_data.append(DataPart(line_parts[0], int(line_parts[1]), int(line_parts[2])))
            except (IndexError, ValueError) as e:
                print("\nERROR> {}".format(e))
                print("  The line: \n    \"{}\"\n  could not be converted to a DataPart object!".format(i))
                print("  This line will be skipped, please review your csv file to ensure it is correct.")

        return data_part_data

    def create_default_file(self) -> None:
        # Write all of the default csv 'file data' to the current file.
        # This is used when the file doesn't exist, in order to create
        # a new csv file with comments so the user is able to better use
        # the csv file. In addition to this, add the default data lines
        # for the csv file, so it will be able to operate on the
        # expected input unless changed.
        with open(self.filename, 'w') as f:
            header_comment: str = (
                "; Balloon Raw Data Translator v0.1" +
                "\n; Created by: Thomas Westpfal" +
                "\n; Filter Data Format: v1.0" +
                "\n; Commented lines are denoted with a ';'" +
                "\n;" +
                "\n; NOTE: Use this file to modify the way the 'Data Translator' filters" +
                "\n; the given data." +
                "\n;" +
                "\n; The 'lower_index' is position of the starting character and the" +
                "\n; 'upper_index' is the position of the last character (inclusive)" +
                "\n;" +
                "\n; Indices start with the first character being 0 and include all" +
                "\n; characters (i.e. includes spaces)" +
                "\n;" +
                "\n; Ex. 'test sentence' -> {1, 8} will give you -> 'est sent'" +
                "\n;" +
                "\n; The 'name' of any of the items MUST NOT contain a ';' or a ','" +
                "\n; ANY USAGE of these characters in the 'name' will break the way" +
                "\n; the file is read." +
                "\n;" +
                "\n; If this file is ever deleted, a new one will automatically be created" +
                "\n; with all of the default values." +
                "\n;" +
                "\n; name,lower_index,upper_index"
            )

            default_filter: str = (
                "\n" +
                "\nPACKET SEND TIME, 1, 7" +
                "\n| - hour, 1, 2" +
                "\n| - minute, 3, 4" +
                "\n| - second, 5, 6" +
                "\nLATITUDE COORDINATES, 8, 15" +
                "\nLONGITUDE COORDINATES, 17, 25" +
                "\nBALLOON INDICATOR, 26, 26" +
                "\nCOURSE (degrees), 27, 29" +
                "\nSPEED (nautical miles), 31, 33" +
                "\nALTITUDE (feet), 37, 42" +
                "\nTELEMETRY COUNTER, 44, 49" +
                "\nTEMPERATURE (celsius), 53, 56" +
                "\nPRESSURE (millibars), 60, 65" +
                "\nBATTERY VOLTAGE (volts), 71, 74" +
                "\nVALID SATELLITES, 77, 78" +
                "\nCOMMENT, 81, 999"
            )

            f.write(header_comment)
            f.write(default_filter)


class Operator:
    """Contains operation functions.


    Methods
    ----------
    display_items(data_parts: List[DataPart], data: str) -> None
        Displays each of the DataParts to the user, from a list of
        DataParts passed into the function. At the end, it will wait
        for user input before continuing.
    """

    @staticmethod
    def display_items(data_parts: List[DataPart], data: str) -> None:
        # Print out each of the data parts after retrieving the
        # data-section from them which is extracted from the original
        # data string.
        print("\n====================================")
        [print(i.get_data_string(data)) for i in data_parts]
        print("====================================\n")
        input("\nPress enter to continue.")


if __name__ == '__main__':
    print("\nBalloon Raw Data Translator v0.1\nCreated by: Thomas Westpfal")

    # Get the filename from the user if they would like to use a custom
    # csv file, or save multiple configurations. If left blank then the
    # default csv file will be used.
    default_csv_filename: str = "filter_data.csv"
    input_filename: str = input("\n\nEnter the csv settings filename below (or leave blank to use default one)\n > ").strip()
    csv_filename: str = input_filename if input_filename != "" else default_csv_filename

    # Attempt to make a FileProcessor with the user's desired filename
    # if the filename is invalid, then revert to the default csv file
    # and proceed using that file.
    processor: FileProcessor
    try:
        processor = FileProcessor(csv_filename)
    except OSError:
        print("\nERROR> Unable to make a file with the given filename, reverting to default file.")
        processor = FileProcessor(default_csv_filename)

    # Request input string from the user to 'translate' or display, then
    # do so to each string entered.
    while True:
        # Example input string:
        # /231641h4259.91N/07847.46WO000/002/A=000750 002TxC   6.40C  999.18hPa  4.69V 04S http://www.lightaprs.com
        raw_data: str = input("\n\nEnter the entire raw data string below... (or 'q' to quit)\n > ").strip()

        current_input: str = raw_data.strip().lower()
        if current_input == 'q' or current_input == 'quit' or current_input == 'exit':
            break

        Operator.display_items(processor.file_data, raw_data)
