import hashlib
import sqlite3
from flask_restful import reqparse


my_args = reqparse.RequestParser()
my_args.add_argument("superhero_name", type=str, help="superhero_name is not defined or has wrong type!")
my_args.add_argument("full_name", type=str, help="full_name is not defined or has wrong type!")
my_args.add_argument("gender_id", type=int, help="gender_id is not defined or has wrong type!")
my_args.add_argument("eye_colour_id", type=int, help="eye_colour_id is not defined or has wrong type!")
my_args.add_argument("hair_colour_id", type=int, help="hair_colour_id is not defined or has wrong type!")
my_args.add_argument("skin_colour_id", type=int, help="skin_colour_id is not defined or has wrong type!")
my_args.add_argument("race_id", type=int, help="race_id is not defined or has wrong type!")
my_args.add_argument("publisher_id", type=int, help="publisher_id is not defined or has wrong type!")
my_args.add_argument("alignment_id", type=int, help="alignment_id is not defined or has wrong type!")
my_args.add_argument("height_cm", type=int, help="height_cm is not defined or has wrong type!")
my_args.add_argument("weight_kg", type=int, help="weight_kg is not defined or has wrong type!")
my_args.add_argument("power_name", type=str, help="power_name is not defined or has wrong type!")
my_args.add_argument("new_superhero_name", type=str, help="new_superhero_name is not defined or has wrong type!")

my_args.add_argument("login", type=str, help="login is not defined or has wrong type!")
my_args.add_argument("password", type=str, help="password is not defined or has wrong type!")


