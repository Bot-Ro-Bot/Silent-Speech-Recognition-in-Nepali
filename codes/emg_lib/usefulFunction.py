#TODO : rename this file later
def reshapeChannelIndexToLast(data_feature):
    reshape_feature = np.zeros((data_feature['data'].shape[0], data_feature['data'].shape[2],
                         data_feature['data'].shape[3], data_feature['data'].shape[1]))
    for i in range(data_feature['data'].shape[0]):
        for j in range(8):
            reshape_feature[i,:,:,j] = data_feature['data'][i,j,:,:]
    data_feature['data'] = reshape_feature
    return data_feature

#confusion matrix
from matplotlib import font_manager
font_dirs = ['../../fonts/']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
# set font
plt.rcParams['font.family'] = 'mangal'

from sklearn.metrics import confusion_matrix
def confusion_matrix_plt(y_value , pred_value, labels, normalize = None):
    print(y_value)
    print(pred_value)
    plt.matshow(confusion_matrix(y_value, pred_value,  normalize = 'true'), interpolation = 'nearest', cmap = plt.cm.Reds)
    plt.xticks(range(len(labels)), labels, rotation = 45)
    plt.yticks(range(len(labels)), labels)

    cm = confusion_matrix(y_value, pred_value, normalize = normalize)
    for i in range(len(labels)):
        for j in range(len(labels)):
            plt.text(j, i, "%.2f"%cm[i][j], horizontalalignment='center', verticalalignment='center')
    plt.show()
