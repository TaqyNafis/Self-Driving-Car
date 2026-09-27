from NeuralNetwork.network import NeuralNetwork

def mutate(brain, method="default", amount =1, rate = 1):
    if method == "default":
        NeuralNetwork.mutate(brain, amount, rate)
    else:
        raise ValueError(f"unknown mutation method: {method}")