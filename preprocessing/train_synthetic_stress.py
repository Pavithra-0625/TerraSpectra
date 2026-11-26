import h5py
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from model_3dcnn import TerraSpectra3DCNN

# Reproducibility
np.random.seed(42)
torch.manual_seed(42)

# Load synthetic data
with h5py.File('data/mock/crop_hyperspectral.h5', 'r') as f:
    cube = f['hyperspectral_cube'][:]
    mask = f['stress_mask'][:]

print('Cube shape:', cube.shape)
print('Mask shape:', mask.shape)

# Convert pixels into samples
y = mask.reshape(-1).astype(np.int64)

# Spatially separated split
# Training rows: 2 to 39
# Testing rows: 46 to 61
# Rows between them act as a safety gap.

train_rows = np.arange(2, 40)
test_rows = np.arange(46, 62)

train_idx = np.concatenate([
    np.arange(r * cube.shape[1], (r + 1) * cube.shape[1])
    for r in train_rows
])

test_idx = np.concatenate([
    np.arange(r * cube.shape[1], (r + 1) * cube.shape[1])
    for r in test_rows
])

# Prepare 5x5 spatial-spectral patches
padded = np.pad(
    cube,
    ((2, 2), (2, 2), (0, 0)),
    mode='reflect'
)

def get_patch(index):
    row, col = divmod(index, cube.shape[1])
    patch = padded[row:row+5, col:col+5, :]
    return patch.transpose(2, 0, 1)

X_train = np.stack([get_patch(i) for i in train_idx])
X_test = np.stack([get_patch(i) for i in test_idx])

# Convert to PyTorch tensors
X_train = torch.tensor(
    X_train[:, None, :, :, :], dtype=torch.float32
)
X_test = torch.tensor(
    X_test[:, None, :, :, :], dtype=torch.float32
)

y_train = torch.tensor(y[train_idx], dtype=torch.long)
y_test = torch.tensor(y[test_idx], dtype=torch.long)

# Check that both classes exist in each split
print('Training class counts:', np.bincount(y_train.numpy(), minlength=2))
print('Testing class counts:', np.bincount(y_test.numpy(), minlength=2))

if len(torch.unique(y_train)) < 2 or len(torch.unique(y_test)) < 2:
    raise ValueError('Both classes must be present in training and testing data.')

print('Training samples:', len(y_train))
print('Testing samples:', len(y_test))
print('Input batch shape:', tuple(X_train[:4].shape))

y_train = torch.tensor(y[train_idx], dtype=torch.long)
y_test = torch.tensor(y[test_idx], dtype=torch.long)

print('Training samples:', len(y_train))
print('Testing samples:', len(y_test))
print('Input batch shape:', tuple(X_train[:4].shape))

# DataLoaders
train_loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=16,
    shuffle=True
)

# Model
model = TerraSpectra3DCNN()

# Class weights for imbalanced labels
counts = np.bincount(y_train.numpy(), minlength=2)
weights = len(y_train) / (2.0 * counts)
criterion = nn.CrossEntropyLoss(
    weight=torch.tensor(weights, dtype=torch.float32)
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
epochs = 15

for epoch in range(epochs):
    model.train()
    total_loss = 0

    for xb, yb in train_loader:
        optimizer.zero_grad()
        outputs = model(xb)
        loss = criterion(outputs, yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(
        f'Epoch {epoch+1}/{epochs}, '
        f'Loss: {total_loss / len(train_loader):.4f}'
    )

# Evaluation
model.eval()
with torch.no_grad():
    outputs = model(X_test)
    predictions = outputs.argmax(dim=1).numpy()

actual = y_test.numpy()

print('\nSYNTHETIC STRESS CLASSIFICATION RESULTS')
print('Accuracy:', round(accuracy_score(actual, predictions), 4))
print('Precision:', round(precision_score(actual, predictions, zero_division=0), 4))
print('Recall:', round(recall_score(actual, predictions, zero_division=0), 4))
print('F1-score:', round(f1_score(actual, predictions, zero_division=0), 4))
print('Confusion matrix:')
print(confusion_matrix(actual, predictions))
print(classification_report(actual, predictions, zero_division=0))

# Save model
torch.save(
    model.state_dict(),
    'outputs/synthetic_stress_3dcnn.pth'
)

print('Model saved: outputs/synthetic_stress_3dcnn.pth')
print('NOTE: Results apply only to synthetic demonstration data.')
