"""Gestion de facture

1. Faire un template MS access des infos
	a. Nom
	b. Catégorie
	c. date d'émission
	d. date de paiement ou date prévue de paiement
		i. petit calendrier serait nice
		ii. permettre de mettre une date pas standard, ex. hiver 2017
	e. prix
	f. payée?
	g. note
2. Permettre d'ajouter
	a. facture
	b. catégorie
	c. dépenses qui ne sont pas des factures
3. Permettre d'archiver les factures déjà payées
4. Facilement pouvoir filtrer les factures (bcp de filtre possible)
5. Apparence nice
	a. fond noir
	b. foreground gris
	c. les factures sont à l'horizontale comme sur itunes
	d. Mettre un barre de menu en haut avec des options
		i. quitter
		ii. stats
		iii. ajouter...
		iv. supprimer...
		v. copier
		vi. coller
6. Permettre de pouvoir sélectionner plusieurs factures à supprimer, à modifier, etc.
7. Raccourcis clavier


1. Faire l'apparence de base : menu en haut, background vide.
2. Faire un template MS Access
3. Essayer d'afficher une requete
4. Essayer de modifier la base de données
5. Essayer d'ajouter sur MS access
6. Afficher un ajout
7. Afficher les modifications qu'on fait sur une facture
8. Compléter
9. Tests


Classes : GUI, Facture

1. Main
	a. Scrollbar
	b. Bouton supprimer
	c. Permettre le double click pour modifier
	d. TREEVIEW TTK.TKINTER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	e. Faire un GitHub
	f.
5. Permettre le resizing
6. Commande des options du menu
	c. Stats
	d.
7. top_about
	a. Grosseur
	b. endroit dans l'écran
	c. Beau
	d.
9. toplevel add
	a. menu déroulant catégorie
	b. bouton payé
	c. note
	d. Mettre ca beau
	e. Grosseur
	f. endroit dans l'écran
	i. command button confirm
	j.
10. top_categories
	a. Grosseur
	b. Endroit dans l'écran
	f. command insérer
	g. command supprimer
	h. Distribution widgets du bas
	i. Mettre ca beau
	j. Gestion erreur bouton supprimer
	k.
11. Faire des tests dans un fichier à part
12.
PROCHAINE ETAPE : Faire un github
ENSUITE : command button insérer categorie
ENSUITE : command supprimer catégorie (sans gestion d'erreur)
"""
