import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QCheckBox, QPushButton, QMainWindow, QScrollArea, \
    QHBoxLayout, QLabel, QSizePolicy, QFrame
from PyQt6.QtCore import Qt


class INTERFACE_RECETTE(QApplication):
    def __init__(self, structured_data: dict):
        """Initialize the GUI with a label and a button.
        :param structured_data: A dictionary where keys are ingredient names
            and values are lists of dict {key: recipe_name, value: page_number}."""
        super().__init__(sys.argv)
        self.structured_data = structured_data
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("GUI")
        self.main_window.setFixedSize(600, 600)  # Set a fixed size for the window

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.main_window.setCentralWidget(self.scroll)

        self.checkboxes_recettes = {}  # Dict key: ingredient, value: list des checkboxes des recettes
        # Initialize checkboxes_recettes with empty lists for each ingredient
        for ingredient in self.structured_data.keys():
            self.checkboxes_recettes[ingredient] = []
        self.valider_recettes()

        self.button = QPushButton(text="Valider", parent=self.main_window)
        self.button.setFixedHeight(30)
        self.button.clicked.connect(self.valider_selection)
        self.layout.addWidget(self.button)


    def valider_recettes(self):
        """Crée des blocks de checkboxs de chaque recette pour chaque ingrédient."""

        for ingredient, recipes in list(self.structured_data.items()):
            widget_ingredient = QFrame()
            widget_ingredient.setFrameShape(QFrame.Shape.Box)
            widget_ingredient.setLineWidth(1)

            # Create a horizontal layout for each ingredient
            layout_ingredient = QHBoxLayout()

            widget_ingredient.setLayout(layout_ingredient)
            self.layout.addWidget(widget_ingredient)

            # Create a Label for the ingredient
            current_ingredient = QLabel(parent=self.main_window, text=f"{ingredient}")

            layout_ingredient.addWidget(current_ingredient)

            widget_recipes = QWidget()
            widget_recipes.setFixedWidth(400)
            # Create a vertical layout for the ingredient's recipes
            layout_recipes = QVBoxLayout()
            widget_recipes.setLayout(layout_recipes)
            layout_ingredient.addWidget(widget_recipes)

            for recipe in recipes:
                # Create a checkbox for each recipe associated with the ingredient
                current_check = QCheckBox(parent=self.main_window, text=f"{recipe['recipe']} (Page: {recipe['page']})")
                current_check.setChecked(True)
                layout_recipes.addWidget(current_check)
                self.checkboxes_recettes[ingredient].append(current_check)


    def maj_recette(self, ingredient: str, recette: str):
        """ Met à jour la liste des recettes suite à la validation de la fenetre"""
        if ingredient in self.structured_data.keys():
            # Si la recette est dans la liste, on la supprime de la liste des recettes
            # Il faut isoler la recette du texte de la checkbox
            recette = recette.split(' (')[0]  # On prend juste le nom de la recette sans la page
            self.structured_data[ingredient] = [value for value in self.structured_data[ingredient]
                                                if recette not in value['recipe']]
            print(f"Recette {recette} removed from ingredient {ingredient}.")
            print(self.structured_data)


    def valider_selection(self):
        """Le bouton valider termine la saisie dans l'interface et ferme la fenêtre."""
        print("Valider")
        for ingredient, checkboxes in self.checkboxes_recettes.items():
            for checkbox in checkboxes:
                if not checkbox.isChecked():
                    recette = checkbox.text()
                    self.maj_recette(ingredient, recette)

        self.main_window.close()

    def run(self):
        """Run the GUI application.
        This method starts the application and returns the updated list of ingredients.
        :return: list: The updated list of ingredients after user selection."""

        self.main_window.show()
        self.exec()
        return self.structured_data  # Return the updated list of ingredients


# mywindow = GUI(["Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert","Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert","Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert"])
# mywindow.run()
# print("ok")
