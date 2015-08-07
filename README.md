# IMA-Deep-Learning

## `deepsix`

### `deepsix.collection`

This subpackage contains modules for downloading images from various sources.

- `flickr` (requires flickr API key)
- `imagenet`

Each source has a function `urls_tagged` which returns a list of image URLs with a particular tag, keyword, synset id, etc.

Example usage:
```
human_urls = deepsix.collection.imagenet.urls_tagged('n07942152', max_images=5)
deepsix.collection.get_images_from_urls(human_urls, output_folder='downloads')
```



### `deepsix.anomalize`

This subpackage contains modules for creating anomalies in an image, in order to provide a training set of "bad" images.



### `deepsix.preprocessing`

This subpackage contains modules for loading images into nparrays and applying filters to examine various aspects of the image.