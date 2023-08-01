import sys
from pathlib import Path

# Add the parent directory of the current file to the system path
current_file = Path(__file__).resolve()
parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))

from model.recommender import recommend
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def movie_recommendation(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        
        # Call the recommend function with the movie_name
        recommendations = recommend(movie_name)

        if len(recommendations)==0:
            return HttpResponse("Sorry, the movie is currently not available in our database.")
        
        if recommendations:
            # Render the recommended movies in a template
            return render(request, 'recommendations.html', {'recommendations': recommendations})
        else:
            # Return a response indicating that the movie is not available
            return HttpResponse("Sorry, the movie is currently not available in our database.")
    
    # Render the form template for the user to input a movie name
    return render(request, 'movie_input.html')




