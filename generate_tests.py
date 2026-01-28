import json
import random
import os

BASE_PATH = "/Users/abdulazim/webapps/zehnly-subs/gamified_learning/data"

# Word definitions and sentences for each category
WORD_DATA = {
    "Animals": {
        "dog": {"definition": "A domesticated pet that barks and is known as man's best friend", "sentence": "The ___ wagged its tail happily when the owner came home."},
        "cat": {"definition": "A small furry pet that meows and purrs", "sentence": "The ___ climbed up the tree to catch a bird."},
        "elephant": {"definition": "The largest land animal with a long trunk and big ears", "sentence": "The ___ used its trunk to drink water from the river."},
        "lion": {"definition": "A large wild cat known as the king of the jungle", "sentence": "The ___ roared loudly to protect its territory."},
        "tiger": {"definition": "A large wild cat with orange fur and black stripes", "sentence": "The ___ is one of the most powerful hunters in Asia."},
        "bear": {"definition": "A large furry animal that hibernates in winter", "sentence": "The ___ caught a fish from the stream with its paws."},
        "wolf": {"definition": "A wild animal similar to a dog that lives in packs", "sentence": "The ___ howled at the moon in the forest."},
        "fox": {"definition": "A clever wild animal with reddish fur and a bushy tail", "sentence": "The ___ is known for being clever and quick."},
        "rabbit": {"definition": "A small animal with long ears that hops", "sentence": "The ___ hopped through the garden eating carrots."},
        "deer": {"definition": "A graceful forest animal, males have antlers", "sentence": "The ___ ran quickly through the forest."},
        "horse": {"definition": "A large animal that people ride and use for transportation", "sentence": "She learned to ride a ___ at the farm."},
        "cow": {"definition": "A farm animal that produces milk", "sentence": "The farmer milked the ___ every morning."},
        "pig": {"definition": "A pink farm animal that oinks", "sentence": "The ___ rolled in the mud to cool down."},
        "sheep": {"definition": "A farm animal with woolly fur", "sentence": "The ___ provided wool for making sweaters."},
        "goat": {"definition": "A farm animal with horns that can climb", "sentence": "The ___ climbed up the rocky mountain easily."},
        "chicken": {"definition": "A bird that lays eggs and is raised on farms", "sentence": "The ___ laid three eggs in the nest today."},
        "duck": {"definition": "A bird that swims and says 'quack'", "sentence": "The ___ swam across the pond with her babies."},
        "turkey": {"definition": "A large bird often eaten during holidays", "sentence": "We had roasted ___ for Thanksgiving dinner."},
        "eagle": {"definition": "A large bird of prey with excellent vision", "sentence": "The ___ soared high above the mountains."},
        "owl": {"definition": "A bird that hunts at night and can turn its head around", "sentence": "The ___ hooted in the tree at midnight."},
        "parrot": {"definition": "A colorful bird that can mimic human speech", "sentence": "The ___ repeated everything we said."},
        "penguin": {"definition": "A black and white bird that cannot fly but swims well", "sentence": "The ___ lives in cold Antarctica."},
        "dolphin": {"definition": "A smart sea mammal known for being friendly", "sentence": "The ___ jumped out of the water playfully."},
        "whale": {"definition": "The largest animal in the ocean", "sentence": "The ___ sprayed water from its blowhole."},
        "shark": {"definition": "A dangerous fish with sharp teeth", "sentence": "The ___ swam silently beneath the surface."},
        "fish": {"definition": "An animal that lives in water and breathes through gills", "sentence": "The ___ swam in circles in the aquarium."},
        "octopus": {"definition": "A sea creature with eight arms", "sentence": "The ___ used its eight arms to catch prey."},
        "crab": {"definition": "A sea creature with claws that walks sideways", "sentence": "The ___ walked sideways across the beach."},
        "lobster": {"definition": "A sea creature with large claws, often eaten as food", "sentence": "The restaurant served fresh ___ for dinner."},
        "jellyfish": {"definition": "A sea creature with a soft body that can sting", "sentence": "Be careful! That ___ can sting you."},
        "butterfly": {"definition": "An insect with colorful wings", "sentence": "The ___ landed gently on the flower."},
        "bee": {"definition": "An insect that makes honey and can sting", "sentence": "The ___ collected nectar from the flowers."},
        "ant": {"definition": "A tiny insect that lives in colonies and works together", "sentence": "The ___ carried food back to its colony."},
        "spider": {"definition": "A creature with eight legs that spins webs", "sentence": "The ___ spun a beautiful web between the branches."},
        "snake": {"definition": "A long reptile with no legs that slithers", "sentence": "The ___ slithered through the grass silently."},
        "lizard": {"definition": "A small reptile with four legs and a tail", "sentence": "The ___ basked in the sun on the warm rock."},
        "turtle": {"definition": "A reptile with a hard shell on its back", "sentence": "The ___ moved slowly but steadily toward the water."},
        "frog": {"definition": "An amphibian that hops and lives near water", "sentence": "The ___ jumped from one lily pad to another."},
        "crocodile": {"definition": "A large reptile with sharp teeth that lives in water", "sentence": "The ___ waited quietly in the river for its prey."},
        "monkey": {"definition": "A clever animal that swings from trees", "sentence": "The ___ swung from branch to branch in the jungle."},
        "gorilla": {"definition": "A large, powerful ape that lives in Africa", "sentence": "The ___ beat its chest to show strength."},
        "chimpanzee": {"definition": "An intelligent ape that is closely related to humans", "sentence": "The ___ used a stick as a tool to get food."},
        "giraffe": {"definition": "The tallest animal with a very long neck", "sentence": "The ___ ate leaves from the top of the tree."},
        "zebra": {"definition": "An African animal with black and white stripes", "sentence": "The ___ has unique stripes like fingerprints."},
        "hippopotamus": {"definition": "A large African animal that spends time in water", "sentence": "The ___ opened its huge mouth wide."},
        "rhinoceros": {"definition": "A large animal with thick skin and a horn on its nose", "sentence": "The ___ charged at anything that threatened it."},
        "kangaroo": {"definition": "An Australian animal that hops and carries babies in a pouch", "sentence": "The ___ hopped across the Australian outback."},
        "koala": {"definition": "An Australian animal that eats eucalyptus leaves and looks like a bear", "sentence": "The ___ slept in the eucalyptus tree all day."},
        "panda": {"definition": "A black and white bear from China that eats bamboo", "sentence": "The ___ munched on bamboo in the forest."},
        "polar bear": {"definition": "A large white bear that lives in the Arctic", "sentence": "The ___ hunted seals on the Arctic ice."},
    },
    "Food & Drinks": {
        "apple": {"definition": "A round red or green fruit that grows on trees", "sentence": "She packed an ___ in her lunch box."},
        "banana": {"definition": "A long yellow fruit that monkeys love", "sentence": "The ___ was perfectly ripe and sweet."},
        "orange": {"definition": "A round citrus fruit with vitamin C", "sentence": "I squeezed fresh ___ juice for breakfast."},
        "bread": {"definition": "A common food made from flour and baked", "sentence": "We need to buy a loaf of ___ from the bakery."},
        "rice": {"definition": "Small white grains that are a staple food in Asia", "sentence": "We had steamed ___ with our dinner."},
        "pizza": {"definition": "A flat round food with cheese and toppings", "sentence": "Let's order a ___ for dinner tonight."},
        "burger": {"definition": "A sandwich with a meat patty inside a bun", "sentence": "He ordered a ___ with fries at the restaurant."},
        "sandwich": {"definition": "Food made with filling between two pieces of bread", "sentence": "I made a cheese ___ for lunch."},
        "salad": {"definition": "A dish made of mixed vegetables", "sentence": "She ordered a fresh ___ to stay healthy."},
        "soup": {"definition": "A liquid food made by boiling ingredients in water", "sentence": "The hot ___ warmed me up on the cold day."},
        "chicken": {"definition": "Meat from a farm bird, commonly eaten worldwide", "sentence": "Mom cooked delicious fried ___ for dinner."},
        "egg": {"definition": "An oval food laid by birds, often eaten for breakfast", "sentence": "I had a boiled ___ for breakfast."},
        "cheese": {"definition": "A dairy product made from milk", "sentence": "Add some ___ to make the pasta tastier."},
        "milk": {"definition": "A white liquid from cows that we drink", "sentence": "Children should drink ___ for strong bones."},
        "water": {"definition": "A clear liquid essential for life", "sentence": "Drink eight glasses of ___ every day."},
        "juice": {"definition": "A drink made from squeezed fruits", "sentence": "Would you like apple or orange ___?"},
        "coffee": {"definition": "A hot brown drink that helps you wake up", "sentence": "He drinks ___ every morning to start his day."},
        "tea": {"definition": "A hot drink made by steeping leaves in water", "sentence": "Would you like some ___ with your cake?"},
        "cake": {"definition": "A sweet baked dessert often eaten at parties", "sentence": "We had chocolate ___ at the birthday party."},
        "cookie": {"definition": "A small sweet baked treat", "sentence": "She baked chocolate chip ___ for the kids."},
    },
    "Family & People": {
        "mother": {"definition": "A female parent", "sentence": "My ___ always takes care of me when I'm sick."},
        "father": {"definition": "A male parent", "sentence": "My ___ taught me how to ride a bicycle."},
        "brother": {"definition": "A male sibling", "sentence": "My older ___ helps me with homework."},
        "sister": {"definition": "A female sibling", "sentence": "My ___ and I share a bedroom."},
        "grandmother": {"definition": "The mother of your parent", "sentence": "My ___ makes the best cookies."},
        "grandfather": {"definition": "The father of your parent", "sentence": "My ___ tells amazing stories about the past."},
        "aunt": {"definition": "The sister of your parent", "sentence": "My ___ lives in another city."},
        "uncle": {"definition": "The brother of your parent", "sentence": "My ___ took me fishing last weekend."},
        "cousin": {"definition": "The child of your aunt or uncle", "sentence": "My ___ is the same age as me."},
        "friend": {"definition": "A person you like and enjoy spending time with", "sentence": "My best ___ always makes me laugh."},
        "teacher": {"definition": "A person who helps students learn", "sentence": "The ___ explained the lesson clearly."},
        "student": {"definition": "A person who studies at school", "sentence": "Every ___ must do their homework."},
        "doctor": {"definition": "A person who helps sick people get better", "sentence": "The ___ checked my temperature."},
        "nurse": {"definition": "A person who helps doctors care for patients", "sentence": "The ___ gave me my medicine."},
        "baby": {"definition": "A very young child", "sentence": "The ___ smiled when she saw her mother."},
        "child": {"definition": "A young person who is not yet an adult", "sentence": "Every ___ deserves a good education."},
        "husband": {"definition": "A married man", "sentence": "Her ___ surprised her with flowers."},
        "wife": {"definition": "A married woman", "sentence": "His ___ is an excellent cook."},
        "neighbor": {"definition": "A person who lives next to you", "sentence": "Our ___ has a friendly dog."},
        "boss": {"definition": "A person in charge at work", "sentence": "My ___ approved my vacation request."},
    },
}

