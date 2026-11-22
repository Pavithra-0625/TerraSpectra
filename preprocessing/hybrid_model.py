
"""
TerraSpectra - Hybrid 3D-CNN + Transformer
Input: (batch, 1, 20, 48, 352)
"""

import torch
import torch.nn as nn


class TerraSpectraHybrid(nn.Module):

    def __init__(self):
        super().__init__()

        # 3D-CNN feature extraction
        self.cnn = nn.Sequential(
            nn.Conv3d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2)),

            nn.Conv3d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool3d((1, 1, 1))
        )

        # Transformer feature learning
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=16,
            nhead=4,
            dim_feedforward=32,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=2
        )

        # Classification head
        self.classifier = nn.Linear(16, 2)

    def forward(self, x):

        x = self.cnn(x)

        # Convert CNN features into a sequence.
        x = x.flatten(2).transpose(1, 2)

        x = self.transformer(x)

        x = x.mean(dim=1)

        return self.classifier(x)


if __name__ == "__main__":

    model = TerraSpectraHybrid()

    sample = torch.randn(4, 1, 20, 48, 352)

    output = model(sample)

    print("===== TERRASPECTRA HYBRID MODEL =====")
    print("Input shape:", tuple(sample.shape))
    print("Output shape:", tuple(output.shape))
    print(
        "Number of parameters:",
        sum(p.numel() for p in model.parameters())
    )
    print("Model test: SUCCESS")
    print("=====================================")
