# Sign-Recognition
Identify your hand gesture to write characters using image processing and for future development we can changed to make orders to your computer to make something.


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

## Main Pipeline
we categorized our problem to recognize the hand into two categories:
1. mask the hand out of background.
2. detect the characters from hand.

## Performance
All code for all tries were very fast and we didn’t face any problem with performance.

## Conclusion
#### Points of strength
   1) detect hand dynamically.
   2) detect hand under any illumination or position.
   3) recognize hand signs effectively.
   4) no need to put static color to segment hand.
#### Points of weakness
   1) if the hand area - not the whole background - has background with the same hand color and illumination the program will see the hand and its background as the hand.
   2) you need your body to be static so the program can detects the dynamic movement of the hand

## References
   1. OpenCV Documentation: https://goo.gl/Epmiwd
   2. NumPy Documentation: https://goo.gl/P4CJYk


