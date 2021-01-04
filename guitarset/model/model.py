import torch.nn as nn
import torch.nn.functional as F
import torch
from model.resnet import ResNetBasicBlock
from base import BaseModel      

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),          
            nn.ReLU(),

            nn.BatchNorm2d(8), # added for gradient stability
            nn.Conv2d(8, 16, kernel_size=3, padding=1),          
            nn.ReLU(),
                     
            #nn.Dropout(0.2),
            #nn.BatchNorm2d(16), # added for gradient stability
            nn.Conv2d(16, 8, kernel_size=3, padding=1),         
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(), 
            nn.Dropout(0.2),
            nn.Linear(8*60*80, 256), 
            nn.ReLU(),      
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(256, 256),
                nn.ReLU(),
                
                nn.Linear(256, 128),
                nn.ReLU(),
                #nn.Dropout(0.2),
                #nn.BatchNorm1d(128),
 
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)
