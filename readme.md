![title](https://user-images.githubusercontent.com/40852277/74530803-50ded880-4f6e-11ea-9c66-f106a129ab84.png)

# UDP 통신 기반 Parametric Body 구현 on Windows 10

![image](https://user-images.githubusercontent.com/40852277/72328580-85087480-36f6-11ea-97e5-002cba193d83.png)

원본 Git : https://github.com/1900zyh/3D-Human-Body-Shape

참고자료 : [3D Human Body Reshaping with Anthropometric Modeling](https://link.springer.com/chapter/10.1007/978-981-10-8530-7_10)

## 1 . 환경 설정

1-1. 본 작업은 Windows에서 진행하도록한다.

1-2. 일단 Git clone 한다. 원하는 폴더 (여기에서는 C:\src)에 이동하고, ```git@github.com:KimYC1223/3D-Body-Estimation.git```

1-3. 완료후 ```C:\src\3D-Body-Estimation\whl```로 이동, Python 3.7을 설치한다.

![image](https://user-images.githubusercontent.com/40852277/72327776-17a81400-36f5-11ea-82ef-f47048bb7398.png)

1-4. 설치를 완료한 다음, cmd창을 열고 다음과 같이 입력한다.

```
cd "C:\src\3D-Body-Estimation\whl"
python -m pip install --upgrade pip
pip install cython
pip install numpy==1.16.1
pip install scipy
pip install openpyxl
pip install ecos
pip install "VTK-8.2.0-cp37-cp37m-win_amd64.whl"
pip install "traits-5.2.0-cp37-cp37m-win_amd64.whl"
pip install "cvxopt-1.2.3-cp37-cp37m-win_amd64.whl"
pip install "scs-2.1.1.post2-cp37-cp37m-win_amd64.whl"
pip install "osqp-0.6.1-cp37-cp37m-win_amd64.whl"
pip install "cvxpy-1.0.25-cp37-cp37m-win_amd64.whl"
pip install fancyimpute
pip install mayavi
pip install pyopengl
pip install "PyQt4-4.11.4-cp37-cp37m-win_amd64.whl"
```

시간이 오래걸리는 작업이다.

**패키지 설치는 스타크래프트의 테크트리처럼 서로 선후관계가 있기 때문에 순서가 중요하다.**

예를들어 numpy가 있어야 scipy를 설치 할 수 있다.

따라서 반드시 저 순서로 설치한다.

""로 설치하는 것은 windows용 패키지를 따로 받아야 하는 것인데,

이는 이곳 [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)에서 받을 수 있는 것들이다.

1-5. 데모 프로그램을 실행하기 위해 ```python C:\src\3D-Body-Estimation\src\demo.py```를 입력한다.

이는 [원본 Git](https://github.com/1900zyh/3D-Human-Body-Shape)에서 만든 데모 프로그램이다.

## 2. 데모 실행

![image](https://user-images.githubusercontent.com/40852277/72317905-13243100-36de-11ea-9074-336af54e5344.png)

환경 설정 및 예제 실행에 성공하였다.

단순히 해당 신체 사이즈 UI가 정상을 기준으로 -30~+30의 "단계"로 되어 있는 모습을 볼 수 있는데,

PREDICT를 누르면 정확한 치수를 입력 할 수 있다.

![image](https://user-images.githubusercontent.com/40852277/72318466-b295f380-36df-11ea-97f3-0921dc5335a7.png)

weight는 KG, 나머지는 cm 단위이며

키와 몸무게를 제외한 나머지 값들은 굳이 입력하지 않으면

[학습한 데이터 셋](https://graphics.soe.ucsc.edu/data/BodyModels/index.html)을 기반으로 하여 **근사값으로 추정해 맞춰나간다.**

아래는 키 178에 85를 입력했을 때 비율이다.

![image](https://user-images.githubusercontent.com/40852277/72318597-0accf580-36e0-11ea-80f2-bf3b46feb478.png)

실제로 얼마나 정확한지 알아보기 위해

유명 연예인들의 프로필을 바탕으로 검증절차를 진행하였다.

## 이수근

![image](https://user-images.githubusercontent.com/40852277/72319404-6ef0b900-36e2-11ea-91c0-d7bf927c000e.png)

## 서장훈

![image](https://user-images.githubusercontent.com/40852277/72319417-77e18a80-36e2-11ea-86eb-4b84e9eecd72.png)

## 민경훈

![image](https://user-images.githubusercontent.com/40852277/72319437-829c1f80-36e2-11ea-8d91-ace961e4a700.png)

## 강호동

![image](https://user-images.githubusercontent.com/40852277/72319456-8af45a80-36e2-11ea-88ed-2f31fcb3f27d.png)

대략 잘 맞는 느낌이며, 해당 결과는 오로지 키와 몸무게를 기반으로 입력한 결과이다.

더 구체적일 수록, 실제와 비슷 할 것으로 보인다.

추가적으로 저장 버튼 또는 Ctrl + S를 누르면 저장을 할 수 있다.

![image](https://user-images.githubusercontent.com/40852277/72319826-9005d980-36e3-11ea-9ec5-2b8a3585b66f.png)

![image](https://user-images.githubusercontent.com/40852277/72319794-7a90af80-36e3-11ea-95e9-667fa95c59dd.png)

OBJ 파일이 잘 출력된 모습을 보여준다.

## 3 . UDP 통신 프로그램

![image](https://user-images.githubusercontent.com/40852277/73247223-c23f2d00-41f3-11ea-8248-91a7f8808b91.png)

이번에는 ```python C:\src\3D-Body-Estimation\src\UDP_Demo.py```를 입력하면 조금 수정된 버전을 볼 수 있다.

해당 프로그램과 기존 데모의 다른점은 사용자가 마우스를 이용해 입력하지 않고 UDP 패킷을 통해 조작할 수 있다는 것이다.

**해당 프로그램은 5566 포트를 통해 외부로부터 입력을 받고, localhost의 5577포트로 메세지를 전송한다.**

프로그램이 처음 켜지고 실행될 준비를 마치면, localhost:5577로 ```3D body estimation program load complete.```라는 메세지를 보내준다.

그 후에는 5566포트로 메세지를 받아 Body Estimation을 진행 할 수 있는데, 아래는 메세지 양식이다.

```
weight/height/neck/chest/belly_button_waist/gluteal_hip/neck_shoulder_elbow_wrist/crotch_knee_floor/across_back_shoulder_neck/neck_to_gluteal_hip/natural_waist/max_hip/natural_waist_rise/shoulder_to_midhand/upper_arm/wrist/outer_natural_waist_to_floor/knee/max_thigh/gender
```

기존 Inpector에 있던 값을 ```/``` 구분자를 통해 이어 붙힌 것 뿐이다.

4번의 '사용 예제'에서, Unity에서 정보를 전달하기 위해 ```BodySpec``` 클래스에는 ```ToString```메소드를 오버라이딩했다.

```C#
  override public string ToString() {
        string result = "";
        result += this.weight + "/";
        result += this.height + "/";
        result += (this.neck != 0)?this.neck + "/": "/";
        result += (this.chest != 0)?this.chest + "/": "/";
        result += (this.belly_button_waist != 0)?this.belly_button_waist + "/": "/";
        result += (this.gluteal_hip != 0)?this.gluteal_hip + "/": "/";
        result += (this.neck_shoulder_elbow_wrist != 0)?
                  this.neck_shoulder_elbow_wrist + "/": "/";
        result += (this.crotch_knee_floor != 0)?this.crotch_knee_floor + "/": "/";
        result += (this.across_back_shoulder_neck != 0)?
                  this.across_back_shoulder_neck + "/": "/";
        result += (this.neck_to_gluteal_hip != 0)?this.neck_to_gluteal_hip + "/": "/";
        result += (this.natural_waist != 0)?this.natural_waist + "/": "/";
        result += (this.max_hip != 0)?this.max_hip + "/": "/";
        result += (this.natural_waist_rise != 0)?this.natural_waist_rise + "/": "/";
        result += (this.shoulder_to_midhand != 0)?this.shoulder_to_midhand + "/": "/";
        result += (this.upper_arm != 0)?this.upper_arm + "/": "/";
        result += (this.wrist != 0)?this.wrist + "/": "/";
        result += (this.outer_natural_waist_to_floor != 0)?
                  this.outer_natural_waist_to_floor + "/": "/";
        result += (this.knee != 0)?this.knee + "/": "/";
        result += (this.max_thigh != 0) ? this.max_thigh.ToString(): "";
        return result;
    }
```

5566포트에서 메세지를 잘 수신받으면, OBJ파일을 저장하고, localhost의 5577포트로 ```Done```이라는 메세지를 보낸다.

## 4 . 사용 예제

#### Unity - Python 연동

해당 프로젝트를 응용하여 외부프로그램인

Unity에서 불러올 수 있도록 한다.

#### 2 . Unity <-> Python 명령 전달

![image](https://user-images.githubusercontent.com/40852277/73253438-e274e900-41ff-11ea-85f6-85e585a41ca2.png)

Unity <-> Python은 UDP 통신으로 한다.

- Python : 5566포트
- Unity : 5577 포트

#### 3 . Unity에서 OBJ파일 가져오기

[![image](https://user-images.githubusercontent.com/40852277/72321901-67cca980-36e8-11ea-81ea-584a35b1cee4.png)](https://assetstore.unity.com/packages/tools/modeling/runtime-obj-importer-49547)

클릭시 [에셋 스토어](https://assetstore.unity.com/packages/tools/modeling/runtime-obj-importer-49547)로 이동.

은근 이게 어려울 것 같았는데 아닌것 같았다.

Runtime FBX Importer는 찾기 힘드나 OBJ파일은 [자료](https://www.google.com/search?q=Unity+Runtime+OBJ+file+import&oq=Unity+Runtime+OBJ+file+import&aqs=chrome..69i57j0l3.4997j0j4&sourceid=chrome&ie=UTF-8)도 많아보인다.

### 4 . 결과

```C#
// Testing.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Testing : MonoBehaviour
{
    void Update() {
        if (Input.GetKeyDown(KeyCode.A)) {
            BodyEstimation.GetInstance().sendBodySpec(45f, 170f, false);
            // 45kg 170cm 여성
        } else if (Input.GetKeyDown(KeyCode.S)) {
            BodyEstimation.GetInstance().sendBodySpec(120f, 150f, false);
            // 120kg 150cm 여성
        } else if (Input.GetKeyDown(KeyCode.D)) {
            BodyEstimation.GetInstance().sendBodySpec(60f, 180f, true);
            // 60kg 180cm 남성
        } else if (Input.GetKeyDown(KeyCode.F)) {
            BodyEstimation.GetInstance().sendBodySpec(130f, 170f, true);
            // 130kg 170cm 남성
        }
    }
}
```

테스트를 위해 위와 같은 코드를 추가하였다.

![ezgif-3-a4987def4a3a](https://user-images.githubusercontent.com/40852277/73253574-1f40e000-4200-11ea-85cb-770b5a399707.gif)

(Unity 연동 Gif)

아주 잘 동작하는 모습을 볼 수 있다.

# 5 . QnA

### 연락처

- kau_esc@naver.com
- kimyc1223@keti.re.kr

<br><br><br>

---



![제목 없음-4](https://user-images.githubusercontent.com/40852277/74530798-4e7c7e80-4f6e-11ea-8b4f-03601e288ef4.png)

# UDP Protocol based Parametric Body Estimation On Windows 10

![image](https://user-images.githubusercontent.com/40852277/72328580-85087480-36f6-11ea-97e5-002cba193d83.png)

Original Git: https://github.com/1900zyh/3D-Human-Body-Shape

Reference: [3D Human Body Reshaping with Anthropometric Modeling] (https://link.springer.com/chapter/10.1007/978-981-10-8530-7_10)

## 1 . Preferences

1-1. This work is done in Windows.

1-2. Git clone Navigate to the desired folder (here C: \ src), and use `` git@github.com: KimYC1223 / 3D-Body-Estimation.git```

1-3. When done, go to ```C:\src\3D-Body-Estimation\whl``` and install Python 3.7.

![image](https://user-images.githubusercontent.com/40852277/72327776-17a81400-36f5-11ea-82ef-f47048bb7398.png)

1-4. After the installation is complete, open a cmd window and enter:

```
cd "C:\src\3D-Body-Estimation\whl"
python -m pip install --upgrade pip
pip install cython
pip install numpy==1.16.1
pip install scipy
pip install openpyxl
pip install ecos
pip install "VTK-8.2.0-cp37-cp37m-win_amd64.whl"
pip install "traits-5.2.0-cp37-cp37m-win_amd64.whl"
pip install "cvxopt-1.2.3-cp37-cp37m-win_amd64.whl"
pip install "scs-2.1.1.post2-cp37-cp37m-win_amd64.whl"
pip install "osqp-0.6.1-cp37-cp37m-win_amd64.whl"
pip install "cvxpy-1.0.25-cp37-cp37m-win_amd64.whl"
pip install fancyimpute
pip install mayavi
pip install pyopengl
pip install "PyQt4-4.11.4-cp37-cp37m-win_amd64.whl"
```

This is a time-consuming task.

**The order of installation is important because package installations are related to each other like StarCraft's tech tree.**

For example, you need numpy to install scipy.

Therefore, be sure to install them in that order.

Installing as "" requires a separate package for windows.

These are available here [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4).

1-5. Enter ```python C:\src\3D-Body-Estimation\src\demo.py```to run the demo program.

This is a demo program created by [original Git](https://github.com/1900zyh/3D-Human-Body-Shape).

## 2. Run the demo

![image](https://user-images.githubusercontent.com/40852277/72317905-13243100-36de-11ea-9074-336af54e5344.png)

The environment setup and example execution were successful.

You can see that the body size UI is -30 ~ 30 "steps" based on normal.

Press PREDICT to enter the correct dimensions.

![image](https://user-images.githubusercontent.com/40852277/72318466-b295f380-36df-11ea-97f3-0921dc5335a7.png)

The weight is KG and the rest is in cm.

The rest of the values except for height and weight are automatically calculated based

[learned data set](https://graphics.soe.ucsc.edu/data/BodyModels/index.html) unless you enter them.

Below is the ratio of height 178 to weight 85.

![image](https://user-images.githubusercontent.com/40852277/72318597-0accf580-36e0-11ea-80f2-bf3b46feb478.png)

In order to find out how accurate it is,

the verification process was conducted based on the profiles of korean celebrity.

## 이수근

![image](https://user-images.githubusercontent.com/40852277/72319404-6ef0b900-36e2-11ea-91c0-d7bf927c000e.png)

## 서장훈

![image](https://user-images.githubusercontent.com/40852277/72319417-77e18a80-36e2-11ea-86eb-4b84e9eecd72.png)

## 민경훈

![image](https://user-images.githubusercontent.com/40852277/72319437-829c1f80-36e2-11ea-8d91-ace961e4a700.png)

## 강호동

![image](https://user-images.githubusercontent.com/40852277/72319456-8af45a80-36e2-11ea-88ed-2f31fcb3f27d.png)

This looks like suitable!

And the result is based on the height and weight of the person.

The more specific you are, the more likely it is real.

You can also save it by pressing the Save button or Ctrl + S.

![image](https://user-images.githubusercontent.com/40852277/72319826-9005d980-36e3-11ea-9ec5-2b8a3585b66f.png)

![image](https://user-images.githubusercontent.com/40852277/72319794-7a90af80-36e3-11ea-95e9-667fa95c59dd.png)

The OBJ file shows good output.

## 3 . UDP communication program

![image](https://user-images.githubusercontent.com/40852277/73247223-c23f2d00-41f3-11ea-8248-91a7f8808b91.png)

This time, type ```python C:\src\3D-Body-Estimation\src\UDP_Demo.py```to see a slightly modified version.

The difference between this program and the existing demo is

that the user can manipulate it via UDP packets without typing them with the mouse.

**The program receives input from port 5566 and sends a message to port 5577 on localhost.**

When the program is first started and ready to run,

It sends a message to localhost: 5577 saying `` 3D body estimation program load complete.```

After that, you can proceed with Body Estimation by receiving a message on port 5566.

Below is the message form.

```
weight/height/neck/chest/belly_button_waist/gluteal_hip/neck_shoulder_elbow_wrist/crotch_knee_floor/across_back_shoulder_neck/neck_to_gluteal_hip/natural_waist/max_hip/natural_waist_rise/shoulder_to_midhand/upper_arm/wrist/outer_natural_waist_to_floor/knee/max_thigh/gender
```

It simply combines the values in the existing Inpector with the ```/``` separator.

In Chapter 4 'Usage example', I have overridden the ```ToString``` method in the ```BodySpec``` class to convey information in Unity.

```C#
  override public string ToString() {
        string result = "";
        result += this.weight + "/";
        result += this.height + "/";
        result += (this.neck != 0)?this.neck + "/": "/";
        result += (this.chest != 0)?this.chest + "/": "/";
        result += (this.belly_button_waist != 0)?this.belly_button_waist + "/": "/";
        result += (this.gluteal_hip != 0)?this.gluteal_hip + "/": "/";
        result += (this.neck_shoulder_elbow_wrist != 0)?
                  this.neck_shoulder_elbow_wrist + "/": "/";
        result += (this.crotch_knee_floor != 0)?this.crotch_knee_floor + "/": "/";
        result += (this.across_back_shoulder_neck != 0)?
                  this.across_back_shoulder_neck + "/": "/";
        result += (this.neck_to_gluteal_hip != 0)?this.neck_to_gluteal_hip + "/": "/";
        result += (this.natural_waist != 0)?this.natural_waist + "/": "/";
        result += (this.max_hip != 0)?this.max_hip + "/": "/";
        result += (this.natural_waist_rise != 0)?this.natural_waist_rise + "/": "/";
        result += (this.shoulder_to_midhand != 0)?this.shoulder_to_midhand + "/": "/";
        result += (this.upper_arm != 0)?this.upper_arm + "/": "/";
        result += (this.wrist != 0)?this.wrist + "/": "/";
        result += (this.outer_natural_waist_to_floor != 0)?
                  this.outer_natural_waist_to_floor + "/": "/";
        result += (this.knee != 0)?this.knee + "/": "/";
        result += (this.max_thigh != 0) ? this.max_thigh.ToString(): "";
        return result;
    }
```

If  receive a good message on port 5566, ```UDP_Demo.py``` save the OBJ file and send the message ```Done``` to port 5577 on localhost.

## 4 . Usage example

#### Unity-Python Combine

Apply this project so that it can be loaded from the external program Unity.

#### 2 . Unity-Python communication

![image](https://user-images.githubusercontent.com/40852277/73253438-e274e900-41ff-11ea-85f6-85e585a41ca2.png)

Unity <-> Python is communicated by UDP protocol.

- Python : 5566 port
- Unity : 5577 port

#### 3 . Import OBJ Files from Unity

[![image](https://user-images.githubusercontent.com/40852277/72321901-67cca980-36e8-11ea-81ea-584a35b1cee4.png)](https://assetstore.unity.com/packages/tools/modeling/runtime-obj-importer-49547)

Click to go to [Asset Store](https://assetstore.unity.com/packages/tools/modeling/runtime-obj-importer-49547).

It seemed to be difficult, but it wasn't.

The Runtime OBJ Importer seems to have a lot of [reference](https://www.google.com/search?q=Unity+Runtime+OBJ+file+import&oq=Unity+Runtime+OBJ+file+import&aqs=chrome..69i57j0l3.4997j0j4&sourceid=chrome&ie=UTF-8).

### 4 . Result

```C#
// Testing.cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Testing : MonoBehaviour
{
    void Update() {
        if (Input.GetKeyDown(KeyCode.A)) {
            BodyEstimation.GetInstance().sendBodySpec(45f, 170f, false);
            // 45kg 170cm female
        } else if (Input.GetKeyDown(KeyCode.S)) {
            BodyEstimation.GetInstance().sendBodySpec(120f, 150f, false);
            // 120kg 150cm female
        } else if (Input.GetKeyDown(KeyCode.D)) {
            BodyEstimation.GetInstance().sendBodySpec(60f, 180f, true);
            // 60kg 180cm male
        } else if (Input.GetKeyDown(KeyCode.F)) {
            BodyEstimation.GetInstance().sendBodySpec(130f, 170f, true);
            // 130kg 170cm male
        }
    }
}
```

I added the code above for testing.

![ezgif-3-a4987def4a3a](https://user-images.githubusercontent.com/40852277/73253574-1f40e000-4200-11ea-85cb-770b5a399707.gif)

(Unity Example gif)

You can see it works very well.

# 5 . QnA

### Contact

- kau_esc@naver.com
- kimyc1223@keti.re.kr
