"""
CSC111 Project 2
Group members: Colleen Chang, Richard Lin, Roy Liu, Mina (Chieh-Yi) Wu

File Description
=============================================================================
This is the main file for running the program.
"""
import csv
import python_ta
from storage import Tree, Song
from visualization import generate_region_df_by_streams, generate_region_df_by_score, visualize_world_song_data, \
    all_options_table


def initialize_spotify_file(file_name: str) -> Tree:
    """Intializes this tree according to the provided csv file of the top songs data.
    """
    new_tree = Tree('World', [])
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            city = row[0]
            country = row[1]
            continent = row[2]
            new_tree.insert_sequence([continent, country, city])
            city = new_tree.navigate_sequence([continent, country, city])

            # Note, countries without cities still have a city child labeled '0'
            rank = 1
            for s in range(3, 8):
                song_obj = create_song_object(row[s], rank)
                city.insert_sequence([song_obj])
                rank += 1
    return new_tree


def create_song_object(string_data: str, rank: int) -> Song:
    """Creates a Song object from the given string data.

    A helper for initialize_spotify_file.

    The string should be in the following format:
            "<title>, <main_artist>, <streams>"
    """
    split_str = string_data.split(', ')
    title, artist, streams = split_str[0].lower().strip(), split_str[1].lower().strip(), int(split_str[2].strip())
    return Song(title, artist, streams, rank)


def get_personality_test(tree: Tree, available_songs: set[str]) -> None:
    """Runs the personality test in the user input menu.
    """
    print("This choice returns the regions who have the most similar top songs as your top list on a score of (0-1).")

    region_range = get_region_range()
    num_regions = 0
    while num_regions <= 0:
        curr_input = input('Enter the max number of scores you want to see in descending order (>= 1): ').strip()
        if curr_input.isnumeric() and int(curr_input) > 0:
            num_regions = int(curr_input)
        else:
            print('Invalid input')

    user_songs = get_user_top_songs(available_songs)

    message = "Do you want the scores to consider the rankings of the songs? (type 'Y' for yes): "
    ranked = input(message).strip().lower()
    if ranked == 'y':
        ranked = True
    else:
        ranked = False

    test = tree.region_personality(num_regions, user_songs, region_range, ranked)

    print('\nHere are the top regions with the most similar top songs:')
    count = 1
    for region in test:
        print(f"{count}. {', '.join(region[1][::-1])}: {region[0]}")
        count += 1
    print("\n")


def run_recommendation(tree: Tree, available_songs: set[str]) -> None:
    """Runs the song recommendation function for user interaction
    """
    print("This choice returns new song recommendations from the regions that have the most similar "
          "top songs as your top list")

    max_rec = 0
    while max_rec <= 0:
        message = 'Enter the max number of recommendations you want scored in descending order (>= 1): '
        curr_input = input(message).strip()
        if curr_input.isnumeric() and int(curr_input) > 0:
            max_rec = int(curr_input)
        else:
            print('Invalid input')

    region = get_region_range()
    max_region = 0
    while max_region <= 0:
        message = 'Enter the max number of most similar regions you want to look through for recommendations (>= 1): '
        curr_input = input(message).strip()
        if curr_input.isnumeric() and int(curr_input) > 0:
            max_region = int(curr_input)
        else:
            print('Invalid input')

    user_songs = get_user_top_songs(available_songs)

    message = "Do you want the recommendation to consider the rankings of the songs? (type 'Y' for yes): "
    ranked = input(message).strip().lower()
    if ranked == 'y':
        ranked = True
    else:
        ranked = False

    recommendations = tree.recommend_songs((max_rec, max_region), user_songs, region, ranked)
    print('\nHere are your recommendations:')
    count = 1
    for s in recommendations:
        print(f'{count}. {s.title} by {s.artist}')
        count += 1
    print("\n")


def get_region_range() -> str:
    """Gets the user input for a region range in ('continent', 'country', 'city')
    """
    region = ''
    while region not in {'continent', 'country', 'city'}:
        region = input("What region range do you want to use? (continent, country, city): ").strip().lower()
        if region not in {'continent', 'country', 'city'}:
            print('Invalid input')
    return region


