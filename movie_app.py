import storage_csv

menu = """_____MENU_____________________________________________________________________
0. Exit                 1. List movies          2. Add movie
3. Delete movie         4. Update movie         5. Stats
6. Random movie         7. Search movie         8. Movies sorted by rating
9. Generate website     10. Favorite movie      11. Movie histogram
12. Save to csv file
______________________________________________________________________________
"""

class MovieApp:
    def __init__(self, storages):
        self._storage = storages

    def _command_list_movies(self):
        self._storage.list_movies()

    def _command_add(self):
        self._storage.add_movie()

    def _command_del(self):
        self._storage.delete_movie()

    def _command_update(self):
        self._storage.update_movie()

    def _command_movie_stats(self):
        self._storage.list_movies()
        self._storage.stats_movie()

    def _command_statistics(self):
        self._storage.list_movies()
        self._storage.stats_movie()

    def _command_random(self):
        self._storage.random_movie()

    def _command_search(self):
        self._storage.search_movie()

    def _command_sort(self):
        self._storage.sort_movies()

    def _generate_website(self):
        self._storage.generate_web()

    def _command_favorite(self):
        self._storage.favorite_movies()

    def _command_histogram(self):
        self._storage.movies_histogram()

    def run(self):
        print(menu)
        while True:
            choice = input("Enter choice (0-12): ")
            if choice == '0':
                print("Bye!")
                break

            try:
                choice = int(choice)
                if 0 < choice < 13:

                    if choice == 1:
                        self._command_list_movies()
                    elif choice == 2:
                        self._command_add()
                    elif choice == 3:
                        self._command_del()
                    elif choice == 4:
                        self._command_update()
                    elif choice == 5:
                        self._command_statistics()
                    elif choice == 6:
                        self._command_random()
                    elif choice == 7:
                        self._command_search()
                    elif choice == 8:
                        self._command_sort()
                    elif choice == 9:
                        self._generate_website()
                        print('Enjoy index.html! Thank you')
                    elif choice == 10:
                        self._command_favorite()
                        print('Enjoy index.html! Thank you')
                    elif choice == 11:
                        self._command_histogram()
                    elif choice == 12:
                        storage_csv.save_to_csv()
                    else:
                        print("Over limited")

                else:
                    print("Invalid choice. Please enter a number between 0 and 11.")
            except ValueError:
                print("Invalid choice. Please enter a number between 0 and 11.")

            button = input('press any key to continue (N to skip)? : ')
            if button.upper() == "N":
                print("Thank you!")
                break
