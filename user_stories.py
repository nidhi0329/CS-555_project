""" Implement user stories for GEDCOM parser

    date: 30-Sep-2020
    python: v3.8.4
"""
import operator
from typing import List, Dict, TextIO, Union
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from models import Individual, Family
from app import get_lines, generate_classes, findParents, checkIfSiblings

lines = get_lines('SSW555-P1-fizgi.ged')
individuals, families = generate_classes(lines)
individuals.sort(key=operator.attrgetter('id'))
families.sort(key=operator.attrgetter('id'))


def birth_before_death_of_parents(family: Family, individuals: List[Individual]) -> bool:
    """ US09: verify that children are born before death of mother
        and before 9 months after death of father """

    husb = next(ind for ind in individuals if ind.id == family.husb)
    wife = next(ind for ind in individuals if ind.id == family.wife)

    if not husb.deat and not wife.alive:
        return True

    for child_id in family.chil:
        child_birth_date = next(ind.birt['date'] for ind in individuals if ind.id == child_id)
        child_birth_date = datetime.strptime(child_birth_date, "%d %b %Y")

        if husb.deat:
            husb_death_date = husb.deat['date']
            husb_death_date = datetime.strptime(husb_death_date, "%d %b %Y")

            if child_birth_date > husb_death_date + timedelta(days=270):
                print(f"✘ Family ({family.id}): Child ({child_id}) should be born "
                      f"before 9 months after death of father")
                return False

        if wife.deat:
            wife_death_date = wife.deat['date']
            wife_death_date = datetime.strptime(wife_death_date, "%d %b %Y")

            if child_birth_date > wife_death_date:
                print(f"✘ Family ({family.id}): Child ({child_id}) should be born before death of mother")
                return False
    else:
        print(f"✔ Family ({family.id}): Children are born before death of mother "
              f"and before 9 months after death of father")
        return True


def were_parents_over_14(family: Family, individuals: List[Individual]) -> bool:
    """ US10: verify that parents were at least 14 years old at the marriage date """
    marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")

    husb_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.husb)
    husb_birthday = datetime.strptime(husb_birthday, "%d %b %Y")
    husb_marr_age = marr_date.year - husb_birthday.year - \
                    ((marr_date.month, marr_date.day) < (husb_birthday.month, husb_birthday.day))

    wife_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.wife)
    wife_birthday = datetime.strptime(wife_birthday, "%d %b %Y")
    wife_marr_age = marr_date.year - wife_birthday.year - \
                    ((marr_date.month, marr_date.day) < (wife_birthday.month, wife_birthday.day))

    if husb_marr_age >= 14 and wife_marr_age >= 14:
        print(f"✔ Family ({family.id}): Both parents were at least 14 at the marriage date")
        return True

    if husb_marr_age < 14 and wife_marr_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_marr_age}) "
              f"and Wife ({wife_marr_age}) can not be less than 14")
    elif husb_marr_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_marr_age}) can not be less than 14")
    elif wife_marr_age < 14:
        print(f"✘ Family ({family.id}): Wife ({wife_marr_age}) can not be less than 14")

    return False


def fewer_than_15_siblings(family: Family) -> bool:
    if len(family.chil) < 15:
        print(f"✔ Family ({family.id}): Siblings are less than 15")
        return True
    else:
        print(f"✘ Family ({family.id}): Siblings are greater than 15")
        return False


def male_last_names(family: Family, individuals: List[Individual]):
    ids = [family.husb, family.wife]
    ids.extend(family.chil)
    males = [individual for individual in individuals if individual.sex == 'M' and individual.id in ids]
    names = [male.name.split('/')[1] for male in males]
    return len(set(names)) == 1


