from websocket_server import WebsocketServer
from lands import *
from euler import *

servidor = WebsocketServer(port=6660)
passou = 0
output = 0.0
count = 0
previous_level = 0

def convert_message(message):
    # Pega a mensagem recebida e separa ela para ser tratada e utilizada
    wins = int(message[0])
    land = int(message[1])
    level = int(message[2])
    player = message[3], message[4]
    target = message[5], message[6]
    bonus, skulls = [], []

    if(len(message) > 8):
        bonus.append((message[7], message[8]))
    if(len(message) > 10):
        bonus.append((message[9], message[10]))
    if(len(message) > 12):
        bonus.append((message[11], message[12]))
        for i in range(13, len(message), 2):
            skulls.append((message[i], message[i+1]))
    # Converte a mensagem em uma lista de valores
    return wins, land, level, player, target, bonus, skulls

def client(client, server):
    # Envia uma mensagem ao cliente com valor 0 quando um novo cliente se conecta ao servidor
    server.send_message(client, str(0))

def message_received(client, server, message):
    global output
    global count
    global previous_level
    global passou

    # Separa a message na string values utilizando split
    values = [float(x) for x in message[:-1].split(",") if x.strip()]
    wins, land, level, player, target, bonus, skulls = convert_message(values)

    # verifica se passou de fase
    if previous_level != level:
        print("Quantidade de fases passadas:", passou)
        previous_level = level
        passou += 1
        output = 0

    # Calcula os valores das constantes `k` que são usadas para calcular a melhor direção para o jogador se mover
    k = define_maps_equations(land, level, 0, 0, 0, False)
    SkullsX = []
    SkullsY = []
    GoalsX = []
    GoalsY = []
    GoalsX.append(target[0])
    GoalsY.append(target[1])
    quant = 25
    dt = 0.01

    # Calcula as distâncias entre o jogador, o alvo, os bônus e os crânios
    if(len(bonus) >= 1 and level != 3):
        GoalsX.append(bonus[0][0])
        GoalsY.append(bonus[0][1])
        if(len(bonus) >= 2):
            GoalsX.append(bonus[1][0])
            GoalsY.append(bonus[1][1])
            if(len(bonus) >= 3):
                GoalsX.append(bonus[2][0])
                GoalsY.append(bonus[2][1])
    if(len(skulls) >= 1):
        SkullsX.append(skulls[0][0])
        SkullsY.append(skulls[0][1])
        if(len(skulls) >= 2):
            SkullsX.append(skulls[1][0])
            SkullsY.append(skulls[1][1])
            if(len(skulls) >= 3):
                SkullsX.append(skulls[2][0])
                SkullsY.append(skulls[2][1])
    # Calcula a melhor direção para o jogador se mover
    output = output + (k)*calculate_distances(player[0], player[1], land, level, quant, dt, GoalsX, GoalsY, SkullsX, SkullsY)
    # Se o valor da saída for maior ou igual a 1, normaliza-o para o intervalo [-1, 1]
    if abs(output) >= 1:
        output = (output/abs(output))

    # Envia uma resposta ao cliente com a saída da função `calculate_distances`
    server.send_message(client, str(output))

# Inicia o servidor
servidor.set_fn_new_client(client)
servidor.set_fn_message_received(message_received)
servidor.run_forever()
