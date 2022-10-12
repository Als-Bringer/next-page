# Next-page system with OpenCV
: 실시간 영상과 영상 처리 기술을 기반으로 눈 깜빡임으로 화면이 넘어가게하는 프로그램을 제작하였습니다. 실시간 Vision System에 사용자의 얼굴 및 안구 검출 기법, 조명 영향 제거에 따른 안구 오검출 제거 방법, 졸음 감지 기법등을 구현하였습니다. 
  
## Description
: 얼굴 및 안구 검출을 하기 위해 **Histogram of Oriented Gradients 기술과 학습된 Face landmark estimation 기법**을 사용하였습니다. **조명 영향을 제거하기 위해선 원본 영상의 조명 채널을 분리해 역 조명을 쏘아 Grayscale 된 이미지와 합쳐**주었고, 졸음 상태를 감지하기 위해선 **Eye Aspect Ratio**라는 개념을 사용하였습니다.
    
***This code is in Python 3.6***

## System diagram
Get face images from the camera -> Grayscaling -> Light processing -> HOG & find face -> Face Landmark Estimation -> Turn to the next page or Detect drowsiness reading. 

## Extracting face and eye region
+ 그레이스케일링 한 이미지에서 얼굴을 찾기 위해 **HOG face pattern**을 사용했습니다.
  
<img src="https://user-images.githubusercontent.com/36785390/52613168-3b088480-2ed0-11e9-8651-97afc34f4bae.png" width="60%">

+ Face Landmark Estimation 알고리즘을 사용해 얼굴의 68개 랜드마크를 찾아냈습니다.
  
<img src="https://user-images.githubusercontent.com/36785390/52613175-3d6ade80-2ed0-11e9-9290-ee5dc2f2d525.png" width="30%">
<img src="https://user-images.githubusercontent.com/36785390/52613176-3f34a200-2ed0-11e9-8f3f-94998fd2ab63.png" width="30%">
  


## Preprocessing
+ 영상에 있어서 조명의 영향은 영상처리에 상당히 많은 영향을 끼칩니다. 특히 그라데이션 조명을 받았을 경우 에러를 일으키는 요소가 되기 때문에, 전처리 과정으로 영상에서 조명 영향을 받을 때 그 영향을 최소화하는 작업을 진행했습니다.
+ 전처리를 위해 영상에서 분리한 Lightness 채널을 반전시키고 Grayscale 된 원본 영상과 합성하여 Clear 한 Image를 만들었습니다.
   
<img src="https://user-images.githubusercontent.com/36785390/52613306-bb2eea00-2ed0-11e9-9b64-5c45981e953e.png" width="40%">

+ 그레이스케일링 과정은 Luma 기법을 사용했습니다.

<img src="https://user-images.githubusercontent.com/36785390/52613343-dc8fd600-2ed0-11e9-93f6-e154e20df31d.png" width="35%">
  
<img src="https://user-images.githubusercontent.com/36785390/52613308-bc601700-2ed0-11e9-999e-40a2782932c9.png" width="40%">
  
