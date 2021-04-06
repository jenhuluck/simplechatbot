# -*- coding: utf-8 -*-
import numpy as np
import random
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk_utils import bag_of_words, tokenize, stem
from model import MLP

with open('intents.json', 'r') as f:
    intents = json.load(f)

tags = []
patterns = []
responses = []
for intent in intents['intents']:
     tags.append(intent['tag'])
     patterns.append(intent['patterns'])
     responses.append(intent['responses'])

all_words = []

#get all words for the whole document
for pattern in patterns:
    for sentence in pattern:
        words = tokenize(sentence)      
        for word in words:
            stem_word = stem(word)
            all_words.append(stem_word)
all_words = list(set(all_words))
ignore_list =['?','!','.']
all_words = [w for w in all_words if w not in ignore_list]

X = []
y = []
for index, pattern in enumerate(patterns):
    for each in pattern:
        words = tokenize(each)
        bag = bag_of_words(words, all_words)
        X.append(bag)
        y.append(index)
        
X = np.array(X)
y = np.array(y)
print(X.shape)
print(y.shape)
# Hyper-parameters
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X[0])
hidden_size = 8
output_size = len(tags)   

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X)
        self.x_data = X
        self.y_data = y

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples   
    
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = MLP(input_size, hidden_size, output_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        outputs = model(words)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
      
data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags,
"responses" : responses
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')        
    
    
