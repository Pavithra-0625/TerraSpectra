
"""
TerraSpectra - 3D CNN Architecture
Input: (batch, 1, 20, 48, 352)
"""

import torch
import torch.nn as nn


class TerraSpectra3DCNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(

            nn.Conv3d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2)),

            nn.Conv3d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2)),

            nn.AdaptiveAvgPool3d((1, 1, 1))
        )

        self.classifier = nn.Linear(16, 2)

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)


if __name__ == "__main__":

    model = TerraSpectra3DCNN()

    # Create a sample batch.
    sample = torch.randn(4, 1, 20, 48, 352)

    output = model(sample)

    print("===== TERRASPECTRA 3D-CNN =====")
    print("Input shape:", tuple(sample.shape))
    print("Output shape:", tuple(output.shape))
    print("Number of parameters:", sum(p.numel() for p in model.parameters()))
    print("Model test: SUCCESS")
    print("===============================")
