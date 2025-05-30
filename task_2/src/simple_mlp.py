import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, activation='relu'):
        super(SimpleMLP, self).__init__()

        self.hidden = nn.Linear(input_size, hidden_size)
        self.output = nn.Linear(hidden_size, output_size)

        if activation == 'relu':
            self.activation = F.relu
        elif activation == "sigmoid":
            self.activation = torch.sigmoid
        elif activation == "tanh":
            self.activation = torch.tanh
        else:
            raise ValueError(f"Unsupported activation: {activation}")

    def forward(self, x):
        x = self.activation(self.hidden(x))
        return self.output(x)