def get_user_top_songs(song_set: set[str]) -> list[str]:
    """Gets the user input for their 1-5 top songs that are in song_set.
    """
    user_songs = []
    n = 0
    while n < 1 or n > 5:
        n = input("How many top songs do you want to use? (1-5 inclusive): ").strip()
        if not n.isnumeric() or (int(n) < 1 or int(n) > 5):
            n = 0
            print("Invalid input. Please try again.")
        else:
            n = int(n)

    # ask if the user wants to see the list of all songs
    print("\nFirst, provide us a few songs.\n"
          "The song MUST be listed in the program to be valid. Would you like to see a pop up listing all\n"
          "the songs we have? Y/N")
    show_song_list = input("\nEnter your choice here: ").strip().lower()

    while show_song_list not in {'y', 'yes', 'n', 'no'}:
        print("\nSorry, but that's not a valid option. Please re-enter your choice.")
        show_song_list = input("Enter your choice here: ").strip().lower()

    if show_song_list in {'y', 'yes'}:
        all_options_table(song_set, 'song')

    i = 1
    while i <= n:
        s = input(f'Enter song #{i}: ').lower().strip()
        if s not in song_set:
            print('Song not found')
        else:
            i += 1
            user_songs.append(s)
    return user_songs


def choice1(tree: Tree, choices: set) -> None:
    """Prints the top n songs in a specific region of the user's choice.
    """
    print("\nLet's find the top songs in a region of your choice!")
    c = input("Enter any continent/country/city:(Title Case): ").strip()

    while c not in choices:
        print("The input is either invalid or not in the database. Please try again.")
        c = input("Enter any continent/country/city:(Capitalize the first letter): ").strip()

    n = input("Please enter the number of top songs you would like to see: ").lower().strip()
    print("\nP.s. Only the top 5 songs will be shown if n is greater than 5 "
          "and only the top 5 songs are avaliable for that region.")
    while not n.isnumeric() or int(n) < 1:
        print("Invalid input. Please try again.")
        n = input("Please enter the number of top songs you would like to see: ").lower().strip()

    output = tree.top_n(int(n), c)
    num = 1
    for item in output:
        print(str(num) + ". " + item[0] + " by " + item[1])
        num += 1

    print("\n")


def choice2(tree: Tree, countries: set) -> None:
    """Prints the common artists of two user inputted countries.
    """
    print("You must be wondering what the most common artists between two countries of your choice are.\nAsk away!")

    c1 = input("Enter the first country (Capitalize the first letter): ").strip()
    c2 = input("Enter the second country (Capitalize the first letter): ").strip()

    while c1 not in countries or c2 not in countries:
        print("Invalid input. Please try again.")
        c1 = input("Enter the first country (Capitalize the first letter): ").strip()
        c2 = input("Enter the second country (Capitalize the first letter): ").strip()

    common = tree.common_artist(c1, c2)

    print("\nHere are the common artists between " + c1 + " and " + c2 + ":")
    for i in range(len(common)):
        print(f'{i + 1}: {common[i]}')
    print("\n")


def choice3(tree: Tree, countries: set) -> None:
    """Prints the common songs between two user inputted countries.
    """
    print("You must be wondering what the most common songs between two countries of your choices are.\nAsk away!")

    c1 = input("Enter the first country (Capitalize the first letter): ").strip()
    c2 = input("Enter the second country (Capitalize the first letter): ").strip()

    while c1 not in countries or c2 not in countries:
        print("Invalid input. Please try again.")
        c1 = input("Enter the first country (Capitalize the first letter): ").strip()
        c2 = input("Enter the second country (Capitalize the first letter): ").strip()

    common = tree.common_song(c1, c2)

    print('\nHere are the common songs between ' + c1 + ' and ' + c2 + ':')
    for i in range(len(common)):
        print(f'{i + 1}: {common[i]}')
    print("\n")


