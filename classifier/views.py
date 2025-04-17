# classifier/views.py
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.utils import load_img, img_to_array # type: ignore
import numpy as np
import tensorflow as tf

# Load the model once when the server starts
model_path = os.path.join(settings.BASE_DIR, 'classifier', 'Chest_Recog_Model.h5')
model = load_model(model_path)

flower_names = ['Lung_Opacity', 'Normal', 'Pneumonia', 'Pneumonia-Viral']

@csrf_exempt
def classify_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Save the uploaded image temporarily
        uploaded_image = request.FILES['image']
        temp_image_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.name)
        with open(temp_image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        # Preprocess the image
        input_image = load_img(temp_image_path, target_size=(180, 180))
        input_image_array = img_to_array(input_image)
        input_image_exp_dim = tf.expand_dims(input_image_array, 0)

        # Make predictions
        predictions = model.predict(input_image_exp_dim)
        result = tf.nn.softmax(predictions[0])
        predicted_class = flower_names[np.argmax(result)]
        confidence_score = np.max(result) * 100

        # Clean up the temporary file
        os.remove(temp_image_path)

        # Return the result as JSON
        return JsonResponse({
            'class': predicted_class,
            'confidence': f'{confidence_score:.2f}%'
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)