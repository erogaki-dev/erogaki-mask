# erogaki-mask

This compenent handles detection and masking of censored regions.

It replaces the [hent-AI-erogaki-wrapper](https://github.com/erogaki-dev/hent-AI-erogaki-wrapper).

## Using the Dockerfile

### 1. Building the Docker Image

Just build the docker image, when you're in the root directory of this repository, using the following command:

```
docker image build -t erogaki-mask .
```

### 2. Getting the Model Ready

**The Model isn't included with this repository, since we're unsure about its licensing.**

Create a Docker volume for the models (this volume can be shared with other parts of the erogaki infrastructure):

```
docker volume create erogaki-models
```

Get the following model and put it in the `erogaki-models` docker volume (find out the mountpoint using `docker volume inspect erogaki-models`):

- `hent-AI model 268`

You can find link to it [here](https://github.com/erogaki-dev/hent-AI/blob/master/README.md#the-model).

Your `erogaki-models` volume should then have the following subdirectories:

- `hent-AI model 268/`

### 3. Running the container

Then finally run the container like so:

```
docker run -it -v erogaki-models:/models --network=host erogaki-mask
```

## Acknowledgements

The code has mostly been copied from the [hent-AI project](https://github.com/natethegreate/hent-AI) by [natethegreate](https://github.com/natethegreate) with minimal changes to make it work with the Erogaki infrastructure.

As with hent-AI, the Mask Rcnn implementation is from [Matterport](https://github.com/matterport/Mask_RCNN). All changes to it where inherited from the hent-AI project.
