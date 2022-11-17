from __future__ import annotations

import torch.nn.functional as F
from torch import Tensor

from ..base import Module
from ..basic import Linear


class GEGLU(Module):
    def __init__(self, dim_in: int, dim_out: int) -> None:
        super().__init__()

        self.dim_in = dim_in
        self.dim_out = dim_out

        self.proj = Linear(dim_in, 2 * dim_out)

    def __call__(self, x: Tensor) -> Tensor:
        x, gate = self.proj(x).chunk(2, dim=-1)

        return F.gelu(gate).mul_(x)
