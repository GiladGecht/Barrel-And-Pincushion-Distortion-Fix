# Barrel-&-Pincushion-Distortion-Fix
Fixing Barrel &amp; Pincushion distortion using OpenCV with GUI

###### Inroduction:
CREDIT: This project was made in collaboration with Anton Vasserman
https://www.linkedin.com/in/anton-vasserman-460b31149/

The project revolves around fixing Radial distortion which is also knows as the "Fisheye Lens Effect".
This causes the picture to distort in a way which resembels either a barrel or a pincushion.

The process is initiated by training our model with a set of chessboard images from different angles, simulating different distortions.
This is followed by the use of OpenCV functions to extract the Radial Coefficients and Camera Matrix from the given picture to adjust the distortion to the desired result.




NOTE:
Make sure to put the icons in the scripts folder.
