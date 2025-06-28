import os
import random # Added for quest generation chance
from symai import Symbol, EngineRepository

# Attempt to configure the neurosymbolic engine (e.g., OpenAI or Gemini)
# Users should have NEUROSYMBOLIC_ENGINE_API_KEY and NEUROSYMBOLIC_ENGINE_MODEL set in their environment
# For Gemini, symbolicai might require specific setup or might use a general LLM interface.
# We'll proceed assuming a compatible engine is configured.

class Player:
    def __init__(self, name, health, attack, backstory):
        self.name = Symbol(name)
        self.health = health
        self.attack = attack
        self.backstory = Symbol(backstory) # Using Symbol for potential semantic operations later
        self.current_location = None
        self.inventory = []
        self.current_quest = None

    def __str__(self):
        quest_status = "None"
        if self.current_quest:
            quest_status = f"'{self.current_quest.description}' (Objective: {self.current_quest.objective}) - {'Completed' if self.current_quest.is_completed else 'Active'}"
        return f"Name: {self.name.value}\nHealth: {self.health}\nAttack: {self.attack}\nBackstory: {self.backstory.value}\nCurrent Quest: {quest_status}"

class Quest:
    def __init__(self, description, objective):
        self.description = Symbol(description)
        self.objective = Symbol(objective)
        self.is_completed = False

    def __str__(self):
        return f"Quest: {self.description.value}\nObjective: {self.objective.value}\nStatus: {'Completed' if self.is_completed else 'Active'}"

def create_character():
    print("Welcome to the Dynamic RPG Character Creator!")
    name = input("Enter your character's name: ")

    # For simplicity, fixed stats for now
    health = 100
    attack = 10

    # Generate backstory using an LLM via symbolicai
    print("Generating character backstory...")
    backstory_generated = False
    try:
        # symbolicai should ideally auto-configure the engine based on environment variables.
        # We ensure that an API key is set, which is a prerequisite.
        if os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
            prompt = f"Generate a short, adventurous backstory for a character named {name} in a fantasy RPG setting. Keep it to 1-2 sentences."
            # The .query() method should use the configured neurosymbolic engine.
            backstory_sym = Symbol(prompt).query()

            if backstory_sym is not None and str(backstory_sym).strip():
                backstory = str(backstory_sym)
                backstory_generated = True
            else:
                print("LLM returned empty backstory, using a default one.")
        else:
            print("NEUROSYMBOLIC_ENGINE_API_KEY not set. Cannot generate backstory.")

    except Exception as e:
        print(f"Error during backstory generation: {e}")

    if not backstory_generated:
        print("Using a default backstory.")
        backstory = f"{name} has a mysterious past and a desire for adventure."

    player = Player(name, health, attack, backstory)
    print("\nCharacter Created!")
    print(player)
    return player

if __name__ == "__main__":
    # This is a placeholder for where the neurosymbolic engine API key would be set
    # For actual execution, ensure environment variables like NEUROSYMBOLIC_ENGINE_API_KEY
    # and NEUROSYMBOLIC_ENGINE_MODEL are set.
    # Example (do not run this directly without setting real keys):
    # os.environ['NEUROSYMBOLIC_ENGINE_API_KEY'] = 'YOUR_API_KEY'
    # os.environ['NEUROSYMBOLIC_ENGINE_MODEL'] = 'your_model_name' # e.g., 'gpt-3.5-turbo' or a Gemini model if supported

    if not os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
        print("WARNING: NEUROSYMBOLIC_ENGINE_API_KEY not set. LLM features will likely fail.")
        print("Please set this environment variable to your LLM provider's API key.")

    # Attempt to select an engine if none are active - this is speculative
    # and depends on how symbolicai handles engine initialization.
    # The user of symbolicai is typically expected to have their environment configured.
    try:
        if not EngineRepository.ENGINES:
            # This is a fallback, ideally symbolicai loads from config or env vars.
            # Trying to default to a commonly available one if keys are set.
            # The specific engine (OpenAI, Cohere, Gemini via adapter) would depend on user's setup.
            print("Attempting to initialize a default neurosymbolic engine if API keys are present...")
            # symbolicai's documentation should be consulted for the best way to initialize engines.
            # For now, we rely on the user having set this up or symbolicai's auto-detection.
            pass # Avoid explicit engine activation here if it's meant to be auto-configured
    except Exception as e:
        print(f"Could not auto-initialize an engine: {e}")

    player_character = create_character()
    if player_character:
        print(f"\nWelcome, {player_character.name.value}!")
        generate_starting_location(player_character)
        if player_character.current_location:
            print(f"\nYou find yourself in: {player_character.current_location.value}")
            game_loop(player_character) # Start the game loop
        else:
            print("Failed to set a starting location. Exiting.")

    print("\n--- Thank you for playing! ---")


