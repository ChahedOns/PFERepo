from datetime import datetime
from urllib import request

from PIL import Image
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


class Reparation(db.Document):
    ref = db.StringField()
    vh = db.StringField(required=True)
    En = db.StringField(required=True)
    date = db.DateTimeField(required=True, default=datetime.now)

    def to_json(self):
        return {
            "Référence": self.ref,
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
    mail = db.StringField()
    type = db.StringField(required=True)
    nbPls = db.IntField(required=True)
    cap = db.FloatField(default=0.0)
    date_res = db.DateField(required=True)
    mot = ["Location", "Livraison", "Maintenance", "Transportation", "Déplacement"]
    objet = db.StringField(choice=mot, required=True)

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
                return make_response("Reparation ajoutée avec succées ", 200)

            else:
                return make_response("Réparation Existe déjà  ", 201)
    else:
        for r in Reparation.objects():
            r.delete()
        for v in Vehicule.objects():
            v.update(etat=False, dispo=False)
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
                    V.update(etat=False, dispo=False)

                return make_response("Suppression terminée! ", 200)
            else:
                for r in Reparation.objects(vh=matricule):
                    r.delete()
                    V = Vehicule.objects(mat=matricule).first()
                    V.update(etat=False, dispo=False)

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
            return make_response("Suppression effectuée avec succées  ! ", 200)
    else:
        if R == None:
            return make_response("Aucune Réparation à modifier", 201)
        else:
            mat = request.form.get("matricule")
            code = request.form.get("codeent")
            R.update(vh=mat, En=code, date=datetime.now())
            return make_response("Mise à jour avec succées", 200)


# Entretien crud
@app.route("/entretien", methods=['POST', 'GET', 'DELETE'])
def Ent():
    if request.method == 'GET':
        Es = []
        for e in Entretien.objects():
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
        for e in Entretien.objects():
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


# Vehicule crud
@app.route("/vehicule", methods=['POST', 'GET', 'DELETE'])
def CrudVehicule():
    if request.method == "GET":
        Vs = []
        for v in Vehicule.objects():
            Vs.append(v.to_json())
        return make_response(jsonify("Tous les véhicules :", Vs), 200)

    elif request.method == "POST":

        MAT = request.form.get("Matricule")
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
        TYP = request.form.get("TypePermis")
        MOT = request.form.get("Mot")
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
        TYP = request.form.get("TypePermis")
        MOT = request.form.get("Mot")

        if V == None:
            return make_response("Vehicule inexistante", 201)
        else:
            V.update(mat=MAT, ty=TYPE, an=ANNEE, mr=MARQ,
                     conso=CONSO, tyC=TYPC,
                     powr=POW,
                     cap=CAP, dispo=DISPO, kilo=KILO,
                     nb=NBr, tyP=TYP, motClé=MOT)
            return make_response("Mise à jour avec sucées ! ", 200)

    elif request.method == "DELETE":
        if V == None:
            return make_response("Vehicule inexistante", 201)
        else:
            rep_vec(MAT)
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
        email = request.form.get("Email")
        nom = request.form.get("Nom")
        pre = request.form.get("prénom")
        num = request.form.get("N° Télephone")
        dn = request.form.get("Date Naissance")
        de = request.form.get("Date Embauche")
        adr = request.form.get("Adresse")
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
        email = request.form.get("Email")
        nom = request.form.get("Nom")
        pre = request.form.get("prénom")
        num = request.form.get("N° Télephone")
        dn = request.form.get("Date Naissance")
        de = request.form.get("Date Embauche")
        adr = request.form.get("Adresse")
        pwd = request.form.get("pwd")
        typ = request.form.get("Permis")
        sup = request.form.get("NomSup")
        im = request.form.get("image")
        if V == None:
            return make_response("Superviseur Inexistant", 201)
        else:
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
        email = request.form.get("Email")
        nom = request.form.get("Nom")
        pre = request.form.get("prénom")
        num = request.form.get("N° Télephone")
        dn = request.form.get("Date Naissance")
        de = request.form.get("Date Embauche")
        adr = request.form.get("Adresse")
        pwd = request.form.get("pwd")
        typ = request.form.get("Permis")
        sup = request.form.get("NomSup")
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
        email = request.form.get("Email")
        nom = request.form.get("Nom")
        pre = request.form.get("prénom")
        num = request.form.get("N° Télephone")
        dn = request.form.get("Date Naissance")
        de = request.form.get("Date Embauche")
        adr = request.form.get("Adresse")
        pwd = request.form.get("pwd")
        typ = request.form.get("Permis")
        sup = request.form.get("NomSup")
        im = request.form.get("image")
        if V == None:
            return make_response("Chauffeur inexistant ! ", 201)
        else:
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


@app.route("/reservation", methods=['GET', 'POST', 'DELETE'])
def reserv():
    if request.method == "GET":
        Rs = []
        for r in Reservation.objects():
            Rs.append(r.to_json())
        return make_response(jsonify("Tous les réservations : ", Rs), 200)

    elif request.method == "POST":
        R = Reservation()
        R.save()
    else:
        Reservation.objects.delete()


if __name__ == '__main__':
    app.run()
