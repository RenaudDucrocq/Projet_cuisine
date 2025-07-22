class Associationintelligente:
    def __init__(self, recettes: dict, pages: dict):
        self.recettes = recettes  # Dictionnaire keys: recette, values: nombre de répétitions de la recette
        self.pages = pages  # Dictionnaire keys: page, values: nombre de répétitions de la page

    def associer_par_repetition(self):
        """
        Associe les recettes et les pages en fonction du nombre de répétitions.
        :return: Dictionnaire keys: nombre de répétitions, values: tuples de liste ([recette], [page])
        """
        associations = {}
        for recette, recette_repetition in self.recettes.items():
            if recette_repetition not in associations:
                associations[recette_repetition] = ([], [])
            # on ajoute la recette à la liste des recettes associées à ce nombre de répétitions
            associations[recette_repetition][0].append(recette)

        for page, page_repetition in self.pages.items():
            if page_repetition not in associations:
                associations[page_repetition] = ([], [])
            # on ajoute la page à la liste des pages associées à ce nombre de répétitions
            associations[page_repetition][1].append(page)

        # on trie les associations par nombre de répétitions décroissant
        associations = dict(sorted(associations.items(), key=lambda item: item[0], reverse=True))

        return associations

    @property
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'association.
        :return: Chaîne de caractères représentant l'association.
        """
        result = []
        for repetition, pairs in self.associer_par_repetition().items():
            if repetition == 3:
                result.append(f"Répétition: {repetition}")

                for recette in pairs[0]:
                    result.append(f"  Recette: {recette}")
                for page in pairs[1]:
                    result.append(f"  Page: {page}")
        return "\n".join(result)


# Exemple d'utilisation
RECETTES_SANS_PAGE = {'Abricot': 1, 'Agneau': 1, 'Ail': 1, 'Aligot traditionnel': 1, 'Amandes': 1, 'Ananas': 1,
                      'Ananas rôti à la cardamome': 2, 'Anchois': 1, 'Aneth': 1, 'Artichaut': 1, 'Asperge blanche': 1,
                      'Asperge verte': 1, 'Aubergine': 1, 'Aubergines farcies au chèvre': 1, 'Aubergines à la': 1,
                      'Aubergines à la grecque': 1, 'Aubergines à la parmesane': 1, 'Avocat': 1,
                      'Avocats farcis aux œufs': 1, 'Bacon': 1, 'Banane': 1, 'Bananes mijotées au lait de coco': 2,
                      'Basilic': 1, 'Betterave': 1, 'Betterave et épeautre façon risotto': 1, 'Beurre de cacahuètes': 1,
                      'Biscuits langues-de-chat': 1, 'Bière': 1, 'Blanquette de lieu': 2, 'Blé': 1,
                      'Blé au citron et au poulet': 1, 'Boeuf bourguignon': 3, 'Boulettes de lieu en bouillon': 1,
                      'Boulettes de saucisses aux herbes': 1, 'Boulettes de veau façon tajine': 1, 'Boulgour': 1,
                      'Boulgour façon paella': 2, 'Brochettes de cabillaud au citron vert': 1, 'Brocoli': 1,
                      'Brouillade de tofu aux herbes': 1, 'Burgers de pulled pork': 3, 'Bœuf': 1, 'Cabillaud': 1,
                      'Cabillaud mijoté à la thaïe': 2, 'Cacahuètes': 1, 'Cacao': 1, 'Cake au brocoli et au chèvre': 1,
                      'Canard': 1, 'Cannelle': 1, 'Caramel': 1, 'Cardamome': 1, 'Carotte': 1, 'Carrot cake': 2,
                      'Cassoulet express': 2, 'Cerfeuil': 1, 'Cerise': 1, 'Champignon': 1,
                      'Champignons farcis aux lardons': 1, 'Champignons à la grecque': 1, 'Chantilly': 1,
                      'Chili con carne': 1, 'Chocolat': 1, 'Chorizo': 1, 'Chou': 1, 'Chou rouge': 1, 'Chou-fleur': 1,
                      'Chou-fleur aux deux fromages': 1, 'Chou-fleur sauté au curry': 1, 'Chowder au saumon': 1,
                      'Chutney de pêches aux épices': 1, 'Châtaignes': 1, 'Clafoutis aux abricots': 1,
                      'Clafoutis aux prunes et au miel': 1, 'Cocotte de haricots rouges': 2, 'Couscous veggie': 2,
                      'Crumble express': 1, 'Crème de champignons aux noisettes': 1, 'Crème renversée au caramel': 1,
                      'Curry de bœuf au lait de coco': 2, 'Curry de cabillaud': 1, 'Cébette': 1, 'Céleri': 1,
                      'Céleri-rave': 1, 'Dahl de lentilles corail': 1, 'Flan aux cerises': 1,
                      'Flans de tomate et chorizo': 2, 'Fondue de poireaux au chorizo': 1,
                      'Galette veggie de pois chiches': 1, 'Gâteau de semoule rhum et raisins': 1,
                      'Gâteau moelleux aux amandes': 1, 'Lentilles au petit salé': 1, 'Mi-cuits au chocolat': 1,
                      'Mijoté de thon et légumes': 3, 'One': 1, 'Papillotes de cabillaud': 1,
                      'Petits pois à la française': 1, 'Piperade au jambon cru': 1, 'Pissaladière': 1,
                      'Poires pochées et caramel': 1, 'Poivrons farcis à la grecque': 2,
                      'Polenta crémeuse aux champignons': 1, 'Poule au pot': 1, 'Poulet': 1,
                      'Poulet curry-coco et riz': 1, 'Poêlée de pommes de terre': 1,
                      'Pâte à tartiner aux deux chocolats': 1, 'Quiche aux champignons': 1, 'Quinoa à la mexicaine': 1,
                      'Rillettes de thon en sandwich': 3, 'Risotto à la courge et champignons': 1,
                      'Riz pilaf aux épinards et aux fruits secs': 2, 'Riz sauté au tofu': 1,
                      'Salade complète de chou': 1, 'Salade complète de chou rouge': 4,
                      'Salade de betteraves primeurs': 2, 'Salade de blé niçoise': 2,
                      'Salade de petits pois et vinaigrette': 1, 'Sauce tomate au basilic': 1,
                      'Saumon aux légumes verts': 1, 'Sauté de porc aux champignons': 1,
                      'Seitan braise façon bourguignon': 1, 'Seitan braisé façon bourguignon': 1,
                      'Soupe de haricots du sud-ouest': 2, 'Soupe de nouilles ramen': 3, 'Soupe goulash': 1,
                      'Soupe épicée de cerises': 1, 'Tajine de boeuf aux pois chiches': 1,
                      'Tajine de bœuf aux pois chiches': 2, 'Tajine de carottes et haricots blancs': 1,
                      'Tofu et champignons à la chinoise': 1, 'Velouté de carotte fanes': 1,
                      'Wok de crevettes aux légumes': 2}

PAGES_SANS_RECETTE = {'106': 3, '107': 3, '108': 1, '110': 3, '116': 1, '122': 2, '138': 1, '14': 2, '140': 1, '142': 1,
                      '146': 2, '154': 1, '166': 1, '170': 1, '172': 2, '174': 2, '176': 1, '178': 1, '180': 1,
                      '186': 1, '192': 1, '194': 1, '198': 1, '204': 1, '205': 1, '206': 1, '208': 1, '210': 1,
                      '218': 1, '220': 1, '224': 1, '226': 1, '23': 2, '230': 1, '232': 2, '234': 2, '236': 1, '24': 1,
                      '252': 1, '254': 1, '256': 5, '260': 1, '266': 1, '272': 1, '276': 1, '282': 2, '286': 3,
                      '290': 2, '292': 1, '300': 2, '302': 1, '304': 2, '308': 2, '310': 1, '312': 1, '318': 3,
                      '322': 1, '324': 1, '328': 1, '334': 1, '336': 1, '338': 1, '340': 2, '344': 1, '346': 2,
                      '362': 1, '363': 1, '364': 1, '366': 1, '372': 1, '38': 1, '380': 1, '382': 2, '392': 1, '396': 1,
                      '398': 2, '400': 1, '402': 3, '406': 1, '408': 1, '42': 3, '420': 2, '422': 1, '43': 3, '438': 1,
                      '439': 1, '44': 1, '50': 2, '550': 1, '56': 1, '58': 1, '62': 1, '63': 2, '64': 2, '66': 2,
                      '74': 1, '82': 1, '84': 2, '86': 2, '90': 1, '92': 1}

association = Associationintelligente(RECETTES_SANS_PAGE, PAGES_SANS_RECETTE)
print(association.__str__)
