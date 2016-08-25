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


Classes : GUI, Facture

1. Main
	a. Scrollbar
	b. Bouton supprimer
	c. Permettre le double click pour modifier
	f. paid = oui/non
	g. del bill
	h. modify bill
	i.
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
	d. Mettre ca beau
	e. Grosseur
	f. endroit dans l'écran
	k.
10. top_categories
	a. Grosseur
	b. Endroit dans l'écran
	f. command insérer
	g. command supprimer
	h. Distribution widgets du bas
	i. Mettre ca beau
	j. Gestion erreur bouton supprimer
	k.
11. Faire tests dans un fichier à part
13. Base de données
	f. del bill
	g. modify bill
	h.
14. Filtrage
	a. clickage des headings pour sorter
	b. permettre de sorter asc, des
	c.
15. Passer à ttk?
16. Erreurs
	a. Lister toutes les erreurs possibles
	b. 
17. paid -> 1 dans la database

PROCHAINE ETAPE : del_bill DB à terminer
ENSUITE : del bill gui
ENSUITE : modify db
ENSUITE : modify GUI
ENSUITE : clickage des heading ORDER BY x".format(init_date, due_date, etc.)
"""