+  [Median filtering](https://en.wikipedia.org/wiki/Median_filter)
+ Color Space 모델에는 다양한 모델이 있는데 그중 LAB 모델은 Lightness를 가장 잘 분리해 낼 수 있는 모델입니다. 
+ LAB 컬러 공간을 사용해 얻게 된 명도 값은 실제 조명의 상태와는 차이가 있기 때문에 실제 조명의 상태에 맞게 변환하고자 메디안 필터링(Median Filtering)을 적용하는 과정을 진행했고, 이렇게 검출된 조명에 역상을 취하여 원 이미지와 합성함으로써 조명의 영향을 줄였습니다.
+ 아래의 사진은 왼쪽부터 순서대로 원본 이미지, L 채널을 분리한 이미지, Median Filter를 적용한 이미지, Invert 된 이미지입니다.
  
    
<img src="https://user-images.githubusercontent.com/36785390/52613441-35f80500-2ed1-11e9-9c6c-819b9e92b150.png" width="70%">
   
+ Results of preprocessing
   
<img src="https://user-images.githubusercontent.com/36785390/52613443-385a5f00-2ed1-11e9-94e3-e325b3436041.png" width="20%">
    
     
## Drowsiness detection method
+ Each eye is represented by 6 (x, y)-coordinates
+ 이 프로젝트에서는 2016년 Tereza Soukupova & Jan ´ Cech에 의해 제시된 Eyes Aspect Ratio(이하 EAR) 방식을 사용합니다. EAR은 검출된 안구에 여섯 개의 (x, y) 좌표를 이용하여 계산됩니다.
  
<img src="https://user-images.githubusercontent.com/36785390/52702447-83eb3680-2fbf-11e9-985f-f96ec72f5b26.png" width="20%">
   
+ The EAR equation
   
<img src="https://user-images.githubusercontent.com/36785390/52702578-cb71c280-2fbf-11e9-9a06-d4434250d622.png" width ="30%">

+ Calculated EAR
<img src="https://user-images.githubusercontent.com/36785390/52702645-ee9c7200-2fbf-11e9-9757-975fa22da6e1.png" width="60%">
+ 
+ .1) == 과정 1),   2) == 과정 2),   3) == 과정 3) (in next_page code)
+ **계산된 EAR은 눈을 뜨고 있을 땐 0이 아닌 어떤 값을 갖게 되고, 눈을 감을 땐 0에 가까운 값**을 갖습니다. 여기에 어떤 Constant로 **Threshold**를(졸음을 판단할 때 사용하는 임곗값) 설정할 시 그 값보다 EAR 값이 작아지는지 확인하는 방식으로 사용자가 졸음 졸리다는 것을 감지할 수 있습니다.
+ 추가로 졸음 판별 시 양쪽 눈을 따로 검사할 필요는 없기 때문에 양쪽 눈 각각의 EAR 값을 평균 계산해서 사용하였습니다.
+ **Threshold** 값은 눈을 가장 크게 떴을 때 EAR 값의 50%로 설정했습니다. 이보다 작을 때는(눈 크기가 작아졌을 때) 사용자가 졸린 상태인 것으로 판단, 사용자가 졸려 하는지에 관심을 뒀기 때문에 완전 수면에 빠지지 않더라도 알람이 울립니다.
+ 이 알고리즘을 적용하기 위해 다음의 세 과정을 적용했습니다. 1) 사용자가 눈을 뜨고 있을 때 평균 EAR 값을 결정, 2) 사용자가 눈을 감고 있을 때 평균 EAR 값을 결정, 3) 위의 두 값을 이용해 눈을 뜨고 있는 상태의 50%가 되는 EAR 값을 결정.

  
## KNN
. 1. Create arrays with random (x, y)-coordinates.
  
<img src="https://user-images.githubusercontent.com/36785390/52762829-82bc1700-305c-11e9-97cb-b41e35dfb9e6.png" width="30%">
  
  2. Labeling
<img src="https://user-images.githubusercontent.com/36785390/52762830-8485da80-305c-11e9-96db-f24a7a1ebdd6.png" width="40%">
  
  3. Define K value.
<img src="https://user-images.githubusercontent.com/36785390/52762904-e6dedb00-305c-11e9-952c-f201390eb9bd.png" width="50%">
  
  4. Test KNN algorithm.
<img src="https://user-images.githubusercontent.com/36785390/52762907-e8a89e80-305c-11e9-8928-9409bd4eaa7a.png" width="50%">
  
  
## Synthesis
<img src="https://user-images.githubusercontent.com/36785390/52762972-36bda200-305d-11e9-99a6-314dfae8f3c7.png" width="50%">
****
  
## References
+ [Machine Learning is Fun! Part 4: Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
+ [Real-Time Eye Blink Detection using Facial Landmarks](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
+ [Eye blink detection with OpenCV, Python, and dlib](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
+ [dlib install tutorial that I refer to](https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/)
+ [Histograms of Oriented Gradients for Human Detection](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)
+ [조명(Lighting)의 영향을 제거하는 방법](https://t9t9.com/60)
