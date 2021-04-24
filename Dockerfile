FROM continuumio/miniconda3 AS deploy

## Setup erogaki-mask.
WORKDIR /app

# Create the conda environment.
RUN conda create --name erogaki-mask python=3.5.2 --channel conda-forge

# Copy the requirements file.
COPY ./src/requirements.txt ./

# Install the dependencies.
RUN conda run --no-capture-output --name erogaki-mask pip install -r requirements.txt

# Install libgl.
RUN apt-get install -y libgl1-mesa-glx

# Copy the source code.
COPY ./src ./

# Install Mask Rcnn
RUN conda run --no-capture-output --name erogaki-mask python setup.py install

# Start hent-AI-erogaki-wrapper.
ENTRYPOINT ["conda", "run", "--no-capture-output", "--name", "erogaki-mask", "python", "main.py"]
