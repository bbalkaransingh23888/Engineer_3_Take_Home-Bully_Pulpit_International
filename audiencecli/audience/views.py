from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from .forms import AudienceForm
from .models import Audience
from django.http import HttpResponse, JsonResponse
import pandas as pd
import numpy as np
from src.reach_efficiency_by_zipcode import get_efficiency_stats, get_reach_efficiency
import logging
# Create your views here.

logger = logging.getLogger(__name__)

# handle uploading csv files to django
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = AudienceForm(request.POST, request.FILES)
        # save the file if it's a valid form, 
        # otherwise send a message that the upload failed or the request is invalid
        if form.is_valid():
            audience = form.save()
            return JsonResponse({'id': audience.id})
        else:
            logger.error("Form is not valid: %s", form.errors)
            return JsonResponse({'error': 'Failed to upload file'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# log if the upload was successful
def success(request):
    return HttpResponse('Upload successful')


# handle processing of the data in each file so as to log the information and be able to chart it
def process(file_path):
    try:
        raw_data_file = pd.read_csv(file_path)
        processed_data_file = get_efficiency_stats(raw_data_file)
        output = get_reach_efficiency(processed_data_file, 0.5)
        return processed_data_file, output
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return None, None
    
# handle converting the data to serializable data, 
# resolves previous object not jsonserializable error
# caused by pandas using numpy data types 
def convert_to_serializable(data):
    if isinstance(data, pd.Series):
        return data.tolist()
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='list')
    if isinstance(data, (pd.Timestamp, pd.Timedelta)):
        return str(data)
    if isinstance(data, (np.integer, np.floating, np.bool_)):
        return data.item()
    return data

# get the stats from the parsed data files
def get_stats(request, id):
    try:
        file = get_object_or_404(Audience, id=id)
        
        processed_data, stats = process(file.file.path)

        if processed_data is None or stats is None:
            return JsonResponse({"error": "Failed to process file"})
        
        # verify data structure so the data can be displayed as accurately as possible
        logger.debug(f"Processed Data Columns: {processed_data.columns}")
        logger.debug(f"Processed Data Head: {processed_data.head()}")
        labels = processed_data['ZIPCODE'].tolist(),
        data = processed_data['CUMULATIVE_PCT_REACH'].tolist()

        # flatten the labels array; fixes previous issue where the labels were being returned as an embedded array
        # which caused the data to be displayed incorrectly in the chart
        if isinstance(labels[0], list):
            labels = [label for sublist in labels for label in sublist]
        
        logger.debug(f"Labels: {labels}")
        logger.debug(f"Data: {data}")

        response_data = {
            "labels": labels,
            "data": data,
            "zipcode": convert_to_serializable(stats['zipcode_number']),
            "audience_reach": convert_to_serializable(stats['audience_reach']),
            "total_reach": convert_to_serializable(stats['total_reach']),
            "pct_rech": convert_to_serializable(stats['pct_reach']),
            "target_density": convert_to_serializable(stats['target_density']),
        }
        return JsonResponse(response_data)
    # handle edge cases for if either there is no audience object or otherwise there's an issue getting the stats
    except Audience.DoesNotExist:
        logger.error(f"Audience object with id {id} does not exist")
        return JsonResponse({'error': 'Audience does not exist'}, status=404)
    except Exception as e:
        logger.error(f"Error getting stats from file with id {id}: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
