
"""
TerraSpectra - Vision Transformer (ViT)
Processes PCA-reduced hyperspectral images.
Input: (batch, 1, 20, 48, 352)
"""

import torch
import torch.nn as nn


class TerraSpectraViT(nn.Module):

    def __init__(self):
        super().__init__()

        # Convert image patches into embeddings.
        self.patch_embedding = nn.Conv2d(
            20, 64,
            kernel_size=8,
            stride=8
        )

        # Transformer encoder.
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=64,
            nhead=4,
            dim_feedforward=128,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=2
        )

        self.classifier = nn.Linear(64, 2)

    def forward(self, x):

        # Remove the single input channel.
        x = x.squeeze(1)

        # Patch embedding.
        x = self.patch_embedding(x)

        # Flatten spatial patches.
        x = x.flatten(2).transpose(1, 2)

        # Transformer processing.
        x = self.transformer(x)

        # Average patch features.
        x = x.mean(dim=1)

        return self.classifier(x)


if __name__ == "__main__":

    model = TerraSpectraViT()

    sample = torch.randn(4, 1, 20, 48, 352)

    output = model(sample)

    print("===== TERRASPECTRA VISION TRANSFORMER =====")
    print("Input shape:", tuple(sample.shape))
    print("Output shape:", tuple(output.shape))
    print(
        "Number of parameters:",
        sum(p.numel() for p in model.parameters())
    )
    print("Model test: SUCCESS")
    print("===========================================")
