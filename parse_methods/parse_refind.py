import json
import re
from collections import defaultdict


# --- Utility Functions (unchanged, for brevity, copy from previous code) ---
def normalize_ingredient_name(ingredient_name):
    name = ingredient_name.lower().strip()
    reps = {'œ': 'oe', 'é': 'e', 'à': 'a', 'ç': 'c', 'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u'}
    for old, new in reps.items():
        name = name.replace(old, new)
    replacements = {
        'œufs': 'œuf', 'pommes': 'pomme', 'tomates': 'tomate', 'poivrons': 'poivron',
        'blanches': 'blanc', 'vertes': 'vert', 'rouges': 'rouge', 'secs': 'sec',
        'fraises': 'fraise', 'cerises': 'cerise', 'pois': 'poix',
        'lentilles': 'lentille', 'haricots': 'haricot', 'champignons': 'champignon',
        'noix': 'noix', 'prunes': 'prune', 'bananes': 'banane', 'pêches': 'pêche',
        'figues': 'figue', 'raisins': 'raisin', 'olives': 'olive', 'crevettes': 'crevette',
        'moules': 'moule', 'patates': 'patate', 'carottes': 'carotte', 'courgettes': 'courgette',
        'citrons': 'citron', 'asperges': 'asperge', 'pâtes': 'pate',
        'epinards': 'epinard', 'pois chiches': 'pois chiche', 'petits pois': 'petit pois',
        'cébettes': 'cébette', 'abricots': 'abricot', 'artichauts': 'artichaut',
        'betteraves': 'betterave', 'choux': 'chou', 'chocolats': 'chocolat',
        'agneau': 'agneau'
    }
    sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
    for old, new in sorted_replacements:
        name = name.replace(old, new)
    name = re.sub(r'^\W*\d*\s*', '', name).strip()
    name = re.sub(r'\s*\d*\W*$', '', name).strip()
    return name


def get_words_with_coords(json_data):
    words_data = []
    for page in json_data.get('responses', [])[0].get('fullTextAnnotation', {}).get('pages', []):
        for block in page.get('blocks', []):
            for paragraph in block.get('paragraphs', []):
                for word_info in paragraph.get('words', []):
                    word_text = ''.join([symbol['text'] for symbol in word_info.get('symbols', [])])
                    vertices = word_info['boundingBox']['normalizedVertices']
                    x = vertices[0]['x']
                    y = vertices[0]['y']
                    words_data.append({'text': word_text, 'x': x, 'y': y})
    return words_data


# **MAJOR CHANGE in how lines are grouped: now it happens AFTER column assignment**
# So this function will become part of the processing for each column.
# Let's keep a simplified `group_words_into_lines` for initial broad line grouping,
# but the true "line" formation for parsing will happen per column.
def group_words_into_raw_lines(words_data, y_tolerance_ratio=0.007):
    """Groups words into broad horizontal strips based on Y-coordinates, before column awareness."""
    words_data.sort(key=lambda w: (w['y'], w['x']))

    raw_lines = []
    current_line = []

    if not words_data:
        return []

    current_line_y = words_data[0]['y']

    for word in words_data:
        if abs(word['y'] - current_line_y) <= y_tolerance_ratio:
            current_line.append(word)
        else:
            raw_lines.append(current_line)
            current_line = [word]
            current_line_y = word['y']

    if current_line:
        raw_lines.append(current_line)

    # We will not combine words into full lines here yet. We keep them as lists of words.
    # The actual line formation will happen per column later.
    return raw_lines


