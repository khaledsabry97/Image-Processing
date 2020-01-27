# Sign-Recognition
 identify your hand gesture to write characters using image processing and for future development we can changed to make orders to your computer to make something.


## Inputs and Outputs
#### Inputs
##### To open/close windows press following keys:
    - f => Frame window
    - m => Mask window
    - t => Threshold window
    - h => Hue window
    - s => Saturation window
    - v => Value window
#### Output
letters extracted from image

## Open Sources used
- OpenCV
- NumPy

## Identification
Identification
We assigned 5 characters to our program to identify: “A, L, M,
V, W”

<img width="250" height="200" src="https://github.com/khaledsabry97/Sign-Recognition/blob/master/Attempts/Photos/A2.jpg"> <img width="250" height="200" src="https://github.com/khaledsabry97/Sign-Recognition/blob/master/Attempts/Photos/L2.jpg"> <img width="250" height="200" src="https://github.com/khaledsabry97/Sign-Recognition/blob/master/Attempts/Photos/M2.jpg"> <img width="250" height="200" src="https://github.com/khaledsabry97/Sign-Recognition/blob/master/Attempts/Photos/V2.jpg"> <img width="250" height="200" src="https://github.com/khaledsabry97/Sign-Recognition/blob/master/Attempts/Photos/W2.jpg"> 

## Attempts which guided us to solution
we categorized our problem to recognize the hand into two
categories:
### mask the hand out of background.
##### Try No.1: try to predict hand color by static values.
##### Problem: the hue channel was okay but the value and saturation channel was changing from position to another according to the light incident on the hand.

##### Try No.2: take the sample color from hand by first take the background without hand and after you take a sample you put your hand on the screen.
##### Problem: it was worse than previous tries because if you moved your body the image will detect your body also so you needed to take a sample from time to time and also you refused this idea.

##### Try No.3: take a sample from hand color by making a big rectangle to take the sample by averaging the hue, value and saturation channels from the whole rectangle.
##### Problem: didn’t make good sample because of the we take it on the whole area.

##### Try No.4: try to fix the previous try by taking a sample from hand color by making multiple rectangles to take the sample by averaging the hue, value and saturation channels from the multiple rectangles and take the most common.
##### Problem: didn’t make good sample because of some sampleswhere very different than others.

##### Try No.5: we tried to make change to previous try by not taking the average but sort the values and take the lowest and highest value from each rectangle and then take the average among them all.
##### Problem: some areas now were having different hue and value so the mask excluded a lot of areas from the hand.

##### Try No.6: we then tried to make slight change to the previous try by not taking the lowest and highest value from each rectangle and then take the average among them all but we made multiple masks from the lowest and highest value from each rectangle and then add all these masks together.
##### Problem: results also were very bad a lot of background noise.

##### Try No.7: we then tried to make slight change again to the previous try by not taking lowest and highest value from each rectangle but taking the average of the rectangle.
##### Problem: results also were better than previous but there were also a lot of background noise.

##### Try No.8 : try to get a good quality camera to apply it on the previous try as we thought the problem from the laptop camera. ##### Problem: found that the problem was not in the camera but the problem the idea itself.



### detect the characters from hand.




