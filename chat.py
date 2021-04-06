# -*- coding: utf-8 -*-
import random
import json
import torch
from model import MLP
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

FILE = "data.pth"
data = torch.load(FILE)
model_state = data["model_state"]
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
responses = data['responses']

model = MLP(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "Bob"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    #print(X.shape)
    X = X.reshape(1, X.shape[0]) #for single input
    #print(X.shape)
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
    #print(output)
    predicted_label = int(torch.argmax(output.data))
    
    probs = torch.softmax(output,dim=1)
    
    if probs[0][predicted_label].item() < 0.75:
        return "I do not understand..."
    else:
        return random.choice(responses[predicted_label])




    
    