
import timm
import torch

from AEYE.application.AI.registry import vision_register


@vision_register.register("OCTDL")
class OCTDL:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = _generate_model(self.cfg)
        
    def get_model(self):
        return self.model
        
def _generate_model(cfg):
    model = _build_model(cfg)

    print(cfg.Vision_AI.checkpoint)
    if cfg.Vision_AI.checkpoint:
        weights = torch.load(cfg.Vision_AI.checkpoint)
        model.load_state_dict(weights, strict=True)
        print('Load weights form {}'.format(cfg.Vision_AI.checkpoint))
    model = model.to('cuda')

    return model

regression_loss = ['mean_square_error', 'mean_absolute_error', 'smooth_L1']

def _build_model(cfg):
    network = cfg.Vision_AI.network
    out_features = _select_out_features(
        cfg.Vision_AI.num_classes,
        cfg.Vision_AI.criterion
    )

    if 'vit' in network or 'swin' in network:
        model = timm.create_model(
            network,
            img_size=cfg.Vision_AI.input_size,
            in_chans=cfg.Vision_AI.in_channels,
            num_classes=out_features,
            pretrained=cfg.Vision_AI.pretrained,
        )
    else:
        model = timm.create_model(
            network,
            in_chans=cfg.Vision_AI.in_channels,
            num_classes=out_features,
            pretrained=cfg.Vision_AI.pretrained,
        )

    return model

# convert output dimension of network according to criterion
def _select_out_features(num_classes, criterion):
    out_features = num_classes
    if criterion in regression_loss:
        out_features = 1
    return out_features