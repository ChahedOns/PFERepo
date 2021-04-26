from datetime import datetime
from random import random
from urllib import request

import bson
import folium
from flask_mail import Mail, Message
from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine import EmbeddedDocumentListField, ReferenceField, EmbeddedDocumentField, ListField

from APIConst import db_name, user_pwd, secret_key

# configurations !
app = Flask(__name__)
DB_URI = f"mongodb+srv://OnsChahed:{user_pwd}@pfecluster.c2obu.mongodb.net/{db_name}?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
mail = Mail()
db.init_app(app)
mail.init_app(app)


class Reparation(db.Document):
    vh = db.StringField(required=True)
    En = db.StringField(required=True)
    date = db.DateTimeField(required=True, default=datetime.now)

    def to_json(self):
        return {
            "CodeEnt": self.En,
            "Matricule": self.vh,
            "Date": self.date
        }


class Entretien(db.Document):
    codeEnt = db.StringField(required=True, Primary_key=True)
    Libelle = db.StringField(required=True)

    def to_json(self):
        return {
            "CodeEntretien": self.codeEnt,
            "NomEntretien": self.Libelle,
        }


class Vehicule(db.Document):
    mat = db.StringField(primary_key=True)
    ty = db.StringField(required=True)
    an = db.IntField(required=True)
    mr = db.StringField(required=True)
    tyC = db.StringField(default="Essence")
    conso = db.FloatField(default=0.0)
    powr = db.IntField(default=5)
    etat = db.BooleanField(default=False)
    cap = db.FloatField(default=0.0)
    dispo = db.BooleanField(default=False)
    kilo = db.FloatField()
    nb = db.IntField()
    types = ["A", "B", "C", "D", "E", "H"]
    mot = ["Location", "Livraison", "Maintenance", "Transportation", "Déplacement"]
    tyP = db.StringField(choice=types, required=True)
    motClé = db.ListField(db.StringField(choice=mot, default=mot))

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
            "Disponibilité": self.dispo,
            "Type de permis ": self.tyP,
            "Mot Clé : ": self.motClé

        }


class Chauffeur(db.Document):
    nom = db.StringField(required=True)
    pre = db.StringField(required=True)
    num = db.StringField(required=True)
    dn = db.DateField(required=True)
    de = db.DateField(required=True)
    mail = db.StringField(primary_key=True)
    pwd = db.StringField(required=True)
    adr = db.StringField(required=True)
    dispo = db.BooleanField(default=True)
    types = ["A", "B", "C", "D", "E", "H"]
    typ = db.ListField(db.StringField(choice=types), required=True)

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
            "Disponibilité": self.dispo

        }


class Superviseur(db.Document):
    nom = db.StringField(required=True)
    pre = db.StringField(required=True)
    num = db.StringField(required=True)
    dn = db.DateField(required=True)
    de = db.DateField(required=True)
    mail = db.StringField(primary_key=True)
    pwd = db.StringField(required=True)
    adr = db.StringField(required=True)

    def to_json(self):
        return {

            "Nom": self.nom,
            "prénom": self.pre,
            "N° Télephone": self.num,
            "Date Naissance": self.dn,
            "Date Embauche": self.de,
            "Adresse": self.adr,
            "Email": self.mail,
            "Mot de passe": self.pwd,

        }


class Client(db.Document):
    cin = db.StringField(length=8)
    nom = db.StringField(required=True)
    pre = db.StringField(required=True)
    num = db.StringField(required=True, length=8)
    dn = db.DateField(required=True)
    mail = db.StringField(required=True, primary_key=True)
    pwd = db.StringField(required=True)
    adr = db.StringField(required=True)


class User(db.Document):
    nom = db.StringField()
    pre = db.StringField()
    ref = db.StringField(primary_key=True)
    pwd = db.StringField()
    mail = db.StringField()
    idu = db.StringField()

    def to_json(self):
        return {
            "ID": self.id,
            "Nom ": self.nom,
            "prénom": self.pre,
            "Email": self.mail,
            "Mot de passe ": self.pwd,
        }


