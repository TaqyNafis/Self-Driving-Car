from network import NeuralNetwork

def mutate(brain, method="default", amount = 0.2):
    if method == "default":
        NeuralNetwork.mutate(brain, amount)
    else:
        raise ValueError(f"unknown mutation method: {method}")