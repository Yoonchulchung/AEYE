## 2024 한이음 AEYE 프로젝트
AEYE AI 리포지토리 입니다.  
AWS EC2 인스턴스 안에서 빠르게 환경설정을 할 수 있도록 쉘을 작성하였습니다.  

| 작성된 쉘을 통해 자동으로 도커를 설치하고 도커 컨테이너 안에서 `Django`와 `Tensorflow`를 하나의 AWS EC2 인스턴스 안에서 쉽게 실행할 수 있습니다.  

브랜치 구성은 다음과 같이 구성되어 있습니다.  
```
main    : 프로젝트 테스트까지고 끝난 완성된 버전
test    : 코드 작성이 끝나고 테스트 중인 버전
develop : 코드 작성중인 버전 
```

**test 브랜치**에서는 `Github Actions`를 통해 CI가 진행되어 작성된 코드가 정의된 테스트 기준에 충족하는지 평가합니다. `pytest` 프레임워크를 통해 pytest 플더에 정의된 테스트 기준에 충족하는지 평가합니다. 



## 서버 환경
**Python** : 3.6  
**Django** : 3.2  
**djangorestframework** : 3.13.1  
**Tensorflow** : 1.12  
**Keras** : 2.2.4  
**CUDA** : 9  

Python 버전은 AI 서버가 요구하는 Tensorflow 버전이 파이선 3.6에서 동작이 가능하여 일관성을 위해 AEYE 프로젝트의 모든 Python 버전을 3.6으로 통일시켰습니다. Django 3.2는 파이선 3.6에서 동작 가능한 Django 버전이어서 Django 3.2 버전을 사용했습니다.  
 

## 서버 디렉토리 구성

```
.
├── AEYE_AI_Back_3_2/
│   ├── AEYE_AI_Back_3_2/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── db.sqlite3
│   └── manage.py
├── AI_automate.sh
├── Docker
│   ├── AI/
│   │   └── Dockerfile
│   ├── BackEnd/
│   │   └── Dockerfile
│   ├── Untitled.ipynb
│   └── docker-compose.yml
├── LICENSE
├── OpticNet-71-master/
│   ├── LICENSE
│   ├── README.md
│   ├── data_preprocess_sri2014.py
│   ├── img1.png
│   ├── inference.py
│   ├── requirements.txt
│   ├── src/
│   │   ├── dataloader.py
│   │   ├── metrics.py
│   │   ├── model.py
│   │   ├── utils.py
│   │   └── visualize.py
│   ├── test.py
│   └── train.py
├── README.md
└── dependencies_AI.txt
```   

## 프로젝트 사용 방법
아래는 Linux 환경에서 AEYE 프로젝트를 시작하는 명령어 입니다.  
```bash
./AI_automate.sh
```
Shell을 시작하면 AEYE 웹 서버를 시작하기 위해 필요한 `dependencies`를 설치하고, Docker를 설치한 후, 본 프로젝트에서 정의한 Docker Compose를 통해 서버를 시작합니다. 

## REST API EndPoint
아래는 AEYE 웹 벡엔드 서버에서 제공하는 REST API EndPoint 입니다. HTTP POST 요청을 할 경우, 다음 주소를 이용하면 됩니다.
```bash
https://127.0.0.1:8000/api/receive-image/ 
```

