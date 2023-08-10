#!/usr/bin/env python

import ray
from ray import air, tune
from ray.rllib.env.policy_server_input import PolicyServerInput
from ray.rllib.examples.custom_metrics_and_callbacks import MyCallbacks
from ray.tune.logger import pretty_print
from ray.tune.registry import get_trainable_cls

###############################################################################
# Init
###############################################################################

ray.init()

config = (
    get_trainable_cls('PPO').get_default_config()
    # Indicate that the Algorithm we setup here doesn't need an actual env.
    # Allow spaces to be determined by user (see below).
    .environment(
        env=None,
        observation_space=[],
        action_space=[],
    )
    # DL framework to use.
    .framework('tf2')
    # Create a "chatty" client/server or not.
    .callbacks(None)
    # Use the `PolicyServerInput` to generate experiences.
    # .offline_data(input_=_input)
    # Use n worker processes to listen on different ports.
    .rollouts(
        num_rollout_workers=1,
        # Connectors are not compatible with the external env.
        enable_connectors=False,
    )
    # Disable OPE, since the rollouts are coming from online clients.
    .evaluation(off_policy_estimation_methods={})
    # Set to INFO so we'll see the server's actual address:port.
    .debugging(log_level="INFO")
)

config.rl_module(_enable_rl_module_api=False)
config.training(_enable_learner_api=False)

config.update_from_dict(
    {
        "rollout_fragment_length": 1000,
        "train_batch_size": 4000,
        # "model": {"use_lstm": false},
    }
)

algo = config.build()

