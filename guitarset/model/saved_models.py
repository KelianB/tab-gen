# Store models for reference

"""
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
"""


""" #1

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
        
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),

            nn.BatchNorm2d(32), # added for gradient stability
            nn.Conv2d(32, 64, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),
            
                                                 # N x 32 x 240 x 320
            nn.BatchNorm2d(64), # added for gradient stability
            nn.Conv2d(64, 64, kernel_size=3, padding=1),         # N x 64 x 240 x 320
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),   # N x (64*120*160)            
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(64*60*80, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.BatchNorm1d(128), # added for gradient stability
                nn.Linear(128, 64),
                nn.Dropout(0.2),
                nn.Linear(64, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

""" #7

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),

            nn.BatchNorm2d(8), # added for gradient stability
            nn.Conv2d(8, 16, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),
                     
            #nn.Dropout(0.5),
            nn.BatchNorm2d(16), # added for gradient stability
            nn.Conv2d(16, 16, kernel_size=3, padding=1),         # N x 64 x 240 x 320
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),   # N x (64*120*160)            
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(16*60*80, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

""" #11

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),

            nn.BatchNorm2d(8), # added for gradient stability
            nn.Conv2d(8, 16, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),
              
            ResNetBasicBlock(16, 16),

            #nn.Dropout(0.5),
            nn.BatchNorm2d(16), # added for gradient stability
            nn.Conv2d(16, 16, kernel_size=3, padding=1),         # N x 64 x 240 x 320
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),   # N x (64*120*160)            
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(16*60*80, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

""" #12

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),

            nn.BatchNorm2d(8), # added for gradient stability
            nn.Conv2d(8, 16, kernel_size=3, padding=1),          # N x 32 x 480 x 640
            nn.ReLU(),
              
            ResNetBasicBlock(16, 16),

            #nn.Dropout(0.5),
            nn.BatchNorm2d(16), # added for gradient stability
            nn.Conv2d(16, 16, kernel_size=3, padding=1),         # N x 64 x 240 x 320
            nn.ReLU(),
         
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                ResNetBasicBlock(16, 16),
                ResNetBasicBlock(16, 8),

                nn.MaxPool2d(2),
                nn.Flatten(),   # N x (64*120*160)    

                nn.Linear(8*60*80, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

""" #13 

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            ResNetBasicBlock(1, 8),
            ResNetBasicBlock(8, 16),            
            ResNetBasicBlock(16, 32),
            ResNetBasicBlock(32, 64),
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                ResNetBasicBlock(64, 64),
                ResNetBasicBlock(64, 32),
                ResNetBasicBlock(32, 8),

                nn.MaxPool2d(2),
                nn.Flatten(),   # N x (64*120*160)    

                nn.Linear(8*60*80, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

""" #14

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            ResNetBasicBlock(1, 8),
            ResNetBasicBlock(8, 16),            
            ResNetBasicBlock(16, 32),
            ResNetBasicBlock(32, 64),
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                ResNetBasicBlock(64, 64),
                nn.MaxPool2d(2),
                ResNetBasicBlock(64, 32),
                ResNetBasicBlock(32, 8),
                nn.MaxPool2d(2),
                ResNetBasicBlock(8, 4),

                nn.Flatten(),   # N x (64*120*160)    

                nn.Linear(4*30*40, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""

""" #15

class GuitarSetModel(BaseModel):
    def __init__(self):
        super().__init__()
    
        self.main_block = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),          
            nn.ReLU(),

            nn.BatchNorm2d(8), # added for gradient stability
            nn.Conv2d(8, 16, kernel_size=3, padding=1),          
            nn.ReLU(),
                     
            nn.Dropout(0.2),
            nn.BatchNorm2d(16), # added for gradient stability
            nn.Conv2d(16, 16, kernel_size=3, padding=1),         
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Flatten(),        
        )

        self.out_layers = nn.ModuleList([
            nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(16*60*80, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.BatchNorm1d(128),
                nn.Linear(128, 19),
                nn.Softmax(dim=1),
            ) for i in range(6)
        ])

    def forward(self, x): 
        x = self.main_block(x)
        outs = [sequential(x) for sequential in self.out_layers]
        return torch.stack(outs, dim=1)

"""
