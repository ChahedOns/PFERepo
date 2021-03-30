from random import random
from urllib import request

from flask_mail import Mail, Message
from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from APIConst import db_name, user_pwd, secret_key

# configurations !
app = Flask(__name__)
DB_URI = f"mongodb+srv://OnsChahed:{user_pwd}@pfecluster.c2obu.mongodb.net/{db_name}?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
mail = Mail()
db.init_app(app)
mail.init_app(app)


class Vehicule(db.Document):
    mat = db.StringField()
    ty = db.StringField()
    an = db.IntField()
    mr = db.StringField()
    tyC = db.StringField()
    conso = db.IntField()
    powr = db.IntField()
    clim = db.BooleanField()
    para = db.BooleanField()
    vid = db.BooleanField()
    mout = db.BooleanField()
    pneau = db.BooleanField()
    etat = db.StringField()
    cap = db.FloatField()
    dispo = db.BooleanField()
    kilo = db.FloatField()
    nb = db.IntField()

    def set_etat(self):

        if self.clim == True and self.para == True and self.pneau == True and self.vid == True and self.mout == True:
            self.etat = "Validé"
        else:
            self.etat = "Terminer tous les entretiens"
            self.dispo = False

    def to_json(self):
        return {

            "Matricule ": self.mat,
            "Type de véhicules ": self.ty,
            "Année de Fabrication": self.an,
            "Marque ": self.mr,
            "Power": self.powr,
            "Type Carburant ": self.tyC,
            "Consomation Carburant (L)": self.conso,
            "Kilométrage": self.kilo,
            "Nombre des Places ": self.nb,
            "Capacité (kg) ": self.cap,
            "Maintenance ": {
                "Climatisation": self.clim,
                "Parallélisme": self.para,
                "Vidange": self.vid,
                "Pneaumatique": self.pneau,
                "Mouteur": self.mout,
                "Etat": self.etat
            },
            "Disponibilité": self.dispo

        }


class Chauffeur(db.Document):
    counter = 0
    idCh = db.IntField()
    nom = db.StringField()
    pre = db.StringField()
    num = db.StringField()
    dn = db.StringField()
    de = db.StringField()
    mail = db.StringField()
    pwd = db.StringField()
    adr = db.StringField()
    nomSup = db.StringField()
    sup = db.IntField()

    def addpwd(self):
        liste = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9']
        motDePass = []
        n = 1
        while n <= 25:
            c = int(random() * 62)
            motDePass.append(liste[c])  # Liste motDePass mis a jour
            n = n + 1

        """msg = Message(
            f"Hello{self.nom} {self.pre} This is your App Password : {motDePass} use it to login and becareful ",
            sender="mail@gmail.com", recipients=self.mail)
        mail.send(msg)"""
        ch = ""
        for c in motDePass:
            ch = ch + str(c)

        return ch

    def set_id(self):
        Chauffeur.counter += 1
        self.idCh = Chauffeur.counter

    def set_pwd(self):
        self.pwd = str(hash(self.addpwd()))

    def to_json(self):
        return {

            "ID Chauffeur ": self.idCh,
            "Nom ": self.nom,
            "prénom": self.pre,
            "N° Télephone ": self.num,
            "Date Naissance ": self.dn,
            "Date Embauche": self.de,
            "Adresse ": self.adr,
            "Email": self.mail,
            "Mot de passe ": self.pwd,
            "Nom Superviseur": self.nomSup

        }


class Superviseur(db.Document):
    counter = 0
    idsup = db.IntField()
    nom = db.StringField()
    pre = db.StringField()
    num = db.StringField()
    dn = db.DateField()
    de = db.DateField()
    mail = db.StringField()
    pwd = db.StringField()
    adr = db.StringField()

    def set_id(self):
        Superviseur.counter += 1
        self.idsup = Superviseur.counter

    def set_pwd(self):
        self.pwd = str(hash(self.pwd))

    def to_json(self):
        return {

            "ID Superviseur": self.idsup,
            "Nom": self.nom,
            "prénom": self.pre,
            "N° Télephone": self.num,
            "Date Naissance": self.dn,
            "Date Embauche": self.de,
            "Adresse": self.adr,
            "Email": self.mail,
            "Mot de passe": self.pwd,

        }


class Users(db.Document):
    nom = db.StringField()
    pre = db.StringField()
    num = db.StringField()
    dn = db.DateField()
    mail = db.StringField()
    pwd = db.StringField()
    adr = db.StringField()

    def set_pwd(self):
        self.pwd = str(hash(self.pwd))

    def to_json(self):
        return {

            "Nom ": self.nom,
            "prénom": self.pre,
            "N° Télephone ": self.num,
            "Date Naissance ": self.dn,
            "Date Embauche": self.de,
            "Adresse ": self.adr,
            "Email": self.mail,
            "Mot de passe ": self.pwd,

        }


