
import os
import gc
import time
import psutil
import torch
from torch.utils.data import DataLoader
from pytorch_dataset import HyperSpectralDataset

process = psutil.Process(os.getpid())

def ram_usage():
    return process.memory_info().rss / (1024 ** 2)

def run_memory_test(batch_size):

    gc.collect()

    print("\nBatch size:", batch_size)

    start_ram = ram_usage()
    peak_ram = start_ram
    start_time = time.time()

    dataset = HyperSpectralDataset()

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0
    )

    batches = 0

    for batch in loader:
        batches += 1

        current_ram = ram_usage()
        peak_ram = max(peak_ram, current_ram)

        del batch

    end_time = time.time()

    print("Images processed:", len(dataset))
    print("Batches processed:", batches)
    print("Starting RAM:", round(start_ram, 2), "MB")
    print("Peak RAM:", round(peak_ram, 2), "MB")
    print("RAM increase:", round(peak_ram - start_ram, 2), "MB")
    print("Processing time:", round(end_time - start_time, 2), "seconds")

    del loader, dataset
    gc.collect()


print("===== TERRASPECTRA MEMORY PROFILING =====")

for size in [2, 4, 8]:
    run_memory_test(size)

print("\n===== MEMORY TEST COMPLETED =====")
