from __future__ import annotations
from typing import Optional

from torch import Tensor

try:
    from xformers.ops import memory_efficient_attention  # type: ignore
except ImportError:
    memory_efficient_attention = None


def flash_attention(
    q: Tensor,  # (B, heads, T, C)
    k: Tensor,  # (B, heads, T', C)
    v: Tensor,  # (B, heads, T', C)
    bias: Optional[Tensor] = None,  # (B, heads, T', C)
) -> Tensor:
    """xformers flash-attention computation."""

    raise NotImplementedError

    assert memory_efficient_attention is not None

    q = q.contiguous()
    k = k.contiguous()
    v = v.contiguous()

    return memory_efficient_attention(q, k, v, bias)