def game_loop(player):
    playing = True
    while playing:
        print("\n" + "="*30)
        # Ensure player.current_location is not None before accessing .value
        if player.current_location:
            print(f"Current Location: {player.current_location.value}")
        else:
            print("Current Location: Unknown (this shouldn't happen after starting location generation)")
        print("="*30)

        action_input = input("\nWhat do you do? (explore, look, interact, status, quit): ").strip().lower()
        action_outcome_for_quest_check = ""

        if action_input == "quit":
            playing = False
            print("You decide to end your adventure for now.")
        elif action_input == "status":
            print(f"\n--- {player.name.value}'s Status ---")
            print(f"Health: {player.health}")
            print(f"Attack: {player.attack}")
            if player.inventory:
                print("Inventory: " + ", ".join(player.inventory))
            else:
                print("Inventory: Empty")
            if player.current_quest and not player.current_quest.is_completed:
                print("\n--- Current Quest ---")
                print(f"Description: {player.current_quest.description.value}")
                print(f"Objective: {player.current_quest.objective.value}")
                print("--------------------")
            elif player.current_quest and player.current_quest.is_completed:
                print("\n--- Current Quest ---")
                print(f"Description: {player.current_quest.description.value} (Completed)")
                print("--------------------")
            else:
                print("No active quest.")
            print("---")
        elif action == "explore":
            explore_action(player)
        elif action == "look":
            look_action(player)
        elif action == "interact":
            interact_action(player)
        else:
            print("Unknown action. Try: explore, look, interact, status, or quit.")

        # After action, check for quest completion and new quest generation
        action_outcome_for_quest_check = ""
        if action == "explore":
            action_outcome_for_quest_check = explore_action(player)
        elif action == "look":
            look_action(player) # look_action doesn't typically advance quests
        elif action == "interact":
            action_outcome_for_quest_check = interact_action(player)
        else:
            print("Unknown action. Try: explore, look, interact, status, or quit.")

        if action in ["explore", "interact"]: # Only check after actions that change state
            if action_outcome_for_quest_check: # Ensure there was some result
                check_quest_completion(player, action_outcome_for_quest_check)
            maybe_generate_new_quest(player)


def explore_action(player):
    print("\nYou venture forth...")
    action_result = ""
    try:
        if os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
            prompt = f"Player {player.name.value} is currently at: \"{player.current_location.value}\". They decide to explore further. Describe what they discover next or a new adjacent area they find. Keep it concise (2-3 sentences)."
            new_discovery_sym = Symbol(prompt).query()
            if new_discovery_sym is not None and str(new_discovery_sym).strip():
                action_result = str(new_discovery_sym)
                player.current_location = Symbol(action_result) # Update current location with the new discovery
                print(f"You discovered: {action_result}")
            else:
                action_result = "The way forward is unclear, or perhaps nothing new is found this time."
                print(action_result)
                # Optionally, current_location could remain unchanged or be subtly modified
        else:
            action_result = f"Despite {player.name.value}'s efforts to explore, the surroundings remain eerily similar, or perhaps a dense fog rolls in, obscuring the path."
            print("NEUROSYMBOLIC_ENGINE_API_KEY not set. Exploration yields no new discoveries (using default).")
            player.current_location = Symbol(action_result) # Update location to reflect this
    except Exception as e:
        action_result = f"An unnatural stillness falls as {player.name.value} tries to explore. The path ahead is confusing."
        print(f"Error during exploration: {e}")
        player.current_location = Symbol(action_result) # Update location
    return action_result

def look_action(player):
    print("\nYou take a closer look at your surroundings...")
    print(player.current_location.value)
    # Potentially, this could also be an action_result if we want quests based on looking.
    # For now, it's passive.

def interact_action(player):
    print("\nYou try to interact with your environment or any beings...")
    action_result = ""
    try:
        if os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
            prompt = f"Player {player.name.value} is at: \"{player.current_location.value}\". They try to interact with anything or anyone of interest. Describe what happens or what they notice. If nothing specific is apparent, describe their attempt."
            interaction_sym = Symbol(prompt).query()
            if interaction_sym is not None and str(interaction_sym).strip():
                action_result = str(interaction_sym)
                print(action_result)
            else:
                action_result = "You find nothing specific to interact with, or your attempt yields no results."
                print(action_result)
        else:
            action_result = f"{player.name.value} calls out, but only the echo answers. The area seems devoid of immediate response."
            print("NEUROSYMBOLIC_ENGINE_API_KEY not set. Interaction is uneventful (using default).")
            print(action_result)
    except Exception as e:
        action_result = f"A strange interference prevents {player.name.value} from interacting clearly."
        print(f"Error during interaction: {e}")
        print(action_result)
    return action_result

