import redis
import json

from Detector import Detector
from NoCensoredRegionsFoundError import NoCensoredRegionsFoundError

from erogaki_wrapper_shared_python.ErogakiWrapperConfig import config
from erogaki_wrapper_shared_python.ImageProcessor import ImageProcessor

def main():
    r = redis.Redis(host=config.redis.hostname, port=config.redis.port, db=config.redis.db)
    detector = Detector("/models/hent-AI model 268/weights.h5")
    detector.load_weights()

    # Test the connection to Redis.
    r.get("connection-test")

    while True:
        print("ready to receive censored image")
        key, uuid = r.blpop(["mask-requests:bar", "mask-requests:mosaic"], 0)
        print("received censored image")

        censored_img_data = r.get("censored-images:%s" % uuid.decode())

        is_mosaic = key.decode() == "mask-requests:mosaic"

        try:
            prepared_img = detector.detect_and_mask(ImageProcessor.bytes_to_image(censored_img_data), is_mosaic, 3)

            print("processed image, saving to redis")
            r.set("masked-images:%s" % uuid.decode(), ImageProcessor.image_to_bytes(prepared_img))
            r.rpush("decensor-requests:%s" % ("mosaic" if is_mosaic else "bar"), "%s" % uuid.decode())
        except NoCensoredRegionsFoundError as e:
            print(e.description)
            r.set("errors:%s" % uuid.decode(), e.json)

if __name__ == "__main__":
    main()
