"""
Author: Vítor Carvalho Marx Lima

Link para o repositório com o código:
Github: https://github.com/HeiwaRyuu/jokenpo-python

Vídeo explicando e demonstrando as funcionalidades do código
Youtube Video: https://youtu.be/OKkJh8vIlhU

Email: vitor.carvalho.ufu@gmail.com

Escolhi Python por já ter uma afinidade com a linguagem e por ela proporcionar 
uma implementação mais ágil se comparada à outras linguagens como C/C++
"""
import random
import os
import json
import math

## Game Class
class Jokenpo:
    def __init__(self):
        self.user_session_menu = {1:"Entrar com um usuário", 2:"Continuar como visitante"}
        self.main_menu_options = {1:"Jogar", 2:"Estatísticas", 3:"Trocar de Usuário", 4:"Sair"}
        self.game_mode_options = {1:"Uma partida", 2:"Melhor de 3", 3:"Melhor de 5", 4:"Retornar ao menu princial"}
        self.possible_moves = {1:"pedra", 2:"papel", 3:"tesoura", 4:"cancelar partida"}

        self.player_score = 0
        self.computer_score = 0
        self.game_draws = 0

        self.player_score_best_of_3 = 0
        self.computer_score_best_of_3 = 0

        self.player_score_best_of_5 = 0
        self.computer_score_best_of_5 = 0

        self.user_data_file_path = "user_data.json"
        self.user_index = -1
        self.session_username = "visitor"
        

    def clear_terminal_input(self):
        os.system('cls||clear')

    def display_menu(self):
        self.clear_terminal_input()
        print(f"Bem vindo {self.session_username if self.session_username is not 'visitor' else 'Visitante'}!\n")
        print("JOKENPÔ\n")
        print("\n".join([f"{key} - {value}" for key,value in self.main_menu_options.items()]))
        print("\n")

    def display_username_list(self):
        with open(self.user_data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if len(data["users"])>0:
            usernames = [user["username"] for user in data["users"]]
            numbered_names = [f"{index} - {name}" for index, name in enumerate(usernames)]
            user_lst = "\n".join(numbered_names)
            print("Lista de usuáios existentes:")
            print(user_lst)
            print("\n")
        else:
            print("No momento não há nenhum usuário criado, seja o primeiro a criar um usuário!\n")
        

    # Checking if all characters are either numbers or letters
    # Return True if invalid characters are found
    def check_invalid_username_characters(self, username):
        for char in username:
            if not ((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122) or (ord(char) >= 48 and ord(char) <= 57)):
                return True
        return False
            
    def ask_for_username(self):
        menu_message = """Por favor, informe um nome de usuário.\nSe o nome já existir, os dados já existentes serão usados.\nSe o usuário ainda não existir, o usuário será criado.\n\nO nome de usuário deve conter de 4 a 20 letras e deve possuir somente letras e números:\nSe deseja retornar ao menu anterior, apenas pressione ENTER.\n"""
        while True:
            self.clear_terminal_input()
            print(menu_message)
            self.display_username_list()
            username = input()
            if not username:
                return ""
            if (len(username) < 4) or (len(username) > 20) or self.check_invalid_username_characters(username):
                print("Por favor, informe um nome de usuário válido! Pressione ENTER para tentar novamente:\n")
                input()
                continue
            return username

    def validate_user_session(self):
        max_menu_option = len(self.user_session_menu.keys())
        invalid_input_message = f"Por favor, informe um número de 1 a {max_menu_option}.\nPressione ENTER para tentar novamente."
        while True:
            self.clear_terminal_input()
            print("Bem vindo! Escolha como prosseguir\nSe escolher a opção de visitante, seus dados só serão armazenados durante essa sessão!")
            print("\n".join([f"{key} - {value}" for key,value in self.user_session_menu.items()]))
            option = input()
            if not option.isnumeric():
                print(invalid_input_message)
                input()
                option = 0
                continue
            option = int(option)
            if (option<1 or option>max_menu_option):
                print(invalid_input_message)
                input()
                option = 0
                continue
            return option

    def create_user_data(self, username, data):
        self.__init__()
        with open(self.user_data_file_path, "w", encoding="utf-8") as f:
            user_default_data_dict = {"username":username,
            "scores":[{
                "single_game":
                    {"player_score": 0,"computer_score": 0, "draws":0},
                "best_of_3":
                    {"player_score": 0, "computer_score": 0},
                "best_of_5":
                    {"player_score": 0,"computer_score": 0
                    }
                }]
            }
            data["users"].append(user_default_data_dict)
            json.dump(data, f)
        # User Index in Database
        self.user_index = len(data["users"]) - 1

    def load_user_data(self, username):
        with open(self.user_data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        flag_user_exists = False
        for index, user in enumerate(data["users"]):
            if user["username"] == username:
                flag_user_exists = True
                # Single Game Score
                self.player_score = user["scores"][0]["single_game"]["player_score"]
                self.computer_score = user["scores"][0]["single_game"]["computer_score"]
                self.game_draws = user["scores"][0]["single_game"]["draws"]
                # Best of 3
                self.player_score_best_of_3 = user["scores"][0]["best_of_3"]["player_score"]
                self.computer_score_best_of_3 = user["scores"][0]["best_of_3"]["computer_score"]
                # Best of 5
                self.player_score_best_of_5 = user["scores"][0]["best_of_5"]["player_score"]
                self.computer_score_best_of_5 = user["scores"][0]["best_of_5"]["computer_score"]
                # User Index in Database
                self.user_index = index
        if not flag_user_exists:
            self.create_user_data(username, data)
        # Username in Session
        self.session_username = username

    def initiate_user_session(self):
        option = self.validate_user_session()
        if option == 1:
            username = self.ask_for_username()
            if not username:
                return False
            self.load_user_data(username)
        else:
            self.__init__()
        return True
        
    def validate_menu_option(self):
        max_menu_option = len(self.main_menu_options.keys())
        invalid_input_message = f"Por favor, informe um número de 1 a {max_menu_option}.\nPressione ENTER para tentar novamente."
        while True:
            self.display_menu()
            option = input()
            if not option.isnumeric():
                print(invalid_input_message)
                input()
                option = 0
                continue
            option = int(option)
            if (option<1 or option>max_menu_option):
                print(invalid_input_message)
                input()
                option = 0
                continue
            return option
    
    def validate_user_move(self, game_mode, match_number=0):
        max_menu_option = len(self.possible_moves.keys())
        invalid_input_message = f"Por favor, informe um número de 1 a {max_menu_option}.\nPressione ENTER para tentar novamente."
        chose_message = "Escolha um movimento:\n" + "\n".join([f"{key} - {value}" for key,value in self.possible_moves.items()])
        game_mode_header = f"Modo de Jogo: {self.game_mode_options[game_mode]}"
        if self.game_mode_options[game_mode] != 1:
            game_mode_header += f" - Rodada {match_number}"
        while True:
            self.clear_terminal_input()
            print(game_mode_header)
            print(chose_message)
            user_move = input()
            if not user_move.isnumeric():
                print(invalid_input_message)
                input()
                user_move = 0
                continue
            user_move = int(user_move)
            if (user_move<1 or user_move>max_menu_option):
                print(invalid_input_message)
                input()
                user_move = 0
                continue
            # If user wants to CANCEL the match
            if user_move == max_menu_option:
                quit_confirmation = input("Cancelar a partida?! Digite 'sim' e pressione ENTER.\nSe deseja continuar, apenas pressione ENTER:\n")
                if quit_confirmation == "sim":
                    print("\nVocê CANCELOU a partida atual!\n")
                    return user_move
                continue
            return user_move
        
    def validate_game_mode(self):
        max_menu_option = len(self.game_mode_options.keys())
        invalid_input_message = f"Por favor, informe um número de 1 a {max_menu_option}.\nPressione ENTER para tentar novamente."
        chose_message = "Escolha um modo de jogo:\n" + "\n".join([f"{key} - {value}" for key,value in self.game_mode_options.items()])
        while True:
            self.clear_terminal_input()
            print(chose_message)
            user_move = input()
            if not user_move.isnumeric():
                print(invalid_input_message)
                input()
                user_move = 0
                continue
            user_move = int(user_move)
            if (user_move<1 or user_move>max_menu_option):
                print(invalid_input_message)
                input()
                user_move = 0
                continue
            return user_move

    # generating random computer movement
    def gen_random_move(self):
        return random.randrange(1,4,1)# start, stop(not inclusive), step

    def play(self, game_mode_option, match_number=0):
        ## Asking for User Move
        user_move = self.validate_user_move(game_mode_option, match_number)
        ## If CANCELING a match
        cancel_match = len(self.possible_moves.keys())
        if user_move == cancel_match:
            return cancel_match
        ## Generating Computer Move
        computer_move = self.gen_random_move()

        self.clear_terminal_input()
        played_moves = f"Seu movimento: {self.possible_moves[user_move]}\nMovimento do Computador: {self.possible_moves[computer_move]}\n"
        print("Resultado:")
        ## Winner Check Logic
        if user_move == computer_move:
            print("Empate!\n")
            print(played_moves)
            return 0
        ## pedra -> tesoura OU papel -> pedra OU tesoura -> papel
        elif (user_move == 1 and computer_move == 3) or (user_move == 2 and computer_move == 1) or (user_move == 3 and computer_move == 2):
            print(f"Parabéns! Você venceu! :D\n{self.possible_moves[user_move]} ganha de {self.possible_moves[computer_move]}\n")
            print(played_moves)
            return 1
        else:
            print(f"Você perdeu! :(\n{self.possible_moves[user_move]} perde para {self.possible_moves[computer_move]}\n")
            print(played_moves)
            return -1
        
    def show_local_statistics(self, number_of_games, local_player_score, local_cpu_score, result, n):
        print(f"Placar atual - Rodada {number_of_games}:")
        print(f"Jogador: {local_player_score}")
        print(f"Computador: {local_cpu_score}")
        if result == 0:
            print(f"OBS: Jogos que resultam em empate não são contabilizados em uma melhor de {n}!\n")
        print("\n")
        print("\nPressione ENTER para prosseguir")
        input()

    def play_best_of_n(self, n=3, game_mode_option=2):
        local_player_score = 0
        local_cpu_score = 0
        number_of_games = 1
        cancel_match = len(self.possible_moves.keys())
        win_threshold = math.ceil(n/2)
        while (number_of_games <= n) and not (local_player_score==win_threshold or local_cpu_score==win_threshold):
            result = self.play(game_mode_option, match_number=number_of_games)
            if result == cancel_match:
                return len(self.possible_moves.keys())
            if result == 1:
                local_player_score += 1
            if result == -1:
                local_cpu_score += 1
            self.show_local_statistics(number_of_games, local_player_score, local_cpu_score, result, n)
            if result != 0:
                number_of_games += 1

        self.clear_terminal_input()
        if local_player_score > local_cpu_score:
            print(f"Parabéns! Você venceu essa melhor de {n}!\n")
            return 1
        else:
            print(f"Você perdeu essa melhor de {n}! Mais sorte na próxima!\n")
            return -1
        
    def show_statistics(self, game_mode_to_show=-1):
        print("Placar atual dos modos de jogo:\n")
        if game_mode_to_show == 1 or game_mode_to_show == -1:
            total_number_of_games = self.player_score + self.computer_score + self.game_draws
            print("Jogos únicos:")
            print(f"Vitórias do Jogador: {self.player_score} | Porcentagem: {round(100*self.player_score/total_number_of_games,2)}%")
            print(f"Vitórias do Computador: {self.computer_score} | Porcentagem: {round(100*self.computer_score/total_number_of_games,2)}%")
            print(f"Empates: {self.game_draws} | Porcentagem: {round(100*self.game_draws/total_number_of_games,2)}%")
            print(f"Total de jogos: {total_number_of_games}")
            print("\n")
        if game_mode_to_show == 2 or game_mode_to_show == -1:
            total_number_of_games = self.player_score_best_of_3 + self.computer_score_best_of_3
            print("Melhor de 3:")
            print(f"Vitórias do Jogador: {self.player_score_best_of_3} | Porcentagem: {round(100*self.player_score_best_of_3/total_number_of_games,2)}%")
            print(f"Vitórias do Computador: {self.computer_score_best_of_3} | Porcentagem: {round(100*self.computer_score_best_of_3/total_number_of_games,2)}%")
            print(f"Total de jogos: {total_number_of_games}")
            print("\n")
        if game_mode_to_show == 3 or game_mode_to_show == -1:
            total_number_of_games = self.player_score_best_of_5 + self.computer_score_best_of_5
            print("Melhor de 5:")
            print(f"Vitórias do Jogador: {self.player_score_best_of_5} | Porcentagem: {round(100*self.player_score_best_of_5/total_number_of_games,2)}%")
            print(f"Vitórias do Computador: {self.computer_score_best_of_5} | Porcentagem: {round(100*self.computer_score_best_of_5/total_number_of_games,2)}%")
            print(f"Total de jogos: {total_number_of_games}")

        print("\nPressione ENTER para prosseguir")
        input()

    def save_game_state(self):
        with open(self.user_data_file_path, 'r+', encoding="utf-8") as f:
            data = json.load(f)

        with open(self.user_data_file_path, 'w', encoding="utf-8") as f:
            ## Updating the data
            data["users"][self.user_index]["scores"][0]["single_game"]["player_score"] = self.player_score
            data["users"][self.user_index]["scores"][0]["single_game"]["computer_score"] = self.computer_score
            data["users"][self.user_index]["scores"][0]["single_game"]["draws"] = self.game_draws

            data["users"][self.user_index]["scores"][0]["best_of_3"]["player_score"] = self.player_score_best_of_3
            data["users"][self.user_index]["scores"][0]["best_of_3"]["computer_score"] = self.computer_score_best_of_3

            data["users"][self.user_index]["scores"][0]["best_of_5"]["player_score"] = self.player_score_best_of_5
            data["users"][self.user_index]["scores"][0]["best_of_5"]["computer_score"] = self.computer_score_best_of_5

            ## Writing Changes
            json.dump(data, f)

    ## Here we update the player and computer scores with:
    ## 1  == Player Victory
    ## -1 == Computer Victory
    ## 0  == Draw (only applies to single games)
    def update_player_cpu_score(self, result, game_mode_option=1):
        if result == 0 and game_mode_option == 1:
            self.game_draws += 1
        if result == 1:
            if game_mode_option == 1:
                self.player_score += 1
            if game_mode_option == 2:
                self.player_score_best_of_3 += 1
            if game_mode_option == 3:
                self.player_score_best_of_5 += 1
        if result == -1:
            if game_mode_option == 1:
                self.computer_score += 1
            if game_mode_option == 2:
                self.computer_score_best_of_3 += 1
            if game_mode_option == 3:
                self.computer_score_best_of_5 += 1

        if self.session_username != "visitor":
            self.save_game_state()

    def start(self):
        # Checking if data backup file exists, it not, create it
        if not os.path.isfile(self.user_data_file_path):
            with open(self.user_data_file_path, 'w+', encoding="utf-8") as f:
                data = {"users":[]}
                json.dump(data, f)
        # Asking for username/visitor and loading existing user data if already exists
        while not self.initiate_user_session():
            continue
        quit_game = False
        while not quit_game:
            option = self.validate_menu_option()
            # Jogar
            if option==1:
                game_mode_option = -1
                while game_mode_option != len(self.game_mode_options.values()): # while not return to main menu
                    game_mode_option = self.validate_game_mode()
                    if game_mode_option == 1:
                        match_number = self.player_score + self.computer_score + self.game_draws
                        result = self.play(game_mode_option=1, match_number=match_number+1)
                        self.update_player_cpu_score(result, game_mode_option=1)
                        self.show_statistics(game_mode_to_show=1)
                    if game_mode_option == 2:
                        result = self.play_best_of_n(n=3, game_mode_option=2)
                        self.update_player_cpu_score(result, game_mode_option=2)
                        self.show_statistics(game_mode_to_show=2)
                    if game_mode_option == 3:
                        result = self.play_best_of_n(n=5, game_mode_option=3)
                        self.update_player_cpu_score(result, game_mode_option=3)
                        self.show_statistics(game_mode_to_show=3)
            # Estatísticas
            elif option==2:
                self.clear_terminal_input()
                self.show_statistics()
            # Entrar com Usuário / Trocar de Usuário
            elif option==3:
                while not self.initiate_user_session():
                    continue
            # Sair
            elif option==4:
                quit_confirmation = input("Realmente deseja sair do jogo?! Digite 'sim' e pressione enter:\n")
                if quit_confirmation == "sim":
                    print("Obrigado por jogar, até uma próxima!")
                    quit_game = True

def main():
    jokenpo = Jokenpo()
    jokenpo.start()

if __name__ == "__main__":
    main()