def identify_columns_improved(words_data, x_cluster_tolerance=0.02):
    """
    Identifies distinct columns by clustering X-coordinates of *all* words.
    This gives a more robust column detection by using all available word positions.
    """
    if not words_data:
        return []

    # Use X-coordinates of *all words* for better column clustering
    x_coords = [w['x'] for w in words_data]
    x_coords.sort()

    if not x_coords:
        return []

    clusters = []
    if x_coords:
        current_cluster = [x_coords[0]]
        for x in x_coords[1:]:
            if x - current_cluster[-1] < x_cluster_tolerance:
                current_cluster.append(x)
            else:
                clusters.append(current_cluster)
                current_cluster = [x]
        clusters.append(current_cluster)

    column_ranges = []
    for cluster in clusters:
        # A column should have a significant number of words, not just a few stragglers.
        # This threshold might need tuning.
        if len(cluster) > 100:  # Increased threshold for words, not lines.
            column_ranges.append({'min_x': min(cluster), 'max_x': max(cluster)})

    column_ranges.sort(key=lambda r: r['min_x'])

    return column_ranges


def assign_words_to_columns(words_data, column_ranges):
    """Assigns each word to its identified column."""
    columns_content_words = defaultdict(list)

    for word in words_data:
        assigned = False
        for i, col_range in enumerate(column_ranges):
            # Check if word's X is within the column's X range (with a small buffer)
            if col_range['min_x'] - 0.005 <= word['x'] <= col_range['max_x'] + 0.005:
                columns_content_words[f"col_{i}"].append(word)
                assigned = True
                break
    return columns_content_words


def group_words_into_lines_per_column(column_words, y_tolerance_ratio=0.007):
    """
    Groups words *within a single column* into logical lines.
    This is where the actual lines for parsing are formed.
    """
    if not column_words:
        return []

    # Sort words within the column primarily by Y, then by X
    column_words.sort(key=lambda w: (w['y'], w['x']))

    formatted_lines = []
    current_line_words = []

    current_line_y = column_words[0]['y']

    for word in column_words:
        if abs(word['y'] - current_line_y) <= y_tolerance_ratio:
            current_line_words.append(word)
        else:
            if current_line_words:
                # Sort words within the detected line by X to ensure correct order
                current_line_words.sort(key=lambda w: w['x'])
                full_line_text = " ".join([w['text'] for w in current_line_words])
                start_x = current_line_words[0]['x']
                start_y = current_line_words[0]['y']
                formatted_lines.append({'text': full_line_text, 'x': start_x, 'y': start_y})

            current_line_words = [word]
            current_line_y = word['y']

    # Add the last line
    if current_line_words:
        current_line_words.sort(key=lambda w: w['x'])
        full_line_text = " ".join([w['text'] for w in current_line_words])
        start_x = current_line_words[0]['x']
        start_y = current_line_words[0]['y']
        formatted_lines.append({'text': full_line_text, 'x': start_x, 'y': start_y})

    return formatted_lines


