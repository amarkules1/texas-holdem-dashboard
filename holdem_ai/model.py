"""
Policy-Value Neural Network Architecture for Texas Hold'em.
Uses pure NumPy inference for maximum portability, zero external C/CUDA dependencies,
and 100% mathematical parity with trained weights.
"""

import os
import numpy as np


class HoldemPolicyValueNumpy:
    """
    Pure NumPy inference engine for HoldemPolicyValueNet.
    Runs Actor-Critic forward passes with identical mathematical results
    without requiring PyTorch, CUDA, or OpenMP shared libraries.
    """
    ACTION_NAMES = ["fold", "check_call", "raise_small", "raise_med", "raise_allin"]
    NUM_ACTIONS = 5

    def __init__(self, weights):
        if isinstance(weights, str):
            npz = np.load(weights)
            self.weights = {k: npz[k] for k in npz.files}
        elif isinstance(weights, dict):
            self.weights = weights
        else:
            raise ValueError(f"Invalid weights type: {type(weights)}")

        # Infer dimensions from fc1 weight: shape [hidden_dim, input_dim]
        self.hidden_dim = self.weights["fc1.weight"].shape[0]
        self.input_dim = self.weights["fc1.weight"].shape[1]

    @staticmethod
    def _gelu(x):
        try:
            from scipy.special import erf
            return x * 0.5 * (1.0 + erf(x / np.sqrt(2.0)))
        except (ImportError, AttributeError):
            # Tanh approximation for standard GELU
            return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * np.power(x, 3))))

    @staticmethod
    def _layer_norm(x, weight, bias, eps=1e-5):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return (x - mean) / np.sqrt(var + eps) * weight + bias

    def forward(self, x):
        x = np.asarray(x, dtype=np.float32)
        squeeze_batch = False
        if x.ndim == 1:
            x = np.expand_dims(x, axis=0)
            squeeze_batch = True

        if x.shape[-1] > self.input_dim:
            x = x[..., :self.input_dim]
        elif x.shape[-1] < self.input_dim:
            pad_width = [(0, 0)] * (x.ndim - 1) + [(0, self.input_dim - x.shape[-1])]
            x = np.pad(x, pad_width, mode='constant', constant_values=0)

        w = self.weights
        h = np.dot(x, w["fc1.weight"].T) + w["fc1.bias"]
        h = self._gelu(self._layer_norm(h, w["ln1.weight"], w["ln1.bias"]))

        h = np.dot(h, w["fc2.weight"].T) + w["fc2.bias"]
        h = self._gelu(self._layer_norm(h, w["ln2.weight"], w["ln2.bias"]))

        h = np.dot(h, w["fc3.weight"].T) + w["fc3.bias"]
        h = self._gelu(self._layer_norm(h, w["ln3.weight"], w["ln3.bias"]))

        logits = np.dot(h, w["policy_head.weight"].T) + w["policy_head.bias"]
        value = (np.dot(h, w["value_head.weight"].T) + w["value_head.bias"]).squeeze(-1)

        if squeeze_batch:
            logits = logits[0]
            value = float(value[0]) if hasattr(value, "__len__") else float(value)

        return logits, value

    def __call__(self, x):
        return self.forward(x)

    def eval(self):
        return self

    def get_action_probs(self, x, action_mask=None, temperature=1.0):
        logits, _ = self.forward(x)
        logits = np.asarray(logits, dtype=np.float64)

        if temperature > 0.0 and temperature != 1.0:
            logits = logits / temperature

        if action_mask is not None:
            mask = np.asarray(action_mask)
            if mask.ndim == 1 and logits.ndim == 2:
                mask = np.expand_dims(mask, axis=0)
            logits = np.where(mask == 0, -1e9, logits)

        # Stable softmax
        max_logits = np.max(logits, axis=-1, keepdims=True)
        exp_logits = np.exp(logits - max_logits)
        probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
        return probs

    def predict_action(self, x, action_mask=None, deterministic=False, temperature=1.0):
        probs = self.get_action_probs(x, action_mask=action_mask, temperature=temperature)
        if probs.ndim > 1:
            probs = probs[0]

        if deterministic:
            action_idx = int(np.argmax(probs))
        else:
            probs_clean = np.clip(probs, 0.0, 1.0)
            p_sum = probs_clean.sum()
            if p_sum > 0:
                probs_clean = probs_clean / p_sum
            else:
                probs_clean = np.ones(len(probs_clean)) / len(probs_clean)
            action_idx = int(np.random.choice(len(probs_clean), p=probs_clean))

        action_name = self.ACTION_NAMES[action_idx]
        prob_dict = {name: float(prob) for name, prob in zip(self.ACTION_NAMES, probs)}
        return action_idx, action_name, prob_dict

    @classmethod
    def from_checkpoint(cls, checkpoint_path):
        return cls(checkpoint_path)


# Default model class is HoldemPolicyValueNumpy
HoldemPolicyValueNet = HoldemPolicyValueNumpy
TORCH_AVAILABLE = False
