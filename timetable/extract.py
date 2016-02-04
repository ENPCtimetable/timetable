# encoding utf8
# Importation des donnees contenues dans le fichier excel

# xlrd doit être téléchargé
import xlrd
import datetime

# La fonction transforme la string contenue dans le excel en datetime.date
def imp_datefromexl(exl_str):
    list = []
    splited = exl_str.split(",")
    for i in range(0,3):
        str = splited[i].strip(" ")
        if str.isdigit():
            nbr = int(str)
            list.insert(i,nbr)
    date = datetime.date(list[2],list[1],list[0])
    return date

# La fonction transforme la string contenue dans le excel en datetime.time
def imp_timefromexl(exl_str):
    list = []
    splited = exl_str.split(",")
    for i in range(0,2):
        str = splited[i].strip(" ")
        if str.isdigit():
            nbr = int(str)
            list.insert(i,nbr)
    time = datetime.time(list[0],list[1])
    return time

###########################################################################
# Les classes utilisés

# La classe des salles avec aile, étage, numéro
class Room:
    def __init__(self,building,floor,number):
        self.build = building
        self.floor = floor
        self.nbr = number
    def __repr__(self):
        if self.build != 0:
            if self.nbr >= 10:
                str = "{} {}{}".format(self.build, self.floor, self.nbr)
            else:
                str = "{} {}0{}".format(self.build, self.floor, self.nbr)
        else:
            str = "{}".format(self.nbr)
        return str
    def __eq__(self,otheroom):
        if (self.build == otheroom.build 
        and self.floor == otheroom.floor
        and self.nbr == otheroom.nbr):
            return True
        else:
            return False
    def imp_room(self,exl_str):
        if exl_str[0] in ["V","P","M","B"]:
            self.build = exl_str[0]
            str = exl_str[1:]
            str = str.strip(" ")
            if str.isdigit():
                integr = int(str)
                nbr = integr % 100
                self.nbr = nbr
                hundred = integr - nbr
                floor = int(hundred / 100)
                self.floor = floor
        else:
            self.nbr = exl_str

# La classe qui contient des salles classées en dico par room_type
# Le nom de la salle est toujours une liste suivie ou non des horaires de disponibilité
class RoomDico:
    def __init__(self,dicooflist):
        self.dico = dicooflist
    def imp_excel(self, address, sheet_name,list_column):
        self.dico = {}
        wb = xlrd.open_workbook(address)
        sheet = wb.sheet_by_name(sheet_name)
        for rownum in range(1,sheet.nrows):
            room_type = sheet.row_values(rownum)[1]
            exl_str = sheet.row_values(rownum)[2]
            room = Room(0,0,0)
            room.imp_room(exl_str)
            if room_type not in self.dico:
                self.dico[room_type] = [[room]]
            else:
                notin = True
                for i in range(len(self.dico[room_type])):
                    if room == self.dico[room_type][i][0]:
                        notin = False
                        break
                if notin:
                    self.dico[room_type].append([room])
    def adopenclose(self,open,close):
        for key in self.dico:
            for i in range(len(self.dico[key])):
                self.dico[key][i].append([open,close])
    def available(self,rooms,today,timetable):
        self.dico = rooms.dico
        for row in range(1,len(timetable.table)):
            if timetable.table[row][4] == today:
                room_type = timetable.table[row][1]
                room = timetable.table[row][2]
                begin = timetable.table[row][5]
                end = timetable.table[row][6]
                for i in range(len(self.dico[room_type])):
                    if self.dico[room_type][i][0] == room:
                        for j in range(1,len(self.dico[room_type][i])):
                            avbegin = self.dico[room_type][i][j][0]
                            avend = self.dico[room_type][i][j][1]
                            if (avbegin <= begin
                            and end <= avend):
                                self.dico[room_type][i][j][1] = begin
                                self.dico[room_type][i].insert(j+1,[end,avend])
                            #break
                        #break
                #break


# La classe qui contient les cours disponibles à partir d'aujourd'hui.
# C'est une liste de liste formant un tableau dont la première colonne
# contient le département, la deuxième le nom du cours.
class Lessons:
    def __init__(self, listoflist):
        self.table = listoflist
    def imp_all(self, timetable):
        self.table = []
        for i in range(1,len(timetable.table)):
            lesson = timetable.table[i][3]
            notin = True
            for j in range(len(self.table)):
                if lesson == self.table[j][1]:
                    notin = False
                    break
            if notin:
                index = len(self.table)
                list = [timetable.table[i][0],lesson]
                self.table.insert(index,list)

# La classe qui contient toutes les données de bases à partir d'un jour
class TimeTable:
    def __init__(self, listoflist):
        self.table = listoflist
    def imp_excel(self, address, sheet_name, list_column,today):
        self.table = []
        wb = xlrd.open_workbook(address)
        sheet = wb.sheet_by_name(sheet_name)
        # Importation des titres
        row = []
        for column in range(len(list_column)):
            value = sheet.row_values(0)[list_column[column]]
            row.insert(column,value)
        self.table.insert(0,row)
        # Importation des données
        for rownum in range(1,sheet.nrows):
            row = []
            exl_str = sheet.row_values(rownum)[list_column[4]]
            date = imp_datefromexl(exl_str)
            # Comparaison avec aujourd'hui pour aléger le nombre de données
            if date >= today:
                for column in range(len(list_column)):
                    if column == 2:
                        exl_str = sheet.row_values(rownum)[list_column[column]]
                        room = Room(0,0,0)
                        room.imp_room(exl_str)
                        value = room
                    elif column == 4:
                        value = date
                    elif (column == 5 or column == 6):
                        exl_str = sheet.row_values(rownum)[list_column[column]]
                        value = imp_timefromexl(exl_str)
                    else:
                        value = sheet.row_values(rownum)[list_column[column]]
                    row.insert(column,value)
                self.table.insert(rownum,row)

def importation(): 
    #####################################################################
    #Liste permettant de s'adapter à une modification  
    #de l'ordre des colonnes sur excel
    list_column = [0,1,2,3,4,6,7]
    #####################################################################
    #Opérations annuelles
    #Importation de toutes les salles de l'école
    rooms = RoomDico({})
    rooms.imp_excel("utilisation-salles.xls", u'utilisation-salles',list_column)
    #####################################################################
    #Opérations quotidiennes
    now = datetime.datetime.now()
    today = datetime.date(now.year,now.month,now.day)
    # Importation du excel
    T = TimeTable([])
    T.imp_excel("utilisation-salles.xls", u'utilisation-salles',list_column,today)
    # Création de la liste des cours disponibles
    base = Lessons([])
    base.imp_all(T)
    # Définition des horaires d'ouverture et de fermeture des salles
    open = datetime.time(8,0)
    close = datetime.time(22,0)
    rooms.adopenclose(open,close)
    # Création du dictionnaire des salles avec leur disponibilité
    dispo = RoomDico({})
    dispo.available(rooms,today,T)
    return dispo.dico
