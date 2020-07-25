"""
ref: https://stackoverflow.com/a/56709915/9878098
I've found del to be useful for pseudo-manual memory management when handling large data with Numpy. For example:
"""

for image_name in large_image_set:
    large_image = io.imread(image_name)
    height, width, depth = large_image.shape

    large_mask = np.all(large_image == "<some_condition>")

    # Clear memory, make space
    del large_image
    gc.collect()

    large_processed_image = np.zeros((height, width, depth))
    large_processed_image[large_mask] = new_value
    io.imsave("processed_image.png", large_processed_image)

    # Clear memory, make space
    del large_mask, large_processed_image
    gc.collect()

"""
This can be the difference between bringing a script to a grinding halt as the system swaps like mad when the Python GC can't keep up, and it running perfectly smooth below a loose memory threshold that leaves plenty of headroom to use the machine to browse and code while it's working.
"""
