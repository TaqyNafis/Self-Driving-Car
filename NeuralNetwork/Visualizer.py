import pygame

class NetworkVisualizer:
  
        def __init__(self,brain, track_width):
            self.brain = brain
            self.track_width = track_width

        def get_node_positions(self, layer_index):
            positions = []

            if layer_index == 0:
                  node_count = len(self.brain.levels[0].inputs)
            else:
                 node_count = len(self.brain.levels[layer_index - 1].outputs)

            for i in range(node_count):
                x = self.track_width + layer_index * 200
                y = 300 + (i-(node_count - 1)/2)* 75
                positions.append((x, y))

            return positions

        def draw_nodes(self, win, layer_index, positions):
            if layer_index == 0:
                values = self.brain.levels[0].inputs
            else:
                values = self.brain.levels[layer_index - 1].outputs

            for i in range(len(positions)):
                value = values[i]

                if value > 0 :
                    node_color = (0,200, 0)
                else:
                    node_color = (200,0,0)
                pygame.draw.circle(
                    win,
                    node_color,
                    positions[i],
                    20
                )

        def draw_connections(self, win, level, input_position, output_position):
            for i in range(len(input_position)):
                for j in range(len(output_position)):

                    weight = level.weights[i][j]

                    if weight>0:
                        line_color = (0,200,0)
                    else:
                         line_color = (200, 0, 0)

                    line_width = max(1, int(abs(weight)*5))

                    pygame.draw.line(
                        win,
                        line_color,
                        input_position[i],
                        output_position[j],
                        line_width
                    )
             

        def draw(self,win):

            layer_count = len(self.brain.levels) + 1

            for i in range (layer_count - 1):
                input_positions = self.get_node_positions(i)
                output_positions = self.get_node_positions(i+1)

                self.draw_connections(
                      win,
                      self.brain.levels[i],
                      input_positions,
                      output_positions
                )

            for i in range(layer_count):
                positions = self.get_node_positions(i)
                self.draw_nodes(
                    win,
                    i,
                    positions
                )