def maybe_generate_new_quest(player):
    if player.current_quest is None or player.current_quest.is_completed:
        if random.random() < 0.25: # 25% chance to generate a new quest
            print("\nA new feeling of purpose washes over you...")
            try:
                if os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
                    prompt = f"Player {player.name.value} is currently at: \"{player.current_location.value}\". Generate a simple, short fantasy quest description and a clear objective for them that seems relevant to this situation. Format as 'Quest: [description]\\nObjective: [objective]'."
                    quest_gen_sym = Symbol(prompt).query()
                    if quest_gen_sym is not None and str(quest_gen_sym).strip():
                        quest_text = str(quest_gen_sym)
                        # Basic parsing, assuming "Quest: ...\nObjective: ..." format
                        desc_part = ""
                        obj_part = ""
                        if "Objective: " in quest_text and "Quest: " in quest_text:
                            desc_part = quest_text.split("Quest: ")[1].split("\nObjective: ")[0]
                            obj_part = quest_text.split("\nObjective: ")[1]

                        if desc_part and obj_part:
                            player.current_quest = Quest(desc_part, obj_part)
                            print(f"New Quest: {player.current_quest.description.value}")
                            print(f"Objective: {player.current_quest.objective.value}")
                        else:
                            print("Could not parse the generated quest text properly.")
                    else:
                        print("The winds of fate offer no new quest at this moment.")
                else:
                    print("NEUROSYMBOLIC_ENGINE_API_KEY not set. No new quests are generated.")
            except Exception as e:
                print(f"Error generating new quest: {e}")

def check_quest_completion(player, last_action_result):
    if player.current_quest and not player.current_quest.is_completed:
        print(f"\nChecking quest '{player.current_quest.objective.value}'...")
        try:
            if os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
                prompt = f"Player {player.name.value}'s current quest objective is: \"{player.current_quest.objective.value}\". Their last action/result was: \"{last_action_result}\". The overall situation is \"{player.current_location.value}\". Based SOLELY on this, does it seem like they have directly completed their quest objective? Answer ONLY with YES or NO."
                completion_sym = Symbol(prompt).query()
                if completion_sym is not None:
                    answer = str(completion_sym).strip().upper()
                    if "YES" in answer:
                        player.current_quest.is_completed = True
                        print(f"** Quest Completed: {player.current_quest.description.value}! **")
                        # Potentially give a reward or trigger another event here
                        player.current_quest = None # Clear quest or move to a completed list
                    elif "NO" in answer:
                        print("The quest objective doesn't seem to be met by that action.")
                    else:
                        print(f"Received ambiguous answer for quest completion: {answer}")
                else:
                    print("Could not determine quest completion from LLM response.")
            else:
                print("NEUROSYMBOLIC_ENGINE_API_KEY not set. Cannot check quest completion.")
        except Exception as e:
            print(f"Error checking quest completion: {e}")


def generate_starting_location(player):
    print("\nGenerating your starting location...")
    location_description_generated = False
    try:
        if os.getenv('NEUROSYMBOLIC_ENGINE_API_KEY'):
            prompt = f"Describe a mysterious and intriguing starting location for a new adventurer named {player.name.value} in a fantasy RPG. The location should evoke a sense of old magic and potential discovery. Keep it to 2-3 sentences."
            location_sym = Symbol(prompt).query()

            if location_sym is not None and str(location_sym).strip():
                player.current_location = Symbol(str(location_sym))
                location_description_generated = True
            else:
                print("LLM returned empty location description, using a default one.")
        else:
            print("NEUROSYMBOLIC_ENGINE_API_KEY not set. Cannot generate location description.")

    except Exception as e:
        print(f"Error during location generation: {e}")

    if not location_description_generated:
        print("Using a default starting location.")
        default_location = f"{player.name.value} stands at the edge of an ancient, mist-shrouded forest. Old, gnarled trees seem to whisper secrets, and a barely visible path leads into the shadows."
        player.current_location = Symbol(default_location)


# Next steps:
# 1. Implement the main game loop (Describe, Input, Process, Update).
# 2. Add more dynamic interactions and exploration capabilities.
