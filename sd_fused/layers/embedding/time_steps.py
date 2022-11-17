from __future__ import annotations

import math

import torch
from torch import Tensor

from ..base import Module


class Timesteps(Module):
    freq: Tensor
    amplitude: Tensor
    phase: Tensor

    def __init__(
        self,
        *,
        num_channels: int,
        flip_sin_to_cos: bool,
        downscale_freq_shift: float,
        scale: float = 1,
        max_period: int = 10_000,
    ) -> None:
        super().__init__()

        self.num_channels = num_channels
        self.flip_sin_to_cos = flip_sin_to_cos
        self.downscale_freq_shift = downscale_freq_shift
        self.scale = scale
        self.max_period = max_period

        assert num_channels % 2 == 0
        half_dim = num_channels // 2

        idx = torch.arange(half_dim)

        exponent = -math.log(max_period) * idx
        exponent /= half_dim - downscale_freq_shift

        freq = exponent.exp()
        freq = torch.cat([freq, freq]).unsqueeze(0)

        amplitude = torch.full((1, num_channels), scale)

        zeros = torch.zeros((1, half_dim))
        ones = torch.ones((1, half_dim))
        phase = torch.cat([zeros, ones], dim=1) * torch.pi / 2

        if flip_sin_to_cos:
            freq = reverse(freq, half_dim)
            phase = reverse(phase, half_dim)
            amplitude = reverse(amplitude, half_dim)

        # TODO create nn.Buffer
        self.freq = freq
        self.phase = phase
        self.amplitude = amplitude

    def __call__(self, x: Tensor) -> Tensor:
        x = x[..., None]

        kwargs = dict(device=self.device, dtype=self.dtype, non_blocking=True)
        self.freq = self.freq.to(**kwargs)
        self.phase = self.phase.to(**kwargs)
        self.amplitude = self.amplitude.to(**kwargs)

        return self.amplitude * torch.sin(x * self.freq + self.phase)


def reverse(x: Tensor, half_dim: int) -> Tensor:
    return torch.cat([x[:, half_dim:], x[:, :half_dim]], dim=1)
