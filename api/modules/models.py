from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

def create_nn_model(input_dim):
    """
    Fonction pour créer et compiler un modèle de réseau de neurones simple.
    """
    model = Sequential([
        Input(shape=(input_dim,), name=f'input_{input_dim}f'),
        Dense(64, activation='relu', name='dense_1'),
        Dense(32, activation='relu', name='dense_2'),
        Dense(1, name='output')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def create_nn_model_based_on(base_model, input_dim):
    """
    Fonction pour créer un modèle de réseau de neurones basé sur un modèle existant.
    """
    new_model = Sequential([
        Input(shape=(input_dim,), name=f'input_{input_dim}f'),
        Dense(64, activation='relu', name='dense_1'),
        Dense(32, activation='relu', name='dense_2'),
        Dense(1, name='output')
        ])

    for layer in new_model.layers:
        try:
            old_layer = base_model.get_layer(layer.name)
            layer.set_weights(old_layer.get_weights())
            print(f"✅ Poids transférés pour : {layer.name}")
        except ValueError:
            print(f"⛔ Incompatible ou nouvelle couche : {layer.name}")

    new_model.compile(optimizer='adam', loss='mse')

    return new_model

def train_model(model, X, y, X_val=None, y_val=None, epochs=30, batch_size=32, validation_split=0.2, verbose=0 ):
    hist = model.fit(X, y, 
                validation_data=(X_val, y_val) if X_val is not None and y_val is not None else None,
                epochs=epochs, batch_size=batch_size, 
                validation_split=validation_split, verbose=verbose)
    return model , hist

def model_predict(model, X):
    y_pred = model.predict(X).flatten()
    return y_pred