from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Googly Eyes"
    version: str = "0.0.0"
    predictor_path: str = "models/shape_predictor_68_face_landmarks.dat"
    max_image_dimension: int = 1200
    debug: bool = False


settings = Settings()