class Destination(db.Document):
    ref = db.StringField(primary_key=True)
    lat = db.FloatField(required=True)
    lar = db.FloatField(required=True)
    gouv = db.StringField(required=True)
    reg = db.StringField(required=True)
    rue = db.StringField(required=True)
    numR = db.IntField(required=True)
    codePostal = db.IntField(required=True)

    def to_json(self):
        return {
            "Lati"
            "Gouvernement": self.gouv,
            "Région": self.reg,
            "Rue": self.rue,
            "Numéro": self.numR,
            "Code Postal": self.codePostal

        }


class Demande(db.Document):
    ref = db.StringField(primary_key=True)
    date_dem = db.DateField(default=datetime.now)
    # vehicule

    type = db.StringField(required=True)
    nbPls = db.IntField(required=True)
    cap = db.FloatField(default=0.0)
    date_res = db.DateField(required=True)

    def to_json(self):
        return {
            "RéferenceDemande": self.ref,
            "Date Demande": self.date_dem,
            "Type de vehicule souhaité": self.type,
            "Nombre de places": self.nbPls,
            "Capacité": self.cap,
            "Date Réservation": self.date_res

        }

    def to_json(self):
        return {
            "Demande": {
                "Réference": self.ref,
                "Email Client": self.email_cl,
                "Date Demande": self.date,
                "Objet du demande": self.obj,
                "Urgente": self.urg,
                "Traitée": self.done,
            },
            "Véhicule souhaité": {
                "Avec chauffeur": self.chaff,
                "Type": self.type,
                "Nombre de places": self.nbPls,
                "capacité": self.capacité,
                "Date de réservation": self.capacité,
            },
            "Destination": {
                "Gouvernement": self.gouv,
                "Région": self.reg,
                "Rue": self.rue,
                "Numéro": self.numR,
                "Code Postal": self.codePostal,
            }
        }


class Reservation(db.Document):
    # reservation
    RefR = db.StringField(primary_key=True)
    mat = ReferenceField("Vehicule")
    date = db.DateField(required=True)
    # Destination
    gouv = db.StringField(required=True)
    reg = db.StringField(required=True)
    rue = db.StringField(required=True)
    numR = db.IntField(required=True)
    codePostal = db.IntField(required=True)
    # affecation
    chauff = ReferenceField("Chauffeur")
    objet = db.StringField(required=True)
    email_cl = db.StringField(required=True)
    urg = db.BooleanField(required=True)
    done = db.BooleanField(default=False)


# Routes !
# Reparation crud

@app.route("/reparation", methods=['POST', 'GET', 'DELETE'])
def repar():
    if request.method == 'GET':
        Rs = []
        for r in Reparation.objects():
            Rs.append(r)
        return make_response(jsonify(Rs), 200)
    elif request.method == "POST":
        content = request.json
        n = Entretien.objects.count()
        E = Entretien.objects(codeEnt=content["codeEnt"]).first()
        V = Vehicule.objects(mat=content["Matricule"]).first()
        if E == None:
            return make_response("Entretien Inexistant", 201)
        elif V == None:
            return make_response("Véhicule Inexistante", 201)
        else:
            x = Reparation.objects(vh=content["Matricule"], En=content["codeEnt"]).count()
            if x == 0:
                R = Reparation(vh=content["Matricule"], En=content["codeEnt"])
                R.save()
                c = Reparation.objects(vh=content["Matricule"]).count()
                if c == n or c > n:
                    et = True
                else:
                    et = False
                R.update(etat=et, dispo=et)
                return make_response("Reparation ajoutée avec succées ", 200)

            else:
                return make_response("Réparation Existe déjà  ", 201)
    else:
        for r in Reparation.objects():
            r.delete()
        for v in Vehicule.objects():
            v.update(etat=False, dispo=False)
        return make_response("Suppression de tous les Réparations avec succées!", 200)


