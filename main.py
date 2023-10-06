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
    return wins, land, level, player, target, bonus, skulls

def client(client, server):
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
        passou += 1
        previous_level = level
        output = 0

    # chama função para obter os valores de K
    k = define_maps_equations(land, level, 0, 0, 0, False)
    SkullsX = []
    SkullsY = []
    BonusX = []
    BonusY = []
    BonusX.append(target[0])
    BonusY.append(target[1])
    quant = 20
    dt = 0.01
    if(len(bonus) >= 1 and level != 3):
        BonusX.append(bonus[0][0])
        BonusY.append(bonus[0][1])
        if(len(bonus) >= 2):
            BonusX.append(bonus[1][0])
            BonusY.append(bonus[1][1])
            if(len(bonus) >= 3):
                BonusX.append(bonus[2][0])
                BonusY.append(bonus[2][1])
    if(len(skulls) >= 1):
        SkullsX.append(skulls[0][0])
        SkullsY.append(skulls[0][1])
        if(len(skulls) >= 2):
            SkullsX.append(skulls[1][0])
            SkullsY.append(skulls[1][1])
            if(len(skulls) >= 3):
                SkullsX.append(skulls[2][0])
                SkullsY.append(skulls[2][1])
    output = output + (k)*calculate_distances(player[0], player[1], land, level, quant, dt, BonusX, BonusY, SkullsX, SkullsY)
    if abs(output) >= 1:
        output = (output/abs(output))

    server.send_message(client, str(output))

servidor.set_fn_new_client(client)
servidor.set_fn_message_received(message_received)
servidor.run_forever()
