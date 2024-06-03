FROM python:3.12.3-slim as deps

# Build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential cmake pipx

# Install Poetry
RUN pipx install poetry==1.8.3 && pipx inject poetry poetry-plugin-bundle

# Add Poetry binary dir to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Poetry files
WORKDIR /app
COPY README.md ./
COPY poetry.lock pyproject.toml ./

# Create virtualenv
RUN poetry bundle venv --python=/usr/local/bin/python3 --only=main /api/venv


FROM python:3.12.3-slim

ENV PATH="/api/venv/bin:$PATH"
ENV PREDICTOR_PATH="/api/models/shape_predictor_68_face_landmarks.dat"

RUN apt-get update && apt-get install --no-install-recommends -y cmake ffmpeg libsm6 libxext6

COPY --from=deps /api/venv/ /api/venv/
COPY app /api/app
COPY models /api/models/
WORKDIR /api
CMD ["fastapi", "run", "--app", "app", "--proxy-headers", "--port", "80"]