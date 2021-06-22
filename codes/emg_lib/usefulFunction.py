#TODO : rename this file later
def reshapeChannelIndexToLast(data_feature):
    reshape_feature = np.zeros((data_feature['data'].shape[0], data_feature['data'].shape[2],
                         data_feature['data'].shape[3], data_feature['data'].shape[1]))
    for i in range(data_feature['data'].shape[0]):
        for j in range(8):
            reshape_feature[i,:,:,j] = data_feature['data'][i,j,:,:]
    data_feature['data'] = reshape_feature
    return data_feature