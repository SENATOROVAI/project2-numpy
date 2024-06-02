import numpy as np

# Параметры задачи
A1 = 211
A2 = 335
B3 = 297
B4 = 43

costs = {
    'transport': [12640, 20244, 10830, 10194],
    'load_unload': [17000, 20000, 16000, 14000],
    'storage': [3000, 6000, 6000, 9000]
}

max_transport_A_to_B = 176
max_transport_B_to_A = 200

max_capacity = {
    'A3': 377,
    'A4': 66,
    'B1': 188,
    'B2': 316
}

# Инициализация таблицы DP
days = [4, 7, 21]
results = {}

for D in days:
    dp = np.full((D+1, A1+1, A2+1, B3+1, B4+1), np.inf)
    dp[0, 0, 0, 0, 0] = 0

    for d in range(1, D+1):
        for a1 in range(A1+1):
            for a2 in range(A2+1):
                for b3 in range(B3+1):
                    for b4 in range(B4+1):
                        for y_a1 in range(max(0, a1-max_transport_A_to_B), min(a1, max_transport_A_to_B)+1):
                            for y_a2 in range(max(0, a2-max_transport_A_to_B), min(a2, max_transport_A_to_B)+1):
                                for y_b3 in range(max(0, b3-max_transport_B_to_A), min(b3, max_transport_B_to_A)+1):
                                    for y_b4 in range(max(0, b4-max_transport_B_to_A), min(b4, max_transport_B_to_A)+1):
                                        x_a1 = a1 - y_a1
                                        x_a2 = a2 - y_a2
                                        x_b3 = b3 - y_b3
                                        x_b4 = b4 - y_b4

                                        if (x_a1 + x_a2 <= max_transport_A_to_B and 
                                            x_b3 + x_b4 <= max_transport_B_to_A and 
                                            x_b3 <= max_capacity['A3'] and 
                                            x_b4 <= max_capacity['A4'] and 
                                            x_a1 <= max_capacity['B1'] and 
                                            x_a2 <= max_capacity['B2']):

                                            cost = (costs['transport'][0] * y_a1 + costs['load_unload'][0] * y_a1 + costs['storage'][0] * (A1 - a1) +
                                                    costs['transport'][1] * y_a2 + costs['load_unload'][1] * y_a2 + costs['storage'][1] * (A2 - a2) +
                                                    costs['transport'][2] * y_b3 + costs['load_unload'][2] * y_b3 + costs['storage'][2] * (B3 - b3) +
                                                    costs['transport'][3] * y_b4 + costs['load_unload'][3] * y_b4 + costs['storage'][3] * (B4 - b4))

                                            dp[d, a1, a2, b3, b4] = min(dp[d, a1, a2, b3, b4], dp[d-1, x_a1, x_a2, x_b3, x_b4] + cost)

    min_cost = dp[D, A1, A2, B3, B4]
    results[D] = {'cost': min_cost, 'transports': []}

    a1, a2, b3, b4 = A1, A2, B3, B4
    for d in range(D, 0, -1):
        for y_a1 in range(max(0, a1-max_transport_A_to_B), min(a1, max_transport_A_to_B)+1):
            for y_a2 in range(max(0, a2-max_transport_A_to_B), min(a2, max_transport_A_to_B)+1):
                for y_b3 in range(max(0, b3-max_transport_B_to_A), min(b3, max_transport_B_to_A)+1):
                    for y_b4 in range(max(0, b4-max_transport_B_to_A), min(b4, max_transport_B_to_A)+1):
                        x_a1 = a1 - y_a1
                        x_a2 = a2 - y_a2
                        x_b3 = b3 - y_b3
                        x_b4 = b4 - y_b4

                        if (x_a1 + x_a2 <= max_transport_A_to_B and 
                            x_b3 + x_b4 <= max_transport_B_to_A and 
                            x_b3 <= max_capacity['A3'] and 
                            x_b4 <= max_capacity['A4'] and 
                            x_a1 <= max_capacity['B1'] and 
                            x_a2 <= max_capacity['B2']):

                            cost = (costs['transport'][0] * y_a1 + costs['load_unload'][0] * y_a1 + costs['storage'][0] * (A1 - a1) +
                                    costs['transport'][1] * y_a2 + costs['load_unload'][1] * y_a2 + costs['storage'][1] * (A2 - a2) +
                                    costs['transport'][2] * y_b3 + costs['load_unload'][2] * y_b3 + costs['storage'][2] * (B3 - b3) +
                                    costs['transport'][3] * y_b4 + costs['load_unload'][3] * y_b4 + costs['storage'][3] * (B4 - b4))

                            if dp[d, a1, a2, b3, b4] == dp[d-1, x_a1, x_a2, x_b3, x_b4] + cost:
                                results[D]['transports'].insert(0, (y_a1, y_a2, y_b3, y_b4))
                                a1, a2, b3, b4 = x_a1, x_a2, x_b3, x_b4
                                break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
            break

for D in days:
    print(f"Results for {D} days:")
    print(f"Total cost: {results[D]['cost']}")
    for d, transports in enumerate(results[D]['transports'], 1):
        print(f"Day {d}:")
        print(f"  Transport from A1: {transports[0]} wagons")
        print(f"  Transport from A2: {transports[1]} wagons")
        print(f"  Transport from B3: {transports[2]} wagons")
        print(f"  Transport from B4: {transports[3]} wagons")
    print("\n")