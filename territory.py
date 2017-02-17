class Territory:
    """Represents abstract administrative subdivision object.

        Class attributes:
            global_list (list of lists): table loaded from csv file.
            names (list): names of each entities.
            names_extended (list): names with types of each entities.
        Attributes:
            _id (str): id number of particular entity.
            name(str): name of entity.
            type(str): type of entity
            wojewodztwa(list): list of wojewodztwa objects
    """
    global_list = []
    names = []
    names_extended = []

    def __init__(self, _id=None, name=None, type=None):
        self._id = _id
        self.name = name
        self.type = type
        self.wojewodztwa = []
        Territory.names.append(self.name)
        Territory.names_extended.append([self.name, self.type])

    @classmethod
    def import_csv(cls, filename):
        """
        Imports data from csv file into global_list table.

        Args:
            filename (str): path to csv file

        Returns:
            None
        """
        handler = open(filename, "r")
        data = handler.readlines()
        for row in data[1:]:
            row = row.strip()
            row = row.split("\t")
            cls.global_list.append(row)

    def create_objects(self):
        """
        Creates objects for all entities.

        Args:
            None

        Returns:
            None
        """
        for row in Territory.global_list:
            number = row[0] + row[1] + row[2] + row[3]
            if len(number) == 2:
                wojewodztwo = Wojewodztwo(row[0], row[4], row[5])
                self.wojewodztwa.append(wojewodztwo)
                for row in Territory.global_list:
                    if row[5] == "miasto na prawach powiatu" and wojewodztwo._id == row[0]:
                        miasto_na_prawach_powiatu = Powiat(row[1], row[4], row[5])
                        wojewodztwo.miasta_na_prawach_powiatu.append(miasto_na_prawach_powiatu)
                        for row in Territory.global_list:
                            if row[5] == "gmina miejska" and miasto_na_prawach_powiatu._id == row[1]:
                                gmina = Gmina(row[2], row[4],  row[5])
                                miasto_na_prawach_powiatu.gminy_miejskie.append(gmina)
                    elif row[5] == "delegatura" and wojewodztwo._id == row[0]:
                        delegatura = Delegatura(row[4], row[5])
                        wojewodztwo.delegatury.append(delegatura)
                    elif row[5] == "powiat" and wojewodztwo._id == row[0]:
                        powiat = Powiat(row[1], row[4], row[5])
                        wojewodztwo.powiaty.append(powiat)
                        for row in Territory.global_list:
                            if row[5] == "gmina wiejska" and powiat._id == row[1]:
                                gmina = Gmina(row[2], row[4],  row[5])
                                powiat.gminy_wiejskie.append(gmina)
                            elif row[5] == "gmina miejska" and powiat._id == row[1]:
                                gmina = Gmina(row[2], row[4],  row[5])
                                powiat.gminy_miejskie.append(gmina)
                            elif row[5] == "gmina miejsko-wiejska" and powiat._id == row[1]:
                                gmina = Gmina(row[2], row[4], row[5])
                                powiat.gminy_miejsko_wiejskie.append(gmina)
                            elif row[5] == "miasto" and powiat._id == row[1]:
                                gmina = Gmina(row[2], row[4], row[5])
                                powiat.miasta_w_gminie.append(gmina)
                            elif row[5] == "obszar wiejski" and powiat._id == row[1]:
                                gmina = Gmina(row[2], row[4], row[5])
                                powiat.obszary_wiejskie_w_gminach.append(gmina)

    def name_lenght(self):
        """
        Returns length of name attribute.

        Args:
            None

        Returns:
            (int): length of name attribute.
        """
        return len(self.name)

    def count_subdivisions(self):
        """
        Counts number of subdivisions of particular entity.

        Args:
            None

        Returns:
            (list of int): entity subdivisions quantity.
        """
        return [len(self.wojewodztwa)]


    def cities_with_longest_names(self):
        """
        Seeks for 3 cities with longest names

        Args:
            None

        Returns:
            (list of str): 3 longest names
        """
        longest = []
        output = []
        for wojewodztwo in self.wojewodztwa:
            longest.extend(wojewodztwo.miasta_na_prawach_powiatu)
            for powiat in wojewodztwo.powiaty:
                longest.extend(powiat.miasta_w_gminie)
        longest_sort = sorted(longest, key=lambda x: x.name_lenght(), reverse=True)
        for city in longest_sort[:3]:
            output.append(city.name)
        return output


    def counties_with_largest_communities(self):
        """
        Finds county's with the largest number of communities

        Args:
            None

        Returns:
            (str): county's name.
        """
        largest_communities = 0
        largest_powiat = None
        for wojewodztwo in self.wojewodztwa:
            for powiat in wojewodztwo.powiaty:
                if powiat.count_communities() > largest_communities:
                   largest_powiat = powiat
                   largest_communities = powiat.count_communities()
        return largest_powiat.name

    def locations_with_several_categories(self):
        """
        Finds locations, that belong to more than one category

        Args:
            None

        Returns:
            (list of lists): names of territory entities and quantities of locations of this entities.
        """
        return list([name, Territory.names.count(name)] for name in set(Territory.names) if Territory.names.count(name) > 1)


    def advanced_search(self, keyword):
        """
        Search for entities which matches string pattern given

        Args:
            keyword(str): string to find in entities names given by user

        Returns:
            (list of lists): names of territory entities (and their types) which match user keyword.
            (False): if keyword given doesnt match any entities names
        """
        output_list = [names_extended for names_extended in Territory.names_extended if str(keyword) in
                       str(names_extended[0])]
        output = sorted(output_list, key=lambda tup: (tup[0], tup[1]))
        if not output:
            return False
        return output

    def count_entities(self):
        """
        Counts entities of each categories.

        Args:
            None

        Returns:
            (list of int): numbers of entities.
        """
        wojewodztwa_quantity, miasta_na_prawach_powiatu_quantity, powiaty_quantity, gminy_wiejskie_quantity, gminy_miejskie_quantity, gminy_miejsko_wiejskie_quantity, miasta_w_gminie_quantity, obszary_wiejskie_w_gminach_quantity, delegatury_quantity = 0, 0, 0, 0, 0, 0, 0, 0, 0
        wojewodztwa_quantity += self.count_subdivisions()[0]
        for wojewodztwo in self.wojewodztwa:
            powiaty_quantity += wojewodztwo.count_subdivisions()[0]
            miasta_na_prawach_powiatu_quantity += wojewodztwo.count_subdivisions()[1]
            delegatury_quantity += wojewodztwo.count_subdivisions()[2]
            gminy_miejskie_quantity += wojewodztwo.count_subdivisions()[3]
            for powiat in wojewodztwo.powiaty:
                gminy_wiejskie_quantity += powiat.count_subdivisions()[0]
                gminy_miejskie_quantity += powiat.count_subdivisions()[1]
                gminy_miejsko_wiejskie_quantity += powiat.count_subdivisions()[2]
                miasta_w_gminie_quantity += powiat.count_subdivisions()[3]
                obszary_wiejskie_w_gminach_quantity += powiat.count_subdivisions()[4]
        return [wojewodztwa_quantity, miasta_na_prawach_powiatu_quantity + powiaty_quantity,
                gminy_miejskie_quantity, gminy_wiejskie_quantity, gminy_miejsko_wiejskie_quantity,
                obszary_wiejskie_w_gminach_quantity, miasta_w_gminie_quantity, miasta_na_prawach_powiatu_quantity, delegatury_quantity]


