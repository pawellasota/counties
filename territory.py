class Territory:
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
        handler = open(filename, "r")
        data = handler.readlines()
        for row in data[1:]:
            row = row.strip()
            row = row.split("\t")
            cls.global_list.append(row)

    def create_objects(self):
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
        return len(self.name)

    def count_subdivisions(self):
        return [len(self.wojewodztwa)]


    def cities_with_longest_names(self):
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
        largest_communities = 0
        largest_powiat = None
        for wojewodztwo in self.wojewodztwa:
            for powiat in wojewodztwo.powiaty:
                if powiat.count_communities() > largest_communities:
                   largest_powiat = powiat
                   largest_communities = powiat.count_communities()
        return largest_powiat.name

    def locations_with_several_categories(self):
        return list([x, Territory.names.count(x)] for x in set(Territory.names) if Territory.names.count(x) > 1)


    def advanced_search(self, keyword):
        output_list = [names_extended for names_extended in Territory.names_extended if str(keyword) in
                       str(names_extended[0])]
        output = sorted(output_list, key=lambda tup: (tup[0], tup[1]))
        if not output:
            return False
        return output

    def count_entities(self):
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
    def __init__(self, _id, name, type):
        super().__init__(_id, name, type)
        self.powiaty = []
        self.miasta_na_prawach_powiatu = []
        self.delegatury = []

    def count_subdivisions(self):
        count_miasta = sum([len(miasto.gminy_miejskie) for miasto in self.miasta_na_prawach_powiatu])
        return [len(self.powiaty), len(self.miasta_na_prawach_powiatu), len(self.delegatury), count_miasta]

class Powiat(Territory):
    def __init__(self, _id, name, type):
        super().__init__(_id, name, type)
        self.gminy_wiejskie = []
        self.gminy_miejskie = []
        self.gminy_miejsko_wiejskie = []
        self.miasta_w_gminie = []
        self.obszary_wiejskie_w_gminach = []

    def count_subdivisions(self):
        return [len(self.gminy_wiejskie), len(self.gminy_miejskie), len(self.gminy_miejsko_wiejskie), len(self.miasta_w_gminie),
                len(self.obszary_wiejskie_w_gminach)]

    def count_communities(self):
        return len(self.gminy_miejskie) + len(self.gminy_miejsko_wiejskie) + len(self.gminy_wiejskie) + len(self.miasta_w_gminie) +len(self.obszary_wiejskie_w_gminach)


class Gmina(Territory):
    def __init__(self, _id, name, type):
        super().__init__(_id, name, type)

class Delegatura(Territory):
    def __init__(self, name, type):
        super().__init__(name, type)
