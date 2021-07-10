<h2 align="center">
  Image Viewer
</h2>
<div align="center">
  <img src="https://img.shields.io/badge/python-v3.8-blue.svg"/>
  <img src="https://img.shields.io/badge/PyQt5-v5.15.4-blue.svg"/>
</div>


<div align="center">
  <img src="/images/draft/image_viewer.jpg" width="50%">
</div>


## Description

PyQT , Python을 활용한 이미지 뷰어



##### 기능

- 폴더 이미지 열기
- URL 이미지 열기
- drag&drop 이미지 열기
- 파일삭제
- 파일이름변경
- 이미지 확대
- 이미지 축소
- 이미지 Fit
- slider를 이용한 이미지 확대/축소



##### 추가 개발 사항

- 이미지 회선
- 이미지 자르기
- 노이즈 제거
- 이미지 저장




## Features

- [x] config 활용

- [x] 이미지 파일 열기

  * QFileDialog 를 활용하며 Image File(*.jpg, *.gif, *.png 등) 만 선택가능 해야 합니다.
  * 경로에 한글이 포함되어 있어서 File Open이 가능해야 합니다.
  * 향후 이미지 처리를 감안하여 image load fomat(cv2, PIL, binary)을 정하고 개발해야 합니다.

- [x] 폴더 열기
  
- [x] 이미지 다운로드 (URL 주소)

- [x] 확대/축소

- [x] 이미지 Fit Size

- [x] Status bar (image size)

- [x] 파일 리스트 (Tree Widget)

- [x] 파일 목록 필터

- [x] Drag & Drop 으로 이미지 파일 열기

  

## Structure

```
Image-Viewer/
├── config/    
|  └── __init__.py                           # 버전관리
|  └── default_config.yaml                   # config 파일
|  └── default_path.yaml                     # image 경로
├── libs/    
|  └── version.py                            # 버전관리
|  └── utils.py                              # 일반적으로 사용되는 편의 기능 모음
├── widgets/   
|  └── canvas_widget.py                      # image를 보여주는 widget
|  └── file_browser_widget.py                # 폴더의 image 파일을 보여주는 widget
|  └── url_search_widget.py                  # url 경로를 통해서 이미지를 가져오기 위한 widget
├── UI/
|  └── icon/
|     └── appicon.png
|     └── init.png
|     └── main.png
|     └── open_image.png
|     └── zoom_in.png
|     └── zoom_out.png
|     └── zoom_to_actual_size.png
|     └── zoom_to_extents.png
|  └── res.qrc                               # resource 파일
|  └── canvas_widget.ui                      # canvas widget ui 파일
|  └── file_browser_widget.ui                # file_browser_widget widget ui 파일
|  └── url_search_widget.ui                  # url_search_widget widget ui 파일
|  └── image_viewer_main.ui                  # image_viewer ui 파일
├── main.py                                  # main 
└── res_rc.py                                # pyqt Resource File

```



## Naming Conventions

협업 시 타인의 소스코드를 쉽게 이해하기 위해 프로그램의 Naming Rule을 아래와 같이 일관성있게 유지 합니다. (Python 에서 권장하는 Naming 표준기준)



1. **Code lay-out**

   - 들여쓰기는 공백 4칸
   - 한 줄은 최대 79자까지
   - 최상위(top-level) 함수와 클래스 정의는 2줄씩 띄어 작성
   - 클래스 내의 메소드 정의는 1줄씩 띄어 작성
   - 불필요한 공백은 최소화
   - 키워드 인자(keyword argument)와 인자의 기본값(default parameter value)의 = 는 붙여 작성
   - 불필요한 주석은 작성하지 않음
   - 한 줄 주석은 최소화
   - 언더스코어(_) 시작하는 클래스/함수/변수/메서드는 한 모듈내에서만 사용하는 Private 이며 From module import * 시 _로 시작하는 것들은 임포트 시 모두 무시됨 *(그러나, 파이썬은 진정한 의미의 private을 지원하고 있지는 않기 때문에 private을 완전히 강제할 수는 없다. 즉, 위와 같은 임포트문에서는 무시되지만 직접 가져다 쓰거나 호출을 할 경우엔 사용이 가능함)*


2. **Package and Module Names**

   - 짧은 소문자로만 구성된 이름 (가독성을 개선할 수 있다면 밑줄을 사용할 수 있음) *Ex) canvas.py, canvas_widget.py*

3. **Class Names**
   - 클래스 이름은 일반적으로 CapWord 관례를 따름 *Ex) MyWindows*

4. **Type variable names**
   - 변수명에서 _(밑줄)은 위치에 따라 다음과 같은 의미가 있음 *Ex) step_list*
   - 내부적으로 사용되는 변수 *Ex) _single_leading_underscore*
   
5. **Function Names**
   - 함수명은 소문자로 시작하고 가독성을 위해 대소문자 혼용하여 사용 *Ex) setValue*
   - 내부적으로 사용되는 함수 *Ex) _setValue*



## Installation

| Install                | See                                                          | Download                                                     | Etc.                                                   |
| :--------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------ |
| **Anaconda**           | **[Anaconda3 설치가이드 (Windows)](https://yunwoong.tistory.com/2?category=839341 )** | **[Anaconda3 Download](https://www.anaconda.com/products/individual#Downloads)** |                                                        |
| **Pycharm**            | **[Pycharm 설치가이드 (Windows)](https://yunwoong.tistory.com/4?category=839341 )** | **[Pycharm Download](https://www.jetbrains.com/)**           |                                                        |
| **Create Environment** | **[Python 가상환경 구성](https://yunwoong.tistory.com/3?category=839341 )** |                                                              | *반드시 가상환경을 구성하시고 개발을 하시기 바랍니다.* |
| **PyQt**               | **[PyQt 설치 및 실행](https://yunwoong.tistory.com/7?category=839346 )** |                                                              |                                                        |

