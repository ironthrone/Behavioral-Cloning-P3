from keras.models import load_model
from keras.utils import vis_utils

model = load_model('model.h5')
model.summary()

vis_utils.plot_model(model,'model.png',show_layer_names=True,
                     show_shapes=True)