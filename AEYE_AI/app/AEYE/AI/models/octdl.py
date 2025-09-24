
import torch
import timm


def generate_model(cfg):
    model = _build_model(cfg)

    if cfg.ai.checkpoint:
        weights = torch.load(cfg.ai.checkpoint)
        model.load_state_dict(weights, strict=True)
        print('Load weights form {}'.format(cfg.ai.checkpoint))
    model = model.to(cfg.base.device)

    return model

regression_loss = ['mean_square_error', 'mean_absolute_error', 'smooth_L1']

def _build_model(cfg):
    network = cfg.train.network
    out_features = _select_out_features(
        cfg.data.num_classes,
        cfg.train.criterion
    )

    if 'vit' in network or 'swin' in network:
        model = timm.create_model(
            network,
            img_size=cfg.data.input_size,
            in_chans=cfg.data.in_channels,
            num_classes=out_features,
            pretrained=cfg.train.pretrained,
        )
    else:
        model = timm.create_model(
            network,
            in_chans=cfg.data.in_channels,
            num_classes=out_features,
            pretrained=cfg.train.pretrained,
        )

    return model

# convert output dimension of network according to criterion
def _select_out_features(num_classes, criterion):
    out_features = num_classes
    if criterion in regression_loss:
        out_features = 1
    return out_features