def loginQuery(args):
    if args['login'] == None or args["password"] == None:
            return {"INFO" : "login or password was not entered"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    h = hashlib.new('sha256')
    h.update(bytes(args["password"], 'UTF-8'))
    hashedPasswower = h.hexdigest()

    query = '''SELECT users.role
    FROM users
    WHERE users.login = \"{login}\" AND users.password = \"{password}\"'''.format(login = args["login"], password = hashedPasswower)

    res = dbcursour.execute(query)
    
    role = {}
    for row in res:
        print(row[0], "kek")
        role["role"] = row[0]

    print(role)
    if len(role):
        return role
    else:
        return {"INFO": "These's no user with this login and password"}



def getAllHeroes():
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    heroes = []
    
    res = dbcursour.execute("SELECT superhero_name FROM superhero")
    names = list(map(lambda x: x[0], dbcursour.description))

    for row in res:
        hero = {}
        for i in range(len(names)):
            hero[names[i]] = row[i]
        heroes.append(hero)

    
    con.close()
    return heroes


def getHeroByName(superhero_name):
    if superhero_name == None:
        return {"INFO" : "superhero_name field is not defined"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    res = dbcursour.execute("SELECT superhero.id, " +
    "superhero.superhero_name, " +
    "superhero.full_name, " +
    "gender.gender, " +
    "race.race, " +
    "alignment.alignment, " +
    "skincolor.colour as skin_colour, " +
    "haircolor.colour as hair_colour, " +
    "eyecolor.colour as eye_colour, " +
    "publisher.publisher_name, " +
    "superhero.height_cm, " +
    "superhero.weight_kg " +
    "FROM superhero " +
    "LEFT JOIN colour as skincolor on skincolor.id = superhero.skin_colour_id " +
    "LEFT JOIN colour as haircolor on haircolor.id = superhero.hair_colour_id " +
    "LEFT JOIN colour as eyecolor on eyecolor.id = superhero.eye_colour_id " +
    "LEFT JOIN gender on gender.id = superhero.gender_id " +
    "LEFT JOIN race on race.id = superhero.race_id " +
    "LEFT JOIN publisher on publisher.id = superhero.publisher_id " +
    "LEFT JOIN alignment on alignment.id = superhero.alignment_id " +
    "WHERE superhero.superhero_name = \"{name}\"".format(name=superhero_name) )

    names = list(map(lambda x: x[0], dbcursour.description))

    hero = {}
    for row in res:
        for i in range(len(names)):
            hero[names[i]] = row[i]
    con.close()

    if len(hero) == 0:
        return {"INFO" : "There's no such superhero"}

    return hero

def insertHero(args):
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()
    
    res = dbcursour.execute("INSERT INTO superhero (superhero_name,  full_name,  gender_id,  eye_colour_id, " + 
    "hair_colour_id,  skin_colour_id,  race_id,  publisher_id,  alignment_id,  height_cm,  weight_kg) " +
    "VALUES (\"{sname}\", \"{fname}\", {gid}, {eid}, {hid}, {sid}, {rid}, {pid}, {aid}, {h}, {w});".format(sname=args["superhero_name"],
                                                                                                            fname=args["full_name"],
                                                                                                            gid=args["gender_id"],
                                                                                                            eid=args["eye_colour_id"],
                                                                                                            hid=args["hair_colour_id"],
                                                                                                            sid=args["skin_colour_id"],
                                                                                                            rid=args["race_id"],
                                                                                                            pid=args["publisher_id"],
                                                                                                            aid=args["alignment_id"],
                                                                                                            h=args["height_cm"],
                                                                                                            w=args["weight_kg"]))
    con.commit()
    con.close()

    return {"INFO" : "Hero was inserted"}

def updateHero(args):
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    isEmpty = True

    query = """UPDATE superhero  
    SET """
    if (args["superhero_name"] != None):
        isEmpty = False
        query += "superhero_name = \"{superhero_name}\" ,".format(superhero_name = args["superhero_name"])

    if (args["full_name"] != None):
        isEmpty = False
        query += "full_name = \"{full_name}\" ,".format(full_name = args["full_name"])

    if (args["gender_id"] != None):
        isEmpty = False
        query += "gender_id = \"{gender_id}\" ,".format(gender_id = args["gender_id"])

    if (args["eye_colour_id"] != None):
        isEmpty = False
        query += "eye_colour_id = \"{eye_colour_id}\" ,".format(eye_colour_id = args["eye_colour_id"])

    if (args["hair_colour_id"] != None):
        isEmpty = False
        query += "hair_colour_id = \"{hair_colour_id}\" ,".format(hair_colour_id = args["hair_colour_id"])

    if (args["skin_colour_id"] != None):
        isEmpty = False
        query += "skin_colour_id = \"{skin_colour_id}\" ,".format(skin_colour_id = args["skin_colour_id"])

    if (args["race_id"] != None):
        isEmpty = False
        query += "race_id = \"{race_id}\" ,".format(race_id = args["race_id"])

    if (args["publisher_id"] != None):
        isEmpty = False
        query += "publisher_id = \"{publisher_id}\" ,".format(publisher_id = args["publisher_id"])

    if (args["alignment_id"] != None):
        isEmpty = False
        query += "alignment_id = \"{alignment_id}\" ,".format(alignment_id = args["alignment_id"])

    if (args["height_cm"] != None):
        isEmpty = False
        query += "height_cm = \"{height_cm}\" ,".format(height_cm = args["height_cm"])

    if (args["weight_kg"] != None):
        isEmpty = False
        query += "weight_kg = \"{weight_kg}\" ,".format(weight_kg = args["weight_kg"])

    if isEmpty:
        return {"INFO" : "There's nothing to update"}
    query = query[:-1]

    query += "WHERE superhero.superhero_name = \"{superhero_name}\"".format(superhero_name = args["superhero_name"])

    res = dbcursour.execute(query)

    con.commit()
    con.close()

    return {"INFO" : "Hero was updated"}


def deleteHero(args):

    if args["superhero_name"] == None:
        return {"INFO" : "superhero_name field is not defined"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''DELETE FROM superhero
    WHERE superhero.superhero_name = \"{superhero_name}\"'''.format(superhero_name = args["superhero_name"])

    res = dbcursour.execute(query)

    con.commit()
    con.close()

    return {"INFO" : "{superhero_name} DELETED".format(superhero_name = args["superhero_name"])}


def getHeroSuperpowers(args):
    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    powers = {"superpowers" : []}

    query = """SELECT superpower.power_name
    FROM superpower
    WHERE superpower.id IN (SELECT hero_power.power_id
						FROM hero_power
						WHERE hero_power.hero_id = (SELECT superhero.id
													FROM superhero
													WHERE superhero.superhero_name = \"{superhero_name}\"))""".format(superhero_name = args["superhero_name"])

    res = dbcursour.execute(query)

    for row in res:
        powers["superpowers"].append(row[0])
    
    con.close()
    return powers


def insertHeroPower(args):
    if args["superhero_name"] == None or args["power_name"] == None:
        return {"INFO" : "superhero_name or power_name field is not defined"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''INSERT INTO superpower (power_name)
    SELECT name
    FROM (
            SELECT \"{power_name}\" as name
        ) as o
    WHERE NOT EXISTS (SELECT * from superpower WHERE superpower.power_name == o.name)'''.format(power_name = args["power_name"])

    res = dbcursour.execute(query)

    query = '''INSERT INTO hero_power (hero_id, power_id)
    VALUES ((SELECT superhero.id
            FROM superhero
            WHERE superhero.superhero_name = \"{superhero_name}\"), (SELECT superpower.id
                                            FROM superpower
                                            where superpower.power_name = \"{power_name}\"));'''.format(superhero_name = args["superhero_name"], power_name = args["power_name"])
    res = dbcursour.execute(query)
    
    con.commit()
    con.close()

    return {"INFO" : "{power_name} power was added to {superhero_name}".format(superhero_name = args["superhero_name"], power_name = args["power_name"])}

def deleteHeroPower(args):
    if args["power_name"] == None:
        return {"INFO" : "superhero_name field is not defined"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''DELETE FROM hero_power
    WHERE hero_power.power_id = (SELECT superpower.id
                                FROM superpower
                                WHERE superpower.power_name = \"{power_name}\")'''.format(power_name = args["power_name"])
    res = dbcursour.execute(query)
                                                                                 
    query = '''DELETE FROM superpower
    WHERE superpower.power_name = \"{power_name}\" '''.format(power_name = args["power_name"])

    res = dbcursour.execute(query)

    con.commit()
    con.close()

    return {"INFO" : "{power_name} power was deleted for all heroes((".format(power_name = args["power_name"])}


def updateHeroPower(args):
    if args["superhero_name"] == None or args["power_name"] == None or args["new_superhero_name"] == None:
        return {"INFO" : "superhero_name or power_name or new_superhero_name field is not defined"}

    con = sqlite3.connect("database.db", check_same_thread=False)
    dbcursour = con.cursor()

    query = '''UPDATE hero_power
    SET hero_id = (SELECT superhero.id
                                FROM superhero
                                WHERE superhero.superhero_name = \"{new_superhero_name}\")
    WHERE hero_power.power_id = (SELECT superpower.id
                    FROM superpower
                    where superpower.power_name = \"{power_name}\")  AND hero_power.hero_id = (SELECT superhero.id
																					FROM superhero
																					WHERE superhero.superhero_name = \"{superhero_name}\")'''.format(new_superhero_name = args["new_superhero_name"],
                                                                                                                                                     power_name = args["power_name"],
                                                                                                                                                     superhero_name = args["superhero_name"])
    
    res = dbcursour.execute(query)
    con.commit()
    con.close()

    return {"INFO" : "{new_superhero_name} now has {superhero_name}'s {power_name} power".format(new_superhero_name = args["new_superhero_name"],
                                                                                                                                                     power_name = args["power_name"],
                                                                                                                                                     superhero_name = args["superhero_name"])}