def parse_column_content_v7_debug(column_lines):  # Renamed for debugging version
    structured_column_data = {}
    current_main_ingredient = None

    EXCLUDED_HEADERS = {
        "INDEX", "PAR INGREDIENT",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    }

    # Lines are already sorted by Y within the column

    recipe_page_pattern = re.compile(r'(.+?)\s*\.{2,}\s*(\d+)$')
    recipe_page_pattern_no_dots = re.compile(r'(.+?)\s+(\d+)$')

    print("\n--- Debugging Column Content Parsing ---")
    for line_info in column_lines:
        line_text = line_info['text'].strip()
        print(f"Processing line: '{line_text}' (Y: {line_info['y']:.3f}, X: {line_info['x']:.3f})")

        if not line_text:
            print("  -> Skipped: Empty line")
            continue

        # --- Step 1: Try to detect a RECIPE and PAGE NUMBER FIRST ---
        match = recipe_page_pattern.search(line_text)
        if not match:
            match = recipe_page_pattern_no_dots.search(line_text)

        if match:
            recipe_name = match.group(1).strip()
            page_number = int(match.group(2))

            recipe_name = re.sub(r'^\d+\s*', '', recipe_name).strip()
            recipe_name = re.sub(r'\s*\.+\s*$', '', recipe_name).strip()

            if current_main_ingredient:
                if not any(d['recipe'] == recipe_name and d['page'] == page_number for d in
                           structured_column_data[current_main_ingredient]):
                    structured_column_data[current_main_ingredient].append({"recipe": recipe_name, "page": page_number})
                    print(
                        f"  -> Detected as RECIPE for '{current_main_ingredient}': '{recipe_name}', Page: {page_number}")
            else:
                print(
                    f"  -> Detected as RECIPE but NO current ingredient (likely an orphan recipe or part of a multi-line recipe): '{recipe_name}', Page: {page_number}")
            continue

            # --- Step 2: If not a recipe, try to detect a MAIN INGREDIENT ---
        clean_line_for_ingredient_check = re.sub(r'^\d+\s*', '', line_text).strip()

        is_potential_ingredient_header = re.match(r'^[A-Z][a-zA-Z\s\-]+$', clean_line_for_ingredient_check) and \
                                         '.' not in clean_line_for_ingredient_check and \
                                         ',' not in clean_line_for_ingredient_check and \
                                         any(char.isalpha() for char in clean_line_for_ingredient_check)

        if is_potential_ingredient_header and \
                clean_line_for_ingredient_check not in EXCLUDED_HEADERS and \
                1 <= len(clean_line_for_ingredient_check.split()) <= 4 and \
                1 <= len(clean_line_for_ingredient_check) < 40 and \
                not re.search(r'\d', clean_line_for_ingredient_check):
            current_main_ingredient = clean_line_for_ingredient_check
            structured_column_data[current_main_ingredient] = []
            print(f"  -> Detected as MAIN INGREDIENT: '{current_main_ingredient}'")
            continue

        print(f"  -> Skipped: Not recognized as ingredient or recipe.")
        if current_main_ingredient:
            print(f"     Current Ingredient still: '{current_main_ingredient}'")
        else:
            print("     No current ingredient.")

    print("--- End Debugging Column Content Parsing ---\n")
    return structured_column_data


# --- MAIN EXECUTION ---
json_file_path = '../output_vision_api_output-1-to-1.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    vision_api_output = json.load(f)

# 1. Extract *all* words with coordinates
all_words_with_coords = get_words_with_coords(vision_api_output)

# 2. Identify columns based on *all word X-coordinates* (more robust)
# x_cluster_tolerance for words is critical here. 0.02 seems reasonable, but might need tweaking.
column_ranges = identify_columns_improved(all_words_with_coords, x_cluster_tolerance=0.02)
print(f"Detected column ranges (X-coordinates): {column_ranges}")

# 3. Assign *individual words* to columns
words_by_column = assign_words_to_columns(all_words_with_coords, column_ranges)

final_structured_data = {}
for col_name, words_in_col in words_by_column.items():
    if not words_in_col:
        print(f"\n--- Skipping empty {col_name} ---")
        continue

    # 4. Group words into logical lines *within each column*
    # y_tolerance_ratio: 0.007 is 0.7% of page height. A typical line height.
    lines_in_col = group_words_into_lines_per_column(words_in_col, y_tolerance_ratio=0.007)

    print(f"\n--- Processing {col_name} ({len(lines_in_col)} formatted lines) ---")

    # 5. Parse content within each column using the formatted lines
    parsed_col_data = parse_column_content_v7_debug(lines_in_col)

    for ingredient, recipes in parsed_col_data.items():
        normalized_ing = normalize_ingredient_name(ingredient)
        if normalized_ing not in final_structured_data:
            final_structured_data[normalized_ing] = []

        for recipe_info in recipes:
            if not any(r['recipe'] == recipe_info['recipe'] and r['page'] == recipe_info['page'] for r in
                       final_structured_data[normalized_ing]):
                final_structured_data[normalized_ing].append(recipe_info)

print("\n--- Final Structured and Normalized Data (V7 - Improved Line Segmentation) ---")
count = 0
for ingredient, recipes in list(final_structured_data.items()):
    if count >= 20 and len(final_structured_data) > 20:
        break
    if not recipes:
        continue
    print(f"Ingrédient Principal (Normalisé): {ingredient.capitalize()}")
    for recipe in recipes:
        print(f"  - Recette: {recipe['recipe']}, Page: {recipe['page']}")
    print("-" * 40)
    count += 1

print(f"\nTotal ingrédients principaux uniques après normalisation: {len(final_structured_data)}")