def choice4(tree: Tree, countries: set) -> None:
    """Prints the country that has the most artists in common with the user inputted country.
    """
    print("You must be wondering which country has the most artists in common with your chosen country.\n Ask away!")

    c1 = input("Enter the name of the country you're interested in (Capitalize the first letter): ").strip()

    while c1 not in countries:
        print("Invalid input. Please try again.")
        c1 = input("Enter the name of the country you're interested in (Capitalize the first letter): ").strip()

    print(f"The country that has the most artists in common with yours is: {tree.most_common_artist_country(c1)}!")
    print("\n")


def choice5(tree: Tree, countries: set) -> None:
    """Prints the country that has the most songs in common with the user inputted country.
    """
    print("You must be wondering which country has the most songs in common with your chosen country.\n Ask away!")

    c1 = input("Enter the name of the country you're interested in (Capitalize the first letter): ").strip()

    while c1 not in countries:
        print("Invalid input. Please try again.")
        c1 = input("Enter the name of the country you're interested in (Capitalize the first letter): ").strip()

    print(f"The country that has the most songs in common with yours is: {tree.most_common_song_country(c1)}!")
    print("\n")


def visualization_prompt(tree: Tree, song_set: set) -> None:
    """
    Facilitates needed descriptions and prompts to generate a visualization based on the user's inputs.
    """
    running = True

    # graph descriptions
    print("==============================================================================\n"
          " Welcome to the visualizer! Please select one of the following graph options.\n"
          "=============================================================================="
          )
    print("TOP 5:\n"
          "These maps will visualize all specified regions by the number of total streamed accured by their top\n"
          "5 songs, represented by its shade; darker regions correspond to higher stream counts. If you\n"
          "hover over a certain region, a pop up will display the names of the top 5 songs.\n"
          "\nSIMILARITY SCORE:\n"
          "You'll be prompted to list 1 - 5 songs that must be recorded within this program's dataset, as well as\n"
          "a rank specification. Then, the program will calculate the comparison score of all specified regions and\n"
          "represent them by shade, similar to 'Top 5 maps.' If you hover over a certain region, a pop up will\n"
          "display the exact comparison score calculated."
          )
    print("\nEnter 'quit' to return to the other options.")

    vis_option = input("\nEnter your choice here: ").strip().lower()

    while running:
        # get graph option
        while vis_option not in {'top 5', 'similarity score', 'quit'}:
            print("\nSorry, but that's not a valid option. Please re-enter your choice.")
            vis_option = input("Enter your choice here: ").strip().lower()

        if vis_option == 'top 5':
            # get region
            print("\nPlease select how you want to divide your regions, either by CONTINENT, COUNTRY, or CITY.")
            top_5_region = input("Enter your choice here: ").strip().lower()

            while top_5_region not in {'continent', 'country', 'city'}:
                print("\nSorry, but that's not a valid option. Please re-enter your choice.")
                top_5_region = input("Enter your choice here: ").strip().lower()

            # generate data frame and graph
            print("\nPlease wait a moment while we generate your map...")
            vis_df = generate_region_df_by_streams(tree, top_5_region)
            visualize_world_song_data(top_5_region, 'streams', vis_df)

            # prompt for another graph
            print("\nA graph should have popped up in your browser!")
            print("To generate a new visualization, enter whether you want a 'top 5' or 'similarity score' graph.\n"
                  + "If you want to return to the previous options, enter 'quit.'"
                  )
            vis_option = input("\nEnter your choice here: ").strip().lower()

        elif vis_option == 'similarity score':
            # prompt user for songs
            user_songs = get_user_top_songs(song_set)

            # get rank specification
            print("\nNext, would you like the score to be sensitive to the rank in which you ordered your songs? Y/N")
            user_ranked = input("Enter your choice here: ").strip().lower()

            while user_ranked not in {'y', 'yes', 'n', 'no'}:
                print("\nSorry, but that's not a valid option. Please re-enter your choice.")
                user_ranked = input("Enter your choice here: ").strip().lower()

            rank_op = False
            if user_ranked in {'y', 'yes'}:
                rank_op = True

            # get region
            print("\nPlease select how you want to divide your regions, either by CONTINENT, COUNTRY, or CITY.")
            sim_score_region = input("Enter your choice here: ").strip().lower()

            while sim_score_region not in {'continent', 'country', 'city'}:
                print("\nSorry, but that's not a valid option. Please re-enter your choice.")
                sim_score_region = input("Enter your choice here: ").strip().lower()

            # generate data frame and graph
            print("\nPlease wait a moment while we generate your map...")
            vis_df = generate_region_df_by_score(tree, user_songs, sim_score_region, rank_op)
            visualize_world_song_data(sim_score_region, 'scores', vis_df)

            # prompt for another graph
            print("\nA graph should have popped up in your browser!")
            print("To generate a new visualization, enter whether you want a 'top 5' or 'similarity score' graph.\n"
                  "If you want to return to the previous options, enter 'quit.'"
                  )
            vis_option = input("\nEnter your choice here: ").strip().lower()

        else:  # exits visualizer
            running = False


