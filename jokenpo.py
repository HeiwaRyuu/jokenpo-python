import random
import os
import json
import math

class Jokenpo:
    """Classe para instanciar o jogo"""
    def __init__(self):
        self.main_menu_options = {1:"Jogar", 2:"Entrar com Usuário", 3:"Estatísticas", 4:"Sair"}
        self.game_mode_options = {1:"Uma partida", 2:"Melhor de 3", 3:"Melhor de 5", 4:"Retornar ao menu princial"}
        self.possible_moves = {1:"pedra", 2:"papel", 3:"tesoura"}
        self.player_score = 0
        self.computer_score = 0
        self.player_score_best_of_3 = 0
        self.computer_score_best_of_3 = 0
        self.player_score_best_of_5 = 0
        self.computer_score_best_of_5 = 0
        self.user_data_file_path = "user_data.json"
        self.session_username = "visitor"

    def clear_terminal_input(self):
        os.system('cls||clear')

    def display_menu(self):
        self.clear_terminal_input()
        print(f"Bem vindo {self.session_username}!")
        print("JOKENPÔ")
        print("\n".join([f"{key} - {value}" for key,value in self.main_menu_options.items()]))

    def validate_menu_option(self):
        invalid_input_message = "Por favor, informe um número de 1 a 3"
        while True:
            self.display_menu()
            option = input()
            if not option.isnumeric():
                print(invalid_input_message)
                option = 0
                continue
            option = int(option)
            if (option<1 or option>len(self.main_menu_options.keys())):
                print(invalid_input_message)
                option = 0
                continue
            return option
    
    def validate_user_move(self):
        invalid_input_message = "Por favor, informe um número de 1 a 3"
        chose_message = "Escolha um movimento:\n" + "\n".join([f"{key} - {value}" for key,value in self.possible_moves.items()])
        while True:
            self.clear_terminal_input()
            print(chose_message)
            user_move = input()
            if not user_move.isnumeric():
                print(invalid_input_message)
                user_move = 0
                continue
            user_move = int(user_move)
            if (user_move<1 or user_move>3):
                print(invalid_input_message)
                user_move = 0
                continue
            return user_move
        
    def validate_game_mode(self):
        max_menu_option = len(self.game_mode_options)
        invalid_input_message = f"Por favor, informe um número de 1 a {max_menu_option}"
        chose_message = "Escolha um modo de jogo:\n" + "\n".join([f"{key} - {value}" for key,value in self.game_mode_options.items()])
        while True:
            self.clear_terminal_input()
            print(chose_message)
            user_move = input()
            if not user_move.isnumeric():
                print(invalid_input_message)
                user_move = 0
                continue
            user_move = int(user_move)
            if (user_move<1 or user_move>max_menu_option):
                print(invalid_input_message)
                user_move = 0
                continue
            return user_move

    # generating random computer movement
    def gen_random_move(self):
        return random.randrange(1,4,1)# start, stop(not inclusive), step

    def play(self):
        ## Asking for User Move
        user_move = self.validate_user_move()
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
        print(f"Placar atual - Partida {number_of_games}:")
        print(f"Jogador: {local_player_score}")
        print(f"Computador: {local_cpu_score}")
        if result == 0:
            print(f"OBS: Jogos que resultam em empate não são contabilizados em uma melhor de {n}!\n")
        print("\n")
        print("\nPressione qualquer tecla para prosseguir")
        input()

    def play_best_of_n(self, n=3):
        local_player_score = 0
        local_cpu_score = 0
        number_of_games = 1
        win_threshold = math.ceil(n/2)
        while (number_of_games <= n) and not (local_player_score==win_threshold or local_cpu_score==win_threshold):
            result = self.play()
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
        
    def display_username_list(self):
        with open("user_data.json", "r") as f:
            data = json.load(f)
        names = [user['username'] for user in data]
        names.sort()
        numbered_names = [f"{index} - {name}" for index, name in enumerate(names)]
        user_lst = "\n".join(numbered_names)
        print("Lista de usuáios existentes:")
        print(user_lst)
        print("\n")

    def enter_with_username(self):
        self.display_username_list()
        print("Por favor, informe o nome de usuário, se o nome não estiver na lista, ele será criado:")
        username = input()
        
    def show_statistics(self, game_mode_to_show=-1):
        print("Placar atual:")
        if game_mode_to_show == 1 or game_mode_to_show == -1:
            print(f"Jogador: {self.player_score}")
            print(f"Computador: {self.computer_score}")
            print("\n")
        if game_mode_to_show == 2 or game_mode_to_show == -1:
            print("Melhor de 3:")
            print(f"Jogador: {self.player_score_best_of_3}")
            print(f"Computador: {self.computer_score_best_of_3}")
            print("\n")
        if game_mode_to_show == 3 or game_mode_to_show == -1:
            print("Melhor de 5:")
            print(f"Jogador: {self.player_score_best_of_5}")
            print(f"Computador: {self.computer_score_best_of_5}")

        print("\nPressione qualquer tecla para prosseguir")
        input()

    def update_player_cpu_score(self, result, game_mode_option=1):
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

    def start(self):
        if not os.path.isfile(self.user_data_file_path):
            open(self.user_data_file_path, 'a').close()
        
        quit_game = False
        while not quit_game:
            option = self.validate_menu_option()
            # Jogar
            if option==1:
                game_mode_option = -1
                while game_mode_option != len(self.game_mode_options.values()): # while not return to main menu
                    game_mode_option = self.validate_game_mode()
                    if game_mode_option == 1:
                        result = self.play()
                        self.update_player_cpu_score(result, game_mode_option=1)
                        self.show_statistics(game_mode_to_show=1)
                    if game_mode_option == 2:
                        result = self.play_best_of_n(n=3)
                        self.update_player_cpu_score(result, game_mode_option=2)
                        self.show_statistics(game_mode_to_show=2)
                    if game_mode_option == 3:
                        result = self.play_best_of_n(n=5)
                        self.update_player_cpu_score(result, game_mode_option=3)
                        self.show_statistics(game_mode_to_show=3)
            # Entrar com Usuário
            elif option==2:
                self.clear_terminal_input()
                self.enter_with_username()
            # Estatísticas
            elif option==3:
                self.clear_terminal_input()
                self.show_statistics()
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