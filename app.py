import webbrowser
from datetime import datetime, timedelta
from urllib import request
from flask_cors import CORS, cross_origin
from PIL import Image
import bson
import folium
import numpy as np
import math
from collections import namedtuple
import json
from flask_mail import Mail, Message
from flask import Flask, make_response, request, jsonify, render_template
from flask_mongoengine import MongoEngine
from mongoengine import EmbeddedDocumentListField, ReferenceField, EmbeddedDocumentField, ListField
from APIConst import db_name, user_pwd, secret_key
from pyroutelib3 import Router

# configurations !
app = Flask(__name__)
DB_URI = f"mongodb+srv://OnsChahed:{user_pwd}@pfecluster.c2obu.mongodb.net/{db_name}?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='localhost',
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=None,
    MAIL_PASSWORD=None,
))

mail = Mail(app)
db = MongoEngine()
db.init_app(app)

pnt_dep = (48.866667, 2.333333)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


class Reparation(db.Document):
    ref = db.StringField()
    vh = db.StringField(required=True)
    En = db.StringField(required=True)
    date = db.DateTimeField(required=True, default=datetime.now)

    def to_json(self):
        return {
            "Reference": self.ref,
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

            "Matricule": self.mat,
            "Typev": self.ty,
            "AnFab": self.an,
            "Marque": self.mr,
            "Power": self.powr,
            "TypeC": self.tyC,
            "ConsoC": self.conso,
            "Kilo": self.kilo,
            "NbrPlace": self.nb,
            "Cap": self.cap,
            "Dispo": self.dispo,
            "permis": self.tyP,
            "Mot": self.motClé

        }


class Chauffeur(db.Document):
    id = db.IntField(primary_key=True)
    nom = db.StringField(required=True)
    pre = db.StringField(required=True)
    num = db.StringField(required=True)
    dn = db.DateField(required=True)
    de = db.DateField(required=True)
    mail = db.StringField(required=True)
    pwd = db.StringField(required=True)
    adr = db.StringField(required=True)
    dispo = db.BooleanField(default=True)
    types = ["A", "B", "C", "D", "E", "H"]
    typ = db.ListField(db.StringField(choice=types, default="A"))
    imgProfil = db.ImageField(thumbnail_size=(150, 150, False))
    nomsup = db.StringField()

    def to_json(self):
        return {

            "id": self.id,
            "Nom": self.nom,
            "prenom": self.pre,
            "NumTel": self.num,
            "DateNaissance": self.dn,
            "DateEmbauche": self.de,
            "Adresse": self.adr,
            "Email": self.mail,
            "Mot de passe": self.pwd,
            "Disponibilite": self.dispo

        }


class Superviseur(db.Document):
    id = db.IntField(primary_key=True)
    nom = db.StringField(required=True)
    pre = db.StringField(required=True)
    num = db.StringField(required=True)
    dn = db.DateField(required=True)
    de = db.DateField(required=True)
    mail = db.StringField(required=True)
    pwd = db.StringField(required=True)
    adr = db.StringField(required=True)
    imgProfil = db.ImageField(required=True, thumbnail_size=(150, 150, False))

    # imgProfil = db.ImageField(required=True, thumbnail_size=(150, 150, False))

    def to_json(self):
        return {
            "id": self.id,
            "Nom": self.nom,
            "prenom": self.pre,
            "NumTel": self.num,
            "DateNaissance": self.dn,
            "DateEmbauche": self.de,
            "Adresse": self.adr,
            "Email": self.mail,
            "Mot de passe": self.pwd,


        }


class Client(db.Document):
    id = db.IntField(primary_key=True)
    nom = db.StringField(required=True)
    pre = db.StringField(required=True)
    num = db.StringField(required=True, length=8)
    dn = db.DateField(required=True)
    mail = db.StringField(required=True)
    pwd = db.StringField(required=True)
    adr = db.StringField(required=True)
    imgProfil = db.ImageField(thumbnail_size=(150, 150, False))


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
    reg = db.StringField(required=True)
    dept = db.StringField(required=True)
    rue = db.StringField(required=True)

    def to_json(self):
        return {

            "Gouvernement": self.gouv,
            "Région": self.reg,
            "Rue": self.rue,
            "Numéro": self.numR,
            "Code Postal": self.codePostal

        }

    # def set_coordinates(self):


class Region(db.Document):
    id_reg = db.StringField(primary_key=True)
    code_reg = db.StringField()
    nom_reg = db.StringField()
    slug_reg = db.StringField()


class Dept(db.Document):
    id_dept = db.IntField(primary_key=True)
    code_reg = db.StringField()
    nom_reg = db.StringField()
    slug_reg = db.StringField()
    code_dept = db.StringField(unique=True)
    nom_dept = db.StringField()
    slug_dept = db.StringField()


class Cities(db.Document):
    id_cite = db.IntField(primary_key=True)
    dept = db.StringField(required=True)
    nom_cite = db.StringField(required=True)
    slug_cite = db.StringField(required=True)
    lat = db.FloatField(required=True)
    lng = db.FloatField(required=True)


class Demande(db.Document):
    id_dem = db.IntField(primary_key=True)
    date_dem = db.DateField(default=datetime.now)
    # vehicule
    mail = db.StringField()
    type = db.StringField(required=True)
    nbPls = db.IntField(required=True)
    cap = db.FloatField(default=0.0)
    date_res = db.DateField(required=True)
    date_fin = db.DateField(required=True)
    mot = ["Location", "Livraison", "Maintenance", "Transportation", "Déplacement"]
    obj = db.StringField(choice=mot, required=True)
    reg = db.StringField()
    dept = db.StringField()
    rue = db.StringField()
    chauff = db.BooleanField()


class Reservation(db.Document):
    # reservation
    RefR = db.StringField(primary_key=True)
    mat = ReferenceField("Vehicule")
    datedebR = db.DateField(required=True)
    datefinR = db.DateField()

    # Destination
    dept = db.StringField(required=True)
    reg = db.StringField(required=True)
    rue = db.StringField(required=True)

    # affecation
    chauff = db.BooleanField(required=True)
    objet = db.StringField(required=True)
    email_cl = db.StringField(required=True)
    urg = db.BooleanField(required=True)
    done = db.BooleanField(default=False)
    id_chauff = db.IntField()


