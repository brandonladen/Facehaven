import os
import tempfile
import cv2
from django.shortcuts import render, redirect
import numpy as np
from picApp.models import MissingChild, FoundPerson
from picApp.forms import MissingChildForm, FoundPersonForm
from deepface import DeepFace
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.images import ImageFile
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# from picSearch import settings

from django.conf import settings
import os

from django.core.files.storage import default_storage

#from django.core.files.storage import default_storage
@login_required
def submit_child(request): #missing person
    if request.method == 'POST':
        form = MissingChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            image_name = request.FILES['image'].name
            image_path = os.path.join('missing_children', image_name)
            image = os.path.join(settings.MEDIA_ROOT, image_path)

            # Create the missing_children directory if it doesn't exist
            if not os.path.exists(os.path.dirname(image)):
                os.makedirs(os.path.dirname(image))

            # Save the image file using default_storage
            image_file = request.FILES['image']
            default_storage.save(image_path, image_file)

            child.image.name = image_path
            child.image._committed = True  # Mark the image as committed

            # Generate the image encoding
            image_encoding = DeepFace.represent(img_path=image, model_name='Facenet', enforce_detection=False)
            child.image_encoding = np.array(image_encoding).tobytes()
            child.save()
            # logout(request)
            #give message then logout button
            return redirect('feedback')
    else:
        form = MissingChildForm()

    return render(request, 'submit_child.html', {'form': form})
@login_required
def found_person(request):# found person
    if request.method == 'POST':
        form = FoundPersonForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            image_name = request.FILES['image'].name
            image_path = os.path.join('missing_children', image_name)
            image = os.path.join(settings.MEDIA_ROOT, image_path)

            # Create the missing_children directory if it doesn't exist
            if not os.path.exists(os.path.dirname(image)):
                os.makedirs(os.path.dirname(image))

            # Save the image file using default_storage
            image_file = request.FILES['image']
            default_storage.save(image_path, image_file)

            child.image.name = image_path
            child.image._committed = True  # Mark the image as committed

            # Generate the image encoding
            image_encoding = DeepFace.represent(img_path=image, model_name='Facenet', enforce_detection=False)
            child.image_encoding = np.array(image_encoding).tobytes()
            child.save()
            #give message then logout button
            # logout(request)
            return redirect('feedback')
    else:
        form = FoundPersonForm()

    return render(request, 'found.html', {'form': form})
@login_required
def search_child(request):
    if request.method == 'POST':
        # image = request.FILES['image']
        image_url = request.POST.get('image')
        if image_url:
            # Fetch the image data from the URL
            try:
                response = requests.get(image_url)
                response.raise_for_status()  # Raise an error for bad status codes
                image_data = response.content
            except requests.RequestException as e:
                print("Error fetching image data:", e)
        # Save the uploaded image to a temporary file
        temp_image = tempfile.NamedTemporaryFile(delete=False)
        temp_image.write(image_data)
        temp_image.flush()

        # # Perform face detection on the image
        # try:
        #     detected_faces = DeepFace.extract_faces(temp_image.name, enforce_detection=True)
        # except ValueError as e:
        #     # Clean up the temporary file
        #     temp_image.close()
        #     os.unlink(temp_image.name)

        #     return render(request, 'search_child.html', {'error': 'No face detected. Please upload an image with a face.'})

        missing_children = MissingChild.objects.all()
        similar_children = []

        for child in missing_children:
            child_image_path = os.path.join(settings.MEDIA_ROOT, child.image.name)

            # Perform similarity verification only if a face is detected
            similarity = DeepFace.verify(temp_image.name, child_image_path, model_name='Facenet', distance_metric='euclidean_l2', enforce_detection=False)
            if similarity['verified']:
                distance = similarity['distance']
                distance = float(distance)
                similarity_percentage = round(1 / (1 + distance) * 100, 2)
                if similarity_percentage > 60:
                    similar_children.append((child, similarity_percentage))

        # Clean up the temporary file
        temp_image.close()
        os.unlink(temp_image.name)

        # Sort the similar children by similarity percentage in reverse order
        similar_children.sort(key=lambda x: x[1], reverse=True)

        context = {'similar_children': similar_children}
        return render(request, 'search_results.html', context)

    return render(request, 'search_child.html')

def home(request):
    return render(request, 'picApp/home.html')

@login_required
def admin_dashboard(request):
    MissingPeople = MissingChild.objects.filter(isverified=False).count()
    FoundPeople = FoundPerson.objects.filter(isverified=False).count()
    RP1 = MissingChild.objects.filter(isverified=True).count()
    RP2 = FoundPerson.objects.filter(isverified=True).count()
    ReunitedPersons = RP1 + RP2
    TotalPersons = MissingPeople + FoundPeople + ReunitedPersons
    
    # Check if TotalPersons is zero to avoid division by zero
    if TotalPersons == 0:
        MissingPeople_percentage = 0
        FoundPeople_percentage = 0
        ReunitedPersons_percentage = 0
    else:
        MissingPeople_percentage = round((MissingPeople / TotalPersons) * 100, 2)
        FoundPeople_percentage = round((FoundPeople / TotalPersons) * 100, 2)
        ReunitedPersons_percentage = round((ReunitedPersons / TotalPersons) * 100, 2)
    
    context = {
        'MissingPeople_percentage': MissingPeople_percentage,
        'FoundPeople_percentage': FoundPeople_percentage,
        'ReunitedPersons_percentage': ReunitedPersons_percentage
    }
    return render(request, 'picApp/dashboard.html', context)


@login_required
def case_cart(request):
    cases = MissingChild.objects.filter(isverified=False)
    return render(request,'picApp/cart.html', {"cases":cases})

@login_required
def found_person_cart(request):
    case = FoundPerson.objects.filter(isverified=False)
    return render(request,'picApp/found-cart.html', {"case":case})

@login_required
def verified_profile(request):
    missing_children = MissingChild.objects.filter(isverified=True)
    found_persons = FoundPerson.objects.filter(isverified=True)

    verified_cases = list(missing_children) + list(found_persons)
    
    return render(request, 'picApp/verified-cases.html', {"cases": verified_cases})

@login_required
def verify_case(request, case_id):
    case = MissingChild.objects.get(pk=case_id)
    case.isverified = True
    case.save()
    
    return render(request, 'picApp/verify.html', {'case': case})

@login_required
def verify_found_persons(request, case_id):
    case = FoundPerson.objects.get(pk=case_id)
    case.isverified = True
    case.save()
    
    return render(request, 'picApp/verify-found.html', {'case': case})

def delete_complaint(request, copm_id):
    complaint = None
    if MissingChild.objects.filter(pk=copm_id).exists():
        complaint = get_object_or_404(MissingChild, pk=copm_id)
    elif FoundPerson.objects.filter(pk=copm_id).exists():
        complaint = get_object_or_404(FoundPerson, pk=copm_id)
    
    if complaint:
        complaint.delete()
        # Successfully deleted
    
    return redirect('admin_dashboard')

@login_required
def feedback(request):
    return render(request, 'picApp/feedback.html')