@app.route("/modifier/reparation", methods=['POST', 'GET', 'DELETE'])
def one_rep():
    content = request.json
    if request.method == "GET":
        R = Reparation.objects(vh=content["Matricule"], En=content["codeEnt"]).first()
        if R == None:
            return make_response("Réparation inexistante", 201)
        else:
            return make_response(jsonify("Réparation : ", R.to_jsoon()), 200)

    elif request.method == "POST":
        R = Reparation.objects(vh=content["Matricule"], En=content["codeEnt"]).first()
        if R == None:
            return ("Réparation inexistante ! ", 201)
        else:
            n = Entretien.objects.count()
            R.update(date=datetime.now)
            c = Reparation.objects(vh=content["Matricule"]).count()
            if c == n or c > n:
                et = True
            else:
                et = False
            R.update(etat=et, dispo=et)
            return make_response("Mise à jour effectuée avec succées  ! ", 200)
    else:
        R = Reparation.objects(vh=content["Matricule"], En=content["codeEnt"]).first()
        if R == "None":
            return ("Réparation inexistante ! ", 201)
        else:
            n = Entretien.objects.count()
            R.delete()
            c = Reparation.objects(vh=content["Matricule"]).count()
            if c == n:
                et = True
            else:
                et = False
            R.update(etat=et, dispo=et)
            return make_response("Suppression effectuée avec succées  ! ", 200)


# Entretien crud
@app.route("/entretirn", methods=['POST', 'GET', 'DELETE'])
def Ent():
    if request.method == 'GET':
        Es = []
        for e in Entretien.objects():
            Es.append(e.to_json())
        return make_response(jsonify("Les entretiens disponibles : ", Es), 200)
    elif request.method == 'POST':
        content = request.json
        E = Entretien.objects(codeEnt=content["codeEnt"]).first()
        if E == None:
            E = Entretien(Libelle=content["Libelle"], codeEnt=content["codeEnt"])
            E.save()
            return make_response("Entretien Ajoutée", 200)

        else:
            return make_response("Entretien Existe Deja", 201)
    else:
        for e in Entretien.objects():
            e.delete()
        return make_response("Suppression de tous les Entretiens avec succées!", 200)


@app.route("/modifier/entretien", methods=['POST', 'GET', 'DELETE'])
def one_ent():
    content = request.json
    if request.method == "GET":
        E = Entretien.objects(mat=content["codeEnt"]).first()
        if E == "None":
            return make_response("Entretien inexistante", 201)
        else:
            return make_response(jsonify("Entretien : ", E.to_jsoon()), 200)

    elif request.method == "POST":
        E = Entretien.objects(codeEnt=content["codeEnt"]).first()
        if E == "None":
            return make_response("Entretien Inexxistant", 201)
        else:
            E.update(codeEnt=content["codeEnt"], libelle=content["libelle"])
            return make_response("Mise à jour avec succés !", 200)
    else:
        E = Entretien.objects(codeEnt=content["codeEnt"]).first()
        if E == "None":
            return make_response("Entretien Inexxistant", 201)
        else:
            E.delete()
            return make_response("Suppression avec succés !", 200)


# Vehicule crud
@app.route("/vehicule", methods=['POST', 'GET', 'DELETE'])
def CrudVehicule():
    if request.method == "GET":
        Vs = []
        for v in Vehicule.objects():
            Vs.append(v.to_json())
        return make_response(jsonify("Tous les véhicules :", Vs), 200)

    elif request.method == "POST":
        content = request.json
        MAT = content["Matricule"]
        TYPE = content["Type de véhicules"]
        ANNEE = content["Année de Fabrication"]
        MARQ = content["Marque"]
        CONSO = content["Consomation Carburant (L)"]
        TYPC = content["Type Carburant"]
        POW = content["Power"]
        NBr = content["Nombre des Places"]
        CAP = content["Capacité (kg)"]
        DISPO = content["Disponibilité"]
        KILO = content["Kilométrage"]
        TYP = content["TypePermis"]
        MOT = content["Mot"]
        X = Vehicule.objects(mat=MAT).first()
        if X == None:
            V = Vehicule(mat=MAT, ty=TYPE, an=ANNEE, mr=MARQ,
                         conso=CONSO, tyC=TYPC,
                         powr=POW, cap=CAP, dispo=DISPO, kilo=KILO,
                         nb=NBr, tyP=TYP, motClé=MOT)
            V.save()
            return make_response("Ajout d'un véhicule avec succées", 200)
        else:
            return make_response("Véhicule existe déjà!", 201)

    else:
        Vehicule.objects.delete()
        return make_response("Suppression avec succées du tous les véhicules !", 200)