class Affectation(db.Document):
    id_aff = db.IntField(primary_key=True)
    mat = db.StringField(required=True)
    # Chauffeur
    id_chauff = db.IntField(required=True)
    chauff_mail = db.StringField(required=True)
    # Trajet
    des_lan = db.FloatField(required=True)
    des_lat = db.FloatField(required=True)
    reg = db.StringField(required=True)
    dept = db.StringField(required=True)
    rue = db.StringField(required=True)
    # Reservation
    dateDeb = db.DateField()
    dateFin = db.DateField()
    obj = db.StringField()
    cl = db.StringField()


def find_distance(x, y):
    lat1, lon1 = x
    lat2, lon2 = y
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_bw_ori_desti = radius * c
    return distance_bw_ori_desti


class Planning(db.Document):
    idP = db.IntField(primary_key=True)
    chauffeur = db.IntField()
    vehicule = db.StringField(required=True)
    data = db.ListField()
    # Chauffeur
    # Trajet
    places = db.ListField()
    cls = db.ListField()
    dest = db.ListField()
    trajet = db.StringField()
    total_dist = db.FloatField()
    coût_carb = db.FloatField()

    # Reservation
    dateDeb = db.DateField()
    dateFin = db.DateField()
    obj = db.StringField()
    cl = db.StringField()

    def calculdest(self):
        self.total_dist = 0.0
        for i in range(len(self.dest) - 1):
            self.total_dist = self.total_dist + find_distance(self.dest[i], self.dest[i + 1])

        self.total_dist = self.total_dist + find_distance(pnt_dep, self.dest[0])


class Historique(db.Document):
    id_op = db.IntField(primary_key=True)
    mat = db.StringField(required=True)
    op = db.StringField()
    description = db.StringField()
    date = db.DateField(default=datetime.now())

    def to_json(self):
        return {
            "idoperation": self.id_op,
            "Matricule": self.mat,
            "Operation": self.op,
            "Description": self.description,
            "Dateoperation": self.date
        }


class Notification(db.Document):
    id = db.IntField(primary_key=True)
    obj = db.StringField()
    text = db.StringField()
    id_user = db.StringField()
    date = db.DateField(default=datetime.now())


class Reclamation(db.Document):
    id = db.IntField(primary_key=True)
    mail = db.StringField(required=True)
    obj = db.StringField(required=True)
    date = db.DateField(default=datetime.now())
    desp = db.StringField()
    types = ["Maintenance", "Confidancialité", "Réception", "Relation direct avec le personnel", "autre"]
    typeR = db.StringField(choice=types, required=True)




#----------must be done only one time---------------
#-----------------DATABASE SETUPS ----------
@app.route("/reg", methods=['POST', 'GET'])
def set_reg():
    if request.method == "POST":
        with open('json/regions.json', 'r') as f:
            data = json.load(f)
            i = 0
            while i < len(data):
                R = Region(id_reg=int(data[i]["id"]), code_reg=data[i]["code"], nom_reg=data[i]["name"],
                           slug_reg=data[i]["slug"])
                R.save()
                i = i + 1
            return make_response("Tous les régions ajoutées avec succés", 200)
    else:
        Ls = []
        for r in Region.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucune region  dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les regions sont : ", Ls), 200)


@app.route("/dept", methods=["POST", 'GET'])
def set_dept():
    if request.method == "POST":
        with open('json/departments.json', 'r') as f:
            data = json.load(f)
            i = 0
            while i < len(data):
                R = Region.objects(code_reg=data[i]["region_code"]).first()
                D = Dept(id_dept=int(data[i]["id"]), code_reg=R.code_reg, code_dept=data[i]["code"],
                         nom_dept=data[i]["name"], slug_dept=data[i]["slug"], nom_reg=R.nom_reg, slug_reg=R.slug_reg)
                D.save()
                i = i + 1

            return make_response("Ajout de tous les départements avec succés", 200)
    else:
        Ls = []
        for r in Dept.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun departement dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les departement sont : ", Ls), 200)


@app.route("/cite", methods=["POST", 'GET'])
def set_cite():
    if request.method == "POST":
        with open('json/cities.json', 'r') as f:
            data = json.load(f)
            i = 0
            while i < len(data):
                D = Dept.objects(code_dept=data[i]["department_code"]).first
                if D == None:
                    return make_response("Departement inexistant", 201)
                else:
                    C = Cities(id_cite=int(data[i]["id"]), dept=data[i]["department_code"], nom_cite=data[i]["name"],
                               lat=float(data[i]["gps_lat"]), slug_cite=data[i]["slug"],
                               lng=float(data[i]["gps_lng"]))
                    C.save()
                i = i + 1

            return make_response("Ajout de tous les départements avec succés", 200)
    else:
        Ls = []
        for r in Cities.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun cite dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les cites sont : ", Ls), 200)


# Routes !
#-----------Reparation crud-------------------

@app.route("/reparation", methods=['POST', 'GET', 'DELETE'])
def repar():
    if request.method == 'GET':
        Rs = []
        for r in Reparation.objects():
            Rs.append(r)
        return make_response(jsonify(Rs), 200)
    elif request.method == "POST":
        code = request.form.get("codeEnt")
        mat = request.form.get("Matricule")
        date = request.form.get("date")
        n = Entretien.objects.count()
        E = Entretien.objects(codeEnt=code).first()
        V = Vehicule.objects(mat=mat).first()
        if E == None:
            return make_response("Entretien Inexistant", 201)
        elif V == None:
            return make_response("Véhicule Inexistante", 201)
        else:
            x = Reparation.objects(vh=mat, En=code).count()
            if x == 0:
                R = Reparation(vh=mat, En=code, date=date)
                R.ref = f"{mat}::{code[:3]}"
                R.save()
                c = Reparation.objects(vh=mat).count()
                if c == n or c > n:
                    et = True
                else:
                    et = False
                V.update(etat=et, dispo=et)
                H = Historique(mat=mat, op=f"Nouvelle réparation {E.libelle}", date=datetime.now())
                max = 0
                for c in Historique.objects:
                    if c.id > max:
                        max = c.id
                H.id_op = max + 1
                H.save()
                return make_response("Reparation ajoutée avec succées ", 200)

            else:
                return make_response("Réparation Existe déjà  ", 201)
    else:
        for r in Reparation.objects():
            r.delete()
        for v in Vehicule.objects():
            v.update(etat=False, dispo=False)
            H = Historique(mat=v.mat, op=f"Suppression de tous les réparations de  {v.mat}", date=datetime.now())
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
        return make_response("Suppression de tous les Réparations avec succées!", 200)


