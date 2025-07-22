import re
import locale
from GUI.interface_ingredient import INTERFACE_INGREDIENT
from GUI.interface_recette import INTERFACE_RECETTE


def parse_ingredients_data(text_content):
    """
        Parses the text content to extract structured data for ingredients.

        :param text_content: The text content to parse, typically from OCR output.
        :return: A dictionary where keys are ingredient names and value is empty.
    """

    structured_data = {}

    # Exclude common index markers that are not ingredients
    EXCLUDED_HEADERS = {"INDEX", "PAR INGREDIENT", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                        "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}

    # Split the content into lines
    lines = text_content.split('\n')

    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    # Tri la liste lines par ordre alphabétique
    lines.sort()

    # Definition d'un ingredient principal
    # Une ligne qui commence par une majuscule et ne contient ni chiffre ni point et moins de 3 mots.
    # Un ingrédient peut contenir un trait d'union.
    # Exemple: "Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert".
    # Regex : r'^[A-Z][a-zàâäéèêëîïôöùûüçœ\-]*(?:[\s\-][a-zàâäéèêëîïôöùûüçœA-Z][a-zàâäéèêëîïôöùûüçœ\-]*){0,2}$'
    ingredient_pattern = re.compile(
        r'^[A-Z][a-zàâäéèêëîïôöùûüçœ\-]*(?:[\s\-][a-zàâäéèêëîïôöùûüçœA-Z][a-zàâäéèêëîïôöùûüçœ\-]*){0,2}$')
    for line in lines:
        # On check si la ligne est un ingredient principal.
        line.strip()  # Remove leading and trailing whitespace
        if ingredient_pattern.match(line) and len(line.split()) < 3 and line not in EXCLUDED_HEADERS:
            ingredient = line
            if ingredient not in structured_data:
                structured_data[ingredient] = []

    # Tri des ingrédients par ordre alphabétique
    # locale permet de préciser la langue pour le tri et donc de prendre en compte les accents.
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # Set locale for French sorting
    structured_data = dict(sorted(structured_data.items(), key=lambda item: locale.strxfrm(item[0])))

    # appel de la GUI pour afficher les ingrédients et mettre a jour la liste.
    interface = INTERFACE_INGREDIENT(list(structured_data.keys()))
    ingredients_valides = interface.run()

    # Mise à jour de la liste des ingrédients valides
    for ingredient in list(structured_data.keys()):
        if ingredient not in ingredients_valides:
            del structured_data[ingredient]

    return structured_data


def parse_recettes_data(text_content, structured_data: dict) -> (dict, dict, dict):
    """
        Parses the text content to extract recipes and associates them with ingredients.

        :param text_content: The text content to parse, typically from OCR output.
        :param structured_data: The dictionary where keys are ingredient names.
        :return: A dictionary where keys are ingredient names and values are lists of recipes,
            a dict of recipes without page numbers where values are number of occurence,
            a dict of page numbers without associated recipes where values are number of occurence.
    """

    recette_sans_page = {}
    page_sans_recette = {}

    # Definition d'une recette
    # Une recette est une ligne qui commence par le nom de la recette, suivi de points (au moins deux) et du numéro de page.
    # le nom de la recette ne contient que des lettres, des espaces et des tirets, et commence toujours par une lettre majuscule.
    # le numéro de page est un nombre entier.
    # Exemple: Navarin de dinde aux petits légumes..............30
    recipe_name_pattern = re.compile(r'^(?P<recipe>[A-Z][a-zàâäéèêëîïôöùûüçœ\- ]+)\.*$')
    page_number_pattern = re.compile(r'^\.*(?P<page>\d+)$')
    recipe_pattern = re.compile(r'^(?P<recipe>[A-Z][a-zàâäéèêëîïôöùûüçœ\- ]+)\.{2,}(?P<page>\d+)$')

    # Split the content into lines
    lines = text_content.split('\n')

    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]

    # Tri la liste lines par ordre alphabétique
    lines.sort()

    for line in lines:
        match = recipe_pattern.match(line)
        if match:
            recipe_name = match.group('recipe').strip()
            page_number = match.group('page').strip()

            # Vérifie si le nom de la recette contient un des ingrédients
            # et que le nom de la recette n'est pas déjà associé à cet ingrédient.
            for ingredient in structured_data.keys():
                if ingredient.lower() in recipe_name.lower() and not any(
                        recipe['recipe'] == recipe_name for recipe in structured_data[ingredient]):
                    structured_data[ingredient].append({'recipe': recipe_name, 'page': page_number})

        # On vérifie si la ligne contient un nom de recette et des points, mais pas de numéro de page.
        # Exemple: "Soupe de légumes..............", "Mijoté de thon et légumes".
        elif recipe_name_pattern.match(line):
            recipe_name_match = recipe_name_pattern.match(line).group('recipe').strip()
            # On vérifie si le nom de la recette est déjà présente dans la liste des recettes pour chaque ingrédient.
            for ingredient in structured_data.keys():
                if ingredient.lower() in recipe_name_match.lower() and not any(
                        recipe['recipe'] == recipe_name_match for recipe in structured_data[ingredient]):
                    # On ajoute la recette sans numéro de page.
                    recette_sans_page[recipe_name_match] = recette_sans_page.get(recipe_name_match, 0) + 1

        # On vérifie si la ligne contient un numéro de page sans nom de recette.
        #Exemple: "30", ".45", "..100".
        elif page_number_pattern.match(line):
            page_number_match = page_number_pattern.match(line).group('page').strip()
            # On ajoute la page à la liste qui n'a pas de recette associée mais contient tous les numéros de page.
            for ingredient in structured_data.keys():
                if not any(recipe['page'] == page_number_match for recipe in structured_data[ingredient]):
                    # On ajoute la page sans recette associée.
                    page_sans_recette[page_number_match] = page_sans_recette.get(page_number_match, 0) + 1

    # appel de la GUI pour afficher les ingrédients et mettre a jour la liste.
    interface = INTERFACE_RECETTE(structured_data)
    recettes_valides = interface.run()

    return recettes_valides, recette_sans_page, page_sans_recette


def parse(filein=None):
    """Main function to parse the index data from the OCR output text file."""
    # Read the content of the text file
    with open(filein if filein else '../document_text_annotations/outputs/output.txt', 'r', encoding='utf-8') as file:
        text_from_ocr = file.read()

    # Perform the parsing
    parsed_data = parse_ingredients_data(text_from_ocr)
    parsed_data, recette_sans_page, page_sans_recette = parse_recettes_data(text_from_ocr, parsed_data)

    # Print a snippet of the parsed data for verification
    for ingredient, recipes in list(parsed_data.items()):  # [:5]:  # Limit to first 5 ingredients for brevity
        print(f"Ingredient: {ingredient}:")
        for recipe in recipes:
            print(f"  - {recipe['recipe']} (Page {recipe['page']})")
        print("-" * 40)  # Separator for readability

    print(f"Total ingredients found: {len(parsed_data)}")


if __name__ == "__main__":
    parse()
