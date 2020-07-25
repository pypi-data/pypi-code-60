from monk.tf_keras_1.models.imports import *


class CNNVisualizer():
  '''
  Base class for visualizing features and feature maps of keras models
  
  Args:
        model (): Trained model 
        is_notebook: Check environment type
                      True - Using Jupyter-like environment (Notebook)
                      False - Otherwise 
  '''

  def __init__(self, model, is_notebook=False):
    self.model = model
    self.conv_layers = self._extract_conv_layers()
    self.fmaps = []
    self.is_notebook = is_notebook

  def _extract_conv_layers(self):

    '''
    Extracts convolutional layers from a model 
    '''

    conv_layers = {}
    num_layers = 0
    for layer in self.model.layers:
        if type(layer) == keras.layers.convolutional.Conv2D:
          num_layers += 1
          conv_layers.update({layer.name : layer})
      
    print("Found {} convolutional layers".format(num_layers))
    return conv_layers

  def get_layer_info(self, layer_name=None):

    '''
    Displays imformation of a layer 

    Args:
        layer_name (str): Name of the layer whose information is needed
    '''

    name = layer_name
    layer = self.conv_layers[layer_name]

    num_filters = layer.kernel.shape[3]
    filter_w = layer.kernel.shape[0]
    filter_h = layer.kernel.shape[1]
    num_channels = layer.kernel.shape[2]
    
    print("Found: Layer name: {} | Kernel info: {} filters of size ({} X {}) with {} channels".format(name,num_filters,filter_w,filter_h,num_channels))
    
  def get_feature_maps(self, image_path):

    '''
    Obtain feature maps generated on an image 

    Args:
        image_path (str): Path of the image whose feature maps are needed
    '''

    target_size = (self.model.layers[0].input.shape[1], self.model.layers[0].input.shape[2])
    img = load_img(image_path, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    outputs = [layer.output for layer in self.conv_layers.values()]
    model_temp = Model(inputs=self.model.inputs, outputs=outputs)
    self.fmaps = model_temp.predict(img)

  def visualize_kernel(self, layer_name='conv_1d',filter_id=0, channel_id=0, num_channels=1, cmap='gray', return_kernel=False):

    '''
    Visualize kernel weights of a given layer 

    Args:
        layer_name (str): Name of the layer whose feature map is needed
        filter_id (int): Filter that needs to be visualized
        channel_id (int): Channel that needs to be visualized
        num_channels (int): Number of channels to be displayed at once
        cmap (str): CMAP used for displaying image
        return_kernel (bool): Whether the kernel needs to be returned
    
    Returns:
        Kernel specified by the paramters if return_kernel is True.
    '''

    layer = self.conv_layers[layer_name]
    self.get_layer_info(layer_name)

    kernels = layer.get_weights()[0]

    if filter_id >= layer.kernel.shape[3] or channel_id >= layer.kernel.shape[2]:
       return
    
    if num_channels == 1:
      kernel = kernels[:,:,:,filter_id][:,:,channel_id]
    else:
      kernel = kernels[:,:,:,filter_id][:,:,channel_id:(channel_id+num_channels)]

    if (kernel.max() - kernel.min()) != 0:
      kernel = (kernel - kernel.min())/(kernel.max()-kernel.min())
    
    if return_kernel:
      return kernel
    
    num_rows = int(num_channels/4)
    num_cols = min(4, int(layer.kernel.shape[2]))

    print("")
    
    fig = plt.figure(figsize=(4*num_cols,4*num_rows))

    gs = gridspec.GridSpec(num_rows, num_cols)
    
    fig.subplots_adjust(top=0.88)
    fig.suptitle("Filter id: "+str(filter_id), fontsize=16)
    fig.tight_layout()

    for i in range(kernel.shape[2]):
      channel = kernel[:,:,i]
      ax = plt.subplot(gs[i])
      plt.axis('on')
      ax.set_title("Channel id: "+str(channel_id+i),wrap=True)
      ax.set_xticklabels([])
      ax.set_yticklabels([])
      ax.set_aspect('equal')
      ax.imshow(channel, cmap=cmap)

    plt.show()

    if num_channels == 1:
      plt.title("Filter id: "+str(filter_id)+" | Channel id: "+str(channel_id),wrap=True)
      plt.imshow(kernel,cmap=cmap)
      plt.show()

  def visualize_image(self, layer_name='conv_1d', channel_id=0, num_channels=1, cmap='gray', return_fmap=False):

    '''
    Visualize a feature map given an image 

    Args:
        layer_name (str): Name of the layer whose feature map is needed
        channel_id (int): Channel that needs to be visualized
        num_channels (int): Number of channels to be displayed at once
        cmap (str): CMAP used for displaying image
        return_fmap (bool): Whether the feature map needs to be returned
    
    Returns:
        Feature map specified by the paramters if return_fmap is True.
    '''

    layer = self.conv_layers[layer_name]
    self.get_layer_info(layer_name)
    
    if channel_id >= layer.output.shape[3]:
        return
    
    layer_id = list(self.conv_layers.keys()).index(layer_name)

    if num_channels == 1:
      fmap = self.fmaps[layer_id][0,:,:,channel_id]
    else:
      fmap = self.fmaps[layer_id][0,:,:,channel_id:(channel_id+num_channels)]
    
    if return_fmap:
      return fmap

    num_rows = int(num_channels/4)
    num_cols = min(4, layer.output.shape[3])

    print("")
    
    fig = plt.figure(figsize=(4*num_cols,4*num_rows))

    gs = gridspec.GridSpec(num_rows, num_cols)
    
    fig.subplots_adjust(top=0.88)
    fig.tight_layout()

    for i in range(fmap.shape[2]):
      channel = fmap[:,:,i]
      ax = plt.subplot(gs[i])
      plt.axis('on')
      ax.set_title("Filter id: "+str(channel_id+i),wrap=True)
      ax.set_xticklabels([])
      ax.set_yticklabels([])
      ax.set_aspect('equal')
      ax.imshow(channel, cmap=cmap)

    plt.show()

    if num_channels == 1:
      plt.title("Filter id: "+str(channel_id),wrap=True)
      plt.imshow(fmap,cmap=cmap)
      plt.show() 

  def store_kernels(self, path='kernels', cmap='gray'):

    '''
    Store kernel weights as images 

    Args:
        path (str): Path to the directory where the images need to be stored
        cmap (str): The CMAP used for the images
    '''

    for layer_name, layer in self.conv_layers.items():
      layer_path = os.path.join(path, layer_name) 
      os.mkdir(layer_path)
      
      num_filters = layer.kernel.shape[3]
      num_channels = layer.kernel.shape[2]
      
      for f_id in range(num_filters):
        f_path = os.path.join(layer_path, 'feature_'+str(f_id))
        os.mkdir(f_path)
        for ch_id in range(num_channels):
          kernel = self.visualize_kernel(layer_name=layer_name,filter_id=f_id, channel_id=ch_id, cmap=cmap, return_kernel=True)
          fig_path = f_path + '/channel_' + str(ch_id) + '.png'
          plt.imsave(fname=fig_path, arr=kernel, cmap=cmap)

  def store_feature_maps(self, path='fmaps', cmap='gray'):

    '''
    Stores the feature maps generated by the model on an input image 

    Args:
        path (str): Path to the directory where the feature maps need to be stored
        cmap (str): The CMAP used for the images
    '''

    for layer_name, layer in self.conv_layers.items():
      layer_path = os.path.join(path, layer_name) 
      os.mkdir(layer_path)
      
      num_channels = layer.output.shape[3]
      
      for ch_id in range(num_channels):
        fmap = self.visualize_image(layer_name=layer_name, channel_id=ch_id, cmap=cmap, return_fmap=True)
        fig_path = layer_path + '/channel_' + str(ch_id) + '.png'
        plt.imsave(fname=fig_path, arr=fmap, cmap=cmap)

  def handle_layer_change(self,change):
    clear_output()

    layer = self.conv_layers[change.new]
    self.filters.value = 0
    self.channels.value = 0
    self.filters.max = (layer.kernel.shape[3]-1)
    self.channels.max = (layer.kernel.shape[2]-1)
    self.num_channels.value = 4
    
    interact(self.visualize_kernel,layer_name=self.layers_by_name, filter_id=self.filters, channel_id=self.channels, num_channels=self.num_channels, cmap=self.cmap, return_kernel=fixed(False))
    
  def handle_num_channels_change(self, change):
    self.channels.step = change.new
    
  def handle_layer_change_image(self,change):
    clear_output()

    layer = self.conv_layers[change.new]
    self.filters.value = 0
    self.filters.max = (layer.output.shape[3]-1)
    self.num_channels.value = 4

    interact(self.visualize_image,layer_name=self.layers_by_name, channel_id=self.filters, num_channels=self.num_channels, cmap=self.cmap, return_fmap=fixed(False))
  
  def handle_num_channels_change_image(self, change):
    self.filters.step = change.new
    
  def visualize_kernels(self, store_path=None):

    '''
    Visualize weights of kernels in the model

    Args:
        store_path (str): Path to the directory where the feature visuals need to be stored

    Returns:
        Interactive Ipython widget displaying kernel weights.
    '''

    if (not self.is_notebook) or (store_path is not None): 
      self.store_kernels(path=store_path)
      return

    self.layers_by_name = widgets.Dropdown(options=self.conv_layers.keys(), value=list(self.conv_layers.keys())[0], description='Layer')
    layer = self.conv_layers[self.layers_by_name.value]
    self.filters = widgets.IntSlider(value=0, min=0, max=(layer.kernel.shape[3]-1), step=1, description='Filter')
    self.channels = widgets.IntSlider(value=0, min=0, max=(layer.kernel.shape[2]-1), step=4, description='Channel')
    self.num_channels = widgets.IntSlider(value=4, min=4, max=20, step=4, description='# Channels')
    self.cmap = widgets.Dropdown(options=['viridis','gray'], value='gray', description='CMAP')
    self.layers_by_name.observe(self.handle_layer_change, 'value')
    self.num_channels.observe(self.handle_num_channels_change, 'value')
    
    interact(self.visualize_kernel,layer_name=self.layers_by_name, filter_id=self.filters, channel_id=self.channels, num_channels=self.num_channels, cmap=self.cmap, return_kernel=fixed(False))

  def visualize_feature_maps(self, image_path, store_path=None):

    '''
    Visualize the feature maps given an image 

    Args:
        image_path (str): Path to the image
        store_path (str): Path to the directory where the feature maps need to be stored

    Returns:
        Interactive Ipython widget displaying feature maps.
    '''
    
    self.get_feature_maps(image_path)

    if (not self.is_notebook) or (store_path is not None): 
      self.store_feature_maps(path=store_path)
      return
    
    self.layers_by_name = widgets.Dropdown(options=self.conv_layers.keys(), value=list(self.conv_layers.keys())[0], description='Layer')
    layer = self.conv_layers[self.layers_by_name.value]
    self.num_channels = widgets.IntSlider(value=4, min=4, max=20, step=4, description='# Filters')
    self.filters = widgets.IntSlider(value=0, min=0, max=(layer.output.shape[3]-1), step=4, description='Filter')
    self.cmap = widgets.Dropdown(options=['viridis','gray'], value='gray', description='CMAP')
    
    self.layers_by_name.observe(self.handle_layer_change_image, 'value')
    self.num_channels.observe(self.handle_num_channels_change_image, 'value')
    
    interact(self.visualize_image,layer_name=self.layers_by_name, channel_id=self.filters, num_channels=self.num_channels, cmap=self.cmap, return_fmap=fixed(False))