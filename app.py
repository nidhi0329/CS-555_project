""" A script to parse the data from a .ged file.

    date: 20-Sep-2020
    python: v3.8.4
"""

import re
import operator
from typing import List, Optional, Tuple
from prettytable import PrettyTable
from models import Individual, Family
import user_stories as us

TAGS: List[str] = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM',
                   'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

ARGUMENT_PATTERN: str = '^(0|1|2) (NAME|SEX|FAMC|FAMS|MARR|HUSB|WIFE|CHIL|DATE) (.*)$'  # pattern 1
NO_ARGUMENT_PATTERN: str = '^(0|1) (BIRT|DEAT|MARR|DIV|HEAD|TRLR|NOTE)$'  # pattern 2
ZERO_PATTERN_1: str = '^0 (.*) (INDI|FAM)$'  # pattern 3
ZERO_PATTERN_2: str = '^0 (HEAD|TRLR|NOTE) ?(.*)$'  # pattern 4

regex_list: List[str] = [ARGUMENT_PATTERN, NO_ARGUMENT_PATTERN, ZERO_PATTERN_1, ZERO_PATTERN_2]


def pattern_finder(line: str) -> Optional[str]:
    """ find the pattern of a given line """
    for pattern, regex in zip(['ARGUMENT', 'NO_ARGUMENT', 'ZERO_1', 'ZERO_2'], regex_list):
        if re.search(regex, line):
            return pattern


def get_lines(path) -> List[str]:
    """ get lines read from a .ged file """
    with (file := open(path, "r")):  # close file after opening
        return [line for line in file]


def pretty_print(individuals: List[Individual], families: List[Family]) -> None:
    """ prettify the data """

    individual_table: PrettyTable = PrettyTable()
    family_table: PrettyTable = PrettyTable()
    individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age",
                                    "Alive", "Death", "Child", "Spouse"]
    family_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name",
                                "Wife ID", "Wife Name", "Child"]

    for individual in individuals:  # add individual info to the table
        individual_table.add_row(individual.info())

    for family in families:  # add individual info to the table
        family_table.add_row(family.info(individuals))

    print("Individuals\n", individual_table, sep="")
    print("Families\n", family_table, sep="", end='\n\n')


def generate_classes(lines: List[str]) -> Tuple[List[Individual], List[Family]]:
    """ get lines read from a .ged file """
    individuals: List[Individual] = []
    families: List[Family] = []
    current_record: Optional[Individual, Family] = None
    current_tag: Optional[str] = None

    for line in lines:
        row_fields: List[str] = line.rstrip("\n").split(' ', 2)
        pattern_type = pattern_finder(line)
        if pattern_type == 'ZERO_1':
            current_record = Individual() if row_fields[2] == 'INDI' else Family()
            (individuals if isinstance(current_record, Individual) else families) \
                .append(current_record)
            current_record.id = row_fields[1]
        elif pattern_type == 'ZERO_2':
            pass  # nothing to do with this
        elif pattern_type == 'NO_ARGUMENT':
            if row_fields[0] == '1':
                setattr(current_record, row_fields[1].lower(), {})
                current_tag = row_fields[1].lower()
        elif pattern_type == 'ARGUMENT':
            if row_fields[0] == '1':
                if isinstance(getattr(current_record, row_fields[1].lower()), list):
                    current_list = getattr(current_record, row_fields[1].lower()) + [row_fields[2]]
                    setattr(current_record, row_fields[1].lower(), current_list)
                else:
                    setattr(current_record, row_fields[1].lower(), row_fields[2])
            elif row_fields[0] == '2':
                setattr(current_record, current_tag, {row_fields[1].lower(): row_fields[2]})

    return individuals, families


def findParents(id: int, listFam: List) -> str:
    found: str = ""
    for fam in listFam:
        if id in fam.chil:
            found: str = fam
            break
    return found


def checkIfSiblings(fam1: List, fam2: List, listFam: List) -> bool:
    """just makes sure siblings aren't married, if they are return false"""
    if fam1.id == fam2.id:
        return False
    husb1fam: str = findParents(fam1.husb, listFam)
    husb2fam: str = findParents(fam2.husb, listFam)
    wife1fam: str = findParents(fam1.wife, listFam)
    wife2fam: str = findParents(fam2.wife, listFam)

    if husb1fam:
        if husb2fam:
            if husb1fam.id == husb2fam.id:
                return True
        elif wife2fam:
            if husb1fam.id == wife2fam.id:
                return True
    elif wife1fam:
        if husb2fam:
            if wife1fam.id == husb2fam.id:
                return True
        elif wife2fam:
            if wife1fam.id == wife2fam.id:
                return True

    return False


def main():
    """ the main function to check the data """
    path: str = "SSW555-P1-fizgi.ged"
    lines = get_lines(path)  # process the file
    individuals, families = generate_classes(lines)
    individuals.sort(key=operator.attrgetter('id'))  # sort Individual class list by ID
    families.sort(key=operator.attrgetter('id'))  # sort Family class list by ID
    pretty_print(individuals, families)

    us.list_of_twins(families[0], individuals)


if __name__ == '__main__':
    main()