@app.route("/modifier/vehicule", methods=['PUT', 'GET', 'DELETE'])
def OneVehicule():
    content = request.json
    MAT = content["Matricule"]

    if request.method == "GET":
        V = Vehicule.objects(mat=MAT).first()
        if V == "None":
            return make_response("Vehicule inexistante", 201)
        else:
            return make_response(jsonify("Véhicule : ", V), 200)

    elif request.method == "POST":
        TYPE = request.form.get("Type de véhicules")
        ANNEE = request.form.get("Année de Fabrication")
        MARQ = request.form.get("Marque")
        CONSO = request.form.get("Consomation Carburant (L)")
        TYPC = request.form.get("Type Carburant")
        POW = request.form.get("Power")
        NBr = request.form.get("Nombre des Places")
        CAP = request.form.get("Capacité")
        DISPO = request.form.get("Disponibilité")
        KILO = request.form.get("Kilométrage")
        TYP = request.json("TypePermis")
        V = Vehicule.objects(mat=MAT).first()
        if V == None:
            return make_response("Vehicule inexistante", 201)
        else:
            V.update(mat=MAT, ty=TYPE, an=ANNEE, mr=MARQ,
                     conso=CONSO, tyC=TYPC,
                     powr=POW,
                     cap=CAP, dispo=DISPO, kilo=KILO,
                     nb=NBr, tyP=TYP)
            return make_response("Mise à jour avec sucées ! ", 200)

    elif request.method == "DELETE":
        V = Vehicule.objects(mat=MAT).first()
        if V == None:
            return make_response("Vehicule inexistante", 201)
        else:
            V.delete()
            return make_response("Suppression avec Succés!", 200)


# Superviseur crud
@app.route("/superviseur", methods=['POST', 'GET', 'DELETE'])
def CrudSuperviseur():
    if request.method == "GET":
        Vs = []
        for v in Superviseur.objects():
            Vs.append(v.to_json())
        return make_response(jsonify("Les superviseurs sont : ", Vs), 200)

    elif request.method == "POST":
        content = request.json

        x = Superviseur.objects(mail=content["Email"]).first()
        if x == None:
            V = Superviseur(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                            dn=content["Date Naissance"], de=content["Date Embauche"],
                            mail=content["Email"], adr=content["Adresse"], pwd=content['pwd'])
            U = User(ref=f"{V.nom}{V.pre}", idu="SUPP", nom=V.nom, mail=V.mail, pwd=V.pwd, pre=V.pre)
            V.save()
            U.save()
            return make_response("Ajout avec succées !", 200)
        else:
            return make_response("Superviseur existe déjà", 201)

    else:
        Superviseur.objects.delete()
        for u in User.objects(idu="SUPP"):
            u.delete()
        return make_response("Suppression de tous les superviseurs du systéme!", 200)


@app.route("/modifier/superviseur", methods=['GET', 'POST', 'DELETE'])
def OneSuperviseur():
    content = request.json

    if request.method == "GET":
        V = Superviseur.objects(mail=content["Email"]).first()
        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
            return make_response(jsonify("Superviseur : ", V), 200)

    elif request.method == "PUT":
        V = Superviseur.objects(mail=content["Email"]).first()
        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
            V.update(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                     dn=content["Date Naissance"], de=content["Date Embauche"],
                     mail=content["Email"], adr=content["Adresse"])
            U = User.objects(mail=content["Email"]).first()
            U.update(nom=content["Nom"], mail=content["Email"], pre=content["prénom"])

            return make_response("Mise à jour avec succées! ", 200)

    else:
        V = Superviseur.objects(mail=content["Email"]).first()
        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
            V.delete()
            U = User.objects(mail=content["Email"]).first
            U.delete()
            return make_response("Suppression du superviseur avec succées  !", 200)


