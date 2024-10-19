# Installation guide osx

1. Install conda at [Conda](https://docs.anaconda.com/miniconda/)
2. Install ffmpeg and make it available on $PATH, ex: `brew install ffmpeg`
3. `conda create --name ebook_to_audiobook --file requirements.txt`
4. `conda activate ebook_to_audiobook`
5. `python main.py -h`