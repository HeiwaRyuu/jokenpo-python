import random
import os

class Jokenpo:
    """Classe para instanciar o jogo"""
    def __init__(self):
        self.main_menu_options = {1:"Jogar", 2:"Sair", 3:"Estatísticas"}
        self.possible_moves = {1:"pedra", 2:"papel", 3:"tesoura"}
        self.player_score = 0
        self.computer_score = 0

    def clear_terminal_input(self):
        os.system('cls||clear')

    def display_menu(self):
        self.clear_terminal_input()
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

    # generating random computer movement
    def gen_random_move(self):
        return random.randrange(1,4,1)# start, stop(not inclusive), step

    def play(self):
        ## Asking for User Move
        user_move = self.validate_user_move()
        ## Generating Computer Move
        computer_move = self.gen_random_move()

        self.clear_terminal_input()
        print(f"Seu movimento: {self.possible_moves[user_move]}\nMovimento do Computador: {self.possible_moves[computer_move]}")
        ## Winner Check Logic
        if user_move == computer_move:
            print("Empate!")
        ## pedra -> tesoura OU papel -> pedra OU tesoura -> papel
        elif (user_move == 1 and computer_move == 3) or (user_move == 2 and computer_move == 1) or (user_move == 3 and computer_move == 2):
            print(f"Parabéns! Você venceu! :D\n{self.possible_moves[user_move]} ganha de {self.possible_moves[computer_move]}")
            self.player_score += 1
        else:
            print(f"Você perdeu! :(\n{self.possible_moves[user_move]} perde para {self.possible_moves[computer_move]}")
            self.computer_score += 1
        
        self.show_statistics()
        
    def show_statistics(self):
        print("\nPlacar atual:")
        print(f"Jogador: {self.player_score}")
        print(f"Computador: {self.computer_score}")
        print("Pressione qualquer tecla para prosseguir")
        input()

    def start(self):
        quit_game = False
        while not quit_game:
            option = self.validate_menu_option()
            # Jogar
            if option==1:
                self.play()
            # Sair
            elif option==2:
                quit_confirmation = input("Realmente deseja sair do jogo?! Digite 'sim' e pressione enter:\n")
                if quit_confirmation == "sim":
                    print("Obrigado por jogar, até uma próxima!")
                    quit_game = True
            # Estatísticas
            elif option==3:
                self.clear_terminal_input()
                self.show_statistics()

def main():
    jokenpo = Jokenpo()
    jokenpo.start()

if __name__ == "__main__":
    main()