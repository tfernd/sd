from __future__ import annotations
from typing import Optional

import torch.nn as nn
from torch import Tensor

from .cross_attention import CrossAttention
from .feed_forward import FeedForward


class BasicTransformer(nn.Module):
    def __init__(
        self,
        *,
        dim: int,
        num_heads: int,
        dim_head: int,
        context_dim: Optional[int],
    ):
        super().__init__()

        self.dim = dim
        self.num_heads = num_heads
        self.dim_head = dim_head
        self.context_dim = context_dim

        self.attn1 = CrossAttention(
            query_dim=dim,
            num_heads=num_heads,
            dim_head=dim_head,
            context_dim=None,
        )
        self.attn2 = CrossAttention(
            query_dim=dim,
            num_heads=num_heads,
            dim_head=dim_head,
            context_dim=context_dim,
        )

        self.ff = FeedForward(dim, dim_out=None, mult=4)

    def forward(
        self, x: Tensor, *, context: Optional[Tensor] = None,
    ) -> Tensor:
        x = self.attn1(x)
        x = self.attn2(x, context=context)
        del context
        x = self.ff(x)

        return x
