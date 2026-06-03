
# AI Media Generator

AI Media Generator is a Python application that generates multimedia content based on user prompts. It uses the following capabilities:
- **OpenAI GPT** for text generation.
- **Google Cloud Text-to-Speech** for audio narration.
- **DALL·E** for image generation.
- **MoviePy** for combining images and audio into a video.

## Features
1. **Text Generation**: Generate stories or scripts based on user prompts.
2. **Scene Division**: Automatically splits generated text into scenes.
3. **Image Creation**: Generates one image per scene using DALL·E.
4. **Audio Narration**: Converts the full story into audio using Google Text-to-Speech.
5. **Video Creation**: Combines images and audio into a cohesive video.

## YouTube Channel

Some of the generated videos will be uploaded to our YouTube channel:
[Little Story Explorers](https://www.youtube.com/@LittleStoryExplorers-c2c)

Subscribe to watch the stories come to life!


---

## Installation

### Prerequisites
- Python 3.10+
- Google Cloud account with Text-to-Speech API enabled.
- OpenAI API key for GPT and DALL·E access.
- FFmpeg installed (for MoviePy and Pydub).


### Run the Setup Script
Run the provided setup script to install dependencies and set up the environment:
```bash
 ENV_NAME=ai-media-env PYTHON_VERSION=3.10 PROJECT_NAME=ai-media-generator ./setup.sh
```

This script will:
1. Install Python dependencies using Poetry.
2. Verify your environment variables for OpenAI and Google Cloud credentials.
3. Check if FFmpeg is installed.

---

## Usage
Run the main script:
```bash
poetry run python -m ai_media_generator.main
```

1. Enter a story prompt when prompted.
2. The application will:
   - Generate text based on your prompt.
   - Split the text into scenes.
   - Generate images for each scene.
   - Create audio narration for the full text.
   - Combine images and audio into a video.
3. The video will be saved in `assets/video/output.mp4`.

---

## Directory Structure
```
ai-media-generator/
├── ai_media_generator/
│   ├── main.py                # Main script
│   ├── utils.py               # Utility functions
├── assets/
│   ├── audio/                 # Generated audio files
│   ├── images/                # Generated images
│   ├── video/                 # Generated videos
├── setup.sh                   # Setup script
├── .env                       # Environment variables (not tracked by Git)
├── README.md                  # Project README
```

---

## Troubleshooting
1. **Error: `FileNotFoundError: 'ffprobe'`**
   Ensure FFmpeg is installed and available in your system PATH.

2. **OpenAI Errors**
   - Check your OpenAI API key and ensure your account has sufficient credits.
   - Verify that you have access to the required models (e.g., GPT-4 and DALL·E).

3. **Google TTS Errors**
   - Ensure your Google Cloud credentials file is correct and the API is enabled.

---

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to your fork (`git push origin feature-branch`).
5. Open a pull request.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgements
- [OpenAI GPT](https://openai.com/)
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech)
- [DALL·E](https://openai.com/dall-e/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Pydub](https://github.com/jiaaro/pydub)

## Deployment

Quick steps to build and run locally with Docker:

```bash
# build image
docker build -t ai-media-generator:latest .

# run container (exposes Streamlit on 8501)
docker run -p 8501:8501 --env-file .env -v "$PWD/assets:/app/assets" ai-media-generator:latest
```

CI: A GitHub Actions workflow is included at `.github/workflows/docker-publish.yml` to build and push a Docker image to GitHub Container Registry (`ghcr.io`). Set the `GITHUB_TOKEN` secret (automatically provided) and enable packages for your repo.

For Heroku: push this repo to a Heroku app (the included `Procfile` runs the Streamlit app).

To push these changes to GitHub from your local machine:

```bash
# initialize git (if needed)
git init
git add .
git commit -m "Add Docker + CI deployment files"
# add your remote (replace URL)
git remote add origin git@github.com:USERNAME/REPO.git
git branch -M main
git push -u origin main
```

GitHub Actions secrets for Docker Hub (optional):
- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a Docker Hub access token (create on Docker Hub)

The existing workflow pushes images to GitHub Container Registry (`ghcr.io`) using the repository token automatically. If you set the Docker Hub secrets, the workflow will also push an image to Docker Hub.
