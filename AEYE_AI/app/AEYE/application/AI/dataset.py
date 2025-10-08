from typing import List, Union

import torch
from PIL import Image
from torchvision import transforms

_imgnet_mean = (0.485, 0.456, 0.406)
_imgnet_std  = (0.229, 0.224, 0.225)

_preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(_imgnet_mean, _imgnet_std),
])

def pil_to_tensor(x: Union[Image.Image, torch.Tensor, List[Image.Image], List[torch.Tensor]]) -> torch.Tensor:

    if isinstance(x, torch.Tensor):
        return x.unsqueeze(0) if x.dim() == 3 else x

    if isinstance(x, Image.Image):
        t = _preprocess(x)
        return t.unsqueeze(0)

    if isinstance(x, list):
        tensors = []
        for item in x:
            if isinstance(item, Image.Image):
                tensors.append(_preprocess(item))
            elif isinstance(item, torch.Tensor):
                tensors.append(item if item.dim() == 3 else item.squeeze(0))
            else:
                raise TypeError(f"Unsupported type in list: {type(item)}")
        return torch.stack(tensors, dim=0)

    raise TypeError(f"Unsupported input type: {type(x)}")