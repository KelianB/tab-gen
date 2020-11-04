import torch.nn as nn
import torch.nn.functional as F
import torch
from base import BaseModel

class GuitarSetModel(BaseModel):
    def __init__(self, num_classes=10):
        super().__init__()
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=5, padding=2),          # N x 8 x 480 x 640
            nn.MaxPool2d(2),                                    # N x 4 x 240 x 320
            nn.ReLU(),

            nn.Conv2d(8, 16, kernel_size=3, padding=1),         # N x 16 x 240 x 320
            #nn.Dropout2d(),
            nn.MaxPool2d(2),                                    # N x 16 x 120 x 160
            nn.ReLU(),

            nn.Conv2d(16, 32, kernel_size=3, padding=1),        # N x 32 x 120 x 160 
            nn.MaxPool2d(2),                                    # N x 16 x 60 x 80
            nn.ReLU(),

            nn.Conv2d(32, 16, kernel_size=5, padding=2),         # N x 16 x 60 x 80
            nn.ReLU(),            
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(16, 16, kernel_size=3, padding=1),         # N x 16 x 60 x 80 
                nn.ReLU(),
                nn.Conv2d(16, 4, kernel_size=3, padding=1, stride=2),  # N x 4 x 30 x 40
                nn.Flatten(), # N x (4*30*40)
                nn.Linear(4*30*40, 128),  # N x 128
                nn.ReLU(),
                nn.Linear(128, 64),       # N x 64
                nn.ReLU(),
                nn.Linear(64, 19),        # N x 19
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x):
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

def forward(self, x):
        x = x.float()
        x = self.conv1(x)
        # N x 8 x 480 x 640
        # (3, 4) => 160x160
        x = F.relu(F.max_pool2d(x, 2))
        # N x 8 x 240 x 320
        x = self.conv2_drop(self.conv2(x))
        # N * 16 x 240 x 320
        x = F.relu(F.max_pool2d(x, 2))
        # N * 16 x 120 x 160
        x = self.conv3(x)
        # N * 4 * 120 x 160 
        x = F.relu(F.max_pool2d(x, 2))
        # N * 4 * 60 x 80
        x = x.view(x.shape[0], 4*60*80)
        x = F.relu(self.fc1(x))
        # N x 128
        
        x1 = F.relu(self.fc2_1(x))
        x1 = F.softmax(x1, dim=1)

        x2 = F.relu(self.fc2_2(x))
        x2 = F.softmax(x2, dim=1)

        x3 = F.relu(self.fc2_3(x))
        x3 = F.softmax(x3, dim=1)

        x4 = F.relu(self.fc2_4(x))
        x4 = F.softmax(x4, dim=1)

        x5 = F.relu(self.fc2_5(x))
        x5 = F.softmax(x5, dim=1)

        x6 = F.relu(self.fc2_6(x))
        x6 = F.softmax(x6, dim=1)

        z = torch.stack((x1,x2,x3,x4,x5,x6), dim=1)
        
        # -> get to correct shape (N x 6 x 19)

        # x = F.dropout(x, training=self.training)
        # x = self.fc2(x)
        # return F.log_softmax(x, dim=1)

        return z
"""