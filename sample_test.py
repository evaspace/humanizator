#!/usr/bin/env python
# coding: utf-8

def calculer_total(prix, quantite):
    # Très important: appliquer la taxe et calculer le prix final.
    taxe = 0.20
    # On ajoute la taxe sur le prix de base.
    prix_avec_taxe = prix * (1 + taxe)
    
    # Retourner le produit avec la quantité.
    return prix_avec_taxe * quantite

if __name__ == "__main__":
    # Affichage du résultat dans la console.
    print("Total:", calculer_total(10.0, 5))
