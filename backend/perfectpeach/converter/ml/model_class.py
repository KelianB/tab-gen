import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
from abc import abstractmethod

class BaseModel(nn.Module):
    """
    Base class for all models
    """
    @abstractmethod
    def forward(self, *inputs):
        """
        Forward pass logic

        :return: Model output
        """
        raise NotImplementedError

    def __str__(self):
        """
        Model prints with number of trainable parameters
        """
        model_parameters = filter(lambda p: p.requires_grad, self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        return super().__str__() + '\nTrainable parameters: {}'.format(params)


class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),          
            nn.ReLU(),

            nn.BatchNorm2d(8), # added for gradient stability
            nn.Conv2d(8, 16, kernel_size=3, padding=1),          
            nn.ReLU(),
                     
            nn.Conv2d(16, 8, kernel_size=3, padding=1),         
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(8, 4, kernel_size=3, padding=1),         
            nn.ReLU(),
            
            nn.Flatten(), 
            nn.Dropout(0.2),
            nn.Linear(4*60*80, 512), 
            nn.ReLU(),      
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(512, 256),
                nn.ReLU(),
                
                nn.Linear(256, 128),
                nn.ReLU(),
 
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)