@app.route("/reparation/vehicule/", methods=['GET', 'DELETE'])
def rep_vec(mat=None):
    matricule = request.args.get("matricule")
    R = Reparation.objects(vh=matricule).first()
    if request.method == "GET":
        if R == None:
            return make_response("Aucune Réparation", 201)
        else:
            Rs = []
            for r in Reparation.objects(vh=matricule):
                Rs.append(r)
            return make_response(jsonify("Réparations : ", Rs), 200)

    else:

        if R == None:
            return ("Aucune réparation à supprimer", 201)
        else:
            if mat != None:
                for r in Reparation.objects(vh=mat):
                    r.delete()
                    V = Vehicule.objects(mat=mat).first()
                    H = Historique(mat=mat, op=f"Suppression de tous les réparations de  {mat}", date=datetime.now())
                    max = 0
                    for c in Historique.objects:
                        if c.id > max:
                            max = c.id
                    H.id_op = max + 1
                    H.save()
                    V.update(etat=False, dispo=False)
                return make_response("Suppression terminée! ", 200)
            else:
                for r in Reparation.objects(vh=matricule):
                    r.delete()
                    V = Vehicule.objects(mat=matricule).first()
                    V.update(etat=False, dispo=False)
                    H = Historique(mat=matricule, op=f"Suppression de tous les réparations de  {matricule}",
                                   date=datetime.now())
                    max = 0
                    for c in Historique.objects:
                        if c.id > max:
                            max = c.id
                    H.id_op = max + 1
                    H.save()
                return make_response("Suppression effectuée avec succées  ! ", 200)


@app.route("/reparation/entretien/", methods=['GET', 'DELETE'])
def rep_ent(code=None):
    codeent = request.args.get("code")
    R = Reparation.objects(En=codeent).first()
    if request.method == "GET":
        if R == None:
            return make_response("Aucune Réparation", 201)
        else:
            Rs = []
            for r in Reparation.objects(En=codeent):
                Rs.append(r)
            return make_response(jsonify("Réparations : ", Rs), 200)

    else:
        if code != None:
            if R == None:
                return ("Aucune réparation à supprimer", 201)
            else:
                for r in Reparation.objects(En=code):
                    r.delete()
                return make_response("Suppression terminée  ! ", 200)
        else:
            if R == None:
                return ("Aucune réparation à supprimer", 201)
            else:
                for r in Reparation.objects(En=codeent):
                    r.delete()
            return make_response("Suppression effectuée avec succées  ! ", 200)


@app.route("/reparation/", methods=['GET', 'POST', 'DELETE'])
def rep_one():
    ref = request.args.get("ref")
    R = Reparation.objects(ref=ref).first()
    if request.method == "GET":
        if R == None:
            return make_response("Aucune Réparation à afficher", 201)
        else:
            return make_response(jsonify("Réparation : ", R), 200)
    elif request.method == "DELETE":

        if R == None:
            return ("Aucune réparation à supprimer", 201)
        else:
            R.delete()
            V = Vehicule.objects(mat=R.vh).first()
            c = Reparation.objects(vh=V.mat).count()
            n = Entretien.objects.count()
            if c == n or c > n:
                et = True
            else:
                et = False
            V.update(etat=et, dispo=et)
            H = Historique(mat=V.mat, op=f"Réparation supprimé  {V.mat}", date=datetime.now())
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
            return make_response("Suppression effectuée avec succées  ! ", 200)
    else:
        if R == None:
            return make_response("Aucune Réparation à modifier", 201)
        else:
            mat = request.form.get("matricule")
            code = request.form.get("codeent")
            R.update(vh=mat, En=code, date=datetime.now())
            H = Historique(mat=mat, op=f"Mise a jour d'une Réparation  {mat}")
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
            return make_response("Mise à jour avec succées", 200)


#-------------Entretien crud-------------
@app.route("/entretien", methods=['POST', 'GET', 'DELETE'])
def Ent():
    if request.method == 'GET':
        Es = []
        for e in Entretien.objects().all():
            Es.append(e.to_json())
        return make_response(jsonify("Les entretiens disponibles : ", Es), 200)
    elif request.method == 'POST':

        E = Entretien.objects(codeEnt=request.form.get("codeEnt")).first()
        if E == None:
            E = Entretien(Libelle=request.form.get("libelle"), codeEnt=request.form.get("codeEnt"))
            E.save()
            return make_response("Entretien Ajoutée", 200)

        else:
            return make_response("Entretien Existe Deja", 201)
    else:
        for e in Entretien.objects.all():
            rep_ent(e.codeEnt)
            e.delete()
        return make_response("Suppression de tous les Entretiens avec succées!", 200)


@app.route("/entretien/", methods=['POST', 'GET', 'DELETE'])
def one_ent():
    code = request.args.get("code")
    E = Entretien.objects(codeEnt=code).first()
    if request.method == "GET":
        if E == "None":
            return make_response("Entretien inexistant", 201)
        else:
            return make_response(jsonify("Entretien : ", E), 200)

    elif request.method == "POST":
        if E == "None":
            return make_response("Entretien Inexistant", 201)
        else:
            lib = request.form.get("libelle")
            E.update(libelle=lib)
            return make_response("Mise à jour avec succés !", 200)
    else:
        if E == "None":
            return make_response("Entretien Inexistant", 201)
        else:
            rep_ent(code)
            E.delete()
            return make_response("Suppression avec succés !", 200)


