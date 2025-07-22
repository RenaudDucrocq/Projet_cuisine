class Associationintelligente:
    def __init__(self, recettes: dict, pages: dict):
        self.recettes = recettes  # Dictionnaire keys: recette, values: nombre de répétitions de la recette
        self.pages = pages  # Dictionnaire keys: page, values: nombre de répétitions de la page

    def associer_par_repetition(self):
        """
        Associe les recettes et les pages en fonction du nombre de répétitions.
        :return: Dictionnaire keys: nombre de répétitions, values: liste de tuples (recette, page)
        """
        associations = {}
        for recette, recette_repetition in self.recettes.items():
            for page, page_repetition in self.pages.items():
                if recette_repetition == page_repetition:
                    if recette_repetition not in associations:
                        associations[recette_repetition] = []
                    associations[recette_repetition].append((recette, page))

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
            result.append(f"Répétition: {repetition}")
            for recette, page in pairs:
                result.append(f"  Recette: {recette}, Page: {page}")
        return "\n".join(result)


# Exemple d'utilisation
RECETTES_SANS_PAGE = {'Abricot': 1, 'Agneau': 1, 'Ail': 1, 'Amandes': 1, 'Ananas': 1, 'Ananas rôti à la cardamome': 4,
                      'Anchois': 1, 'Aneth': 1, 'Artichaut': 1, 'Asperge blanche': 1, 'Asperge verte': 1,
                      'Aubergine': 1, 'Aubergines farcies au chèvre': 1, 'Aubergines à la': 1,
                      'Aubergines à la grecque': 1, 'Aubergines à la parmesane': 1, 'Avocat': 1,
                      'Avocats farcis aux œufs': 1, 'Bacon': 1, 'Banane': 1, 'Bananes mijotées au lait de coco': 2,
                      'Basilic': 1, 'Betterave': 1, 'Betterave et épeautre façon risotto': 1, 'Beurre de cacahuètes': 1,
                      'Biscuits langues-de-chat': 1, 'Bière': 1, 'Blé': 1, 'Blé au citron et au poulet': 1,
                      'Blé aux courgettes et tomates séchées': 1, 'Boulgour': 1, 'Boulgour façon paella': 2,
                      'Brocoli': 1, 'Brocoli sauté aux amandes et au tofu': 2, 'Bœuf': 1, 'Cabillaud': 1,
                      'Cabillaud mijoté à la thaïe': 2, 'Cacahuètes': 1, 'Cacao': 1, 'Cake au brocoli et au chèvre': 1,
                      'Canard': 1, 'Cannelle': 1, 'Caramel': 1, 'Cardamome': 1, 'Carotte': 1, 'Cerfeuil': 1,
                      'Cerise': 1, 'Champignon': 1, 'Champignons farcis aux lardons': 1, 'Champignons à la grecque': 1,
                      'Chantilly': 1, 'Chocolat': 1, 'Chorizo': 1, 'Chou': 1, 'Chou rouge': 2, 'Chou-fleur': 2,
                      'Chou-fleur aux deux fromages': 2, 'Chou-fleur sauté au curry': 2, 'Châtaignes': 1,
                      'Clafoutis aux abricots': 1, 'Crème de champignons aux noisettes': 1,
                      'Crème renversée au caramel': 1, 'Curry de bœuf au lait de coco': 2, 'Curry de cabillaud': 1,
                      'Cébette': 1, 'Céleri': 1, 'Céleri-rave': 2, 'Dahl de lentilles corail': 1, 'Flan aux cerises': 1,
                      'Flans de tomate et chorizo': 2, 'Fondue de poireaux au chorizo': 1,
                      'Gâteau moelleux aux amandes': 1, 'Manchons de canard aux lentilles': 1,
                      'Mi-cuits au chocolat': 1, 'Mijoté de carottes gingembre-coco': 2, 'Papillotes de cabillaud': 1,
                      'Poires pochées et caramel': 1, 'Polenta crémeuse aux champignons': 1,
                      'Quiche aux champignons': 1, 'Risotto à la courge et champignons': 1,
                      'Salade complète de chou': 1, 'Salade complète de chou rouge': 8,
                      'Salade de betteraves primeurs': 2, 'Salade de blé niçoise': 2, 'Sauce tomate au basilic': 1,
                      'Sauté de porc aux champignons': 1, 'Soupe épicée de cerises': 1,
                      'Tajine de bœuf aux pois chiches': 2, 'Tajine de carottes et haricots blancs': 1,
                      'Tofu et champignons à la chinoise': 1, 'Velouté de carotte fanes': 1}
PAGES_SANS_RECETTE = {'106': 129, '107': 129, '108': 43, '110': 129, '116': 43, '122': 86, '138': 43, '14': 86,
                      '140': 43, '142': 43, '146': 86, '154': 43, '166': 43, '168': 86, '170': 43, '172': 86, '174': 86,
                      '176': 43, '178': 43, '180': 43, '186': 43, '192': 43, '194': 43, '198': 43, '204': 43, '205': 43,
                      '206': 43, '208': 43, '210': 43, '218': 43, '220': 43, '224': 43, '225': 43, '226': 43, '23': 86,
                      '230': 43, '232': 86, '234': 86, '236': 43, '24': 43, '252': 43, '254': 43, '256': 215, '260': 43,
                      '266': 43, '272': 43, '276': 43, '282': 86, '286': 129, '290': 86, '292': 43, '300': 86,
                      '302': 43, '304': 86, '306': 43, '308': 86, '310': 43, '312': 43, '318': 129, '319': 43,
                      '322': 43, '324': 43, '328': 43, '334': 43, '336': 43, '338': 43, '340': 86, '344': 43, '346': 86,
                      '362': 43, '363': 43, '364': 43, '372': 43, '38': 43, '380': 43, '382': 86, '392': 43, '396': 43,
                      '398': 86, '400': 43, '402': 129, '406': 43, '408': 43, '42': 129, '420': 86, '422': 43,
                      '43': 129, '438': 43, '439': 43, '44': 43, '50': 86, '550': 43, '56': 43, '58': 43, '62': 43,
                      '63': 86, '64': 86, '66': 86, '70': 43, '74': 43, '78': 43, '80': 43, '82': 43, '84': 86,
                      '86': 86, '90': 43, '92': 43}
