from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
import os
from django.conf import settings
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np



def index(request):
    return render(request, "index.html")


def gen(text):
    api_key = settings.API_KEY

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(f"""I will give you the input related to sea creature or plant tell facts about it in a
    paragraph, just give the paragraph, dont give any heading or list

     Now input:- {text}
    """)

    return response.text


def predict(path):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("models/keras_Model.h5", compile=False)

    # Load the labels
    class_names = open("labels/labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name[2:], end="")
    # print("Confidence Score:", confidence_score)
    ans = f"{class_name[2:]}"
    return ans


def getinfo(text):
    api_key = settings.API_KEY


    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(f"""I will give you the input related to sea creature or plant give answer to the question in a
        paragraph, just give the paragraph, dont give any heading or list

         Now input:- {text}
        """)

    return response.text

@csrf_exempt
def details(request):
    global uploaded_query
    ans = None

    if request.method == 'POST':
        uploaded_query = request.POST["query"]
        ans = getinfo(uploaded_query)

    params = {"ans": ans, "question": uploaded_query}
    return render(request, "details.html", params)


@csrf_exempt
def getdata(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        # Process the uploaded file
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'upload')
        os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
        filename = f'uploaded_file-{random.randint(1, 1000)}-{random.randint(444, 894)}-{random.randint(999, 9999)}.jpg'
        path = os.path.join(upload_dir, filename)

        with open(path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        ans = predict(path)

        detail = gen(ans)
        filename = os.path.basename(path)
        final_path = f"../media/upload/{filename}"
        params = {"img_path": final_path, "detail": detail, "topic": ans}

        return render(request, "facts.html", params)


def contact(request):
    return render(request, "contact.html")


def topicsd(request):
    return render(request, "topics-detail.html")


def topicsl(request):
    return render(request, "topics-listing.html")
