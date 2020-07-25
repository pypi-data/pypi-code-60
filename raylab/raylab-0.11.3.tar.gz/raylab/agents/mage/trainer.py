"""Trainer and default config for MAGE."""
from raylab.agents import trainer
from raylab.agents.model_based import ModelBasedTrainer
from raylab.agents.sop.trainer import sop_config
from raylab.policy.model_based.training_mixin import TrainingSpec

from .policy import MAGETorchPolicy


@trainer.configure
@trainer.option("lambda", 0.05, help="TD error regularization for MAGE loss")
@trainer.option("model_training", TrainingSpec().to_dict(), help=TrainingSpec.__doc__)
@sop_config
@trainer.option("module/type", "ModelBasedDDPG")
@trainer.option("torch_optimizer/models", {"type": "Adam"})
@trainer.option(
    "exploration_config/type", "raylab.utils.exploration.GaussianNoise", override=True
)
@trainer.option("holdout_ratio", 0, override=True)
@trainer.option("max_holdout", 0, override=True)
@trainer.option("evaluation_config/explore", False, override=True)
class MAGETrainer(ModelBasedTrainer):
    """Single agent trainer for MAGE."""

    _name = "MAGE"
    _policy = MAGETorchPolicy