#--------Vehicule crud---------
@app.route("/vehicule", methods=['POST', 'GET', 'DELETE'])
def CrudVehicule():
    if request.method == "GET":
        Vs = []
        for v in Vehicule.objects():
            Vs.append(v.to_json())
        return make_response(jsonify("Tous les véhicules :", Vs), 200)

    elif request.method == "POST":

        MAT = request.form.get("Matricule")
        TYPE = request.form.get("Typev")
        ANNEE = request.form.get("AnFab")
        MARQ = request.form.get("Marque")
        CONSO = request.form.get("ConsoC")
        TYPC = request.form.get("TypeC")
        POW = request.form.get("Puiss")
        NBr = request.form.get("NbrPlace")
        CAP = request.form.get("Cap")
        DISPO = request.form.get("Dispo")
        KILO = request.form.get("Kilo")
        TYP = request.form.get("TypeP")
        MOT = request.form.get("Mot")
        X = Vehicule.objects(mat=MAT).first()
        if X == None:
            V = Vehicule(mat=MAT, ty=TYPE, an=ANNEE, mr=MARQ,
                         conso=CONSO, tyC=TYPC,
                         powr=POW, cap=CAP, dispo=DISPO, kilo=KILO,
                         nb=NBr, tyP=TYP, motClé=MOT)
            V.save()
            H = Historique(mat=V.mat, op=f"Creation d'une nouvelle véhicule {V.mat}", date=datetime.now())
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
            return make_response("Ajout d'un véhicule avec succées", 200)
        else:
            return make_response("Véhicule existe déjà!", 201)

    else:
        Vehicule.objects.delete()
        Reparation.objects.delete()
        return make_response("Suppression avec succées du tous les véhicules !", 200)


@app.route("/vehicule/", methods=['PUT', 'GET', 'DELETE'])
def OneVehicule():
    MAT = request.args.get("matricule")
    V = Vehicule.objects(mat=MAT).first()
    if request.method == "GET":
        if V == "None":
            return make_response("Vehicule inexistante", 201)
        else:
            return make_response(jsonify("Véhicule : ", V), 200)

    elif request.method == "POST":
        TYPE = request.form.get("TypeV")
        ANNEE = request.form.get("AnFab")
        MARQ = request.form.get("Marque")
        CONSO = request.form.get("ConsoC")
        TYPC = request.form.get("TypeC")
        POW = request.form.get("Puiss")
        NBr = request.form.get("NbrPlace")
        CAP = request.form.get("Cap")
        DISPO = request.form.get("Dispo")
        KILO = request.form.get("Kilo")
        TYP = request.form.get("TypeP")
        MOT = request.form.get("Mot")

        if V == None:
            return make_response("Vehicule inexistante", 201)
        else:
            V.update(mat=MAT, ty=TYPE, an=ANNEE, mr=MARQ,
                     conso=CONSO, tyC=TYPC,
                     powr=POW,
                     cap=CAP, dispo=DISPO, kilo=KILO,
                     nb=NBr, tyP=TYP, motClé=MOT)
            H = Historique(mat=V.mat, op=f"Mise a jour d'un véhicule {V.mat}")
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
            return make_response("Mise à jour avec sucées ! ", 200)

    elif request.method == "DELETE":
        if V == None:
            return make_response("Vehicule inexistante", 201)
        else:
            rep_vec(MAT)

            H = Historique(mat=V.mat, op=f"Suppression d'une nouvelle véhicule {V.mat}", date=datetime.now())
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
            V.delete()
            return make_response("Suppression avec Succés!", 200)


#--------------Superviseur crud-----------
@app.route("/superviseur", methods=['POST', 'GET', 'DELETE'])
def CrudSuperviseur():
    if request.method == "GET":
        Vs = []
        for v in Superviseur.objects():
            Vs.append(v.to_json())
        return make_response(jsonify("Les superviseurs sont : ", Vs), 200)

    elif request.method == "POST":
        email = request.form.get("mail")
        nom = request.form.get("nom")
        pre = request.form.get("pre")
        num = request.form.get("ntel")
        dn = request.form.get("dn")
        de = request.form.get("de")
        adr = request.form.get("adr")
        pwd = request.form.get("pwd")
        im = request.form.get("image")

        x = Superviseur.objects(mail=email).first()
        if x == None:
            img = open(im, 'rb')
            V = Superviseur(nom=nom, pre=pre, num=num, dn=dn, de=de,
                            mail=email, adr=adr, pwd=pwd)

            U = User(ref=f"{V.nom}{V.pre}", idu="SUPP", nom=V.nom, mail=V.mail, pwd=V.pwd, pre=V.pre)
            V.imgProfil.replace(img, filename=f"{V.nom}.jpg")
            max = 0
            for c in Chauffeur.objects:
                if c.id > max:
                    max = c.id
            V.id = max + 1
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


@app.route("/superviseur/", methods=['GET', 'POST', 'DELETE'])
def OneSuperviseur():
    id = request.args.get("id")
    V = Superviseur.objects(id=id).first()

    if request.method == "GET":

        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
            return make_response(jsonify("Superviseur : ", V), 200)

    elif request.method == "POST":
        email = request.form.get("mail")
        nom = request.form.get("nom")
        pre = request.form.get("pre")
        num = request.form.get("ntel")
        dn = request.form.get("dn")
        de = request.form.get("de")
        adr = request.form.get("adr")
        pwd = request.form.get("pwd")
        im = request.form.get("image")
        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
            if im != "" :
                img = open(im, 'rb')
                V.imgProfil.replace(img, filename=f"{V.nom}.jpg")
            V.update(nom=nom, pre=pre, num=num, dn=dn, de=de,
                     mail=email, adr=adr, pwd=pwd)
            U = User.objects(mail=V.mail).first()
            U.update(nom=nom, mail=email, pre=pre)

            return make_response("Mise à jour avec succées! ", 200)

    else:
        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
            U = User.objects(mail=V.mail).first()
            U.delete()
            V.delete()
            return make_response("Suppression du superviseur avec succées  !", 200)


#--------User--------------
@app.route("/users", methods=['GET', 'DELETE'])
def user():
    if request.method == "GET":
        us = []
        for u in User.objects():
            us.append(u.to_json())

        if not us == []:
            return make_response(jsonify("Users : ", us), 200)
        else:
            return make_response("Aucun utilisateur dans le systéme ", 201)
    else:
        User.objects.delete()



