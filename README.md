# erogaki-mask
This compenent handles detection and masking of censored regions.

It replaces the [hent-AI-erogaki-wrapper](https://github.com/erogaki-dev/hent-AI-erogaki-wrapper).

## Building the Docker Image

### 1. Model

**Model isn't included with this repository, since we're unsure about its licensing.**

Get the following model and put them in the `models` directory:

- `hent-AI model 268`

You can find link to it [here](https://github.com/erogaki-dev/hent-AI/blob/master/README.md#the-model).

Your `models` directory should then have the following subdirectories:

- `hent-AI model 268/`

### 2. `docker image build`

Then just build the docker image, when you're in the root directory of this repository, using the following command:

```
docker image build -t erogaki-mask .
```

## Running a Docker Container

Once you build the Docker image, you can just run a container like this:

```
docker run -it --network=host erogaki-mask
```

## Acknowledgements
The code has mostly been copied from the [hent-AI project](https://github.com/natethegreate/hent-AI) by [natethegreate](https://github.com/natethegreate) with minimal changes to make it work with the Erogaki infrastructure.

As with hent-AI, the Mask Rcnn implementation is from [Matterport](https://github.com/matterport/Mask_RCNN). All changes to it where inherited from the hent-AI project.
