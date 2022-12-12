from pathlib import Path

from params_proto.neo_hyper import Sweep

from config.locomotion_config import Config
from analysis import RUN

with Sweep(RUN, Config) as sweep:
    RUN.prefix = "{project}/{file_stem}/{job_name}"
    Config.seed = 100
    Config.returns_condition = True
    Config.predict_epsilon = True
    Config.n_diffusion_steps = 200
    Config.condition_dropout = 0.25
    Config.diffusion = 'models.GaussianInvDynDiffusion'

    with sweep.product:
        Config.n_train_steps = [1e6]
        Config.dataset = ['hopper-medium-expert-v2']
        Config.returns_scale = [400.0]

@sweep.each
def tail(RUN, Config, *_):
    if Config.predict_epsilon:
        prefix = f'predict_epsilon_{Config.n_diffusion_steps}'
    else:
        prefix = f'predict_x0_{Config.n_diffusion_steps}'

    RUN.prefix, RUN.job_name, _ = RUN(script_path=__file__,
                                      job_name=f"{prefix}_{Config.n_train_steps}/dropout_{Config.condition_dropout}/{Config.dataset}/{Config.seed}")


sweep.save(f"{Path(__file__).stem}.jsonl")