@app.route("/users", methods=['GET' , 'DELETE'])
def user():
    if request.method == "GET":
        us = []
        for u in User.objects():
            us.append(u.to_json())

        if not us == []:
            return make_response(jsonify("Users : ", us), 200)
        else:
            return make_response("Aucun utilisateur dans le systéme ", 201)
    else :
        User.objects.delete()


# Chauffeur crud
@app.route("/chauffeur", methods=['POST', 'GET', 'DELETE'])
def CrudChauffeur():
    if request.method == "GET":
        Vs = []
        for v in Chauffeur.objects():
            Vs.append(v.to_json())
        if Vs == []:
            return make_response("Aucun chauffeur dans le systéme", 201)
        else:
            return make_response(jsonify(Vs), 200)

    elif request.method == "POST":
        content = request.json
        X = Chauffeur.objects(mail=content["Email"]).first()
        if X == None:
            V = Chauffeur(nom=content["Nom"], pre=content["prénom"], num=content["N° Télephone"],
                          dn=content["Date Naissance"], de=content["Date Embauche"],
                          mail=content["Email"], adr=content["Adresse"], pwd=content['pwd'], typ=content["Permis"])
            U = User(ref=f"{V.nom}{V.pre}", idu="CHAUFF", nom=V.nom, mail=V.mail, pwd=V.pwd, pre=V.pre)
            V.save()
            U.save()
            return make_response("Ajout d'un chauffeur avec succées", 200)
        else:
            return make_response("Chauffeur existe déjà!", 201)

    elif request.method == "DELETE":
        Chauffeur.objects.delete()
        for u in User.objects(idu="CHAUFF"):
            u.delete()
        return make_response("Suppression de tous les Chauffeurs avec succées", 200)


@app.route("/modifier/chauffeur", methods=['POST', 'GET', 'DELETE'])
def OneChauffeur():
    content = request.json
    if request.method == "GET":
        V = Chauffeur.objects(mail=content["Email"]).first()
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
            return make_response(jsonify("Your Data ", V), 200)
    elif request.method == "POST":
        V = Chauffeur.objects(mail=content["Email"]).first()
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
            U = User.objects(mail=content["Email"]).first()
            V.update(nom=content["Nom"], pre=content["prénom"],
                     num=content["N° Télephone"],
                     dn=content["Date Naissance"], de=content["Date Embauche"],
                     mail=content["Email"], adr=content["Adresse"])
            U.update(nom=content["Nom"], mail=content["Email"], pre=content["prénom"])

            return make_response("Mise à jour d'un chauffeur avec succées ! ", 200)
    else:
        V = Chauffeur.objects(mail=content["Email"]).first()
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
            V.delete()
            U = User.objects(mail=content["Email"]).first
            U.delete()
            return make_response("Suppression du chauffeur avec succées !", 200)


# Demande Crud
@app.route("/demande", methods=['POST', 'GET', 'DELETE'])
def CrudDemande():
    if request.method == "GET":
        Ds = []
        for d in Demande.objects():
            Ds.append(d.to_json())
        return make_response(jsonify("Tous les demandes  :", Ds), 200)

    elif request.method == "POST":
        content = request.json
        D = Demande(obj=content["Objet"],
                    type=content["type"], nbPls=content["nb"], chaff=content["chauffeur"],
                    capacité=content["cap"], date_res=content["dateR"])
        D.save()
        Vs = []
        for v in Vehicule.objects(ty=content["type"], nb=content["nb"], cap=content["cap"], dispo=True):
            r = Reservation.objects(mat=v.mat, date=content["dateR"])
            if r == None:
                Vs.append(v.to_json())
        return make_response(jsonify("Véhicules recommandés ", Vs), 200)
    else:
        Demande.objects.delete()


@app.route("reservation" , methods=['GET' , 'POST' , 'DELETE'])
def resv():
    if request.method =="GET":
        Rs = []
        for r in Reservation.objects():
            Rs.append(r.to_json())
        return make_response(jsonify("Tous les réservations : " , Rs) , 200)

    elif request.method == "POST":
        R = Reservation ()
        R.save()
    else :
        Reservation.objects.delete()


if __name__ == '__main__':
    app.run()
