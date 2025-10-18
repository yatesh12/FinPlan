import torch
import torch.nn as nn

# Define the same model architecture
class PortfolioModel(nn.Module):
    def __init__(self, input_size=11, hidden_size=64, output_size=10):
        super(PortfolioModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Softmax(dim=1)  # Ensure outputs sum to 1 (percentages)
        )
    
    def forward(self, x):
        return self.network(x)

# Create and save a mock model
model = PortfolioModel()

# Initialize with some reasonable weights for testing
with torch.no_grad():
    # Initialize weights to create reasonable allocations
    for layer in model.network:
        if isinstance(layer, nn.Linear):
            layer.weight.data.normal_(0, 0.1)
            if layer.bias is not None:
                layer.bias.data.zero_()

# Save the model
torch.save(model.state_dict(), 'full_portfolio_model.pth')
print("Mock model created and saved successfully!")

# Test the model
model.eval()
sample_input = torch.randn(1, 11)  # Batch size 1, 11 features
with torch.no_grad():
    output = model(sample_input)
    print(f"Sample output: {output}")
    print(f"Output sum: {output.sum().item()}")  # Should be close to 1.0