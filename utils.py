import numpy as np
from PIL import Image


# ==========================================
# IMAGE PREPROCESSING
# ==========================================

def preprocess_image(image, target_size=(128, 128)):
    """
    Resize and preprocess image for prediction.
    """

    image = image.resize(target_size)
    image = np.array(image)

    # RGBA -> RGB
    if image.shape[-1] == 4:
        image = image[:, :, :3]

    image = image.astype("float32") / 255.0

    image = np.expand_dims(image, axis=0)

    return image


# ==========================================
# PREDICTION
# ==========================================

def predict_disease(model, image, class_names):
    """
    Predict disease using trained model.
    """

    processed_image = preprocess_image(image)

    prediction = model.predict(
        processed_image,
        verbose=0
    )

    predicted_index = np.argmax(prediction)

    confidence = float(np.max(prediction) * 100)

    disease = class_names[predicted_index]

    return disease, confidence, prediction