def get_word_data(category, word):
    """Get definition and sentence for a word"""
    cat_data = WORD_DATA.get(category, {})
    if word in cat_data:
        return cat_data[word]
    # Generate generic data for words not in our database
    return {
        "definition": f"A word related to {category.lower()}",
        "sentence": f"The ___ is an important word to learn."
    }

def generate_definition_match(word, all_words, category):
    """Match word to its definition"""
    word_data = get_word_data(category, word)
    correct_def = word_data["definition"]

    # Get wrong definitions from other words
    wrong_words = random.sample([w for w in all_words if w != word], min(3, len(all_words)-1))
    wrong_defs = [get_word_data(category, w)["definition"] for w in wrong_words]

    options = [correct_def] + wrong_defs
    random.shuffle(options)
    correct_index = options.index(correct_def)

    return {
        "type": "definition_match",
        "question": f"What does '{word.upper()}' mean?",
        "word": word,
        "options": options,
        "correct_answer": correct_index,
        "difficulty": "medium"
    }

def generate_sentence_completion(word, all_words, category):
    """Fill word in a sentence"""
    word_data = get_word_data(category, word)
    sentence = word_data["sentence"]

    wrong_words = random.sample([w for w in all_words if w != word], min(3, len(all_words)-1))
    options = [word] + wrong_words
    random.shuffle(options)
    correct_index = options.index(word)

    return {
        "type": "sentence_completion",
        "question": sentence.replace("___", "_____"),
        "word": word,
        "options": options,
        "correct_answer": correct_index,
        "difficulty": "medium"
    }