# -----------Chauffeur crud-----------
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
        email = request.form.get("mail")
        nom = request.form.get("nom")
        pre = request.form.get("pre")
        num = request.form.get("num")
        dn = request.form.get("dn")
        de = request.form.get("de")
        adr = request.form.get("adr")
        pwd = request.form.get("pwd")
        typ = request.form.get("typ")
        sup = request.form.get("nomsup")
        im = request.form.get("image")
        X = Chauffeur.objects(mail=email).first()
        if X == None:
            img = open(im, 'rb')

            V = Chauffeur(nom=nom, pre=pre, num=num, dn=dn, de=de,
                          mail=email, adr=adr, pwd=pwd, typ=typ, nomsup=sup)

            U = User(ref=f"{V.nom}{V.pre}", idu="CHAUFF", nom=V.nom, mail=V.mail, pwd=V.pwd, pre=V.pre)
            V.imgProfil.replace(img, filename=f"{V.nom}.jpg")
            max = 0
            for c in Chauffeur.objects:
                if c.id > max:
                    max = c.id
            V.id = max + 1

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


@app.route("/chauffeur/", methods=['POST', 'GET', 'DELETE'])
def OneChauffeur():
    id = request.args.get("id")
    V = Chauffeur.objects(id=id).first()
    if request.method == "GET":
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
            return make_response(jsonify("Your Data ", V), 200)
    elif request.method == "POST":
        email = request.form.get("mail")
        nom = request.form.get("nom")
        pre = request.form.get("pre")
        num = request.form.get("num")
        dn = request.form.get("dn")
        de = request.form.get("de")
        adr = request.form.get("adr")
        pwd = request.form.get("pwd")
        typ = request.form.get("permis")
        sup = request.form.get("NomSup")
        im = request.form.get("image")
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
            if im != "" :
                img = open(im, 'rb')
                V.imgProfil.replace(img, filename=f"{V.nom}.jpg")

            U = User.objects(mail=V.mail).first()
            V.update(nom=nom, pre=pre, num=num, dn=dn, de=de,
                     mail=email, adr=adr, pwd=pwd, typ=typ, nomsup=sup)
            U.update(nom=nom, mail=email, pre=pre)

            return make_response("Mise à jour d'un chauffeur avec succées ! ", 200)
    else:
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
            U = User.objects(mail=V.mail).first()
            U.delete()
            V.delete()
            return make_response("Suppression du chauffeur avec succées !", 200)

#------------Crud Client---------------
@app.route("/client", methods=['POST', 'GET', 'DELETE'])
def cl_crud():
    if request.method == "GET":
        Cl = []
        for cl in Client.objects():
            Cl.append(cl)
        if Cl == []:
            return make_response("Aucun Client dans le systéme", 201)
        else:
            return make_response(jsonify("Clients : ", Cl), 200)

    elif request.method == "POST":
        email = request.form.get("mail")
        nom = request.form.get("nom")
        pre = request.form.get("pre")
        num = request.form.get("ntel")
        dn = request.form.get("dn")
        adr = request.form.get("adr")
        pwd = request.form.get("pwd")
        im = request.form.get("image")
        X = Client.objects(mail=email).first()
        if X == None:
            img = open(im, 'rb')

            V = Client(nom=nom, pre=pre, num=num, dn=dn,
                       mail=email, adr=adr, pwd=pwd)

            U = User(ref=f"{V.nom}{V.pre}", idu="CLIENT", nom=V.nom, mail=V.mail, pwd=V.pwd, pre=V.pre)
            V.imgProfil.replace(img, filename=f"{V.nom}.jpg")
            max = 0
            for c in Client.objects:
                if c.id > max:
                    max = c.id
            V.id = max + 1
            V.save()
            U.save()
            return make_response("Ajout d'un client avec succées", 200)
        else:
            return make_response("Client existe déjà!", 201)
    else:
        Client.objects.delete()


