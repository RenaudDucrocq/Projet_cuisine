# Fichier de test pour tester les recettes
from parse_methods.parse import parse_recettes_data
from GUI.interface_recette import INTERFACE_RECETTE

def test_parse_recettes_data(mocker):
    mocker.Mock()
    # Mocking the GUI to avoid user interaction
    mocker.patch('GUI.interface_recette.INTERFACE_RECETTE.run',
                    return_value={'Carottes': [{'page': '31', 'recipe': 'Carottes glacées au miel'}],
                                'Oignons': [{'page': '32', 'recipe': 'Oignons confits'}],
                                'Chou-fleur': [{'page': '33', 'recipe': 'Chou-fleur rôti'}],
                                'Poivron': [{'page': '34', 'recipe': 'Poivron vert farci'}]})
    text_content = (
        "Navarin de dinde aux petits légumes..............30\n"
        "Carottes glacées au miel..........................31\n"
        "Oignons confits....................................32\n"
        "Chou-fleur rôti....................................33\n"
        "Poivron vert farci.................................34"
    )
    structured_data = {
        "Carottes": [],
        "Oignons": [],
        "Chou-fleur": [],
        "Poivron": []
    }

    expected_recipes = {
        "Carottes": [{"recipe": "Carottes glacées au miel", "page": '31'}],
        "Oignons": [{"recipe": "Oignons confits", "page": '32'}],
        "Chou-fleur": [{"recipe": "Chou-fleur rôti", "page": '33'}],
        "Poivron": [{"recipe": "Poivron vert farci", "page": '34'}]
    }

    result, recette_sans_page, page_sans_recette = parse_recettes_data(text_content, structured_data)

    assert result == expected_recipes
    assert recette_sans_page == {}
    assert page_sans_recette == {}


def test_recette_sans_page(mocker):
    mocker.Mock()
    # Mocking the GUI to avoid user interaction
    mocker.patch('GUI.interface_recette.INTERFACE_RECETTE.run',
                 return_value={'Dinde': [{'page': '30', 'recipe': 'Navarin de dinde aux petits légumes'}],
                               'Légumes': [{'page': '30', 'recipe': 'Navarin de dinde aux petits légumes'}]})

    text_content = (
        "Soupe de légumes..............\n"
        "Mijoté de thon et légumes\n"
        "Mijoté de thon et légumes....\n"
        "Navarin de dinde aux petits légumes..30\n"
        "Navarin de dinde aux petits légumes..\n"
    )
    structured_data = {
        "Légumes": [],
        "Thon": [],
        "Dinde": []
    }

    expected_recette_sans_page = {
        "Soupe de légumes": 1,
        "Mijoté de thon et légumes": 2
    }

    result, recette_sans_page, page_sans_recette = parse_recettes_data(text_content, structured_data)

    assert recette_sans_page == expected_recette_sans_page


def test_page_sans_recette(mocker):
    mocker.Mock()
    # Mocking the GUI to avoid user interaction
    mocker.patch('GUI.interface_recette.INTERFACE_RECETTE.run',
                 return_value={'Dinde': [{'page': '30', 'recipe': 'Navarin de dinde aux petits légumes'}],
                               'Légumes': [{'page': '30', 'recipe': 'Navarin de dinde aux petits légumes'}]})

    text_content = (
        "30\n"
        ".45\n"
        "..100\n"
        "Navarin de dinde aux petits légumes..............30\n"
        "45\n"
        "100\n"
        "Soupe de légumes..............\n"
        "30\n"
        "70\n"
    )
    structured_data = {
        "Dinde": [],
        "Légumes": []
    }

    expected_page_sans_recette = {
        "45": 2,
        "100": 2,
        "70": 1
    }

    result, recette_sans_page, page_sans_recette = parse_recettes_data(text_content, structured_data)

    assert page_sans_recette == expected_page_sans_recette
