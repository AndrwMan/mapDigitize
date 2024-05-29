Initially began with looking at map images from [University of Texas Map Collection](https://maps.lib.utexas.edu/maps/ams/indonesia/index.html).

Here is an example image
![ex. img from dataset 1](imgs/raw/indonesia1.1.jpg)

This project begins by automating processes that previously would have been done manually in tools like Adobe Lightroom. This includes cropping the map image from entire image (excluding legend elements) and converting image to grayscale.

![ex. img from dataset 1](imgs/digitized/indonesia_map_extracted.jpg)
![ex. img from dataset 1](imgs/digitized/indonesia_map_cropped2.jpg)
![ex. img from dataset 1](imgs/digitized/intermediate_closed_red_elements4.jpg)

However attempts on extracting road (red elements in these maps) were noisy. This was attributed to other elements that were similar in color to red. A new dataset was found that had roads that were distinctly red. 

Here is an example image
![ex. img from dataset 2](imgs/raw/Medium%20sized%20JPEG.jpg)

Running the unmodified code on new inputs yield completely black images as output. It turns out this was the result of the. Code had to rewritten to automatically crop map images for the new dataset.