def generate_reverse_definition(word, all_words, category):
    """Given definition, pick the word"""
    word_data = get_word_data(category, word)
    definition = word_data["definition"]

    wrong_words = random.sample([w for w in all_words if w != word], min(3, len(all_words)-1))
    options = [word] + wrong_words
    random.shuffle(options)
    correct_index = options.index(word)

    return {
        "type": "reverse_definition",
        "question": f"Which word matches this definition?\n\"{definition}\"",
        "word": word,
        "options": options,
        "correct_answer": correct_index,
        "difficulty": "medium"
    }

def generate_tests_for_category(folder_path):
    """Generate tests for a category"""
    words_file = os.path.join(folder_path, "words.json")

    with open(words_file, 'r') as f:
        data = json.load(f)

    words = data['words']
    category_name = data['name']
    tests = []

    test_generators = [
        generate_definition_match,
        generate_sentence_completion,
        generate_reverse_definition,
    ]

    for word in words:
        for i, generator in enumerate(test_generators):
            try:
                test = generator(word, words, category_name)
                test['id'] = f"{word.replace(' ', '_')}_{i+1}"
                test['category'] = category_name
                tests.append(test)
            except Exception as e:
                print(f"Error generating test for {word}: {e}")

    return {
        "category": category_name,
        "category_id": data['id'],
        "total_tests": len(tests),
        "tests": tests
    }

def main():
    folders = sorted([f for f in os.listdir(BASE_PATH) if f[0].isdigit() and os.path.isdir(os.path.join(BASE_PATH, f))])

    for folder in folders:
        folder_path = os.path.join(BASE_PATH, folder)
        words_file = os.path.join(folder_path, "words.json")

        if not os.path.exists(words_file):
            continue

        print(f"Generating tests for {folder}...")
        tests_data = generate_tests_for_category(folder_path)

        tests_file = os.path.join(folder_path, "tests.json")
        with open(tests_file, 'w') as f:
            json.dump(tests_data, f, indent=2)

        print(f"  Created {tests_data['total_tests']} tests")

    print("\nAll tests generated!")

if __name__ == "__main__":
    random.seed(42)
    main()
