import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QCheckBox, QPushButton, QMainWindow, QScrollArea
from PyQt6.QtCore import Qt


class INTERFACE_INGREDIENT(QApplication):
    def __init__(self, ingredients: list):
        """Initialize the GUI with a label and a button."""
        super().__init__(sys.argv)
        self.ingredients = ingredients
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("GUI")
        self.main_window.setFixedSize(300, 600)  # Set a fixed size for the window

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.main_window.setCentralWidget(self.scroll)

        self.checkboxes = []
        self.valider_ingredients()

        self.button = QPushButton(text="Valider", parent=self.main_window)
        self.button.setFixedHeight(30)
        self.button.clicked.connect(self.valider_selection)
        self.layout.addWidget(self.button)


    def valider_ingredients(self):
        for ingredient in self.ingredients:
            current_check = QCheckBox(parent=self.main_window, text=str(ingredient))
            current_check.setChecked(True)
            self.layout.addWidget(current_check)
            self.checkboxes.append(current_check)


    def maj_ingredients(self, ingredient: str):
        """ Met à jour la liste des ingrédients suite au check d'un ingredient."""
        if ingredient in self.ingredients:
            self.ingredients.remove(ingredient)
            # print(f"Ingredient {ingredient} removed from the list.")
            # print(self.ingredients)
        # else:
        #     print(f"Ingredient {ingredient} not found in the list.")


    def valider_selection(self):
        """Le bouton valider termine la saisie dans l'interface et ferme la fenêtre."""
        print("Valider")
        for checkbox in self.checkboxes:
            if not checkbox.isChecked():
                ingredient = checkbox.text()
                self.maj_ingredients(ingredient)

        self.main_window.close()

    def run(self):
        """Run the GUI application.
        This method starts the application and returns the updated list of ingredients.
        :return: list: The updated list of ingredients after user selection."""

        self.main_window.show()
        self.exec()
        return self.ingredients  # Return the updated list of ingredients


# mywindow = GUI(["Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert","Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert","Aubergine", "Carotte", "Oignon", "Chou-fleur", "Poivron vert"])
# mywindow.run()
# print("ok")
