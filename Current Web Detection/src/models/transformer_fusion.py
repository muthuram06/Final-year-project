import torch
import torch.nn as nn


class TransformerFusionModel(nn.Module):

    def __init__(self, input_dim=4, model_dim=32, num_heads=4, num_layers=2):

        super().__init__()

        self.embedding = nn.Linear(input_dim, model_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=model_dim,
            nhead=num_heads,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.classifier = nn.Sequential(
            nn.Linear(model_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):

        x = self.embedding(x)
        x = self.transformer(x)

        # Use last token representation
        x = x[:, -1, :]

        output = self.classifier(x)

        return output