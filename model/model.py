import torch
import torchvision
import numpy as np
import pandas as pd

if __name__ == '__main__':
    
    df = pd.read_csv('./data/data.csv')
    data = df.to_numpy()
    X_train = 1
    X_test = 1
    y_train = 1
    y_test = 1  
    # Convert the data to PyTorch tensors 
    X_train = torch.tensor(X_train).float() 
    X_test = torch.tensor(X_test).float() 
    y_train = torch.tensor(y_train) 
    y_test = torch.tensor(y_test) 
    
    # Normalize the features 
    mean = X_train.mean(dim=0) 
    std = X_train.std(dim=0) 
    X_train = (X_train - mean) / std 
    X_test = (X_test - mean) / std

    # Define the model 
    model = torch.nn.Sequential( 
        torch.nn.Linear(in_features = 23, out_features =2), 
        torch.nn.Softmax(dim=1) 
    )
    # Train the model 
    criterion = torch.nn.CrossEntropyLoss() 
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1) 
    
    num_epochs = 1000
    for epoch in range(num_epochs): 
        # Forward pass 
        y_pred = model(X_train) 
        loss = criterion(y_pred, y_train) 
    
        # Backward pass and optimization 
        optimizer.zero_grad() 
        loss.backward() 
        optimizer.step() 
    
        # Print the loss every 100 epochs 
        if (epoch+1) % 100 == 0: 
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # Evaluate the model 
    with torch.no_grad(): 
        y_pred = model(X_test) 
        _, predicted = torch.max(y_pred, dim=1) 
        accuracy = (predicted == y_test).float().mean() 
        print(f'Test Accuracy: {accuracy.item():.4f}')