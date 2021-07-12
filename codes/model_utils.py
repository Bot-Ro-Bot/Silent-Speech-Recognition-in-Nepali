import numpy as np 
import os
import glob
import pickle
from tqdm import tqdm

from sklearn import preprocessing
import torch
import torch.nn as nn
import torch.nn.functional as F



SAMPLING_RATE = 250
NUM_CHANNELS = 8
CURR_DIR = os.getcwd()
MAIN_DIR = "."
if os.path.basename(os.getcwd())!="Silent-Interface-for-IOT-Devices":
    os.chdir("..")
PICKLE_DIR = os.path.join(MAIN_DIR,"pickles")


# ============= IMPORT FILTERED PICKLE DATA ===============
Picklefile = "data_dict_sfeature_aug1.pickle"
if Picklefile in os.listdir(PICKLE_DIR):
    all_data = pickle.load(open(os.path.join(PICKLE_DIR,Picklefile),"rb"))
    print("-------Read Task Accomplished----------")

print(all_data["data"].shape)
print(all_data.keys())
print(type(all_data["labels"]))

int_labels = []
label_encoder =  preprocessing.LabelEncoder()
int_labels = label_encoder.fit_transform(all_data["labels"])
# int_labels = int_labels.tolist()

print([int_labels[i] for i in range(10)])
print([all_data["labels"][i]for i in range(10)])




#=============== MODEL UTILITIES ==========================
class Flatten(nn.Module):
	"""A custom layer that views inputs as 1D, input.size(0) = batch size """
	def forward(self, input):
		return input.view(input.size(0), -1)


def batchify_data(x_data, y_data, batch_size):
    """Takes a set of data points and labels and groups them into batches
		that can be processed more efficiently than directly runing epoch.
		Only take batch_size chunks (i.e. drop the remainder)"""

    N = int(len(x_data) / batch_size) * batch_size
    batches = []
    for i in range(0, N, batch_size):
        batches.append({
            'x': torch.tensor(x_data[i: i+batch_size], dtype=torch.float32),
            'y': torch.tensor(y_data[i: i+batch_size], dtype=torch.long)
            })
    return batches
	

def compute_accuray(predictions, y):
	"""Computes the accuracy of predictions against the gold labels, y
	   NOTE:
	   Moving to numpy will break the graph thus no gradient will be computed so, can't call numpy() on Variable that requires grad. 
	   Gradient is not necessary here so .detach() is explicitly used here.
	"""
	return np.mean(np.equal(predictions.detach().numpy(), y.numpy()))


# ======================== TRAINING PROCEDURES =====================================

def train_model(train_data, dev_data, model, lr=0.02, momentum=0.9, nesterov=False, n_epochs=20):
	"""Train a model for N epochs given data and hyper-parameters. We use SGD here"""
	train_acc = []
	train_loss = []
	v_acc = []
	v_loss = []

	optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=momentum, nesterov=nesterov)
	for epoch in range(1,n_epochs):
		print("-----------------\nEpoch {}:\n".format(epoch))

		# Run training
		loss, acc, predictions, y = run_epoch(train_data, model.train(), optimizer)
		print("Train loss: {:.6f} | Train accuracy: {:.6f} ".format(loss, acc))
		train_loss.append(loss)
		train_acc.append(acc)

		# Run validation
		val_loss, val_acc, predictions, y = run_epoch(dev_data, model.eval(), optimizer)
		print("Validation loss: {:.6f} | Validation accuracy: {:.6f}".format(val_loss, val_acc))
		v_loss.append(val_loss)
		v_acc.append(val_acc)

		# Save model
		# torch.save(model, 'fully_connected_model.pt')
	return val_acc, train_acc, train_loss, v_loss, v_acc
	
def run_epoch(data, model, optimizer):
    """Train model for one pass of train data, and return loss, acccuracy"""
    
    # Gather losses	
    losses = []
    batch_accuracies = []

    #If model is in train mode, use optimizer
    is_training = model.training	

    #Iterate through batches
    for batch in tqdm(data):
    	x,y = batch['x'],batch['y']				# Grab x and y
    	out = model(x)							# Get output predictions
    	predictions = torch.argmax(out, dim=1)	# Select the max among output predictions tensor as dimension = 1
    	batch_accuracies.append(compute_accuray(predictions, y))	#store accuracy

    	#Comput loss
    	loss = F.cross_entropy(out, y)
    	losses.append(loss.data.item())

    	#If training then update as
    	if is_training:
    		optimizer.zero_grad()
    		loss.backward()
    		optimizer.step()

    #Calculate epoch level scores
    avg_loss = np.mean(losses)
    avg_accuracy = np.mean(batch_accuracies)
    # print(y.shape)
    # print(predictions.shape)	
    return avg_loss, avg_accuracy, predictions, y

