import numpy as np
import torch
import matplotlib.pyplot as plt
import torch.nn as nn

import random
import csv
import itertools

import src.utils as utils
from src.simple_mlp import SimpleMLP

"""-------------------------------- PRZYGOTOWANIE DANYCH --------------------------------"""
"""wczytujemy nasze dane (dane uczace i testowe oddzielnie)"""
stat_f8 = utils.load_data("../data/f8/stat")
stat_f10 = utils.load_data("../data/f10/stat")
train_data = np.vstack([stat_f8, stat_f10])

dyn_f8 = utils.load_data("../data/f8/dyn")
dyn_f10 = utils.load_data("../data/f10/dyn")
test_data = np.vstack([dyn_f8, dyn_f10])

"""skalowanie danych (na podstawie parametrow ustalonych tylko na zbiorze uczacym, ale stosowane do obu zbiorow)"""
train_data_scaled, test_data_scaled = utils.scale_data(train_data, test_data)
# print(train_data[:5])
# print(train_data_scaled[:5])

"""dzielimy na dane wejsca 'X' i wyjscia 'Y' """
X_train_np = train_data_scaled[:, :2]
Y_train_np = train_data_scaled[:, 2:]
X_test_np = test_data_scaled[:, :2]
Y_test_np = test_data_scaled[:, 2:]

"""konwersja do tensorow PyTorch"""
X_train = torch.tensor(X_train_np, dtype=torch.float32)
Y_train = torch.tensor(Y_train_np, dtype=torch.float32)
X_test = torch.tensor(X_test_np, dtype=torch.float32)
Y_test = torch.tensor(Y_test_np, dtype=torch.float32)

menu_input = None
while menu_input != 0:
    print("=====================MENU=====================")
    print(" [1] Stwórz model i przeprowadź eksperyment.")
    print(" [2] Część badawcza zautomatyzowana.")
    print(" [0] EXIT")
    menu_input = int(input("> "))
    while menu_input not in [0,1,2]:
        menu_input = int(input("> "))
    print("----------------------------------------------")

    if menu_input == 1:
        neuron_hidden_amount = int(input("(~) Podaj liczbe neuronów w wastwie ukrytej: "))
        print()

        print("(~) Wybierz funkcję aktywacji w warstwie ukrytej:")
        print(" [1] funkcja logistyczna")
        print(" [2] tangens hiperboliczny")
        print(" [3] jednostronnie obcięta funkcja liniowa (ReLu)")
        activation_func_number = int(input(" (input): "))
        while activation_func_number not in [1, 2, 3]:
            activation_func_number = int(input(" (input): "))
        print()
        activation_func = None
        if activation_func_number == 1:
            activation_func = 'sigmoid'
        elif activation_func_number == 2:
            activation_func = 'tanh'
        elif activation_func_number == 3:
            activation_func = 'relu'

        model = SimpleMLP(input_size=2, hidden_size=neuron_hidden_amount, output_size=2, activation=activation_func)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        #TODO: add learning_rate and epoch_count as input from user (lets say user can choose if he wants to give
        # those parameters)

        epochs = 100
        train_losses = []
        test_losses = []

        for epoch in range(epochs):
            y_pred = model(X_train)
            loss = criterion(y_pred, Y_train)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            with torch.no_grad():
                y_test_pred = model(X_test)
                test_loss = criterion(y_test_pred, Y_test)

            train_losses.append(loss.item())
            test_losses.append(test_loss.item())

            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}, Train MSE: {loss.item():.5f}, Test MSE: {test_loss.item():.5f}")

        plt.plot(train_losses, label='Train MSE')
        plt.plot(test_losses, label='Test MSE')
        plt.xlabel('Epoch')
        plt.ylabel('Mean Squared Error')
        plt.legend()
        plt.title('Train vs Test MSE')
        plt.grid(True)
        plt.show()

    elif menu_input == 2:
        def set_seed(seed):
            torch.manual_seed(seed)
            np.random.seed(seed)
            random.seed(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False


        activation_funcs = ["sigmoid", "tanh", "relu"]
        hidden_sizes = [10, 30, 50]
        seeds = [42, 123, 999]
        epochs = 100

        results = []

        for activation, hidden_size in itertools.product(activation_funcs, hidden_sizes):
            best_test_loss = float("inf")
            best_seed = None
            best_train_losses = []
            best_test_losses = []

            for seed in seeds:
                set_seed(seed)
                model = SimpleMLP(input_size=2, hidden_size=hidden_size, output_size=2, activation=activation)
                optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
                criterion = nn.MSELoss()

                train_losses = []
                test_losses = []

                for epoch in range(epochs):
                    y_pred = model(X_train)
                    loss = criterion(y_pred, Y_train)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    with torch.no_grad():
                        y_test_pred = model(X_test)
                        test_loss = criterion(y_test_pred, Y_test)

                    train_losses.append(loss.item())
                    test_losses.append(test_loss.item())

                if test_loss.item() < best_test_loss:
                    best_test_loss = test_loss.item()
                    best_seed = seed
                    best_train_losses = train_losses.copy()
                    best_test_losses = test_losses.copy()

            print(f"[{activation.upper()}] Ukryte: {hidden_size}, Test MSE: {best_test_loss:.5f}, Seed: {best_seed}")
            results.append([activation, hidden_size, best_test_loss, best_seed])

            # Wykres dla najlepszego egzemplarza
            plt.plot(best_train_losses, label='Train MSE')
            plt.plot(best_test_losses, label='Test MSE')
            plt.xlabel('Epoch')
            plt.ylabel('Mean Squared Error')
            plt.legend()
            plt.title(f'Aktywacja: {activation}, Ukryte: {hidden_size}, Seed: {best_seed}')
            plt.grid(True)
            plt.show()

        # Zapisz wyniki do pliku CSV
        with open("badania_wyniki.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Aktywacja", "Neurony", "Najlepszy Test MSE", "Seed"])
            writer.writerows(results)

        print("✔ Zakończono badania. Wyniki zapisano w 'badania_wyniki.csv'.")
