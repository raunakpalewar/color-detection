# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import ImageUploadSerializer
# from PIL import Image
# import numpy as np
# from sklearn.cluster import KMeans

# class ColorAPIView(APIView):

#     def post(self, request):
#         serializer = ImageUploadSerializer(data=request.data)

#         if serializer.is_valid():
#             image = serializer.validated_data['image']

#             # Open the image
#             img = Image.open(image)

#             # Convert the image to a NumPy array
#             img_np = np.array(img)

#             print("Shape of img_np:", img_np.shape)  # Debugging line

#             # Reshape the array to a list of RGB values
#             pixels = img_np.reshape(-1, 3)

#             # Perform K-Means clustering to find dominant colors
#             kmeans = KMeans(n_clusters=5, random_state=0).fit(pixels)
#             cluster_centers = kmeans.cluster_centers_

#             # Convert RGB values to hexadecimal
#             hex_colors = ['#%02x%02x%02x' % tuple(map(int, color)) for color in cluster_centers]

#             # Get the count of pixels in each cluster
#             counts = np.bincount(kmeans.labels_)

#             # Prepare response data
#             color_info = [{'hex_code': hex_colors[i], 'count': counts[i]} for i in range(len(hex_colors))]

#             return Response(color_info, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ColorAPIView(APIView):

#     def post(self, request):
#         serializer = ImageUploadSerializer(data=request.data)

#         if serializer.is_valid():
#             image = serializer.validated_data['image']

#             # Open the image
#             img = Image.open(image)

#             # Get the RGB values
#             rgb_values = list(img.getdata())

#             # Count the occurrence of each color
#             counts = Counter(rgb_values)

#             if not counts:
#                 return Response({"error": "Image is empty or could not be processed."}, status=status.HTTP_400_BAD_REQUEST)

#             # Get the most common color
#             most_common_color = max(counts, key=counts.get)

#             if not isinstance(most_common_color, tuple):
#                 most_common_color = (most_common_color, most_common_color, most_common_color)

#             # Convert RGB values to hexadecimal
#             hex_code = '#{0:02x}{1:02x}{2:02x}'.format(most_common_color[0], most_common_color[1], most_common_color[2])

#             # Prepare response data
#             color_info = [{'hex_code': hex_code, 'count': counts[most_common_color]}]

#             return Response(color_info, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from PIL import Image
from collections import Counter
import requests
from io import BytesIO
import webcolors



class ColorAPIView(APIView):

    def post(self, request):
    
        serializer = ImageURLSerializer(data=request.data)

        if serializer.is_valid():
            image_url = serializer.validated_data['image_url']

            try:             
                response = requests.get(image_url)
                response.raise_for_status()

                img = Image.open(BytesIO(response.content))

                rgb_values = list(img.getdata())

                counts = Counter(rgb_values)

                if not counts:
                    return Response({"error": "Image is empty or could not be processed." }, status=status.HTTP_400_BAD_REQUEST)

                most_common_color = max(counts, key=counts.get)

                if not isinstance(most_common_color, tuple):
                    most_common_color = (most_common_color, most_common_color, most_common_color)

                # Convert RGB values to hexadecimal
                hex_code = '#{0:02x}{1:02x}{2:02x}'.format(most_common_color[0], most_common_color[1], most_common_color[2])

                # Prepare response data
                
                try:
                    color_name = webcolors.hex_to_name(hex_code)
                    print(f"The color name for {hex_code} is {color_name}")
                except ValueError:
                    print(f"No matching color name found for {hex_code}")
                
                color_info = [{'hex_code': hex_code, 'count': counts[most_common_color]}]
                return Response(color_info, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException:
                return Response({"error": "Failed to fetch image from the provided URL."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    