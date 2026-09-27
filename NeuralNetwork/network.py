import random
from Extra.utils import lerp

class NeuralNetwork:
    def __init__(self,neuronCounts):
        self.levels= []

        for i in range(len(neuronCounts)-1):
            self.levels.append(Level(
                neuronCounts[i],
                neuronCounts[i+1]
            ))
    def feedFoward(self,givenInputs):
        outputs = Level.feedFoward(
            givenInputs,self.levels[0])
        for i in range(1, len(self.levels)):
            outputs = Level.feedFoward(
                outputs, self.levels[i]
            )

        return outputs      

    def mutate(network, amount, rate):
        for level in network.levels:
            for i in range(len(level.biases)):
                if random.random < rate:
                    level.biases[i] = lerp(
                        level.biases[i],
                        random.random()* 2 - 1,
                        amount
                    )
            for i in range(len(level.weights)):
                for j in range(len(level.weights[i])):
                    if random.random < rate:
                        level.weights[i][j] = lerp(
                            level.weights[i][j],
                            random.random()* 2 - 1,
                            amount
                        )


class Level:
    def __init__ (self,inputCount, outputCount):
        self.inputs = [None] * inputCount
        self.outputs = [None] * outputCount
        self.biases = [None] * outputCount

        self.weights = []
        for i in range(inputCount ):
            self.weights.append([None] * outputCount)

        Level.randomize(self)

    @staticmethod
    def randomize(level):
        for i in range (len(level.inputs)):
            for j in range(len(level.outputs)):
                level.weights[i][j] = random.random()*2-1

        for i in range(len(level.biases)):
            level.biases[i] = random.random() * 2-1

    # set value from all sensors into input
    def feedFoward(givenInputs,self):
        for i in range(len(self.inputs)):
            self.inputs[i] = givenInputs[i]

        #to get output => Sum of(W(ji)xi)  
        for i in range(len(self.outputs)):
            sum = 0
            for j in range(len(self.inputs)):
                sum+= self.inputs[j]*self.weights[j][i]

            #neuron activation function
            # if higher than bias activates, if lower neuron does not active
            #if sum> sum+self.biases[i]>0 also work (more scientist use it) == result will be weirder function and need more complex function to process it
            # line equation = Weight * input  + Bias = 0
            if sum >self.biases[i]:
                self.outputs[i] = 1
            else:
                self.outputs[i]=0

        return self.outputs
    