# Routes !
@app.route("/api/Vehicule", methods=['POST', 'GET', 'DELETE'])
def CrudVehicule():
    if request.method == "GET":
        Vs = []
        for v in Vehicule.objects():
            Vs.append(v.to_json())
        return make_response(jsonify(Vs), 200)

    elif request.method == "POST":
        content = request.json
        V = Vehicule(mat=content["Matricule"], ty=content["Type de véhicules"], an=content["Année de Fabrication"], mr=content["Marque"] ,conso=content["Consomation Carburant (L)"], tyC=content["Type Carburant"],
                 powr=content["Power"],
                 clim=content["Climatisation"], para=content["Parallélisme"], vid=content["Vidange"], mout=content["Mouteur"], pneau=content["Pneaumatique"],
                 cap=content["Capacité (kg)"], dispo=content["Disponibilité"], kilo=content["Kilométrage"], nb=content["Nombre des Places"])
        V.set_etat()
        V.save()
        return make_response("", 201)
    elif request.method == "DELETE":
        Vehicule.objects.delete()
        return make_response("All Objects are deleted!", 203)


@app.route("/api/Vehicules/<Matricule>", methods=['PUT', 'GET', 'DELETE'])
def OneVehicule(Matricule):

    if request.method == "GET":
        V = Vehicule.objects(mat=Matricule).first()
        print(Matricule)
        V=V.to_jsoon()
        return make_response(jsonify({"Matricule =" : Matricule , "your Data: " : V}), 200)
    elif request.method == "PUT":
        content = request.json
        V = Vehicule.objects(mat=Matricule).first()
        V.update(mat=content["Matricule"], ty=content["Type de véhicules"], an=content["Année de Fabrication"], mr=content["Marque"] ,conso=content["Consomation Carburant (L)"], tyC=content["Type Carburant"],
                 powr=content["Power"],
                 clim=content["Climatisation"], para=content["Parallélisme"], vid=content["Vidange"], mout=content["Mouteur"], pneau=content["Pneaumatique"],
                 cap=content["Capacité (kg)"], dispo=content["Disponibilité"], kilo=content["Kilométrage"], nb=content["Nombre des Places"])
        V.set_etat()
        return make_response("Update done ! ", 204)
    elif request.method == "DELETE":
        V = Vehicule.objects(mat=Matricule).first()
        V.delete()
        return make_response("Delete done !", 203)


@app.route("/api/Superviseur", methods=['POST', 'GET', 'DELETE'])
def CrudSuperviseur():
    if request.method == "GET":
        Vs = []
        for v in Superviseur.objects():
            Vs.append(v.to_json())
        return make_response(jsonify(Vs), 200)

    elif request.method == "POST":
        content = request.json
        V = Superviseur(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                        dn=content["Date Naissance"], de=content["Date Embauche"],
                        mail=content["Email"], adr=content["Adresse"])
        V.set_pwd()
        V.set_id()
        V.save()
        return make_response("", 201)
    elif request.method == "DELETE":
        Superviseur.objects.delete()
        return make_response("All Objects are deleted!", 203)


@app.route("/api/Superviseur/<idSup>", methods=['PUT', 'GET', 'DELETE'])
def OneSuperviseur(idSup):
    if request.method == "GET":
        V = Superviseur.objects(idsup=idSup).first()
        return make_response(jsonify({"Your Data ": V.to_jsoon()}), 200)
    elif request.method == "PUT":
        content = request.json
        V = Superviseur.objects(idsup=idSup).first()
        V.update(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                 dn=content["Date Naissance"], de=content["Date Embauche"],
                 mail=content["Email"], adr=content["Adresse"])

        return make_response("Update done ! ", 204)
    elif request.method == "DELETE":
        V = Superviseur.objects(idsup=idSup).first()
        V.delete()
        return make_response("Delete done !", 203)


@app.route("/api/Chauffeur", methods=['POST', 'GET', 'DELETE'])
def CrudChauffeur():
    if request.method == "GET":
        Vs = []
        for v in Chauffeur.objects():
            Vs.append(v.to_json())
        return make_response(jsonify(Vs), 200)

    elif request.method == "POST":
        content = request.json
        V = Chauffeur(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                      dn=content["Date Naissance"], de=content["Date Embauche"],
                      mail=content["Email"], adr=content["Adresse"], nomSup=content["Nom Superviseur"])
        V.set_pwd()
        V.set_id()
        V.save()
        return make_response("", 201)
    elif request.method == "DELETE":
        Chauffeur.objects.delete()
        return make_response("All Objects are deleted!", 203)


@app.route("/api/Chauffeur/<idChauf>", methods=['PUT', 'GET', 'DELETE'])
def OneChauffeur(idChauf):
    if request.method == "GET":
        V = Chauffeur.objects(idCh=idChauf).first()
        return make_response(jsonify({"Your Data ": V.to_jsoon()}), 200)
    elif request.method == "PUT":
        content = request.json
        V = Chauffeur.objects(idCh=idChauf).first()
        V.update(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                 dn=content["Date Naissance"], de=content["Date Embauche"],
                 mail=content["Email"], adr=content["Adresse"])

        return make_response("Update done ! ", 204)
    elif request.method == "DELETE":
        V = Chauffeur.objects(idCh=idChauf).first()
        V.delete()
        return make_response("Delete done !", 203)


if __name__ == '__main__':
    app.run()