def marriage_before_death(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that marrriage before death of either spouse """
    mrgDate = datetime.strptime(family.marr.get('date'), "%d %b %Y")

    husb = list(filter(lambda x: x.id == family.husb, individuals))[0]
    wife = list(filter(lambda x: x.id == family.wife, individuals))[0]

    husbandDeathDate = datetime.strptime(husb.deat.get('date'), "%d %b %Y") if husb.deat else None
    wifeDeathDate = datetime.strptime(wife.deat.get('date'), "%d %b %Y") if wife.deat else None

    if (husbandDeathDate and husbandDeathDate - mrgDate > timedelta(minutes=0)) or (
            wifeDeathDate and wifeDeathDate - mrgDate > timedelta(minutes=0)):
        print(
            f"✔ Family ({family.husb}) and ({family.wife}):Their marriage took place, before either of their death, So the condition is valid.")
        return True
    else:
        print(
            f"✘ Husband ({family.husb}): Wife ({family.wife}) Marriage did not take place before either of their death, So that is not valid.")
        return False


def divorce_before_death(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that divorce before death of either spouse """
    divdate = datetime.strptime(family.div.get('date'), "%d %b %Y")

    husb = list(filter(lambda x: x.id == family.husb, individuals))[0]
    wife = list(filter(lambda x: x.id == family.wife, individuals))[0]

    husbandDeathDate = datetime.strptime(husb.deat.get('date'), "%d %b %Y") if husb.deat else None
    wifeDeathDate = datetime.strptime(wife.deat.get('date'), "%d %b %Y") if wife.deat else None

    if (husbandDeathDate and husbandDeathDate - divdate > timedelta(minutes=0)) \
            or (wifeDeathDate and wifeDeathDate - divdate > timedelta(minutes=0)):
        print(f"✔ Family ({family.husb}) and ({family.wife}): Their divorce took place, "
              f"before either of their death, So the condition is valid.")
        return True
    else:
        print(f"✘ Husband ({family.husb}) and Wife ({family.wife}): Divorce did not take place "
              f"before either of their death, So that is not valid.")
        return False


def checkBigamy(family: Dict):
    """Method that checks bigamy in the given gedcom data
    if yes then it pops and update data with no bigamy"""
    for f in family:
        if 'HUSB' in family[f]:
            hus_id = family[f]['HUSB']
            if 'WIFE' in family[f]:
                wife_id = family[f]['WIFE']

        wife_count = 0
        husb_count = 0

        for f in family:
            if 'HUSB' in family[f]:
                hus_id2: List = family[f]['HUSB']
                if hus_id == hus_id2:
                    husb_count += 1
                if 'WIFE' in family[f]:
                    wife_id2: List = family[f]['WIFE']
                    if wife_id == wife_id2:
                        wife_count += 1
            else:
                continue


def getAge(born):
    """returns age of individual"""
    born = datetime.strptime(born, '%d %b %Y')
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def checkForOldParents(fam: Dict, ind: Dict, file: TextIO):
    """check the age of individuals and return boolean value
    if there are old parents in given data false otherwise"""
    result: bool = True
    for f in fam:
        if "CHIL" in fam[f]:
            wife: str = "0"
            husb: str = "0"
            if "HUSB" in fam[f]:
                husb: str = fam[f]["HUSB"]
            if "WIFE" in fam[f]:
                wife: str = fam[f]["WIFE"]
            wifeAge: int = 0
            husbAge: int = 0
            if wife in ind and "BIRT" in ind[wife]:
                wifeAge: Union[int, bool] = getAge(ind[wife]["BIRT"])
            if husb in ind and "BIRT" in ind[husb]:
                husbAge: Union[int, bool] = getAge(ind[husb]["BIRT"])
            for c in fam[f]["CHIL"]:
                childAge: int = 0
                if "BIRT" in ind[c]:
                    childAge: Union[int, bool] = getAge(ind[c]["BIRT"])
                if wifeAge - childAge > 60:  # throw wife error
                    file.write(
                        "ERROR US12: Mother " + wife + " is older than their child, " + c + " by over 60 years\n")
                    result: bool = False
                if husbAge - childAge > 80:  # throw husb error
                    file.write(
                        "ERROR US12: Father " + husb + " is older than their child, " + c + " by over 80 years\n")
                    result: bool = False
    return result


def birth_before_marriage_of_parents(family: Family, individuals: List[Individual]) -> bool:
    """ user story: verify that divorce before death of either spouse """
    mrgdate = datetime.strptime(family.marr.get('date'), "%d %b %Y")
    divdate = datetime.strptime(family.div.get('date'), "%d %b %Y")
    birthdate_child = datetime.strptime(individuals.birt.get('date'), "%d %b %Y")

    if family.marr:
        if birthdate_child - mrgdate > timedelta(minutes=0) and birthdate_child - divdate < timedelta(days=275):
            print(f"({family.id}) : birth_before_marriage_of_parents")
            return True
        else:
            print(f"({family.id}) : not birth_before_marriage_of_parents")
            return False
    else:
        print(f"({family.id}) : marrige is not happen")
        return False


def less_than_150(individual: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individual.birt['date'], "%d %b %Y")
    current_date: datetime = datetime.now()
    years_150 = timedelta(days=54750)

    if individual.deat:
        death_date: datetime = datetime.strptime(individual.deat['date'], "%d %b %Y")
        if birth_date - death_date > timedelta(days=0):
            print(f"✘ individual ({individual.id}): The person's age is grater than 150 ")
            return False
        elif death_date - birth_date < years_150:
            print(f"✔ individual ({individual.id}): The person's age is less than 150 ")
            return True

    else:
        if current_date - birth_date < years_150:
            print(f"✔ individual ({individual.id}): The person's age is less than 150 ")
            return True

    print(f"✘ individual ({individual.id}): The person's age is not than than 150 ")

    return False


today: datetime = datetime.now()
year: timedelta = timedelta(minutes=0)


def marriage(family: Family) -> bool:
    if family.marr:
        marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")
        if today - marr_date > timedelta(minutes=0):
            print(f"✔ ({family.id}): marrige take place before current date ")
            return True
        else:
            print(f"✘ ({family.id}): marrige didn't take place before current date ")

    else:
        print(f"✘ ({family.id}): marrige didn't take place ")


def divo(family: Family) -> bool:
    if family.div:
        div_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")
        if today - div_date > timedelta(minutes=0):
            print(f"✔ ({family.id}): divorce take place before current date ")
            return True
        else:
            print(f"✘ ({family.id}): divorce didn't take place before current date ")

    else:
        print(f"✘ ({family.id}): divorce didn't take place ")


def birth(indi: Individual) -> bool:
    if indi.birt:
        birt_date: datetime = datetime.strptime(indi.birt['date'], "%d %b %Y")
        if today - birt_date > timedelta(minutes=0):
            print(f"✔ ({indi.id}): birth take place before current date ")
            return True
        else:
            print(f"✘ ({indi.id}): birth didn't take place before current date ")

    else:
        print(f"✘ ({indi.id}): birth didn't take place ")


def death(indi: Individual) -> bool:
    if indi.deat:
        death_date: datetime = datetime.strptime(indi.deat['date'], "%d %b %Y")
        if today - death_date > timedelta(minutes=0):
            print(f"✔ ({indi.id}): death take place before current date ")
            return True
        else:
            print(f"✘ ({indi.id}): death didn't take place before current date ")

    else:
        print(f"✘ ({indi.id}): death didn't take place ")


def birth_before_mrg(family: Family, individuals: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individuals.birt['date'], "%d %b %Y")

    if family.marr:  # condition for the divorce
        marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")
        if marr_date - birth_date > timedelta(minutes=0):
            print(f"✔ ({individuals.id}):birth is before mrg")
            return True
        else:
            print(f"✘ ({individuals.id}):birth is not before mrg")
            return False
    else:
        print(f"✘ ({individuals.id}):no mrg")
        return True


def marriage_before_divorce(family: Family) -> bool:
    marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")  # get the marriage date

    if family.div:  # condition for the divorce
        div_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")
        if div_date - marr_date > timedelta(minutes=0):
            print(f"Individual:({family.id}):marriage is before divorce")
            return True
        else:
            print(f"({family.id}):marriage can not take place before divorce")
            return False
    else:
        print(f"({family.id}):There is no divorce")
        return True


# US14 no more than 5 siblings born the same day
def verifySiblingsDates(allDates):
    retValue = True
    datesDict = {}
    for d in allDates:
        if d in datesDict:
            datesDict[d] = datesDict.get(d) + 1
            if datesDict[d] > 5:
                return False
        else:  # if we did not find this date, we first check if we have date within day of already found dates
            found = False
            for d2 in datesDict:
                delta = d2 - d
                if abs(delta.days) < 2:
                    datesDict[d2] = datesDict.get(d2) + 1
                    found = True
                    if datesDict[d2] > 5:
                        retValue = False
                        break
            if not found:
                datesDict[d] = 1

    return retValue


# US13 Sbiling space
def verifySiblingsSpace(allDates):
    retValue = True
    datesSet = set()
    for d in allDates:
        if d in datesSet:
            retValue = False
            break
        else:
            found = False
            for d2 in datesSet:
                delta = d2 - d
                if abs(delta.days) > 1 and abs(delta.days) < 280:
                    retValue = False
                    break
            if retValue:
                datesSet.add(d)
            else:
                break

    return retValue


# siblingsDates = (datetime.date(1990, 1, 1), datetime.date(1991, 1, 1))
# print(verifySiblingsDates(siblingsDates))


def birth_before_death(individuals: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individuals.birt['date'], "%d %b %Y")

    if individuals.deat:  # condition for the divorce
        deat_date: datetime = datetime.strptime(individuals.deat['date'], "%d %b %Y")
        if deat_date - birth_date > timedelta(minutes=0):
            print(f"({individuals.id}):birth is before death")
            return True
        else:
            print(f"({individuals.id}):birth can not take place not before death")
            return False
    else:
        print(f"({individuals.id}):no death")
        return True


def correct_gender_for_role(family: Family, individuals: List[Individual]) -> bool:
    """ US21: verify that Husband in family is male and wife in family is female """
    husb_gender = next(ind.sex for ind in individuals if ind.id == family.husb)
    wife_gender = next(ind.sex for ind in individuals if ind.id == family.wife)

    if husb_gender == 'M' and wife_gender == 'F':
        print(f"✔ Family ({family.id}): Both parents have the correct gender for the role")
        return True

    if husb_gender == 'F' and wife_gender == 'M':
        print(f"✘ Family ({family.id}): Husband should be Male and Wife should be Female")
    elif husb_gender == 'F':
        print(f"✘ Family ({family.id}): Husband should be Male")
    elif wife_gender == 'M':
        print(f"✘ Family ({family.id}): Wife should be Female")

    return False


def unique_ids(families: List[Family], individuals: List[Individual]) -> bool:
    """ US22: verify that All individual IDs are unique and all family IDs are unique """
    ids = [family.id for family in families] + [individual.id for individual in individuals]

    recurrent_ids = list(set([_id for _id in ids if ids.count(_id) > 1]))

    if len(recurrent_ids) > 0:
        print(f"✘ ID check: Recurrent ids detected", recurrent_ids)
        return False

    print(f"✔ ID check: No recurrent ids detected")
    return True


def individual_ages(individuals: List[Individual]):
    list_of_ages = []
    for individual in individuals:
        list_of_ages.append(individual.age())
    print("List of individual age -", list_of_ages)
    return list_of_ages


def order_sibling_by_age(family: Family, individuals: List[Individual]):
    children = []
    for child in family.chil:
        children.append(next(ind for ind in individuals if ind.id == child))
    children.sort(key=lambda x: x.age(), reverse=True)
    print(
        f"Family[{family.id}] age of sibling in descending order " + " ".join([str(child.age()) for child in children]))
    return children


def firstCousinShouldNotMarry() -> List:
    """ check if parents of husband and spouse. If parents are siblings in each others families then first cousins.
    Return """

    listFam: List = families

    individualError: List = []

    for fam in listFam:
        if fam.husb != 'NA' and fam.wife != 'NA':
            husbParents: str = findParents(fam.husb, listFam)
            wifeParents: str = findParents(fam.wife, listFam)
            if husbParents and wifeParents:
                siblings: bool = checkIfSiblings(husbParents, wifeParents, listFam)
                if siblings:
                    individualError.append(fam)
    return individualError


def auntsAndUncle() -> List:
    listFam: List = families

    individualError: List = []
    for fam in listFam:
        if fam.husb != 'NA' and fam.wife != 'NA':
            husbParents: str = findParents(fam.husb, listFam)
            wifeParents: str = findParents(fam.wife, listFam)
            if husbParents and wifeParents:
                hSiblings: bool = checkIfSiblings(husbParents, fam, listFam)
                wSiblings: bool = checkIfSiblings(wifeParents, fam, listFam)
                if hSiblings:
                    individualError.append(fam)
                elif wSiblings:
                    individualError.append(fam)
    return individualError


def hasMultipleBirths(siblingDates):
    retValue = True
    datesDict = {}
    for d in siblingDates:
        if d in datesDict:
            datesDict[d] = datesDict.get(d) + 1
        else:  # if we did not find this date, we first check if we have date within day of already found dates
            found = False
            for d2 in datesDict:
                delta = d2 - d
                if (abs(delta.days) < 2):
                    datesDict[d2] = datesDict.get(d2) + 1
                    found = True
            if not found:
                datesDict[d] = 1
    for birthDate in datesDict.keys():
        if datesDict[birthDate] > 1:
            return birthDate.strftime('%d %b %Y')
    return False


# US24 Uniqye families by spouses - No more than one family with the same spouses by name and the same marriage date
def uniqueFamilyBySpouses(families: List[Family]):
    names_marr = {}
    same_data = []
    for family in families:
        if (family.husb, family.wife) in names_marr:
            if names_marr[family.husb, family.wife] == family.marr["date"]:
                same_data.append([family.id, family.husb, family.wife, family.marr["date"]])
                print(f"✘ Family ({family.id}): duplicate family having same data")

        else:
            names_marr[family.husb, family.wife] = family.marr["date"]
            print(f"✔ Family ({family.id}): No duplicate family having same data")

    print("Duplicate family: ")
    print(same_data)
    return same_data


# US 031

def isSingleAliveOver30():
    retValue = False
    age = -1
    alive = False
    spouse = []
    try:
        retValue = int(age) > 30 and alive and len(spouse) == 0
    except:
        retValue = False

    return retValue


# US_17
def no_parents_marry_child(families: List[Family]):
    parent_pairs = families[:2]
    for child in families[2]:
        if child in parent_pairs:  # If their ids are not same that means that they have not married each other
            print("✘ In family such type of marriages cannot take place where parents marry their.")
            return False  # if their ids match means they have married which is not true So it returns False
        else:
            print("✔ In Family such marriages are allowed and valid.")
            return True


# US_18
def no_sibilings_can_marry(families: List[Family]):
    parent_pairs = families[:4]
    for child1 in families[2]:
        for child2 in families[3]:
            if child1 in parent_pairs or child2 in parent_pairs or child1 in child2:  # If their ids are not same that means that they have not married each other
                print("✘ In family such type of marriages cannot take place where sibilings marry each other.")
                return False  # if their ids match means they have married which is not true So it returns False
            else:
                print("✔ In Family such marriages are allowed and valid.")
                return True

            # US23 Unique name and birth date - No more than one individual with the same name and birth date


def AreIndividualsUnique(individuals: List[Individual]):
    names_bdays = {}
    same_data = []
    for individual in individuals:
        if individual.name in names_bdays:
            if names_bdays[individual.name] == individual.birt["date"]:
                same_data.append([individual.id, individual.name, individual.birt["date"]])
                print(f"✘ Individual ({individual.id}): duplicate individual having same name and birth_date")
        else:
            names_bdays[individual.name] = individual.birt["date"]
            print(f"✔ Individual ({individual.id}): No duplicate individual having same name and birth_date")

    print(same_data)
    return same_data


# User Story 26
def validateFamilyRoles(fam: Family, individuals: List[Individual]) -> bool:
    if fam.husb not in individuals:
        if fam.wife not in individuals:
            return False
    if fam.husb in individuals:
        hus = individuals[fam.husb]
        l1 = len(fam.chil)
        l2 = len(hus.chil)
        if l1 == l2 and not childrenExistInFamily(hus.chil, fam.chil):
            return False
        else:
            return False
    if fam.wife in individuals:
        wife = individuals[fam.wife]
        l3 = len(fam.chil)
        l4 = len(wife.chil)
        if l3 == l4 and not childrenExistInFamily(wife.chil, fam.chil):
            return False
        else:
            return False

    return familyMembersExist(fam, individuals)


def childrenExistInFamily(parentsChildren, familyChildren):
    for parentChild in parentsChildren:
        childFound = False
        for familyChild in familyChildren:
            if familyChild == parentChild:
                childFound = True
                break
        if childFound == False:
            return False
    return True


def validSpouseExists(individId, spouseId, familyDict):
    spouseFound = False
    spouseFound = [True for i in sorted(familyDict.keys()) if
                   (familyDict[i].husbandId == individId and spouseId == familyDict[i].wifeId) or (
                           familyDict[i].wifeId == individId and spouseId == familyDict[i].husbandId)]
    return spouseFound


def isIndividualInFamily(individualId, family):
    if family.husbandId == individualId or family.wifeId == individualId:
        return True
    [True for childId in family.children if childId == individualId]
    return False


def familyMembersExist(family, individualDict):
    if family.husb not in individualDict or family.wifeId not in individualDict:
        return False
    [False for childId in family.children if individualDict.get(childId) is None]
    return True


def oneForOneFamilyIndividualRecords(individualDict, familyDict):
    missingIndividuals = []
    for i in sorted(individualDict.keys()):
        indi = individualDict[i]
        indiExists = False
        indiExists = [True for j in sorted(familyDict.keys()) if isIndividualInFamily(indi.id, familyDict[j])]
        if indiExists == False:
            print(f"✘  ({indi.id}): individual is not exit in the familt member")
            missingIndividuals.append(indi.id)
    missedFamilies = []
    for i in sorted(familyDict.keys()):
        fam = familyDict[i]
        if not familyMembersExist(fam, individualDict):
            print(f"✘  ({fam.id}): family member is not part of individual")
            missedFamilies.append(fam.id)
    l_1 = len(missingIndividuals)
    l_2 = len(missedFamilies)
    if l_1 < 1:
        if l_2 < 1:
            return True
    else:
        return False


# Final code for user story 26
def validateCorrespondingRecords(individualDict, familyDict):
    err = 0
    for i in sorted(individualDict.keys()):
        individ = individualDict[i]
        if len(individ.spouse) > 0:
            s_Count = 0
            s_Count = [s_Count + 1 for spouseId in individ.spouse if
                       validSpouseExists(individ.id, spouseId, familyDict)]
            l_1 = len(individ.spouse)
            if s_Count != l_1:
                err += 1
                print(f"✘  ({individ.id}): spouse is not in family")

        if len(individ.children) > 0:
            childrenFoundInFamily = False
            childrenFoundInFamily = [True for j in sorted(familyDict.keys()) if
                                     childrenExistInFamily(individ.children, familyDict[j].children)]
            if childrenFoundInFamily == False:
                errors = errors + 1
                print(f"✘  ({individ.id}): childer is not part of family member")
    return oneForOneFamilyIndividualRecords(individualDict, familyDict) and errors == 0


# UserStory 25
def are_child_names_unique(family: Family, individuals):
    children = map(lambda x: individuals.get(x), family.chil)
    childInfoSet = set()

    for child in children:
        fname = child.name.split(' ')[0]
        bdate = child.birt
        if (fname, bdate) in childInfoSet:
            print("✘ children having same name or birth day date in the family")
            return False
        childInfoSet.add((fname, bdate))
    print("✔ children name nad birth day date is unique")
    return True


def deceased(individuals: List[Individual]):
    deceased_list = []
    for individual in individuals:
        if individual.deat is not False:
            deceased_list.append(individual.name)

    for i in deceased_list:
        print(f"{i} :  is deaceaed person in the family")
    return deceased_list


def living_marr(families: List[Family], individuals: List[Individual]):
    living_mrr_list_d = []
    indi = [indi.id for indi in individuals if indi.alive]

    idf = [family.id for family in families if not family.div]

    for i in indi:
        if i in idf:
            living_mrr_list_d.append(i)

    for i in living_mrr_list_d:
        print(f"{i} :  is married and alive in the family")

    return living_mrr_list_d


def aunt_uncle_birth_year(families: List[Family], individuals: List[Individual]):
    """ US47: verify that aunts and uncles birth year are not same """

    def get_aunts_and_uncles(family: Family):
        aunt_list = []
        uncle_list = []

        try:
            husb_sibling_ids = next(fam for fam in families if family.husb in fam.chil).chil
        except StopIteration:
            husb_sibling_ids = []

        if family.husb in husb_sibling_ids:
            husb_sibling_ids.remove(family.husb)

        try:
            wife_sibling_ids = next(fam for fam in families if family.wife in fam.chil).chil
        except StopIteration:
            wife_sibling_ids = []

        if family.wife in wife_sibling_ids:
            wife_sibling_ids.remove(family.wife)

        for husb_sibling_id in husb_sibling_ids:
            husb_sibling = next(ind for ind in individuals if ind.id == husb_sibling_id)
            (aunt_list if husb_sibling.sex == 'F' else uncle_list).append(husb_sibling)

        for wife_sibling_id in wife_sibling_ids:
            wife_sibling = next(ind for ind in individuals if ind.id == wife_sibling_id)
            (aunt_list if wife_sibling.sex == 'F' else uncle_list).append(wife_sibling)

        return aunt_list, uncle_list

    same_aunt_uncle = []
    for fam in families:
        aunt_list, uncle_list = get_aunts_and_uncles(fam)
        for aunt in aunt_list:
            for uncle in uncle_list:
                if aunt.birt['date'][-4:] == uncle.birt['date'][-4:]:
                    same_aunt_uncle.append((aunt.id, uncle.id))
                    print(f"Aunt({aunt.id}) and Uncle({uncle.id}) can not have the same birth year")

    return same_aunt_uncle


def all_dead_people(individuals: List[Individual]):
    """ US48: verify that aunts and uncles birth year are not same """
    dead_list = []
    for individual in individuals:
        if individual.deat is not False:
            dead_list.append(individual.name)

    print(f"List of all dead people: {dead_list}")
    return dead_list


def reject_illegal_dates(date: datetime) -> bool:
    """ US42 - reject illegal dates, takes a date in format day/mm/year or 2/19/2020 """

    month, day, year = date.split('/')
    try:
        if datetime(int(year), int(month), int(day)):
            return True
    except ValueError:
        return False


def fixDates(dt):
    # if no day - make 10th day of month
    # if no  month - make first month of year

    dt = dt.split(" ")
    if dt.__len__() == 3:
        return dt[0] + ' ' + dt[1] + ' ' + dt[2]
    if dt.__len__() == 1:
        return '10 JAN ' + dt[0]

    elif dt.__len__() == 2:
        return '10 ' + dt[0] + ' ' + dt[1]


def partialDates(individual: Dict, family: Dict) -> List[str]:
    fixedDates: List = []
    ind: List = []
    fam: List = []
    for key in individual:
        if 'BIRT' in individual[key]:
            if individual[key]['BIRT'].split(' ').__len__() < 3:
                ind.append([key, fixDates(individual[key]['BIRT'])])

        if 'DEAT' in individual[key]:
            if individual[key]['BIRT'].split(' ').__len__() < 3:
                ind.append([key, fixDates(individual[key]['DEAT'])])

    for key in family:
        if family[key]['MARR'].split(' ').__len__() < 3:
            fam.append([key, fixDates(family[key]['MARR'])])

    if ind.__len__() > 0 or fam.__len__() > 0:
        fixedDates.append('US41: All Dates Made Valid:')
    if ind.__len__() > 0:
        fixedDates.append(ind)

    if fam.__len__() > 0:
        fixedDates.append(fam)

    if fixedDates.__len__() == 0:
        fixedDates.append("US41: All Dates Already Valid")
    return fixedDates


# US39 List of all upcoming anniversaries - List all living couples whose marriage anniversaries occur in the next 30 days
def List_anniversary(families: List[Family]):
    today: datetime = datetime.now()
    print(today)
    anniv_list = []
    for family in families:
        if family.marr is not None:
            if family.marr:
                marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")
                marr_date = datetime(today.year, marr_date.month, marr_date.day)
                upcoming_ann = (marr_date - today).days
                if upcoming_ann <= 30 and upcoming_ann >= 0:
                    anniv_list.append([family.id, family.husb, family.wife, family.marr["date"]])
                    print(f"✔ Family ({family.id}): Anniversary is in upcoming days")
                else:
                    print(f"✘ Family ({family.id}): Anniversaery is not in upcoming days")
        else:
            print(f"✘ Family ({family.id}): marrige didn't take place ")

    print("List of couple who have Upcoming anniversary: ")
    print(anniv_list)
    return anniv_list


# marriage date and child's birth date should not be same
def marriage_date_and_child(family: Family, individuals: List[Individual]):
    childIdsList = []
    for childId in family.chil:
        childIdsList.append(childId)

    marriageDate = family.marr["date"]
    marriageDate = datetime.strptime(marriageDate, "%d %b %Y")

    chilBirthDates = []
    for chil in childIdsList:
        childBirth = next(ind.birt["date"] for ind in individuals if ind.id == chil)
        child_birth_date = datetime.strptime(childBirth, "%d %b %Y")
        chilBirthDates.append(child_birth_date)

    dangerous_child = []
    for chilBirt, childId in zip(chilBirthDates, childIdsList):
        if chilBirt <= marriageDate:
            dangerous_child.append(childId)
            print(f"✘ Family ({family.id}): Child ({childId}) born before marriage")
        else:
            print(f"✔  Family ({family.id}): Child ({childId}) born after marriage")

    return dangerous_child


# grandparents can't marry their grandchildren
def grandparents_marriage_and_grandchildren_birthday(families: List[Family], individuals: List[Individual]):
    for family in families:
        husband = next(ind.birt["date"] for ind in individuals if ind.id == family.husb)
        wife = next(ind.birt["date"] for ind in individuals if ind.id == family.wife)
        husband = datetime.strptime(husband, "%d %b %Y")
        wife = datetime.strptime(wife, "%d %b %Y")
        forbidden_marriages = []
        if husband < wife + timedelta(days=18250):
            forbidden_marriages.append(family.id)
            print(f"✘ Child marriage alert!!! ({family.id})")
        else:
            print(f"✔ Not Child marriage ({family.id})")
        return forbidden_marriages


# User_Story 35
def List_recent_death(individuals: List[Individual]):
    today: datetime = datetime.now()
    death_list = []

    for individual in individuals:

        if individual.deat:
            death_date: datetime = datetime.strptime(individual.deat['date'], "%d %b %Y")
            if today - death_date < timedelta(days=30):
                death_list.append(individual.name)
                print("✔ This is the recent death within last 30 days")

            else:
                print("✘ This is not the recent death its not within 30 days")

    return death_list


# User_Story 36
def List_recent_birth(individuals: List[Individual]):
    today: datetime = datetime.now()
    birth_list = []

    for individual in individuals:

        if individual.birt:
            birth_date: datetime = datetime.strptime(individual.birt['date'], "%d %b %Y")
            if today - birth_date <= timedelta(days=30):
                birth_list.append(individual.name)
                print("✔ This is the recent birth within last 30 days")

            else:
                print("✘ This is not the recent birth its not within 30 days")

    return birth_list


def all_alive_people(individuals: List[Individual]):
    all_alive = []
    for indivi in individuals:
        if indivi.alive:
            all_alive.append(indivi.id)
            print(f"{indivi.id}:: people is alive")
        else:
            print(f"{indivi.id}:: not alive")

    return all_alive


def all_marr_couple(individuals: List[Individual], families: List[Family]):
    ind = []

    for indi in individuals:
        ind.append(indi.id)

    mrra = []
    for family in families:
        if family.marr:
            if family.husb in ind and family.wife in ind:
                mrra.append(family.id)
                print("{family.id}:: in this family hubs and wife are alive")

            else:
                print("{family.id}:: in this family hubs and wife are not alive")
    return mrra


# US_37
def List_recent_death_family(individuals: List[Individual], families: List[Family]):
    today: datetime = datetime.now()
    death_list = []

    for individual in individuals:

        if individual.deat:
            death_date: datetime = datetime.strptime(individual.deat['date'], "%d %b %Y")
            if today - death_date < timedelta(days=30):
                death_list.append(individual.id)
                print("✔ This is the recent death within last 30 days")

            else:
                print("✘ This is not the recent death its not within 30 days")

    print(death_list)

    fam_list = []
    for family in families:
        if family.marr:
            if family.husb in death_list and family.wife in death_list or family.chil in death_list:
                fam_list.append(family.id)
    print(fam_list)

    return fam_list


# US_38

def List_Upcoming_birthday(individuals: List[Individual]):
    today: datetime = datetime.now()
    print(today)
    birth_list = []
    for individual in individuals:
        if individual.birt is not None:
            if individual.birt:
                birt_date: datetime = datetime.strptime(individual.birt['date'], "%d %b %Y")
                birt_date = datetime(today.year, birt_date.month, birt_date.day)
                upcoming_birt = (birt_date - today).days
                if upcoming_birt <= 30 and upcoming_birt >= 0:
                    birth_list.append([individual.id, individual.name, individual.birt["date"]])
                    print(f"✔ ({individual.id}): birthday is in upcoming days")
                else:
                    print(f"✘ ({individual.id}): birthday is not in upcoming days")
        else:
            print(f"✘ ({individual.id}): birth didn't take place ")

    print(birth_list)
    return birth_list


def List_recent_divorce(families: List[Family]):
    today: datetime = datetime.now()
    div_list = []
    for family in families:
        if family.div is not None:
            if family.div:
                div_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")
                if today - div_date <= timedelta(days=30) and today - div_date >= timedelta(days=0):
                    div_list.append([family.id, family.husb, family.wife, family.div["date"]])
                    print(f"✔ Family ({family.id}): Divorce take place in last 30 days")
                else:
                    print(f"✘ Family ({family.id}): Divorce didn't take place in last 30 days")
        else:
            print(f"✘ Family ({family.id}): divorce didn't take place ")

    print("List of couple who had recent divorce: ")
    print(div_list)
    return div_list


# US 45
def Parents_and_child(family: Family, individuals: List[Individual]):
    childIdsList = []
    for childId in family.chil:
        childIdsList.append(childId)

    ParentsBirthDate = family.parent["date"]
    ParentsBirthDate = datetime.strptime(ParentsBirthDate, "%d %b %Y")

    chilBirthDates = []
    for chil in childIdsList:
        childBirth = next(ind.birt["date"] for ind in individuals if ind.id == chil)
        child_birth_date = datetime.strptime(childBirth, "%d %b %Y")
        chilBirthDates.append(child_birth_date)

    dangerous_child = []
    for chilBirt, childId in zip(chilBirthDates, childIdsList):
        if chilBirt <= ParentsBirthDate:
            dangerous_child.append(childId)
            print(f"✘ Family ({family.id}): Child ({childId}) parents and child birth date it is not same")
        else:
            print(f"✔  Family ({family.id}): Child ({childId}) Parents and child birth date it is same ")

    return dangerous_child


def Grand_Parents_and_Parents(family: Family, individuals: List[Individual]):
    ParetntIdList = []
    for parentID in family.chil:
        ParetntIdList.append(parentID)

    ParentsBirthDate = family.parent["date"]
    ParentsBirthDate = datetime.strptime(ParentsBirthDate, "%d %b %Y")

    parentBirthDates = []
    for parent in ParetntIdList:
        ParentBirth = next(ind.birt["date"] for ind in individuals if ind.id == parent)
        parent_birth_date = datetime.strptime(ParentBirth, "%d %b %Y")
        parentBirthDates.append(parent_birth_date)

    dangerous_family = []
    for parentBirth, parentID in zip(parentBirthDates, ParetntIdList):
        if parentBirth <= ParentsBirthDate:
            dangerous_family.append(parentID)
            print(f"✘ Family ({family.id}): Child ({parentID}) Grand parents and parents birth date it is not same")
        else:
            print(f"✔  Family ({family.id}): Child ({parentID}) Grand Parents and parents birth date it is same ")

    return dangerous_family


def girls_gender_check(individuals: List[Individual]) -> List:
    """ US63: girls gender should be female """

    girls = [ind for ind in individuals if ind.sex == 'F']
    did_not_match = []

    for girl in girls:
        if girl.sex != 'F':
            print(f"✘ {girl.id}: Gender does not match!")
            did_not_match.append(girl.id)

    return did_not_match


def list_of_twins(family: Family, individuals: List[Individual]) -> List:
    """ US63: find twins """

    children_id_birthday = {}
    for child_id in family.chil:
        child = next(ind for ind in individuals if ind.id == child_id)
        children_id_birthday[child_id] = child.birt['date']

    twins = {}
    for id, birthday in children_id_birthday.items():
        twins.setdefault(birthday, set()).add(id)

    res = list(filter(lambda x: len(x) > 1, twins.values()))
    return res[0]


def listExHusb(fam):
    l = []
    for i in fam:
        if 'HUSB' in fam[i]:
            l.append(fam[i]['HUSB'])
    return [x for n, x in enumerate(l) if x in l[:n]]


def girlMrgeAftr18(fam, ind):
    l = set()
    for i in fam:
        mrg_date = datetime.strptime(fam[i]['MARR'], "%d %b %Y")
        if 'WIFE' in fam[i]:
            w_id = fam[i]['WIFE']
        for j in ind:
            if i == ind[j]['family']:
                if j == w_id:
                    birt_date = datetime.strptime(ind[j]['BIRT'], "%d %b %Y")
                    diff = relativedelta(mrg_date, birt_date)
                    if diff.years > 18:
                        l.add(j)
    return l


def boys_gender_check(individuals: List[Individual]) -> List:
    """ US62: boys gender should be male """

    boys = [ind for ind in individuals if ind.sex == 'M']
    did_not_match = []

    for boi in boys:
        if boi.sex != 'M':
            print(f"✘ {boi.id}: Gender does not match!")
            did_not_match.append(boi.id)

    return did_not_match


def step_sib_birth_diff(family: Family, individuals: List[Individual]):
    """ US61: step brother and sister should not have same birth date """

    children_id_birthday = {}
    for child_id in family.chil:
        child = next(ind for ind in individuals if ind.id == child_id)
        children_id_birthday[child_id] = child.birt['date']

    twins = {}
    for id, birthday in children_id_birthday.items():
        twins.setdefault(birthday, set()).add(id)

    res = list(filter(lambda x: len(x) > 1, twins.values()))

    return False if len(res[0]) > 1 else True

#US_51
def all_divorce_couple(individuals: List[Individual], families:List[Family]):
    ind = []
    for indi in individuals:
        ind.append(indi.id)
    div = []
    for family in families:
        if family.div:
            if family.husb in ind and family.wife in ind:
                div.append(family.id)
                print("✔{family.id}:: in this family hubs and wife have no divorce")

            else:
                print("✘{family.id}:: in this family hubs and wife have divorce")
    return div

#US52
def birth_before_div(family: Family, individuals: Individual) -> bool:
    birth_date: datetime = datetime.strptime(individuals.birt['date'], "%d %b %Y")

    if family.div:  # condition for the divorce
        div_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")
        if div_date - birth_date > timedelta(minutes=0):
            print(f"✔ ({individuals.id}):birth is before divorce")
            return True
        else:
            print(f"✘ ({individuals.id}):birth is not before divorce")
            return False
    else:
        print(f"✘ ({individuals.id}):no divorce")
        return True

#us53
def List_recent_anniversary(families: List[Family]):
    today: datetime = datetime.now()
    marr_list = []
    for family in families:
        if family.marr is not None:
            if family.marr:
                marr_date: datetime = datetime.strptime(family.marr['date'], "%d %b %Y")
                if today - marr_date <= timedelta(days=30) and today - marr_date >= timedelta(days=0):
                    marr_list.append([family.id, family.husb, family.wife, family.marr["date"]])
                    print(f"✔ Family ({family.id}): Anniversary come in last 30 days")
                else:
                    print(f"✘ Family ({family.id}): Anniversary didn't come in last 30 days")
        else:
            print(f"✘ Family ({family.id}): Marrige didn't take place ")

    print("List of couple who had recent anniversaries: ")
    print(marr_list)
    return marr_list


##US54
def divorce_14(family: Family, individuals: List[Individual]) -> bool:
    
    divo_date: datetime = datetime.strptime(family.div['date'], "%d %b %Y")

    husb_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.husb)
    husb_birthday = datetime.strptime(husb_birthday, "%d %b %Y")
    husb_divo_age = divo_date.year - husb_birthday.year - \
                    ((divo_date.month, divo_date.day) < (husb_birthday.month, husb_birthday.day))

    wife_birthday = next(ind.birt['date'] for ind in individuals if ind.id == family.wife)
    wife_birthday = datetime.strptime(wife_birthday, "%d %b %Y")
    wife_divo_age = divo_date.year - wife_birthday.year - \
                    ((divo_date.month, divo_date.day) < (wife_birthday.month, wife_birthday.day))

    if husb_divo_age >= 14 and wife_divo_age >= 14:
        print(f"✔ Family ({family.id}): Both parents were at least 14 at the divorce date")
        return True

    if husb_divo_age < 14 and wife_divo_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_divo_age}) "
              f"and Wife ({wife_divo_age}) can not be less than 14")
    elif husb_divo_age < 14:
        print(f"✘ Family ({family.id}): Husband ({husb_divo_age}) can not be less than 14")
    elif wife_divo_age < 14:
        print(f"✘ Family ({family.id}): Wife ({wife_divo_age}) can not be less than 14")

    return False    

