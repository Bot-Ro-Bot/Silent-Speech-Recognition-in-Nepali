# import numpy as np 
# import torch
# import torch.nn as nn
from model_utils import *
# from torchsummary import summary

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt



def plotAccuracy(val_acc, train_acc, train_loss, v_loss, v_acc):
	epoch_num = np.arange(1,20)
	plt.plot(epoch_num, train_acc, label='train')
	plt.plot(epoch_num, v_acc, label='test_validation')
	plt.xlabel("epochs")
	plt.ylabel("accuracy")
	plt.title('model accuracy')
	plt.legend()
	plt.tight_layout()
	# plt.grid(True)
	plt.show()


def plotCM(y, predictions):
	cm = confusion_matrix(y, predictions.detach().numpy())
	print(cm)
	plt.imshow(cm, interpolation = 'nearest', cmap = plt.cm.Wistia)
	LABELS = ["ABA KO SAMAY SUNAU","EUTA SANGEET BAJAU","AAJA KO MAUSAM BATAU","BATTI KO AWASTHA BADALA","PANKHA KO STHITI BADALA"]
	plt.title('confusion_matrix')
	plt.ylabel('True label')
	plt.xlabel('Predicted value')
	points = np.arange(len(LABELS))
	plt.xticks(points, LABELS, rotation = 45)
	plt.yticks(points, LABELS)
	for i in range(10):
		for j in range(10):
			plt.text(j,i, cm[i][j])
	plt.show()


#============= BATCHIFYING AND SPLITTING TRAIN DATA FOR VALIDATION SET ==================

def dev_batch(X_train, X_test, Y_train, Y_test):
	dev_split_index = int(9* len(X_train)/10)	# 90% train set, 10% Validation set
	X_dev = X_train[dev_split_index:]
	Y_dev = Y_train[dev_split_index:]
	X_train = X_train[:dev_split_index]
	Y_train = Y_train[:dev_split_index]

	permutation = np.array([i for i in range(len(X_train))])
	np.random.shuffle(permutation)
	X_train = [X_train[i] for i in permutation]
	Y_train = [Y_train[i] for i in permutation]

	batch_size = 32
	train_batches = batchify_data(X_train, Y_train, batch_size)
	dev_batches = batchify_data(X_dev, Y_dev, batch_size)
	test_batches = batchify_data(X_test, Y_test, batch_size)
	
	return train_batches, dev_batches, test_batches


# ============== CNN MODEL IMPLEMENTATION ==================
def main(RESHAPE=False):

	X_train, X_test, Y_train, Y_test = train_test_split(all_data["data"], int_labels, test_size=0.2)
	print("X_train.shape:", X_train.shape, ", X_test.shape:", X_test.shape)
	
	# reshape code
	if (RESHAPE==True): 
		X_train = np.reshape(X_train, (X_train.shape[0], 8, 26, 37))
		X_test = np.reshape(X_test, (X_test.shape[0], 8, 26, 37)) 

	train_batches, dev_batches, test_batches = dev_batch(X_train, X_test, Y_train, Y_test)

	model = nn.Sequential(
    			nn.Conv2d(8, 64, (3,3)),
    			nn.ReLU(),
    			nn.MaxPool2d((2,2)),

    			nn.Conv2d(64, 512, (3,3)),
    			nn.ReLU(),
    			nn.MaxPool2d((2,2)),

    			Flatten(),
    			nn.Linear(76800, 4096),
    			nn.Dropout(0.25),
    			nn.Linear(4096, 64),
    			nn.Dropout(0.25),
    			nn.Linear(64, 10),

    		)
	# print(summary(model, (8,31,80)))

	val_acc, train_acc, train_loss, v_loss, v_acc = train_model(train_batches, dev_batches, model, nesterov = True)
	loss, accuracy, predictions, y = run_epoch(test_batches, model.eval(), None)
	print("Loss on test set:" + str(loss) + " Accuracy on test set:" + str(accuracy))

	plotAccuracy(val_acc, train_acc, train_loss, v_loss, v_acc)
	plotCM(y, predictions)

if __name__ == '__main__':
	np.random.seed(2321)
	torch.manual_seed(2321)
	main()