@app.route
# ------------Demande Crud---------
@app.route("/demande", methods=['POST', 'GET', 'DELETE'])
def CrudDemande():
    id = request.args.get("id_cl")
    if request.method == "GET":
        Ds = []
        for d in Demande.objects():
            Ds.append(d)
        if Ds == []:
            return make_response("Rien a afficher", 201)
        else:
            return make_response(jsonify("Tous les demandes  :", Ds), 200)

    elif request.method == "POST":

        obj = request.form.get("objet")
        type = request.form.get("type")
        ok = request.form.get("chauffeur")
        nb = request.form.get("nbplc")
        cap = request.form.get("cap")
        date = request.form.get("dateR")
        dateF = request.form.get("dateF")
        reg = request.form.get("region")
        dept = request.form.get("departement")
        rue = request.form.get("rue")
        urg = request.form.get("urgent")
        cl = Client.objects.get(id=id)
        D = Demande(obj=obj, type=type, nbPls=int(nb), chauff=bool(ok),
                    cap=float(cap), date_res=date, date_fin=dateF, reg=reg, dept=dept, mail=cl.mail, rue=rue,
                    urg=bool(urg))
        max = 0
        for d in Demande.objects():
            if d.id_dem > max:
                max = d.id_dem
        D.id_dem = max
        D.save()

        cl = Client.objects.get(id=id)
        U = User.objects.get(mail=cl.mail)
        N = Notification(id_user=U.ref, obj="Demande",
                         text=f"Votre demande de réservation est effectué avec succés")
        max = 0
        for n in Notification.objects():
            if n.id > max:
                max = n.id
        N.id = max
        N.save()
        X = Vehicule.objects(ty=type, nb=nb, cap=cap)
        if X == None:
            N = Notification(id_user=U.id, obj="Demande",
                             text=f"Votre demande est prise en considération on vous notifie lorsque elle est prête")
            max = 0
            for n in Notification.objects():
                if n.id > max:
                    max = n.id
            N.id = max
            N.save()
            return make_response("Votre demande est prise en considération on vous notifie lorsque elle est prête", 200)
        else:
            X = Vehicule.objects(ty=type, nb=nb, cap=cap)
            rd = []
            if ok == "False":  # sans chaufffeur
                for v in X:
                    if v.dispo == True:
                        rd.append(v)
                if rd == []:
                    N = Notification(id_user=U.ref, obj="Demande",
                                     text=f"Votre demande est prise en considération on vous notifie lorsque un vehicule soit prêt")
                    max = 0
                    for n in Notification.objects():
                        if n.id > max:
                            max = n.id
                    N.id = max
                    N.save()
                    return make_response(jsonify("Aucun vehicule disponible", X), 201)
                else:
                    return make_response(jsonify("Recommandations : ", rd), 200)
            else:

                if obj == "Location":
                    Vs = []
                    for v in X:
                        if v.dispo == True:
                            Vs.append(v.to_json())
                    if Vs == []:
                        N = Notification(id_user=U.ref, obj="Demande",
                                         text=f"Votre demande est prise en considération on vous notifie lorsque un vehicule soit prêt")
                        max = 0
                        for n in Notification.objects():
                            if n.id > max:
                                max = n.id
                        N.id = max
                        N.save()
                        return make_response("Rien a afficher", 201)
                    else:
                        return make_response(jsonify("Location Recommandations", Vs), 200)
                else:

                    Vs = []
                    ref = {}
                    refs = []
                    # dans le cas ou le vehicule a deja une affectation on peut récupérer directement la référence de l'affectation
                    for v in X:
                        # LEs vehicules de mm type et ca qui sont déja disponible sont recommandées directement
                        if v.dispo == True:
                            Vs.append(v.to_json())
                            ref.append()
                        else:
                            af = []
                            # GEt all the affectation de mat V
                            for a in Affectation.objects():
                                if a.mat == v.mat:
                                    af.append(a)
                            # Prend la destination de la demande pour la vérifier avec les autres affectations du même véhicule
                            C = Cities.objects.get(slug_cite=rue)
                            dp = Dept.objects.get(code_dept=C.dept)
                            r = Region.objects.get(code_reg=dp.code_reg)

                            if af == None:
                                pass
                            else:
                                for a in af:
                                    # trouvé si il y une affecation avec la même destination!
                                    if Affectation.objects(mat=a.mat, datedebR=date, datefinR=dateF).count() <= 3:
                                        if a.rue == rue:
                                            Vs.append(v.to_json)
                                            refs.append(jsonify("matricule", a.mat, "Affectation", a.id_aff))

                                        elif a.dept == dept:
                                            Vs.append(v.to_json)
                                            refs.append(jsonify("matricule", a.mat, "Affectation", a.id_aff))
                                        elif a.reg == reg:
                                            Vs.append(v.to_json)
                                            refs.append(jsonify("matricule", a.mat, "Affectation", a.id_aff))
                                        else:
                                            pass
                    if Vs == []:
                        N = Notification(id_user=U.ref, obj="Demande",
                                         text=f"Votre demande est prise en considération on vous notifie lorsque un vehicule soit prêt")
                        max = 0
                        for n in Notification.objects():
                            if n.id > max:
                                max = n.id
                        N.id = max
                        N.save()
                        return make_response("Rien a afficher!", 201)
                    else:
                        # on a utilisé ref pour qu'on peut récupérer la reférence de l'affecation si elle existe !
                        return make_response(jsonify("Véhicules recommandés", Vs, "references : ", refs), 200)

    else:
        Demande.objects.delete()

@app.route("/demande/", methods=["GET", "DELETE"])
def one_dem():
    ref = request.args.get("ref")
    if request.method == "GET":
        R = Demande.objects(id=ref).first()
        if R == None:
            return make_response("Aucune réservation avec cette réference ", 201)
        else:
            make_response(jsonify("Reservation :", R), 200)
    else:
        R = Demande.objects(id=ref).first()
        if R == None:
            return make_response("Aucune réservation avec cette réference ", 201)
        else:
            R.delete()
            return make_response("Suppression avec succées ", 200)


#-------------Historique -----------------
@app.route
@app.route("/histo", methods=['GET', 'DELETE'])
def histo():
    mat = request.args.get("matricule")
    if request.method == "GET":
        Vs = []
        for h in Historique.objects(mat=mat):
            Vs.append(h)
        if Vs == []:
            return make_response("Rien à afficher", 201)
        else:
            return make_response(jsonify(Vs), 200)
    else:
        for h in Historique.objects(mat=mat):
            h.delete()
        return make_response("Suppression de l'historique", 200)