##US55

def all_sister(individuals: List[Individual]) -> List:
    girls = [ind for ind in individuals if ind.sex == 'F']
    sis = []

    for boi in girls:
        if boi.sex != 'F':
            print(f"✘ {boi.name}: it not a sister !")
            sis.append(boi.name)

    return sis
def mrgeAfter18(fam, ind):
        l = set()
        for i in fam:
            mrg_date = datetime.strptime(fam[i]['MARR'], "%d %b %Y")
            if 'HUSB' in fam[i]:
                h_id = fam[i]['HUSB']
            for j in ind:
                if i == ind[j]['family']:
                    if j == h_id:
                        birt_date = datetime.strptime(ind[j]['BIRT'], "%d %b %Y")
                        diff = relativedelta(mrg_date, birt_date)
                        if diff.years > 18:
                            l.add(j)
        return l

def twins_birth_date(family: Family, individuals: List[Individual]):

    children_id_birthday = {}
    for child_id in family.chil:
        child = next(ind for ind in individuals if ind.id == child_id)
        children_id_birthday[child_id] = child.birt['date']

    twins = {}
    for id, birthday in children_id_birthday.items():
        twins.setdefault(birthday, set()).add(id)

        res = list(filter(lambda x: len(x) > 1, twins.values()))
        return True if len(res[0]) > 1 else False



##US56
def listExwife(fam):
    l = []
    for i in fam:
        if 'WIFE' in fam[i]:
            l.append(fam[i]['WIFE'])
    return [x for n, x in enumerate(l) if x in l[:n]]


    
def list_male(individuals: List[Individual]):
    
    male = []
    for indivi in individuals:
        if indivi.sex == "Male":
            male.append(indivi.id)
            print(f"{indivi.id}:: people is male")
        else:
            print(f"{indivi.id}:: not male")

    return male

def list_female(individuals: List[Individual]):
    
    female = []
    for indivi in individuals:
        if indivi.sex == "Female":
            female.append(indivi.id)
            print(f"{indivi.id}:: people is female")
        else:
            print(f"{indivi.id}:: not female")

    return female   
