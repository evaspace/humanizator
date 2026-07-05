#include <stdio.h>

// Déclaration d'une structure pour stocker les informations de l'utilisateur.
typedef struct {
    int id;
    char nom[50];
} Utilisateur;

int main() {
    /* Initialisation de l'utilisateur.
       Cette partie doit être remplie de manière très précise. */
    Utilisateur u = {1, "Alice"};
    
    // Affichage des informations sur la console.
    printf("Utilisateur: %s (ID: %d)\n", u.nom, u.id);
    
    return 0;
}