#-----------Reservation et affectation ------------
@app.route("/reservation", methods=['GET', 'POST', 'DELETE'])
def reservation():
    dem = request.args.get("idDemande")
    mat = request.args.get("mat")
    idaff = request.args.get("idaffc")

    if request.method == "GET":
        Rs = []
        # les réservations urgentes puis les non urgentes!
        for r in Affectation.objects():
            Rs.append(r)
        for r in Affectation.objects():
            Rs.append(r)
        if Rs == []:
            return make_response("Rien a afficher", 201)
        else:
            return make_response(jsonify("Tous les réservations : ", Rs), 200)

    elif request.method == "POST":
        D = Demande.objects.get(id=dem)
        R = Reservation(RefR=f"{mat}|{D.dateD}", mat=mat, date_res=D.date, date_fin=D.dateF, reg=D.reg, dept=D.dept,
                        rue=D.rue,
                        chauff=D.chauff, objet=D.obj, email_cl=D.mail, urg=D.urg)
        R.save()
        V = Vehicule.objects.get(mat=mat)
        # sans Chauffeur ! reservation directement au client
        if D.chauff == "False":
            V.update(dispo=False)
            H = Historique(mat=mat,
                           op=f"Réservation d'une nouvelle véhicule {mat} pour le {D.date_res} jusqu'à le {D.date_fin}",
                           date=datetime.now())
            max = 0
            for c in Historique.objects:
                if c.id > max:
                    max = c.id
            H.id_op = max + 1
            H.save()
            U = User.objects.get(mail=mail)
            N = Notification(id_user=U.ref, obj="Réservation",
                             text=f"Votre demande de réservation est effectué avec succés veuillez nous rejoindre pour recevez le véhicule souhaité")
            max = 0
            for n in Notification.objects():
                if n.id > max:
                    max = n.id
            N.id = max
            N.save()
            return ("Réservation approuvée")

        else:
            if idaff != None:
                # Notifier le chauffeur
                A = Affectation.objects.get(id_aff=idaff)
                U = User.objects.get(mail=A.id_chauff)
                N = Notification(id_user=U.ref, obj="Affectation",
                                 text="Vous avez une nouvelle Affectation consulter le planning pour plus de detail")
                max = 0
                for n in Notification.objects():
                    if n.id > max:
                        max = n.id
                N.id = max
                N.save()

                # creation de la nouvelle affectation
                AF = Affectation(mat=A.mat, reg=D.reg, dept=D.dept, rue=D.rue, chauff_mail=A.chauff_mail,
                                 id_chauff=A.id_chauff,
                                 dateDeb=D.date_res
                                 , dateFin=D.date_fin, cl=D.mail, obj=D.obj)
                C = Cities.objects.get(slug_cite=D.rue)
                Ds = Destination(ref=f"{D.reg} {D.dept} {D.rue}", reg=D.reg, dept=D.dept, rue=D.rue, lat=C.lat,
                                 lar=C.lng)
                AF.des_lan = Ds.lar
                AF.des_lat = Ds.lat
                max = 0
                for a in Affectation.objects():
                    if a.id_aff > max:
                        max = a.id_aff
                AF.id_aff = max + 1
                AF.save()
                Ds.save()
                return make_response("Nouvelle Affectation effectuée ", 200)

            else:
                ch = Chauffeur.objects(dispo=True)
                V = Vehicule.objects.get(mat=mat)
                for chauff in ch:
                    if V.tyP in chauff.typ:
                        A = Affectation(mat=mat, reg=D.reg, dept=D.dept, rue=D.rue, chauff_mail=chauff.mail,
                                        id_chauff=chauff.id,
                                        dateDeb=R.datedebR
                                        , dateFin=R.datefinR, cl=R.email_cl, obj=R.objet)

                        C = Cities.objects.get(nom_cite=R.rue)
                        D = Destination(ref=f"{R.reg} {R.dept} {R.rue}", reg=R.reg, dept=R.dept, rue=R.rue, lat=C.lat,
                                        lar=C.lng)
                        A.des_lan = D.lar
                        A.des_lat = D.lat
                        max = 0
                        for a in Affectation.objects():
                            if a.id_aff > max:
                                max = a.id_aff
                        A.id_aff = max + 1
                        A.save()
                        D.save()
                        chauff.update(dispo=False)
                        U = User.objects.get(mail=chauff.mail)
                        N = Notification(id_user=U.ref, obj="Affectation",
                                         text=f"Vous avez une nouvelle Affectation consulter le planning pour plus de detail")
                        max = 0
                        for n in Notification.objects():
                            if n.id > max:
                                max = n.id
                        N.id = max
                        N.save()
                        chauff.update(dispo=False)
                        break

                return make_response("Affectation effectuée avec succées", 200)

    else:
        Reservation.objects.delete()

@app.route("/reservation/", methods=["GET", "DELETE"])
def one_res():
    ref = request.args.get("ref")
    if request.method == "GET":
        R = Reservation.objects(RefR=ref).first()
        if R == None:
            return make_response("Aucune réservation avec cette réference ", 201)
        else:
            make_response(jsonify("Reservation :", R), 200)

# get les  affectations d'un chauffeur :
@app.route("/affectation/chauffeur", methods=['GET', 'DELETE'])
def affec(id=None):
    id = request.args.get("id_chauff")

    if request.method == "GET":
        As = []
        for a in Affectation.objects(id_chauff=id):
            As.append(a)
        if As == []:
            return make_response("Aucune Affectation en ce moment ", 201)
        else:
            return make_response(jsonify("Affectations : ", As), 200)

    else:
        for a in Affectation.objects(id_chauff=id):
            a.delete()
        return make_response("Suppression avec succés ", 200)

# tirer les affectations par vehicules : coté superviseur

@app.route("/affectation/vehicule", methods=['GET', 'DELETE'])
def affec_v(mat=None):
    mat = request.args.get("mat")
    if request.method == "GET":
        As = []
        for a in Affectation.objects(mat=mat):
            As.append(a)
        if As == []:
            return make_response("Aucune Affectation en ce moment ", 201)
        else:
            return make_response(jsonify("Affectations : ", As), 200)

    else:
        for a in Affectation.objects(mat=mat):
            a.delete()
        return make_response("Suppression avec succés ", 200)



#---------Planning --------
def Createplan(id=None, mat=None):
    coord = []
    lats = []
    lngs = []
    destinations = []
    Cls = []
    data = []
    for a in Affectation.objects(id_chauff=id, mat=mat).order_by("des_lat"):
        lats.append(a.des_lat)
        lngs.append(a.des_lan)
        destinations.append(f"{a.rue} , {a.dept} , {a.reg}")
        Cls.append(a.cl)
        coord = zip(lats, lngs)
        data = zip(Cls, destinations, coord)
    P = Planning(chauffeur=id, vehicule=mat, dest=coord, cls=Cls, places=destinations, data=data)
    max = 0
    for i in Planning.objects():
        if i.idP > max:
            max = i.idP
    P.idP = max + 1
    P.calculdest()
    P.save()
    return make_response("Planning créer avec succés ", 200)


# Le planning de chaque chauffeur : Dashboard
@app.route("/planning", methods=["DELETE", "GET" , "POST"])
def planning(id=None):
    id = request.args.get("chauffeur")
    if request.method == "GET":
        ps = []
        for p in Planning.objects(chauffeur=id):
            ps.append(p)
        if ps == []:
            return make_response("Aucun plan pour le moment" , 201)
        else :
            return make_response(jsonify("Les plannings : " , ps) , 200)

    elif request.method =="POST":
        mats = []
        for A in Affectation.objects(id_chauff=id):
            if A.mat in mats:
                pass
            else:
                mats.append(A.mat)

        for mat in mats:
            P = Planning.objects(id_chauff = id)
            if P != None :
                return make_response("Planning existe dejà " , 201)
            else :
                Createplan(id, mat)
                return make_response("ajout avec succées", 200)
    else :
        Planning.objects(chauffeur=id).delete()
        return make_response("Suppresion avec succées" , 200)




#------------GET LES NOMS DES cites , departement , region-----------
@app.route("/cite", methods=["GET"])
def get_cite():
    cs = []
    for c in Cities.objects():
        cs.append(c.nom_cite)
        return make_response(jsonify("Cites", cs), 200)


@app.route("/dept", methods=["GET"])
def get_dept():
    cs = []
    for c in Dept.objects():
        cs.append(c.nom_dept)
        return make_response(jsonify("Departements:", cs), 200)


