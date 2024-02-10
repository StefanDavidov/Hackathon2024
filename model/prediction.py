import torch

def prediction(predicition_Data):
    model = torch.load('./trainedModel')

    y_pred = model(predicition_Data)

    if y_pred == 1:
        print("The model believes that the stock you chose will go UP!")
    else:
        print("The model believes that the stock you chose will go DOWN")

    return y_pred