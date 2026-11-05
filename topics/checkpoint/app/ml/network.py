"""Small CNN trained from scratch; no downloaded expression-classifier weights."""
import torch
from torch import nn


class Separable(nn.Module):
    def __init__(self, a, b):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(a, a, 3, padding=1, groups=a, bias=False), nn.BatchNorm2d(a), nn.ReLU(),
            nn.Conv2d(a, b, 1, bias=False), nn.BatchNorm2d(b), nn.ReLU(),
        )

    def forward(self, x):
        return self.net(x)


class ExpressionNet(nn.Module):
    def __init__(self, classes=8):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 24, 3, padding=1, bias=False), nn.BatchNorm2d(24), nn.ReLU(),
            Separable(24, 32), nn.MaxPool2d(2),
            Separable(32, 64), Separable(64, 64), nn.MaxPool2d(2),
            Separable(64, 96), Separable(96, 96), nn.MaxPool2d(2),
            Separable(96, 128), nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Dropout(.25),
        )
        self.classifier = nn.Linear(128, classes)

    def forward(self, x):
        return self.classifier(self.features(x))


class TransferExpressionNet(nn.Module):
    """ImageNet-only pretraining, with preprocessing inside the exported graph."""
    def __init__(self, classes=8, pretrained=True, cache=None):
        super().__init__()
        from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights
        if cache is not None:torch.hub.set_dir(str(cache))
        self.backbone=mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.IMAGENET1K_V1 if pretrained else None)
        self.backbone.classifier[-1]=nn.Linear(self.backbone.classifier[-1].in_features,classes)
        self.register_buffer("mean",torch.tensor([.485,.456,.406]).view(1,3,1,1))
        self.register_buffer("std",torch.tensor([.229,.224,.225]).view(1,3,1,1))

    def forward(self,face):
        x=torch.nn.functional.interpolate((face+1).repeat(1,3,1,1)/2,size=(96,96),mode="bilinear",align_corners=False)
        return self.backbone((x-self.mean)/self.std)
