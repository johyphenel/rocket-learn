import torch.nn as nn
from learner import Learner, PPO
from rlgym.utils.terminal_conditions.common_conditions import TimeoutCondition
from rlgym.utils.reward_functions.common_rewards import MoveTowardsBallReward
from rlgym.utils.obs_builders.advanced_obs import AdvancedObs

def get_match_args():
    return dict(
        game_speed=100,
        random_resets=True,
        self_play=True,
        team_size=1,
        obs_builder=AdvancedObs(),
        terminal_conditions=[TimeoutCondition(600)],
        reward_function=MoveTowardsBallReward()
    )

state_dim = 67
action_dim = 8

#example pytorch stuff, delete later
actor = nn.Sequential(
    nn.Linear(state_dim, 64),
    nn.Tanh(),
    nn.Linear(64, 64),
    nn.Tanh(),
    nn.Linear(64, action_dim),
    nn.Softmax(dim=-1)
)

# critic
critic = nn.Sequential(
    nn.Linear(state_dim, 64),
    nn.Tanh(),
    nn.Linear(64, 64),
    nn.Tanh(),
    nn.Linear(64, 1)
)

# make sure to add this to avoid a torch multiprocessing bug
# https://github.com/pytorch/pytorch/issues/5858
if __name__ == '__main__':
    alg = PPO(actor, critic)
    rl_path = "C:\\EpicGames\\rocketleague\\Binaries\\Win64\\RocketLeague.exe"
    log_dir = "C:\\log_directory\\"

    learner = Learner(rl_path, alg, log_dir, get_match_args)
    learner.learn()