@app.route("/region", methods=["GET"])
def get_reg():
    cs = []
    for c in Region.objects():
        cs.append(c.nom_reg)
        return make_response(jsonify("Regions", cs), 200)



#----------Geolocation things -------------
@app.route("/trajet", methods=["GET"])
def trajet():
    id = request.args.get("idp")

    P = Planning.objects.get(idP=id)
    router = Router("car")
    c = folium.Map(location=[P.dest[0][0], P.dest[0][1]], zoom_start=5)
    router = Router("car")
    if len(P.dest) == 1:
        print("only one place")
        folium.Marker(P.dest[0], color="red", popup="Départ").add_to(c)
    elif len(P.dest) == 2:
        folium.Marker(P.dest[0], popup="Départ").add_to(c)
        folium.Marker(P.dest[1], popup="Arrivée").add_to(c)
        dep = router.findNode(P.dest[0][0], P.dest[0][1])
        ar = router.findNode(P.dest[1][0], P.dest[1][1])
        routeLatLons = [P.dest[0], P.dest[1]]
        status, route = router.doRoute(dep, ar)
        if status == 'success':
            print("route trouvé")
            routeLatLons = list(map(router.nodeLatLon, route))
        else:
            print("route pas trouvée!")
        for indice, coord in enumerate(routeLatLons):
            if indice % 10 == 0:
                coord = list(coord)
                folium.CircleMarker(coord, radius=3, weight=11, opacity=1).add_to(c)
        folium.PolyLine(routeLatLons, color="blue", weight=15, opacity=1).add_to(c)
    elif len(P.dest) == 3:
        folium.Marker(P.dest[0], popup="Départ").add_to(c)
        folium.Marker(P.dest[1], popup="Arrivée").add_to(c)
        dep = router.findNode(P.dest[0][0], P.dest[0][1])
        ar = router.findNode(P.dest[1][0], P.dest[1][1])
        routeLatLons = [P.dest[0], P.dest[1]]
        status, route = router.doRoute(dep, ar)
        if status == 'success':
            print("route trouvé")
            routeLatLons = list(map(router.nodeLatLon, route))
        else:
            print("route pas trouvée!")
        for indice, coord in enumerate(routeLatLons):
            if indice % 10 == 0:
                coord = list(coord)
                folium.CircleMarker(coord, radius=3, weight=11, opacity=1).add_to(c)
        folium.PolyLine(routeLatLons, color="blue", weight=15, opacity=1).add_to(c)
        # 2nd route
        folium.Marker(P.dest[1], popup="Départ").add_to(c)
        folium.Marker(P.dest[2], popup="Arrivée").add_to(c)
        dep2 = router.findNode(P.dest[1][0], P.dest[1][1])
        ar2 = router.findNode(P.dest[2][0], P.dest[2][1])
        routeLatLons2 = [P.dest[1], P.dest[2]]
        status, route2 = router.doRoute(dep2, ar2)
        if status == 'success':
            print("route trouvé")
            routeLatLons2 = list(map(router.nodeLatLon, route2))
        else:
            print("route pas trouvée!")
        for indice, coord in enumerate(routeLatLons2):
            if indice % 10 == 0:
                coord = list(coord)
                folium.CircleMarker(coord, radius=3, weight=11, opacity=1).add_to(c)
        folium.PolyLine(routeLatLons2, color="blue", weight=15, opacity=1).add_to(c)

    fich = "mapPlan.html"
    c.save(fich)
    webbrowser.open(fich)
    return make_response("Done", 200)


#------------reclamations-------------
@app.route("/reclamation", methods=["GET", "POST", "DELETE"])
def recl():
    if request.method == "GET":
        Rs = []
        for r in Reclamation.objects():
            Rs.append(r)
        if Rs == []:
            return make_response("Aucune réclamation à afficher", 201)
        else:
            return make_response(jsonify("réclamations :", Rs), 200)

    elif request.method == "POST":
        mail = request.form.get("mail")
        obj = request.form.get("obj")
        dsc = request.form.get("Description")
        typ = request.form.get("type")
        R = Reclamation(mail=mail, obj=obj, desp=dsc, typeR=typ)
        max = 0
        for r in Reclamation.objects():
            if r.id > max:
                max = r.id
        R.id = max + 1
        R.save()
        U = User.objects.get(mail=mail)
        N = Notification(id_user=U.id, obj="Réclamation",
                         text=f"Votre Réclamation de {typ} d'objet : {obj} est bien reçu ")
        N.save()
    else:
        Reclamation.objects.delete()
        return make_response("suppression avec succes", 200)


@app.route("/reclamation/client", methods=["GET", "DELETE"])
def one_rec_cl():
    id = request.args.get("client")
    cl = Client.objects.get(id=id)
    if request.method == "GET":

        ns = []
        for n in Reclamation.objects(mail=cl.mail):
            ns.append(n)
        if ns == None:
            return make_response("Aucune Reclamations ", 201)
        else:
            return make_response(jsonify("Reclamations", ns), 200)

    else:
        for n in Reclamation.objects(mail=cl.mail):
            n.delete()
        return make_response("Suppression des reclamations avec succées ", 201)


@app.route("/reclamation/chauffeur", methods=["GET", "DELETE"])
def one_rec_ch():
    id = request.args.get("chauffeur")
    ch = Chauffeur.objects.get(id=id)
    if request.method == "GET":
        ns = []
        for n in Reclamation.objects(mail=ch.mail):
            ns.append(n)
        if ns == None:
            return make_response("Aucune Reclamations ", 201)
        else:
            return make_response(jsonify("Reclamations", ns), 200)

    else:
        for n in Reclamation.objects(mail=ch.mail):
            n.delete()
        return make_response("Suppression des reclamations avec succées ", 201)

#------------"notifications"----------
@app.route("/notification", methods=["GET", "DELETE"])
def get_notifications():
    id = request.args.get("User")
    if request.method == "GET":

        ns = []
        for n in Notification.objects(id_user=id):
            ns.append(n)
        if ns == None:
            return make_response("Aucune Notification ", 201)
        else:
            return make_response(jsonify("Notifications", ns), 200)

    else:
        for n in Notification.objects(id_user=id):
            n.delete()
        return make_response("Suppression des reclamations avec succées ", 201)

if __name__ == '__main__':
    app.run()