class Wojewodztwo(Territory):
    """Represents 'wojewodztwo' administrative subdivision object.

        Parent: Territory

        Attributes:
            _id (str): id number of wojewodztwo.
            name(str): name of wojewodztwo.
            type(str): type of entity
            powiaty(list): list of powiat objects which this wojewodztwo entity contains
            miasta_na_prawach_powiatu(list): list of powiat objects which this wojewodztwo entity contains
            delegatury(list): list of delegatura objects which this wojewodztwo entity contains
    """
    def __init__(self, _id, name, type):
        super().__init__(_id, name, type)
        self.powiaty = []
        self.miasta_na_prawach_powiatu = []
        self.delegatury = []

    def count_subdivisions(self):
        """
        Counts number of subdivisions in wojewodztwo object.

        Args:
            None

        Returns:
            (list of ints): subdivisions quantity.
        """
        count_miasta = sum([len(miasto.gminy_miejskie) for miasto in self.miasta_na_prawach_powiatu])
        return [len(self.powiaty), len(self.miasta_na_prawach_powiatu), len(self.delegatury), count_miasta]

class Powiat(Territory):
    """Represents 'powiat' administrative subdivision object.

        Parent: Territory

        Attributes:
            _id (str): id number of powiat.
            name(str): name of powiat.
            type(str): type of entity
            gminy_wiejskie(list of objects): list of Gmina objects which this Powiat entity contains
            gminy_miejskie(list of objects): list of Gmina objects which this Powiat entity contains
            gminy_miejsko_wiejskie(list of objects): list of Gmina objects which this Powiat entity contains
            miasta_w_gminie(list of objects): list of Gmina objects which this Powiat entity contains
            obszary_wiejskie_w_gminach(list of objects): list of Gmina objects which this Powiat entity contains
    """
    def __init__(self, _id, name, type):
        super().__init__(_id, name, type)
        self.gminy_wiejskie = []
        self.gminy_miejskie = []
        self.gminy_miejsko_wiejskie = []
        self.miasta_w_gminie = []
        self.obszary_wiejskie_w_gminach = []

    def count_subdivisions(self):
        """
        Counts number of subdivisions in Powiat object.

        Args:
            None

        Returns:
            (list of ints): subdivisions quantity.
        """
        return [len(self.gminy_wiejskie), len(self.gminy_miejskie), len(self.gminy_miejsko_wiejskie), len(self.miasta_w_gminie),
                len(self.obszary_wiejskie_w_gminach)]

    def count_communities(self):
        """
        Counts number of communities in Powiat object.

        Args:
            None

        Returns:
            (list of ints): subdivisions quantity.
        """
        return len(self.gminy_miejskie) + len(self.gminy_miejsko_wiejskie) + len(self.gminy_wiejskie) + len(self.miasta_w_gminie) +len(self.obszary_wiejskie_w_gminach)


class Gmina(Territory):
    """Represents 'gmina' administrative subdivision object.

        Parent: Territory

        Attributes:
            _id (str): id number of Gmina.
            name(str): name of Gmina.
            type(str): type of entity
    """
    def __init__(self, _id, name, type):
        super().__init__(_id, name, type)

class Delegatura(Territory):
    """Represents 'delegatura' administrative subdivision object.

        Parent: Territory

        Attributes:
            _id (str): id number of Delegatura.
            name(str): name of Delegatura.
            type(str): type of entity
    """
    def __init__(self, name, type):
        super().__init__(name, type)
