import ast
import datetime
import os
import numpy as np
from os.path import join
from datetime import date


"""
Writer, reader, and parser based on what we discussed and at least how I understood it. 
Some elements can be adjusted for readability, user experience, or ease of use—such as error handling and variable names.

The writer takes any entry and appends it to the specified file path.
The reader reads entries from a file. A major change is that it now uses tuples,
which improves indexing and searching by comment or header compared to my original idea of dictionaries which has unique keys
It can also handle flux curves if the format for Flux_Curves.txt is changed, and it can convert dictionaries of lists into proper dictionaries.

The parser finds the coefficient corresponding to a given entry.
Uses dictionaries
"""

# testCal class to test similar to before 
class testCal:

    def __init__(self):
        self.mono_max = [1800, 2100, 2500, 3000, 3500]
        self.id_sp_eV = [500, 520, 540, 560, 580]
        self.grt_name = ["MEG"]
        self.id_mode = [0]
        self.fit_coefs = [1.0, 2.0]

    def write(self, new_entry, **kwargs):
        """
        Appends/Writes a new calibration to the calibration file.
        Args: 
            new_entry (dict)
        kwargs: 
            filename (str)
            path (str)
            comment (str)
            debug (bool)
        """
        kwargs.setdefault('filename', "Dict_IDCal.txt")
        kwargs.setdefault('path', ".")
        kwargs.setdefault('debug', False)

        filename = kwargs['filename']
        path = kwargs['path']
        debug = kwargs['debug']
        comment = kwargs.get("comment", "")
    
        # fpath = join(path, filename)
        # fpath for cheerful 
        fpath=r"C:\Users\29iduser\Documents\GitHub\Dict_IDCal.txt"
        # Make the directory if it doesnt exist
        os.makedirs(path, exist_ok=True)

        # Appends it to the file
        with open(fpath, "a+") as f:
            f.write("\n======= " + str(date.today()) + ": " + comment + "\n")
            f.write(str(new_entry))
            f.write("\n")

        if debug:
            print('write_calibration fpath:', fpath)
            print('ID calibration:', new_entry)

    def read(self, **kwargs):
        """
        Reads any dictionary entry from a file.

        Args:
            fpath (str): Path to the file to read from.
            kwargs:
                index (int): -1 to get the last entry, or specific index.
                comment (str): Search by comment string in header.
                date (str): Search by date string in header.
                debug (bool): If True, print debug information.

        Returns:
            dict: The parsed dictionary entry.
        """
        kwargs.setdefault('filename', "Dict_IDCal.txt")
        kwargs.setdefault('path', ".")
        filename = kwargs['filename']
        path = kwargs['path']
        #fpath = join(kwargs.get("path", "."), kwargs.get("filename", "Dict_IDCal.txt"))
        #Fpath set for testing purposes now
        fpath=r"C:\Users\29iduser\Documents\GitHub\Dict_IDCal.txt"
        kwargs.setdefault("index", -1)
        kwargs.setdefault("comment", None)
        kwargs.setdefault("date", None)
        kwargs.setdefault("debug", False)

        index = kwargs["index"]
        comment = kwargs["comment"]
        date_search = kwargs["date"]
        debug = kwargs["debug"]
        #create a list of all the entries to be able to find any enry init 
        entries = []

        with open(fpath, 'r') as f:
            content = f.read()
        #find the five ======, and it split 
        raw_entries = content.split("=======")
        for raw in raw_entries:
                #removes all leading and trailing whitespace
                if raw.strip():  
                    try:
                        #Find first { for the block
                        brace_index = raw.index("{")
                        
                        header = raw[:brace_index].strip()
                        dict_text = raw[brace_index:]
                        last_brace_index = dict_text.rfind("}")
                        clean_block = dict_text[:last_brace_index + 1]

                        # Safely evaluate the dictionary
                        entry_dict = ast.literal_eval(clean_block)
                        #create a tuple and add it to entries
                        entries.append((header, entry_dict))
                    except Exception as e:
                        if debug:
                            print("Error")
                            continue

    # Search entries from top to bottom for a match by comment or date
        index2 = 0
        while index2 < len(entries):
            header, block = entries[index2]
            if (comment in header) or (date_search in header):
                index = index2
                break
            index2 += 1
        #find the entry by index
        if index is not None:
            header, entry = entries[index]

        #Convert list-of-pairs to dict if needed
        for grating in entry:
            for mode in entry[grating]:
                if isinstance(entry[grating][mode], list):
                    entry[grating][mode] = { bkpt: coefs for bkpt, coefs in entry[grating][mode]}

        if debug:
            print("\ Selectede Entry Header", header)
            print("\n Dictionary:", entry )
        
        return header, entry


def parse_cal(entry, grating, ID_mode, energy_eV):
    """
     parse entry only works for dictionaries of the type:
    {"MEG": {0: {bkpt1: [polynomials], bkpt2: [polynomials]}}}

    Parses a calibration dictionary and returns the coefficients corresponding
    to the first breakpoint greater than the specified energy value.

    Args:
        entry (dict): Calibration dictionary.
        grating (str): e.g., "MEG"
        ID_mode (int): e.g., 0
        energy_eV (float): photon energy in eV

    Returns:
        list: Coefficient list for the nearest breakpoint >= energy_eV
    """
    breakpointdict = entry[grating][ID_mode]
    breakpoint_list = list(breakpointdict.keys())
    sorted_breakpoints = np.sort(np.array(breakpoint_list))

    for bp in sorted_breakpoints:
        if energy_eV < bp:
            return breakpointdict[bp]
        else
        #just returns the highest breakpoint if the eV is above all breakpoints 
            return breakpointdict[sorted_breakpoints[-1]]



cal = testCal()

test_entry = {
        "MEG": {
            0: [
                [2000, [1.0, 0.5]],
                [3000, [2.0, 1.0]]
            ]
        }
    }
# First test write
cal.write(test_entry, comment="Test Calibration Entry", debug=True)

# Read an entry at a specific index, will convert list-of-pairs to dictionaries 
#Can be changed but the idea was to be able to get the comment for the entry, or can we just return back the entry 
header, read_entry = cal.read(index=7)

print(read_entry)

# Write it back to the end of the file
# test works as intended

cal.write(read_entry)
coeffs = parse_cal(read_entry, "MEG", 0, 2500)


print(cal.read(index=-1))


print("Coefficients:", coeffs)
