""" Implement test cases for user stories

    date: 30-Sep-2020
    python: v3.8.4
"""
import datetime
import unittest
from typing import List, Dict

import user_stories
import user_stories as us
from models import Individual, Family


class TestApp(unittest.TestCase):
    """ test class of the methods """

    def test_were_parents_over_14(self):
        """ test were_parents_over_14 method """
        # husband is 20 and wife is 14 at the marriage date -> Both are over 14 -> True
        husband: Individual = Individual(_id="I0", birt={'date': "19 SEP 1995"})
        wife: Individual = Individual(_id="I1", birt={'date': "3 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F0", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2015"})
        self.assertTrue(us.were_parents_over_14(family, individuals))

        # husband 11, wife 20 -> Only wife is over 14 -> False
        husband: Individual = Individual(_id="I2", birt={'date': "2 MAR 2007"})
        wife: Individual = Individual(_id="I3", birt={'date': "11 FEB 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2019"})
        self.assertFalse(us.were_parents_over_14(family, individuals))

        # husband 17, wife 10 -> Only husband is over 14 -> False
        husband: Individual = Individual(_id="I4", birt={'date': "22 AUG 2000"})
        wife: Individual = Individual(_id="I5", birt={'date': "5 DEC 2007"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2018"})
        self.assertFalse(us.were_parents_over_14(family, individuals))

        # husband 12, wife 12 -> Both are under 14 -> False
        husband: Individual = Individual(_id="I6", birt={'date': "19 SEP 2007"})
        wife: Individual = Individual(_id="I7", birt={'date': "3 JAN 2008"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 2020"})
        self.assertFalse(us.were_parents_over_14(family, individuals))

        # husband 18, wife 16 -> Both are over 14 -> True
        husband: Individual = Individual(_id="I8", birt={'date': "7 FEB 1980"})
        wife: Individual = Individual(_id="I9", birt={'date': "8 FEB 1982"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id,
                                marr={'date': "11 FEB 1998"})
        self.assertTrue(us.were_parents_over_14(family, individuals))

    def test_birth_before_death_of_parents(self):
        """ test birth_before_death_of_parents method """
        # mother and father are alive (no death date)
        husband: Individual = Individual(_id="I0")
        wife: Individual = Individual(_id="I1")
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F0", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(us.birth_before_death_of_parents(family, individuals))

        # child born on: mother death, 270 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "8 JAN 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "4 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(us.birth_before_death_of_parents(family, individuals))

        # child born on: 1 day before mother death, 1 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "3 OCT 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "5 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "4 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertTrue(us.birth_before_death_of_parents(family, individuals))

        # child born on: after mother death, 10 day after father death
        husband: Individual = Individual(_id="I0", deat={'date': "3 OCT 2000"})
        wife: Individual = Individual(_id="I1", deat={'date': "12 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "13 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertFalse(us.birth_before_death_of_parents(family, individuals))

        # child born on: before mother death, 1 year after father death
        husband: Individual = Individual(_id="I0", deat={'date': "11 OCT 1999"})
        wife: Individual = Individual(_id="I1", deat={'date': "12 OCT 2000"})
        child: Individual = Individual(_id="I2", birt={'date': "11 OCT 2000"})
        individuals: List[Individual] = [husband, wife, child]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id)
        family.chil.append(child.id)
        self.assertFalse(us.birth_before_death_of_parents(family, individuals))

    def test_fewer_than_15_siblings(self):
        husband: Individual = Individual(_id="I0")
        wife: Individual = Individual(_id="I1")
        child1: Individual = Individual(_id="I2")
        child2: Individual = Individual(_id="I3")
        child3: Individual = Individual(_id="I4")
        child4: Individual = Individual(_id="I5")
        child5: Individual = Individual(_id="I6")
        child6: Individual = Individual(_id="I7")
        child7: Individual = Individual(_id="I8")
        child8: Individual = Individual(_id="I9")
        child9: Individual = Individual(_id="I10")
        child10: Individual = Individual(_id="I12")
        child11: Individual = Individual(_id="I13")
        child12: Individual = Individual(_id="I14")
        child13: Individual = Individual(_id="I15")
        child14: Individual = Individual(_id="I16")
        child15: Individual = Individual(_id="I17")
        family: Family = Family(husb=husband.id, wife=wife.id)
        family.chil.extend([child1.id, child2.id, child3.id, child4.id, child5.id, child6.id,
                            child7.id, child8.id, child9.id, child10.id, child11.id, child12.id,
                            child13.id, child14.id, child15.id])
        self.assertFalse(us.fewer_than_15_siblings(family))

        family: Family = Family(husb=husband.id, wife=wife.id)
        family.chil.extend([child1.id, child2.id, child3.id, child4.id, child5.id, child6.id])
        self.assertTrue(us.fewer_than_15_siblings(family))

    def test_male_last_names(self):
        husband: Individual = Individual(_id="I0", name="Pablo /Escobar/", sex='M')
        wife: Individual = Individual(_id="I1", name="Veronika /Esco/", sex='F')
        child1: Individual = Individual(_id="I2", name="Terry /Escobart/", sex='M')
        child2: Individual = Individual(_id="I3", name="Maria /Escobar/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I112", name="Naal /Wagas/", sex='M')
        wife: Individual = Individual(_id="I22", name="Veron /Wagadi/", sex='F')
        child1: Individual = Individual(_id="I33", name="Ter /Wagada/", sex='M')
        child2: Individual = Individual(_id="I44", name="Mara /Wagadi/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I9", name="Eden /Hazard/", sex='M')
        wife: Individual = Individual(_id="I99", name="Veva /Hazard/", sex='F')
        child1: Individual = Individual(_id="I999", name="JR /Hazard/", sex='M')
        child2: Individual = Individual(_id="I9999", name="SR /Hazard/", sex='M')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertTrue(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I07", name="Reese /Walter/", sex='M')
        wife: Individual = Individual(_id="I177", name="Monica /Walter/", sex='F')
        child1: Individual = Individual(_id="I277", name="Malcom /Walter/", sex='M')
        child2: Individual = Individual(_id="I377", name="Hal /Walters/", sex='M')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertFalse(us.male_last_names(family, individuals))

        husband: Individual = Individual(_id="I007", name="Elon /Drogba/", sex='M')
        wife: Individual = Individual(_id="I1008", name="Emma /Drogba/", sex='F')
        child1: Individual = Individual(_id="I2009", name="Agua /Drogba/", sex='F')
        child2: Individual = Individual(_id="I3000", name="Win /Drogbaaa/", sex='F')
        family = Family(husb=husband.id, wife=wife.id)
        family.chil = [child1.id, child2.id]
        individuals = [husband, wife, child1, child2]
        self.assertTrue(us.male_last_names(family, individuals))

    def test_marriage_before_death(self):
        husband: Individual = Individual(_id="I0", deat={'date': "1 JAN 2020"})
        wife: Individual = Individual(_id="I1", deat={'date': "2 JAN 2019"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 1999"})
        self.assertTrue(us.marriage_before_death(family, individuals))

        """Husband and wife they both die before their marriage so False (not possible)"""
        husband: Individual = Individual(_id="I2", deat={'date': "1 JAN 2000"})
        wife: Individual = Individual(_id="I3", deat={'date': "2 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertFalse(us.marriage_before_death(family, individuals))

        """ Husband dies before marriage wife is alive so False (not possible)"""
        husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2000"})
        wife: Individual = Individual(_id="I5")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertFalse(us.marriage_before_death(family, individuals))

        """ Husband dies after marriage and  wife is alive so true"""
        husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2002"})
        wife: Individual = Individual(_id="I5")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertTrue(us.marriage_before_death(family, individuals))

        """Wife dies before marriage and Husband is alive so False (not possible)"""
        husband: Individual = Individual(_id="I6")
        wife: Individual = Individual(_id="I7", deat={'date': "1 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertFalse(us.marriage_before_death(family, individuals))

        """Wife dies after marriage and Husband is alive so true"""
        husband: Individual = Individual(_id="I8")
        wife: Individual = Individual(_id="I9", deat={'date': "1 JAN 2002"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2001"})
        self.assertTrue(us.marriage_before_death(family, individuals))

        """ Husband and wife they both are alive no daeth date is found so false"""
        husband: Individual = Individual(_id="I10")
        wife: Individual = Individual(_id="I11")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, marr={'date': "11 FEB 2002"})
        self.assertFalse(us.marriage_before_death(family, individuals))

    def test_divorce_before_death(self):
        husband: Individual = Individual(_id="I0", deat={'date': "1 JAN 2020"})
        wife: Individual = Individual(_id="I1", deat={'date': "2 JAN 2019"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 1999"})
        self.assertTrue(us.divorce_before_death(family, individuals))

        """Husband and wife they both die before their divorce so False (not possible)"""
        husband: Individual = Individual(_id="I2", deat={'date': "1 JAN 2000"})
        wife: Individual = Individual(_id="I3", deat={'date': "2 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
        self.assertFalse(us.divorce_before_death(family, individuals))

        """ Husband dies before divorce wife is alive so False (not possible)"""
        husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2000"})
        wife: Individual = Individual(_id="I5")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
        self.assertFalse(us.divorce_before_death(family, individuals))

        """ Husband dies after divorce and  wife is alive so true"""
        husband: Individual = Individual(_id="I4", deat={'date': "1 JAN 2002"})
        wife: Individual = Individual(_id="I5")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
        self.assertTrue(us.divorce_before_death(family, individuals))

        """Wife dies before divorce and Husband is alive so False (not possible)"""
        husband: Individual = Individual(_id="I6")
        wife: Individual = Individual(_id="I7", deat={'date': "1 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
        self.assertFalse(us.divorce_before_death(family, individuals))

        """Wife dies after divorce and Husband is alive so true"""
        husband: Individual = Individual(_id="I8")
        wife: Individual = Individual(_id="I9", deat={'date': "1 JAN 2002"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2001"})
        self.assertTrue(us.divorce_before_death(family, individuals))

        """ Husband and wife they both are alive no divorce date is found so false"""
        husband: Individual = Individual(_id="I10")
        wife: Individual = Individual(_id="I11")
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(husb=husband.id, wife=wife.id, div={'date': "11 FEB 2002"})
        self.assertFalse(us.divorce_before_death(family, individuals))

    def test_checkForOldParents(self):
        """Test cases for checking parents are old or not US12"""
        f = open("Output.txt", "a+")
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}
        fam2: Dict = {'F23': {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                              'CHIL': ['I19']}}

        ind1: Dict = {'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1900', 'sex': 'M',
                              'family': 'F23',
                              'DEAT': '31 DEC 2013'},
                      'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1902',
                              'sex': 'F',
                              'family': 'F23',
                              'DEAT': '31 DEC 2013'},
                      'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1999',
                              'sex': 'M', 'family': 'F23',
                              'DEAT': '31 DEC 2013'}}

        ind2: Dict = {'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M',
                              'family': 'F23',
                              'DEAT': '31 DEC 2013'},
                      'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960',
                              'sex': 'F',
                              'family': 'F23'},
                      'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981',
                              'sex': 'M', 'family': 'F23'},
                      'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981',
                              'sex': 'F', 'family': 'F23'},
                      'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                              'family': 'F23'},
                      'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                              'family': 'F23'},
                      'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981',
                              'sex': 'F',
                              'family': 'F23'}}

        self.assertTrue(us.checkForOldParents(fam, ind2, f))
        self.assertFalse(us.checkForOldParents(fam2, ind1, f))

    def test_checkBigamy(self):
        """Test cases for bigamy"""

        # No Bigamy
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}

        indi: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M',
                    'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                    'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                    'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        # bigamy (same husband)
        fam2: Dict = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'HUSB': 'I01'}}

        indi2: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M',
                    'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                    'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                    'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        # bigamy (same wife)
        fam3: Dict = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'WIFE': 'I07'}}

        indi3: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M',
                    'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                    'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M',
                    'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        us.checkBigamy(fam)
        self.assertTrue(('I01' in indi))
        self.assertTrue(('I01' == fam['F23']['HUSB']))
        us.checkBigamy(fam2)
        self.assertTrue(('I01' in indi2))
        self.assertTrue(('I01' in fam2['F23']['HUSB']))
        us.checkBigamy(fam3)
        self.assertTrue(('I07' in indi3))
        self.assertTrue(('WIFE' in fam3['F23']))

    def test_birth_before_marriage_of_parents(self):
        individual = Individual(_id="I20", birt={'date': "11 nov 2008"})
        family = Family(_id="I21", marr={'date': "10 jan 2008"}, div={'date': "15 JAN 2009"})
        self.assertTrue(us.birth_before_marriage_of_parents(family, individual))

        individual = Individual(_id="I20", birt={'date': "11 nov 2009"})
        family = Family(_id="I21", marr={'date': "10 may 2008"}, div={'date': "15 jul 2008"})
        self.assertFalse(us.birth_before_marriage_of_parents(family, individual))

        individual = Individual(_id="I20", birt={'date': "12  dec 2009"})
        family = Family(_id="I21", marr={'date': "11 may 2008"}, div={'date': "15 sep 2008"})
        self.assertFalse(us.birth_before_marriage_of_parents(family, individual))

        individual = Individual(_id="I20", birt={'date': "12  dec 2009"})
        family = Family(_id="I21", marr={'date': "11 may 2009"}, div={'date': "15 sep 2009"})
        self.assertTrue(us.birth_before_marriage_of_parents(family, individual))

    def test_less_than_150(self):
        individual = Individual(birt={'date': "20 Mar 1985"})
        individual.deat = {'date': "15 Aug 2008"}
        self.assertTrue(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 JAN 2000"})
        self.assertTrue(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 Feb 2012"})
        individual.deat = {'date': "21 JAN 2000"}
        self.assertFalse(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 JAN 1500"})
        self.assertFalse(us.less_than_150(individual))

        individual = Individual(birt={'date': "15 JAN 2006"})
        individual.deat = {'date': "15 JAN 1200"}
        self.assertFalse(us.less_than_150(individual))

    def test_dates_before_current(self):
        family = Family(_id="I21",
                        marr={'date': "15 JAN 2019"})  ##marrige date is before current date so result is true
        self.assertTrue(us.marriage(family))

        family = Family(_id="I22", div={'date': "15 JAN 2020"})  ##divorse date is before current date so result is true
        self.assertTrue(us.divo(family))

        Indi = Individual(_id="I23",
                          birt={'date': "15 JAN 2021"})  ##Birth date is after current date so result is false
        self.assertFalse(us.birth(Indi))

        Indi = Individual(_id="I24",
                          deat={'date': "15 JAN 2021"})  ##death date is after current date so result is false
        self.assertFalse(us.death(Indi))

        Indi = Individual(_id="I26",
                          birt={'date': "15 JAN 2020"})  ##Birth date is before current date so result is true
        self.assertTrue(us.birth(Indi))

    def test_Birth_before_death(self):
        individual = Individual(_id='I20', birt={'date': "15 JAN 1995"})
        individual.deat = {'date': "15 JAN 1994"}
        self.assertFalse(us.birth_before_death(individual))

        individual = Individual(_id='I21', birt={'date': "15 JAN 1995"})
        individual.deat = {'date': "15 JAN 1996"}
        self.assertTrue(us.birth_before_death(individual))

        individual = Individual(_id='I22', birt={'date': "25 DEC 1996"})
        individual.deat = {'date': "26 DEC 1996"}
        self.assertTrue(us.birth_before_death(individual))

        individual = Individual(_id='I23', birt={'date': "26 dec 1995"})
        individual.deat = {'date': "25 dec 1995"}
        self.assertFalse(us.birth_before_death(individual))

        individual = Individual(_id='I24', birt={'date': "25 JAN 1996"})
        individual.deat = {'date': "25 dec 1997"}
        self.assertTrue(us.birth_before_death(individual))

        individual = Individual(_id='I25', birt={'date': "26 JAN 1997"})
        individual.deat = {'date': "25 dec 1996"}
        self.assertFalse(us.birth_before_death(individual))

        individual = Individual(_id='I26', birt={'date': "26 JAN 1997"})
        self.assertTrue(us.birth_before_death(individual))

    def test_marriage_before_divorce(self):
        family = Family(_id='I20', marr={'date': "15 JAN 1995"})
        family.div = {'date': "15 JAN 1994"}
        self.assertFalse(us.marriage_before_divorce(family))

        family = Family(_id='I21', marr={'date': "15 JAN 1995"})
        family.div = {'date': "15 JAN 1996"}
        self.assertTrue(us.marriage_before_divorce(family))

        family = Family(_id='I22', marr={'date': "25 DEC 1996"})
        family.div = {'date': "26 dec 1996"}
        self.assertTrue(us.marriage_before_divorce(family))

        family = Family(_id='I23', marr={'date': "26 DEC 1996"})
        family.div = {'date': "25 dec 1996"}
        self.assertFalse(us.marriage_before_divorce(family))

        family = Family(_id='I24', marr={'date': "25 jan 1996"})
        family.div = {'date': "25 dec 1997"}
        self.assertTrue(us.marriage_before_divorce(family))

        family = Family(_id='I25', marr={'date': "26 jan 1997"})
        family.div = {'date': "25 dec 1996"}
        self.assertFalse(us.marriage_before_divorce(family))

        family = Family(_id='I26', marr={'date': "26 jan 1997"})
        self.assertTrue(us.marriage_before_divorce(family))

    def test_Birth_before_mrg(self):
        indi = Individual(_id="I20", birt={'date': "15 JAN 2020"})
        family = Family(
            marr={'date': "15 JAN 2019"})  # marrige date is before birth date so result is fasle
        self.assertFalse(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I21", birt={'date': "5 JUL 2000"})
        family = Family(
            marr={'date': "1 JAN 2010"})  # marrige date is after birth date so result is true
        self.assertTrue(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I22", birt={'date': "7 JUN 2000"})
        family = Family(
            marr={'date': "9 JAN 1995"})  # marrige date is before birth date so result is false
        self.assertFalse(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I23", birt={'date': "15 MAY 1989"})
        family = Family(
            marr={'date': "15 FEB 2000"})  # marrige date is after birth date so result is true
        self.assertTrue(us.birth_before_mrg(family, indi))

        indi = Individual(_id="I24", birt={'date': "15 JAN 2020"})
        family = Family(marr=None)  # marriage is not take place so result is by default true
        self.assertTrue(us.birth_before_mrg(family, indi))

    def test_verifySiblingsDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1991, 1, 1)
        date3 = datetime.date(1992, 1, 1)
        date4 = datetime.date(1993, 1, 1)
        date5 = datetime.date(1994, 1, 1)
        date6 = datetime.date(1995, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertTrue(user_stories.verifySiblingsDates(siblingsDates))

        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        date4 = datetime.date(1993, 1, 1)
        date5 = datetime.date(1994, 1, 1)
        date6 = datetime.date(1995, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertTrue(user_stories.verifySiblingsDates(siblingsDates))

        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        date4 = datetime.date(1990, 1, 1)
        date5 = datetime.date(1990, 1, 1)
        date6 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertFalse(user_stories.verifySiblingsDates(siblingsDates))

        date1 = datetime.date(1990, 1, 2)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 2)
        date4 = datetime.date(1990, 1, 1)
        date5 = datetime.date(1990, 1, 1)
        date6 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3, date4, date5, date6)
        self.assertFalse(user_stories.verifySiblingsDates(siblingsDates))

    def test_alldifferentDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1991, 1, 1)
        date3 = datetime.date(1992, 1, 1)
        siblingsDates = (date1, date2, date3)
        self.assertTrue(user_stories.verifySiblingsSpace(siblingsDates))

    def test_someDifferentDatesSameYear(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 11, 1)
        date3 = datetime.date(1991, 12, 1)
        siblingsDates = (date1, date2, date3)
        self.assertTrue(user_stories.verifySiblingsSpace(siblingsDates))

    def test_allSameDates(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 1)
        siblingsDates = (date1, date2, date3)
        self.assertFalse(user_stories.verifySiblingsSpace(siblingsDates))

    def test_someWithDayDifference(self):
        date1 = datetime.date(1990, 1, 2)
        date2 = datetime.date(1990, 1, 1)
        date3 = datetime.date(1990, 1, 2)
        siblingsDates = (date1, date2, date3)
        self.assertFalse(user_stories.verifySiblingsSpace(siblingsDates))

    def test_someWithMonthsDifference(self):
        date1 = datetime.date(1990, 1, 1)
        date2 = datetime.date(1990, 6, 1)
        date3 = datetime.date(1992, 1, 2)
        siblingsDates = (date1, date2, date3)
        self.assertFalse(user_stories.verifySiblingsSpace(siblingsDates))

    def test_correct_gender_for_role(self):
        """ test correct_gender_for_role method """
        # husband is Male, wife is Female
        husband: Individual = Individual(_id="I0", sex='M')
        wife: Individual = Individual(_id="I1", sex='F')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F0', husb=husband.id, wife=wife.id)
        self.assertTrue(us.correct_gender_for_role(family, individuals))

        # husband is Male, wife is Male
        husband: Individual = Individual(_id="I0", sex='M')
        wife: Individual = Individual(_id="I1", sex='M')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F1', husb=husband.id, wife=wife.id)
        self.assertFalse(us.correct_gender_for_role(family, individuals))

        # husband is Female, wife is Female
        husband: Individual = Individual(_id="I0", sex='F')
        wife: Individual = Individual(_id="I1", sex='F')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F2', husb=husband.id, wife=wife.id)
        self.assertFalse(us.correct_gender_for_role(family, individuals))

        # husband is Female, wife is Male
        husband: Individual = Individual(_id="I0", sex='F')
        wife: Individual = Individual(_id="I1", sex='M')
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id='F3', husb=husband.id, wife=wife.id)
        self.assertFalse(us.correct_gender_for_role(family, individuals))

    def test_unique_ids(self):
        """ test unique_ids method """
        husband1: Individual = Individual(_id="I0")
        wife1: Individual = Individual(_id="I1")
        child1: Individual = Individual(_id="I2")
        child2: Individual = Individual(_id="I3")
        family1: Family = Family(_id='F0', husb=husband1.id, wife=wife1.id)

        husband2: Individual = Individual(_id="I4")
        wife2: Individual = Individual(_id="I5")
        child3: Individual = Individual(_id="I6")
        child4: Individual = Individual(_id="I7")
        family2: Family = Family(_id='F1', husb=husband2.id, wife=wife2.id)

        individuals = [husband1, wife1, husband2, wife2, child1, child2, child3, child4]
        families = [family1, family2]

        self.assertTrue(us.unique_ids(families, individuals))

        husband1: Individual = Individual(_id="I0")
        wife1: Individual = Individual(_id="I1")
        child1: Individual = Individual(_id="I3")
        child2: Individual = Individual(_id="I3")
        family1: Family = Family(_id='F0', husb=husband1.id, wife=wife1.id)

        husband2: Individual = Individual(_id="I4")
        wife2: Individual = Individual(_id="I5")
        child3: Individual = Individual(_id="I6")
        child4: Individual = Individual(_id="I7")
        family2: Family = Family(_id='F0', husb=husband2.id, wife=wife2.id)

        individuals = [husband1, wife1, husband2, wife2, child1, child2, child3, child4]
        families = [family1, family2]

        self.assertFalse(us.unique_ids(families, individuals))

    def test_order_sibling_by_age(self):
        child1: Individual = Individual(_id="I2", birt={'date': "14 OCT 2010"})
        child2: Individual = Individual(_id="I22", birt={'date': "24 OCT 2019"})
        child3: Individual = Individual(_id="I222", birt={'date': "30 OCT 2015"})
        child4: Individual = Individual(_id="I2222", birt={'date': "5 OCT 2009"})
        child5: Individual = Individual(_id="I22222", birt={'date': "6 OCT 2005"})
        individuals: List[Individual] = [child1, child2, child3, child4, child5]
        family: Family = Family(_id="F0")
        family.chil.extend([child1.id, child2.id, child3.id, child4.id, child5.id])
        self.assertEqual(us.order_sibling_by_age(family, individuals),
                         [child5, child4, child1, child3, child2])

        child1: Individual = Individual(_id="I3", birt={'date': "1 OCT 2016"})
        child2: Individual = Individual(_id="I4", birt={'date': "2 OCT 2015"})
        child3: Individual = Individual(_id="I5", birt={'date': "3 OCT 2014"})
        child4: Individual = Individual(_id="I6", birt={'date': "4 OCT 2013"})
        child5: Individual = Individual(_id="I7", birt={'date': "5 OCT 2012"})
        individuals: List[Individual] = [child1, child2, child3, child4, child5]
        family: Family = Family(_id="F0")
        family.chil.extend([child1.id, child2.id, child3.id, child4.id, child5.id])
        self.assertEqual(us.order_sibling_by_age(family, individuals),
                         [child5, child4, child3, child2, child1])

    def test_individual_ages(self):
        indi1: Individual = Individual(birt={'date': "14 OCT 1990"})
        indi2: Individual = Individual(birt={'date': "24 OCT 1991"})
        indi3: Individual = Individual(birt={'date': "4 OCT 1992"})
        indi4: Individual = Individual(birt={'date': "5 OCT 1993"})
        indi5: Individual = Individual(birt={'date': "6 OCT 2000"})
        indi6: Individual = Individual(birt={'date': "7 OCT 1999"})
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5, indi6]
        self.assertEqual(us.individual_ages(individuals), [30, 29, 28, 27, 20, 21])

        indi1: Individual = Individual(birt={'date': "1 OCT 2000"})
        indi2: Individual = Individual(birt={'date': "2 OCT 2001"})
        indi3: Individual = Individual(birt={'date': "3 OCT 2002"})
        indi4: Individual = Individual(birt={'date': "4 OCT 2003"})
        indi5: Individual = Individual(birt={'date': "5 OCT 2004"})
        indi6: Individual = Individual(birt={'date': "6 OCT 2005"})
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5, indi6]
        self.assertEqual(us.individual_ages(individuals), [20, 19, 18, 17, 16, 15])

        indi1: Individual = Individual(birt={'date': "14 OCT 2016"})
        indi2: Individual = Individual(birt={'date': "24 OCT 2015"})
        indi3: Individual = Individual(birt={'date': "4 OCT 2014"})
        indi4: Individual = Individual(birt={'date': "5 OCT 2013"})
        indi5: Individual = Individual(birt={'date': "6 OCT 2012"})
        indi6: Individual = Individual(birt={'date': "7 OCT 2011"})
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5, indi6]
        self.assertEqual(us.individual_ages(individuals), [4, 5, 6, 7, 8, 9])

    def test_firstCousinShouldNotMarry(self):
        """Test Cases for User Story 19"""
        errorList: List = us.firstCousinShouldNotMarry()
        for fam in errorList:
            print(
                "ERROR: FAMILY: US19: In Family id " + fam.id + " Husband " + fam.husb + "Married to first cousin, "
                                                                                         "Wife " + fam.wife)
        self.assertTrue(len(errorList) == 0, "US19: No first cousins are married!")

    def test_auntsAndUncle(self):
        errorList: List = us.auntsAndUncle()
        for fam in errorList:
            print(
                "ERROR: FAMILY: US20: " + fam.id + " Marriage is between Aunt/Uncle and Niece/Nephew!")
        self.assertTrue(len(errorList) == 0,
                        "US20: Marriages are correct and no one is married to an Aunt or Uncle!")

    def test_hasMultipleBirths(self):
        birthdate1 = datetime.now()
        birthdate2 = datetime(2009, 10, 5, 18, 00)
        self.assertFalse(user_stories.hasMultipleBirths([birthdate1, birthdate2]))

    def test_hasMultipleBirths(self):
        birthdate1 = datetime.datetime.now()
        birthdate2 = datetime.datetime.now()
        birthdate3 = datetime.datetime(2009, 10, 5, 18, 00)
        self.assertTrue(user_stories.hasMultipleBirths([birthdate1, birthdate2, birthdate3]))

    def test_isSingleAliveOver30(self):
        ind = user_stories.isSingleAliveOver30()
        # ind.age = 31
        ind.alive = True
        self.assertTrue(ind)

    def test_isSingleAliveOver30(self):
        ind = user_stories.isSingleAliveOver30()

        self.assertFalse(ind)

    # User_Story_Testcases_17
    def test_no_parents_marry_child(self):

        """All have unique ids so no inter marriage in family so true"""
        husband = "I0"
        wife = "I1"
        child = "I2"
        families: List[Family] = [husband, wife, [child]]
        self.assertTrue(us.no_parents_marry_child(families))

        """All have unique ids so no inter marriage in family so true"""
        husband = "I21"
        wife = "I22"
        child = "I23"
        families: List[Family] = [husband, wife, [child]]
        self.assertTrue(us.no_parents_marry_child(families))

        """ Husband(father) and child have same ids so not allowed so False"""
        husband = "I17"
        wife = "I18"
        child = "I17"
        families: List[Family] = [husband, wife, [child]]
        self.assertFalse(us.no_parents_marry_child(families))

        """ Wife(Mother) and child have same ids so not allowed so False"""
        husband = "I17"
        wife = "I18"
        child = "I18"
        families: List[Family] = [husband, wife, [child]]
        self.assertFalse(us.no_parents_marry_child(families))

        """All three have same ids not allowed so False"""
        husband = "I7"
        wife = "I7"
        child = "I7"
        families: List[Family] = [husband, wife, [child]]
        self.assertFalse(us.no_parents_marry_child(families))

    # User_Story_Testcases_18
    def test_no_sibilings_can_marry(self):

        """All have unique ids so no inter marriage in family so true"""
        husband = "I0"
        wife = "I1"
        child1 = "I2"
        child2 = "I3"
        families: List[Family] = [husband, wife, [child1], [child2]]
        self.assertTrue(us.no_sibilings_can_marry(families))

        """All have unique ids so no inter marriage in family so true"""
        husband = "I17"
        wife = "I18"
        child1 = "I19"
        child2 = "I20"
        families: List[Family] = [husband, wife, [child1], [child2]]
        self.assertTrue(us.no_sibilings_can_marry(families))

        """ Husband(father) and child have same ids so not allowed so False"""  # Cousins Family
        husband = "I0"
        wife = "I1"
        child1 = "I4"
        child2 = "I0"
        families: List[Family] = [husband, wife, [child1], [child2]]
        self.assertFalse(us.no_sibilings_can_marry(families))

        """ Wife(Mother) and child have same ids so not allowed so False"""  # Cousins family
        husband = "I21"
        wife = "I22"
        child1 = "I22"
        child2 = "I23"
        families: List[Family] = [husband, wife, [child1], [child2]]
        self.assertFalse(us.no_sibilings_can_marry(families))

        """ Sibilings marry with each other so False"""
        husband = "I21"
        wife = "I25"
        child1 = "I26"
        child2 = "I26"
        families: List[Family] = [husband, wife, [child1], [child2]]
        self.assertFalse(us.no_sibilings_can_marry(families))

    def test_AreIndividualsUnique(self):
        indi1: Individual = Individual(_id="I1", name="John Doe", birt={'date': "14 OCT 1990"})
        indi2: Individual = Individual(_id="I2", name="John Doe", birt={'date': "14 OCT 1990"})
        indi3: Individual = Individual(_id="I3", name="Nidhi Patel", birt={'date': "1 OCT 1998"})
        indi4: Individual = Individual(_id="I4", name="Patrik Kim", birt={'date': "4 NOV 2000"})
        indi5: Individual = Individual(_id="I5", name="John Hill", birt={'date': "11 JAN 2010"})
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5]
        self.assertEqual(us.AreIndividualsUnique(individuals), [["I2", "John Doe", "14 OCT 1990"]])

    def test_uniqueFamilyBySpouses(self):
        fam1: Family = Family(_id="I1", husb="John Doe1", wife="jennifer Doe1",
                              marr={'date': "14 OCT 1993"})
        fam2: Family = Family(_id="I2", husb="John Doe1", wife="jennifer Doe1",
                              marr={'date': "14 OCT 1993"})
        fam3: Family = Family(_id="I3", husb="Anurag Kim", wife="Emma Green",
                              marr={'date': "1 OCT 1998"})
        fam4: Family = Family(_id="I4", husb="Shrey Hill", wife="Olivia Kim",
                              marr={'date': "4 NOV 2000"})
        fam5: Family = Family(_id="I5", husb="Parthik Smith", wife="Sophia Taylor",
                              marr={'date': "11 JAN 2010"})
        families: List[Family] = [fam1, fam2, fam3, fam4, fam5]
        self.assertEqual(us.uniqueFamilyBySpouses(families),
                         [["I2", "John Doe1", "jennifer Doe1", "14 OCT 1993"]])

    # Test case for User Story 26
    def test_FamilyChildDoesNotExist(self):
        fam = Family()
        fam._id = "@FAM"
        fam.chil.append("@testchild")
        famDict = {}
        famDict[fam._id] = fam
        individualDict = {}
        self.assertFalse(us.validateCorrespondingRecords(individualDict, famDict))

    # Test cases for user story 25
    def test_first_names_unique(self):

        father_1 = Individual()
        father_1._id = "F1"
        father_1.name = "James Jonas Jamison"

        mother_1 = Individual()
        mother_1._id = "M1"
        mother_1.name = "Janet Judy Jamison"

        # Generation 2 - Children
        child_1 = Individual()
        child_1._id = "C1"
        child_1.name = "Jacob Jarad Jamison"

        child_2 = Individual()
        child_2._id = "C2"
        child_2.name = "Jessica Joyce Jamison"

        child_3 = Individual()
        child_3._id = "C3"
        child_3.name = "Jenny Jackson Jamison"

        # Family
        family_1 = Family()
        family_1._id = "G1F1"
        family_1.husb = father_1._id
        family_1.wife = mother_1._id
        family_1.chil.append(child_1._id)
        family_1.chil.append(child_2._id)
        family_1.chil.append(child_3._id)

        individuals_dict = {}
        individuals_dict[child_1._id] = child_1
        individuals_dict[child_2._id] = child_2
        individuals_dict[child_3._id] = child_3
        self.assertTrue(us.are_child_names_unique(family_1, individuals_dict))

        father_1 = Individual()
        father_1._id = "F1"
        father_1.name = "James Jonas Jamison"
        father_1.birt = "1 JAN 1910"

        mother_1 = Individual()
        mother_1._id = "M1"
        mother_1.name = "Janet Judy Jamison"
        mother_1.birt = "1 feb 1920"

        # Generation 2 - Children
        child_1 = Individual()
        child_1._id = "C1"
        child_1.name = "Jacob Jarad Jamison"
        child_1.birt = "3 feb 1955"

        child_2 = Individual()
        child_2._id = "C2"
        child_2.name = "Jacob J Jamison"
        child_2.birt = "3 feb 1955"

        child_3 = Individual()
        child_3._id = "C3"
        child_3.name = "Jenny Jackson Jamison"
        child_3.birt = "3 feb 1960"

        # Family 
        family_1 = Family()
        family_1._id = "G1F1"
        family_1.husb = father_1._id
        family_1.wife = mother_1._id
        family_1.chil.append(child_1._id)
        family_1.chil.append(child_2._id)
        family_1.chil.append(child_3._id)

        individuals_dict = {}
        individuals_dict[child_1._id] = child_1
        individuals_dict[child_2._id] = child_2
        individuals_dict[child_3._id] = child_3

        self.assertFalse(us.are_child_names_unique(family_1, individuals_dict))

    def test_deceased(self):
        indi1: Individual = Individual(name="John Doe1",
                                       birt={'date': "14 OCT 1990"}, deat={'date': "14 OCT 1991"})
        indi2: Individual = Individual(name="John Doe2", birt={'date': "14 OCT 1990"})
        indi3: Individual = Individual(name="John Doe3",
                                       birt={'date': "14 OCT 1990"}, deat={'date': "4 OCT 1994"})
        indi4: Individual = Individual(name="John Doe4", birt={'date': "14 OCT 1990"})
        indi5: Individual = Individual(name="John Doe5", birt={'date': "14 OCT 1990"})
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5]
        self.assertEqual(us.deceased(individuals), ["John Doe1", "John Doe3"])

    def test_living_marr(self):
        indi1: Individual = Individual(_id="I1", name="John Doe1", alive=False)
        family1: Family = Family(_id="I1", marr={"14 OCT 1992"})

        indi2: Individual = Individual(_id="I2", name="John Doe2", alive=False)
        family2: Family = Family(_id="I2", marr={"14 OCT 1992"})

        indi3: Individual = Individual(_id="I3", name="John Doe3")
        family3: Family = Family(_id="I3", marr={"14 OCT 1991"}, div={"14 OCT 1990"})

        indi4: Individual = Individual(_id="I4", name="John Doe3")
        family4: Family = Family(_id="I4", marr={"14 OCT 1992"})

        indi5: Individual = Individual(_id="I5", name="John Doe5")
        family5: Family = Family(_id="I5", marr={"14 OCT 1992"}, div={"14 OCT 1995"})

        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5]
        fam: List[Family] = [family1, family2, family3, family4, family5]
        self.assertEqual(us.living_marr(fam, individuals), ["I4"])

    def test_aunt_uncle_birth_year(self):
        """ test aunt_uncle_birth_year method """
        husband: Individual = Individual(_id="I0", birt={'date': "19 SEP 1995"}, sex='M')
        wife: Individual = Individual(_id="I1", birt={'date': "3 JAN 2000"}, sex='F')
        family0: Family = Family(_id="F0", husb=husband.id, wife=wife.id)

        uncle: Individual = Individual(_id="I2", birt={'date': "19 SEP 2001"}, sex='M')
        family1: Family = Family(_id="F1")
        family1.chil = [husband.id, uncle.id]

        aunt: Individual = Individual(_id="I13", birt={'date': "3 JAN 2001"}, sex='F')
        family2: Family = Family(_id="F2", husb=husband.id, wife=wife.id)
        family2.chil = [wife.id, aunt.id]

        individuals: List[Individual] = [husband, wife, aunt, uncle]
        families: List[Family] = [family0, family1, family2]

        self.assertEqual(us.aunt_uncle_birth_year(families, individuals), [('I13', 'I2')])

    def test_all_dead_people(self):
        """ test test_all_dead_people method """
        indi1: Individual = Individual(name="Name /Surname/ 1",
                                       birt={'date': "14 OCT 1990"}, deat={'date': "14 OCT 1991"})
        indi2: Individual = Individual(name="Name /Surname/ 2", birt={'date': "14 OCT 1990"})
        indi3: Individual = Individual(name="Name /Surname/ 3",
                                       birt={'date': "14 OCT 1990"}, deat={'date': "4 OCT 1994"})
        indi4: Individual = Individual(name="Name /Surname/ 4", birt={'date': "14 OCT 1990"})
        indi5: Individual = Individual(name="Name /Surname/ 5", birt={'date': "14 OCT 1990"})
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5]
        self.assertEqual(us.all_dead_people(individuals), ["Name /Surname/ 1", "Name /Surname/ 3"])

    def test_reject_illegal_dates(self):
        """ Test cases for US42 --- Reject Illegal date"""
        self.assertTrue(us.reject_illegal_dates('2/10/2020'), True)
        self.assertTrue(us.reject_illegal_dates('6/30/2020'), True)

        self.assertFalse(us.reject_illegal_dates('2/30/2020'), False)
        self.assertFalse(us.reject_illegal_dates('6/32/2020'), False)

    def testPartialDates(self):
        fam3: Dict = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'WIFE': 'I07'}}
        indi3: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 JUL 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 FEB 1981', 'sex': 'M', 'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': 'FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}

        indi: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1960', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 1981', 'sex': 'M', 'family': 'F23'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}

        self.assertEqual(us.partialDates(indi, fam),
                         ['US41: All Dates Made Valid:',
                          [['I01', '10 15 1960'], ['I01', '31 DEC 2013'], ['I19', '10 13 1981'], ['I32', '10 13 1981']],
                          [['F23', '10 FEB 1980']]])
        self.assertEqual(us.partialDates(indi3, fam3), ['US41: All Dates Already Valid'])

    def test_List_anniversary(self):
        fam1: Family = Family(_id="I1", husb="John Doe1", wife="jennifer Doe1", marr={'date': "1 NOV 2019"})
        fam2: Family = Family(_id="I2", husb="Woody Bing", wife="Billy Smith", marr={'date': "9 NOV 2019"})
        fam3: Family = Family(_id="I3", husb="Anurag Kim", wife="Emma Green", marr={'date': "30 NOV 1978"})
        fam4: Family = Family(_id="I4", husb="Shrey Hill", wife="Olivia Kim", marr={'date': "1 DEC 2019"})
        fam5: Family = Family(_id="I5", husb="Parthik Smith", wife="Sophia Taylor", marr={'date': "2 NOV 2020"})
        fam6: Family = Family(_id="I6", husb="Kamron Geller", wife="Katrina Green")
        families: List[Family] = [fam1, fam2, fam3, fam4, fam5, fam6]
        self.assertTrue(us.List_anniversary(families))

    def test_marriage_date_and_child(self):
        indi1: Individual = Individual(_id="C1", name="John Doe1", birt={'date': "3 FEB 2001"})
        indi2: Individual = Individual(_id="C2", name="Ohn Oka", birt={'date': "3 JAN 2001"})
        family1: Family = Family(_id="M1")
        family1.chil = [indi1.id, indi2.id]
        family1.marr = {'date': "3 JAN 2001"}
        individuals: List[Individual] = [indi1, indi2]
        self.assertEqual(us.marriage_date_and_child(family1, individuals), ['C2'])

    def test_grandparents_marriage_and_grandchildren_marriage(self):
        indi1: Individual = Individual(_id="C1", name="Nino Doe1", birt={'date': "3 FEB 1001"})
        indi2: Individual = Individual(_id="C2", name="Nina Oka", birt={'date': "3 JAN 2001"})
        family: Family = Family(_id='F1', husb=indi1.id, wife=indi2.id)
        individuals: List[Individual] = [indi1, indi2]
        families: List[Family] = [family]
        self.assertEqual(us.grandparents_marriage_and_grandchildren_birthday(families, individuals), ['F1'])

    def test_List_recent_deat(self):

        In1: Individual = Individual(name="Misha", deat={'date': "30 NOV 2020"})
        individuals: List[Individual] = [In1]
        self.assertEqual(us.List_recent_death(individuals), ["Misha"])

        In2: Individual = Individual(name="Nisha", deat={'date': "14 OCT 2019"})
        individuals: List[Individual] = [In2]
        self.assertNotEqual(us.List_recent_death(individuals), ["Nisha"])

        In3: Individual = Individual(name="Lisha", deat={'date': "30 NOV 2020"})
        individuals: List[Individual] = [In3]
        self.assertEqual(us.List_recent_death(individuals), ["Lisha"])

        In4: Individual = Individual(name="Risha", deat={'date': "7 SEP 2020"})
        individuals: List[Individual] = [In4]
        self.assertNotEqual(us.List_recent_death(individuals), ["Risha"])

    def test_List_recent_birth(self):

        In1: Individual = Individual(name="Misha", birt={'date': "20 NOV 2020"})
        individuals: List[Individual] = [In1]
        self.assertEqual(us.List_recent_birth(individuals), ["Misha"])

        In2: Individual = Individual(name="Nisha", birt={'date': "14 OCT 2019"})
        individuals: List[Individual] = [In2]
        self.assertNotEqual(us.List_recent_birth(individuals), ["Nisha"])

        In3: Individual = Individual(name="Lisha", birt={'date': "30 NOV 2020"})
        individuals: List[Individual] = [In3]
        self.assertEqual(us.List_recent_birth(individuals), ["Lisha"])

        In4: Individual = Individual(name="Risha", birt={'date': " 7 SEP 2020"})
        individuals: List[Individual] = [In4]
        self.assertNotEqual(us.List_recent_birth(individuals), ["Risha"])

    def test_all_marr_couple(self):

        hub = Individual(_id="I0")
        wife = Individual(_id="I1")
        fam1 = Family(_id="p1", husb=hub.id, wife=wife.id, marr={"14 Nov 1998"})

        hub1 = Individual(_id="I3")
        wife1 = Individual(_id="I4")
        fam2 = Family(_id="p1", husb=hub1.id, wife=wife1.id)

        hub2 = Individual(_id="I5")
        wife2 = Individual(_id="I6")
        fam3 = Family(_id="p1", husb=hub.id, wife=wife.id, div={"14 Nov 1998"})

        indivi: List[Individual] = [hub, wife, hub1, wife1, hub2, wife2]
        fami = [fam1, fam2, fam3]

        self.assertEqual(us.all_marr_couple(indivi, fami), ["p1"])

    def test_all_alive_people(self):

        indi1 = Individual(_id="I0", alive=False)
        indi2 = Individual(_id="I1")
        indi3 = Individual(_id="I2", alive=False)
        indi4 = Individual(_id="I3", alive=True)
        indi5 = Individual(_id="I4", alive=False)

        indi: List[Individual] = [indi1, indi2, indi3, indi4, indi5]

        self.assertEqual(us.all_alive_people(indi), ["I1", "I3"])

    # US_37
    def test_List_recent_death_family(self):

        hub: Individual = Individual(_id="I1", deat={'date': "30 oct 2020"})
        wife: Individual = Individual(_id="I2", deat={'date': "25 oct 2020"})
        chid: Individual = Individual(_id="I3", deat={'date': "28 oct 2020"})

        fam1: Family = Family(_id="I0", husb=hub.id, wife=wife.id, marr={"28 oct 1998"})

        hub1: Individual = Individual(_id="I4", deat={'date': "22 oct 2019"})
        wife1: Individual = Individual(_id="I5", deat={'date': "21 oct 2020"})
        chid1: Individual = Individual(_id="I6", deat={'date': "7 SEP 2020"})

        fam2: Family = Family(_id="I7", husb=hub.id, wife=wife.id)

        indi: List[Individual] = [hub, wife, chid, hub1, wife1, chid1]
        fami: List[Family] = [fam1, fam2]

        self.assertEqual(us.List_recent_death_family(indi, fami), [])

    # US_38
    def test_List_Upcoming_birthday(self):
        indi1: Individual = Individual(_id="I1", name="Janki Patel", birt={'date': "1 NOV 2019"})
        indi2: Individual = Individual(_id="I2", name="Jigi Patel", birt={'date': "9 NOV 2019"})
        indi3: Individual = Individual(_id="I3", name="Dinky kapadiya", birt={'date': "30 NOV 1978"})
        indi4: Individual = Individual(_id="I4", name="Payal desai", birt={'date': "3 DEC 2019"})
        indi5: Individual = Individual(_id="I5", name="Arjun tejani", birt={'date': "10 DEC 2020"})
        indi6: Individual = Individual(_id="I6", name="Monty kanani")
        individuals: List[Individual] = [indi1, indi2, indi3, indi4, indi5, indi6]
        self.assertTrue(us.List_Upcoming_birthday(individuals))

        # us_40

    def test_List_recent_divorce(self):
        fam1: Family = Family(_id="I1", husb="John Doe1", wife="jennifer Doe1", div={'date': "1 NOV 2020"})
        fam2: Family = Family(_id="I2", husb="Woody Bing", wife="Billy Smith", div={'date': "5 NOV 2020"})
        fam3: Family = Family(_id="I3", husb="Anurag Kim", wife="Emma Green", div={'date': "30 NOV 2020"})
        fam4: Family = Family(_id="I4", husb="Shrey Hill", wife="Olivia Kim", div={'date': "1 DEC 2019"})
        fam5: Family = Family(_id="I5", husb="Parthik Smith", wife="Sophia Taylor", div={'date': "2 NOV 2020"})
        fam6: Family = Family(_id="I6", husb="Kamron Geller", wife="Katrina Green", div=None)
        families: List[Family] = [fam1, fam2, fam3, fam4, fam5, fam6]
        self.assertTrue(us.List_recent_divorce(families))


# US 45
    def test_Parents_and_child(self):
        indi1: Individual = Individual(_id="C1", name="John Doe1", birt={'date': "3 FEB 2001"})
        indi2: Individual = Individual(_id="C2", name="Ohn Oka", birt={'date': "3 JAN 2001"})
        family1: Family = Family(_id="M1")
        family1.chil = [indi1.id, indi2.id]
        family1.parent = {'date': "3 JAN 2001"}
        individuals: List[Individual] = [indi1, indi2]
        self.assertEqual(us.Parents_and_child(family1, individuals), ['C2'])


# US 46
    def test_Grand_Parents_and_Parents(self):
        indi1: Individual = Individual(_id="C1", name="John Doe1", birt={'date': "3 FEB 1966"})
        indi2: Individual = Individual(_id="C2", name="Ohn Oka", birt={'date': "3 JAN 1989"})
        family1: Family = Family(_id="M1")
        family1.parent = [indi1.id, indi2.id]
        family1.parent = {'date': "3 JAN 2001"}
        individuals: List[Individual] = [indi1, indi2]
        self.assertEqual(us.Grand_Parents_and_Parents(family1, individuals), [])

    def test_girls_gender_check(self):
        """ test girls_gender_check method """
        indi1: Individual = Individual(_id="I1", sex='F')
        indi2: Individual = Individual(_id="I2", sex='M')
        indi3: Individual = Individual(_id="I3", sex='F')
        individuals: List[Individual] = [indi1, indi2, indi3]
        self.assertEqual(us.girls_gender_check(individuals), [])

    def test_list_of_twins(self):
        """ test list_of_twins method """
        chil1: Individual = Individual(_id="I1", birt={'date': "3 JAN 2001"})
        chil2: Individual = Individual(_id="I2", birt={'date': "22 NOV 1999"})
        chil3: Individual = Individual(_id="I3", birt={'date': "3 JAN 2001"})

        family1: Family = Family(_id="F1")
        family1.chil = [chil1.id, chil2.id, chil3.id]
        individuals: List[Individual] = [chil1, chil2, chil3]
        self.assertEqual(us.list_of_twins(family1, individuals), {'I3', 'I1'})


    def test_listExHusb(self):
        fam3: Dict = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'HUSB': 'I01'}}
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': 'FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}
        self.assertEqual(us.listExHusb(fam3), ['I01'])
        self.assertEqual(us.listExHusb(fam), [])

    def test_girlMrgeAftr18(self):
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': '12 FEB 1977', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}

        indi: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 MAR 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1965', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 OCT 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 JUL 1981', 'sex': 'M', 'family': 'F16'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}
        fam2 = {'F23':
                          {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                           'CHIL': ['I19', 'I26', 'I30']},
                      'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'HUSB': 'I01', 'WIFE': 'I32'}}
        self.assertEqual(us.girlMrgeAftr18(fam, indi), set())
        self.assertEqual(us.girlMrgeAftr18(fam2, indi), {'I32'})

    def test_mrgeAfter18(self):
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': '12 FEB 1977', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}

        indi: Dict = {
            'I01': {'id': 'I01', 'name': 'Joe /Smith/', 'BIRT': '15 MAR 1960', 'sex': 'M', 'family': 'F23',
                    'DEAT': '31 DEC 2013'},
            'I07': {'id': 'I07', 'name': 'Jennifer /Smith/', 'BIRT': '23 SEP 1965', 'sex': 'F',
                    'family': 'F23'},
            'I19': {'id': 'I19', 'name': 'Dick /Smith/', 'BIRT': '13 OCT 1981', 'sex': 'M', 'family': 'F23'},
            'I26': {'id': 'I26', 'name': 'Jane /Smith/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I30': {'id': 'I30', 'name': 'Mary /Test/', 'BIRT': '13 FEB 1981', 'sex': 'F', 'family': 'F23'},
            'I32': {'id': 'I32', 'name': 'Nick /Tary/', 'BIRT': '13 JUL 1981', 'sex': 'M', 'family': 'F16'},
            'I44': {'id': 'I44', 'name': 'Cersi /Lanister/', 'BIRT': '13 FEB 1981', 'sex': 'F',
                    'family': 'F23'}}
        fam2 = {'F23':
                    {'fam': 'F23', 'MARR': '14 FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                     'CHIL': ['I19', 'I26', 'I30']},
                'F16': {'fam': 'F16', 'MARR': '12 DEC 2007', 'HUSB': 'I01', 'WIFE': 'I32'}}
        self.assertEqual(us.mrgeAfter18(fam, indi), set())
        self.assertEqual(us.mrgeAfter18(fam2, indi), {'I01'})

    def test_boys_gender_check(self):
        """ test boys_gender_check method """
        indi1: Individual = Individual(_id="I1", sex='F')
        indi2: Individual = Individual(_id="I2", sex='M')
        indi3: Individual = Individual(_id="I3", sex='F')
        individuals: List[Individual] = [indi1, indi2, indi3]
        self.assertEqual(us.boys_gender_check(individuals), [])


    def test_step_sib_birth_diff(self):
        """ test step_sib_birth_diff method """
        chil1: Individual = Individual(_id="I1", birt={'date': "3 JAN 2001"})
        chil2: Individual = Individual(_id="I2", birt={'date': "22 NOV 1999"})
        chil3: Individual = Individual(_id="I3", birt={'date': "3 JAN 2001"})

        family1: Family = Family(_id="F1")
        family1.chil = [chil1.id, chil2.id, chil3.id]
        individuals: List[Individual] = [chil1, chil2, chil3]
        self.assertEqual(us.step_sib_birth_diff(family1, individuals), False)
    
    #US51
    def test_all_divorce_couple(self):
        
        hub = Individual(_id="I0")
        wife = Individual(_id="I1")
        fam1= Family(_id = "p1",husb = hub.id,wife= wife.id,div={"14 Nov 1998"})

        hub1 = Individual(_id="I3")
        wife1 = Individual(_id="I4")
        fam2= Family(_id = "p2",husb = hub1.id,wife= wife1.id)

        hub2 = Individual(_id="I5")
        wife2 = Individual(_id="I6")
        fam3= Family(_id = "p3",husb = hub.id,wife= wife.id,div={"14 Nov 1998"})

        indivi: List[Individual] = [hub,wife,hub1,wife1,hub2,wife2]
        fami = [fam1,fam2,fam3]

        self.assertEqual(us.all_divorce_couple(indivi,fami), ["p1","p3"])

    #US52
    def test_Birth_before_div(self):
        indi = Individual(_id="I20", birt={'date': "15 JAN 2020"})
        family = Family(
            div={'date': "15 JAN 2019"})  # divorce date is before birth date so result is fasle
        self.assertFalse(us.birth_before_div(family, indi))

        indi = Individual(_id="I21", birt={'date': "5 JUL 2000"})
        family = Family(
            div={'date': "1 JAN 2010"})  # divorce date is after birth date so result is true
        self.assertTrue(us.birth_before_div(family, indi))

        indi = Individual(_id="I22", birt={'date': "7 JUN 2000"})
        family = Family(
            div={'date': "9 JAN 1995"})  # divorce date is before birth date so result is false
        self.assertFalse(us.birth_before_div(family, indi))

        indi = Individual(_id="I23", birt={'date': "15 MAY 1989"})
        family = Family(
            div={'date': "15 FEB 2000"})  # divorce date is after birth date so result is true
        self.assertTrue(us.birth_before_div(family, indi))

        indi = Individual(_id="I24", birt={'date': "15 JAN 2020"})
        family = Family(div=None)  # divorce is not take place so result is by default true
        self.assertTrue(us.birth_before_div(family, indi))

    #US53
    def test_List_recent_anniversary(self):

        fam1: Family = Family(_id="I1", husb="John Doe1", wife="jennifer Doe1", marr={'date': "11 NOV 2020"})
        fam2: Family = Family(_id="I2", husb="Woody Bing", wife="Billy Smith", marr={'date': "15 NOV 2020"})
        fam3: Family = Family(_id="I3", husb="Anurag Kim", wife="Emma Green", marr={'date': "13 DEC 2020"})
        fam4: Family = Family(_id="I4", husb="Shrey Hill", wife="Olivia Kim", marr={'date': "1 DEC 2019"})
        fam5: Family = Family(_id="I5", husb="Parthik Smith", wife="Sophia Taylor", marr={'date': "2 NOV 2021"})
        fam6: Family = Family(_id="I6", husb="Kamron Geller", wife="Katrina Green", marr=None)
        families: List[Family] = [fam1, fam2, fam3, fam4, fam5, fam6]
        self.assertTrue(us.List_recent_anniversary(families))

    #US54
    def test_divorce_14(self):
        
        # husband 20, wife 14 -> Both are over 14 -> True
        husband: Individual = Individual(_id="I0", birt={'date': "19 SEP 1995"})
        wife: Individual = Individual(_id="I1", birt={'date': "3 JAN 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F0", husb=husband.id, wife=wife.id, div={'date': "11 FEB 2015"})
        self.assertTrue(us.divorce_14(family, individuals))

        # husband 11, wife 20 -> Only wife is over 14 -> False
        husband: Individual = Individual(_id="I2", birt={'date': "2 MAR 2007"})
        wife: Individual = Individual(_id="I3", birt={'date': "11 FEB 2000"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F1", husb=husband.id, wife=wife.id, div={'date': "11 FEB 2019"})
        self.assertFalse(us.divorce_14(family, individuals))

        # husband 17, wife 10 -> Only husband is over 14 -> False
        husband: Individual = Individual(_id="I4", birt={'date': "22 AUG 2000"})
        wife: Individual = Individual(_id="I5", birt={'date': "5 DEC 2007"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F2", husb=husband.id, wife=wife.id, div={'date': "11 FEB 2018"})
        self.assertFalse(us.divorce_14(family, individuals))

        # husband 12, wife 12 -> Both are under 14 -> False
        husband: Individual = Individual(_id="I6", birt={'date': "19 SEP 2008"})
        wife: Individual = Individual(_id="I7", birt={'date': "3 JAN 2008"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F3", husb=husband.id, wife=wife.id, div={'date': "11 FEB 2020"})
        self.assertFalse(us.divorce_14(family, individuals))

        # husband 18, wife 16 -> Both are over 14 -> True
        husband: Individual = Individual(_id="I8", birt={'date': "7 FEB 1970"})
        wife: Individual = Individual(_id="I9", birt={'date': "8 FEB 1972"})
        individuals: List[Individual] = [husband, wife]
        family: Family = Family(_id="F4", husb=husband.id, wife=wife.id, div={'date': "11 FEB 1988"})
        self.assertTrue(us.divorce_14(family, individuals))


    ##US55
    def test_all_sister(self):
        indi1: Individual = Individual(name="Janki", sex='F')
        indi2: Individual = Individual(name="Dhruvil", sex='M')
        indi3: Individual = Individual(name="Dinky", sex='F')
        individuals: List[Individual] = [indi1, indi2, indi3]
        self.assertEqual(us.all_sister(individuals), [])

    
    def test_listExwife(self):
    
        fam: Dict = {'F23':
                         {'fam': 'F23', 'MARR': 'FEB 1980', 'HUSB': 'I01', 'WIFE': 'I07',
                          'CHIL': ['I19', 'I26', 'I30']},
                     'F16': {'fam': 'F16', 'MARR': '12 DEC 2007'}}
      
        self.assertEqual(us.listExwife(fam), [])

    def test_list_male(self):

        indi1 = Individual(_id="I0", sex="Male")
        indi2 = Individual(_id="I1", sex="Female")
        indi3 = Individual(_id="I2", sex="Female")
        indi4 = Individual(_id="I3", sex="Male")
        indi5 = Individual(_id="I4", sex="Male")

        indi: List[Individual] = [indi1, indi2, indi3, indi4, indi5]

        self.assertEqual(us.list_male(indi), ["I0","I3", "I4"])

    def test_list_female(self):

        indi1 = Individual(_id="I0", sex="Male")
        indi2 = Individual(_id="I1", sex="Female")
        indi3 = Individual(_id="I2", sex="Female")
        indi4 = Individual(_id="I3", sex="Male")
        indi5 = Individual(_id="I4", sex="Male")

        indi: List[Individual] = [indi1, indi2, indi3, indi4, indi5]

        self.assertEqual(us.list_female(indi), ["I1","I2"])


def test_twins_birth_date(self):
    """ test twins birthdate same method """
    chil1: Individual = Individual(_id="I1", birt={'date': "3 JAN 2001"})
    chil2: Individual = Individual(_id="I2", birt={'date': "3 JAN 2001"})
    family1: Family = Family(_id="F1")
    family1.chil = [chil1.id, chil2.id]
    individuals: List[Individual] = [chil1, chil2]
    self.assertEqual(us.twins_birth_date(family1, individuals), True)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
