# Googly Eyes

A web application that transforms a user uploaded photo by replacing all eyes with googly eyes.

## Requirements

- Python 3.12.3
- Poetry
- Docker


## Running

Install dependencies:

```bash
poetry install --sync
``` 

Run tests:

```bash
pytest
``` 

Run FastAPI:

```bash
fastapi dev --app app
# Navigate to: http://127.0.0.1:8000/docs
``` 

Build Docker container:

```bash
docker build -t googlyeyes:0.0.0 .
```

Run Docker container:

```bash
docker run --rm -p 18080:80 googlyeyes:0.0.0
# Navigate to: http://localhost:18080/docs
```

## Project Structure

```bash
.
├── app
│     ├── api
│     │     ├── __init__.py
│     │     ├── health.py ~ heartbeat route
│     │     ├── routes.py ~ router
│     │     └── transform.py ~ googly eyes route
│     ├── core
│     │     ├── __init__.py
│     │     ├── config.py ~ configuration
│     │     └── lifespan.py ~ pre-loads heavy services so that they are only instantiated once
│     ├── main.py ~ entrypoint to app
│     └── service
│         ├── __init__.py
│         └── googly.py ~ service that replaces eyes with googly eyes
├── tests ~ tests
├── images ~ directory of images downloaded from Google
├── models ~ pre-trained model files
├── poetry.lock ~ Poetry dependency management
├── pyproject.toml ~ Poetry dependency management
├── research.ipynb ~ notebook used to develop googly eyes
└── Dockerfile ~ Docker manifest
```


## My Approach

* Since I had limited time I decided to limit the scope of the task to:
  * Only accepting JPEG images. 
  * Only accepting images with a max height or width of 1200 pixels.
* Eye tracking / detection is a well known problem, instead of creating a model from scratch I searched online for
  pre-trained models.
  * I found two approaches and I evaluated both in `research.ipynb`. I only implemented one, the DLIB approach.
  * I could not find a dataset that was exactly to my needs: contains one face, multiple faces and no faces.
  * I created my own with Google Images.
* My approach to adding googly eyes was to draw them as a filled ellipse and circle for the pupil.
* The API was designed to be deployable to Kubernetes.
  * This would make it quite easy to deploy.
  * It can be scaled horizontally.
  * I added a Dockerfile and a health route.

## Improvements

If I had more time, things I would have liked to have done:

* A different approach to drawing googly eyes would have been to save a set of googly eyes.
  Then re-size and interpolate them onto the image in the correct location. I would have liked to experiment with
  this approach and see if the results were better.
* One of the requirements was to randomize the orientation of the pupil, this could be done by moving the center
  of the pupil while ensuring it is within the bounds of the outer ellipse.
* More thorough unit testing:
  * I check if the image is different to establish if eyes were added correctly. Something more intelligent might be to
    check the image at the specific eye parts to see if eyes were added.
  * Similarly, my eye detecting tests count the length of eyes detected. Something more intelligent would check their
    location also, e.g. creating a bounding box of an acceptable point and testing to see if the center of the eye
    was in that point.
* Creating a larger and more diverse dataset. My dataset was very small, possibly my choice of approach would have 
  changed if evaluated on a larger and more diverse dataset.
  * The main motivation for limiting my scope to JPEG images with a max height or width of 1200 pixels was because this
    was what my dataset consisted of.
    * To support larger dimensions the dataset could have been copied and re-sized.
    * Similarly, copied and converted to other formats and then tested.