if __name__ == "__main__":
    tree_file = "FINAL_DATA.csv"
    spotify_tree = initialize_spotify_file(tree_file)  # Make sure this is consistent with file names

    # Initializes sets containing all song titles and location titles in the tree
    all_continents = set()
    all_countries = set()
    all_cities = set()
    all_songs = set()
    for curr_city in spotify_tree.get_all_cities_sequence():
        all_continents.add(curr_city[1][0])
        all_countries.add(curr_city[1][1])
        all_cities.add(curr_city[1][2])

        for song in curr_city[0].get_songs():
            all_songs.add(song.title)

    all_cities.discard('0')  # removes the instances where a country doesn't have a city
    all_choice = all_continents.union(all_countries).union(all_cities)

    stop = False
    print("Welcome to the Spotify visualization program!\n"
          "This is the main menu. Please select an option:\n")

    print("To generate a table of all available geographic and song options, please choose the following\n"
          "(This is recommended before running the other options!):\n"
          "a. Show all continents\n"
          "b. Show all countries\n"
          "c. Show all cities\n"
          "d. Show all songs\n")

    while not stop:
        print("1. Get the top n songs for a continent/country/city\n"
              "2. Find the most common artists between two countries\n"
              "3. Find the most common songs between two countries\n"
              "4. Find the most common countries between a country of your choice and the rest"
              " of the world based on top artists\n"
              "5. Find the most common countries between a country of your choice and the rest"
              " of the world based on top songs\n"
              "6. Find the region with the most similar song tastes as you\n"
              "7. Find new song recommendations for a specific continent/country/city\n"
              "8. Visualization options\n"
              "9. Exit the program\n")

        choice = input("Please enter your choice (1 ~ 9) or (a ~ d): ").lower().strip()
        while choice not in {"1", "2", "3", "4", "5", "6", "7", "8", "9", 'a', 'b', 'c', 'd'}:
            print("Invalid input. Please try again.")
            choice = input("Please enter your choice(1 ~ 9): ").lower().strip()

        if choice == "1":
            choice1(spotify_tree, all_choice)
        elif choice == "2":
            choice2(spotify_tree, all_countries)
        elif choice == "3":
            choice3(spotify_tree, all_countries)
        elif choice == "4":
            choice4(spotify_tree, all_choice)
        elif choice == "5":
            choice5(spotify_tree, all_choice)
        elif choice == "6":
            get_personality_test(spotify_tree, all_songs)
        elif choice == "7":
            run_recommendation(spotify_tree, all_songs)
        elif choice == "8":
            visualization_prompt(spotify_tree, all_songs)
        elif choice == "9":
            stop = True
        elif choice == 'a':
            print('\nGenerating Table...\n')
            all_options_table(all_continents, 'continent')
        elif choice == 'b':
            print('\nGenerating Table...\n')
            all_options_table(all_countries, 'country')
        elif choice == 'c':
            print('\nGenerating Table...\n')
            all_options_table(all_cities, 'city')
        elif choice == 'd':
            print('\nGenerating Table...\n')
            all_options_table(all_songs, 'song')

    print("Thank you for using the Spotify visualization program, we hope you enjoyed it!")

    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['storage', 'csv', 'visualization'],
        "forbidden-io-functions": [],  # allows for print and input functions
        'max-line-length': 120
    })
