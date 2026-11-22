
"""
TerraSpectra - PyTorch Hyperspectral Dataset
Loads PCA-reduced images as PyTorch tensors.
"""

from pathlib import Path
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


PCA_DIR = Path("data/processed/shared_pca")
IMAGE_LIST = Path("outputs/reports/selected_1000_images.txt")


class HyperSpectralDataset(Dataset):

    def __init__(self):
        self.image_names = IMAGE_LIST.read_text().splitlines()

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, index):

        image_name = self.image_names[index]
        image_path = PCA_DIR / f"{Path(image_name).stem}_pca.npy"

        image = np.load(image_path).astype(np.float32)

        # Convert to PyTorch tensor.
        tensor = torch.from_numpy(image)

        # Add channel dimension for 3D CNN.
        tensor = tensor.unsqueeze(0)

        return tensor


if __name__ == "__main__":

    dataset = HyperSpectralDataset()

    loader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=False,
        num_workers=0
    )

    print("===== TERRASPECTRA PYTORCH DATASET =====")
    print("Total images:", len(dataset))

    batch = next(iter(loader))

    print("Batch shape:", tuple(batch.shape))
    print("Data type:", batch.dtype)

    memory_mb = batch.nelement() * batch.element_size() / (1024 ** 2)

    print("Batch memory:", round(memory_mb, 2), "MB")
    print("========================================")
