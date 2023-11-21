
from django.urls import include, path
import os

# Get the current directory path
current_directory = os.path.dirname(__file__)

# Add other URL patterns specific to this file
urlpatterns = [
    # Your URL patterns here
]

# Iterate over all files in the current directory
for filename in os.listdir(current_directory):
    # Exclude the current file itself
    if filename != os.path.basename(__file__):
        # Check if the file is a Python module
        if filename.endswith('.py'):
            # Remove the file extension to get the module name
            module_name = os.path.splitext(filename)[0]
            # Import the module dynamically
            module = __import__(module_name, fromlist=['urlpatterns'])
            # Add the module's urlpatterns to the main urlpatterns
            urlpatterns += module.urlpatterns


