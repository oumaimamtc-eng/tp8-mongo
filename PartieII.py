# I.Connectez-vous à la base ecommerceDB
from datetime import datetime
from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017")
db=client["ecommerceDB"]
Produits = db["Produits"]
Clients = db["Clients"]
Commandes=db["Commandes"]
#II. Créez des fonctions permettant de :
#1. Créez une commande
def Cree_Commandes():
    nom_client=input("le nom de client : ")
    c=Clients.find_one({"Nom":nom_client})
    if not c:
       print("Client introuvable")
       exit()
    produits_commande=[]
    total=0
    while True :
        nom_produit=input("Le nom de produit ou (stop):")
        if nom_produit.lower()=="stop":
            break
        pro=Produits.find_one({"Nom":nom_produit})
        if pro:
            quantite=int(input("Entrez quantité : "))
            if quantite <= pro["Stock"]:
                produits_commande.append({quantite,"x",pro["Nom"]})
                total+=quantite * pro["Prix"]
                Produits.update_one({"Nom":pro["Nom"]},{"$inc":{"Stock":-quantite}})
            else :
                print("Stock insuffisant")
        else :
            print("Produit non trouvé")
    Commandes.insert_one({"Client":nom_client,"Produits":produits_commande,"Date_commande":datetime.now(),"Statut":"en cours","Montant_total":total})

#2. Affichez tous les produits de la collection produits.
def affichage_Produits():
    for i in Produits.find():
        print(i)
#3. Recherchez toutes les commandes d’un client spécifique (saisi par l’utilisateur).
def recherche_commandes():
    nom_client=input("le Nom de client : ")
    les_commandes=Commandes.find({"Client":nom_client})
    if les_commandes:
        for i in les_commandes:
            print(i)
    else:
        print("Aucun commande")
#4. Recherchez les commandes ayant le statut : livrée.
def recherche_commandes_parStatut():
    les_commandes=Commandes.find({"Statut":"livréé"})
    if les_commandes:
        for i in les_commandes:
            print(i)
    else:
        print("Aucun commande ayant le statit livrée")
#5. Mettez à jour un produit choisi par son nom.
def Mettez_jour_produit():
    nom_produit=input("Le nom de produit :")
    pro=Produits.find({"Nom":nom_produit})
    if pro:
        cat =input("entrer nouveau categorie : ")
        prix = float(input("entrer nouveau prix : "))
        stock = int(input("entrer nouveau stock : "))
        Produits.update_one({"Nom":nom_produit},{"$set":{"Catégorie":cat,"Prix":prix,"Stock":stock}})
        print(f"Le produit {nom_produit} a mettez à jour !")
    else:
        print("Aucun produit a modifier")
#6. Ajoutez un nouveau champ disponible pour tous les produits ayant une valeur par défaut true.
def ajouter_champ():
    Produits.update_many({}, {"$set": {"disponible": True}})
    print("Champ 'disponible' ajouté à les produits !")
#7. Supprimez une commande en fonction du produit et du client.
def supprimer_commande():
    client_nom = input("Nom de client : ")
    produit_nom = input("Nom de produit : ")
    c = Commandes.delete_one({"Client": client_nom,"Produits": {"$regex": produit_nom}})
    if c.deleted_count > 0:
        print("commande supprimée !")
    else:
        print("Aucune commande trouvée ")

#8. Supprimez tous les commandes d’un client donné.
def suppreimer_commandes():
    nom_client=input("Le nom de client :")
    c=Commandes.delete_many({"Client":nom_client})
    if c.deleted_count > 0:
        print("les commandes supprimée !")
    else:
        print("Aucune commandes trouvée ")
#9. Affichez les commandes triées par date de la commande (du plus récent au plus ancien).
def afficher_commandes_triees():
    print("Liste des commandes triées :\n")
    for c in Commandes.find().sort("Date_commande", -1):
        print(c)
#10. Affichez seulement les produits disponibles.
def afficher_produit_disponible():
    print("les produits disponibles :\n")
    for produit in Produits.find({"Disponible": True}):
        print(produit)
#11. Implémentez un menu en console permettant à l’utilisateur de :
def menu():
    while True:
        print("Menu :")
        print("1. Ajouter une commande")
        print("2. Afficher tous les produits")
        print("3. Rechercher une commande par client")
        print("4. Rechercher une commande ayant la statut : livréé")
        print("5. Mettre à jour un produit")
        print("6. Supprimer une commande")
        print("7. Supprimer toutes les commandes d’un client")
        print("8. Trier les commandes par date")
        print("9.Afficher les produits disponibles")
        print("10. Quitter")

        choix = input("Votre choix (1-10): ")

        if choix == "1":
            Cree_Commandes()
        elif choix == "2":
            affichage_Produits()
        elif choix == "3":
            recherche_commandes_parStatut()
        elif choix == "4":
            recherche_commandes()
        elif choix == "5":
            Mettez_jour_produit()
        elif choix == "6":
            supprimer_commande()
        elif choix == "7":
            suppreimer_commandes()
        elif choix == "8":
            afficher_commandes_triees()
        elif choix == "9":
            afficher_produit_disponible()
        elif choix == "10":
            print("Fin du programme.")
            break
        else:
            print("Choix invalide! Réessayez.")
menu()