import torch

def normalize(x):
    return (x - torch.min(x).item())/(torch.max(x).item() - torch.min(x).item())

tensor = torch.Tensor([[1, 2, 3],
                       [7, 3, 9],
                       [1, 2, 100]])
print(torch.nn.functional.normalize(tensor))