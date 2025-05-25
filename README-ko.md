<div align="center">

  <h1>Ollama-Chutes.ai 프록시 서버</h1>

  <p>
    Chutes.ai의 LLM 서비스와 인터페이스하는 Ollama 호환 API 프록시 서버입니다.
  </p>

<p>:earth_americas: <a href="https://github.com/2jang/ollama-chutesai-proxy">English</a> | <a href="https://github.com/2jang/ollama-chutesai-proxy/blob/main/README-ko.md">한국어 (Korean)</a></p>

</div>

<br />

# :notebook_with_decorative_cover: 목차

- [프로젝트 소개](#star2-프로젝트-소개)
    * [기술 스택](#space_invader-기술-스택)
    * [주요 기능](#dart-주요-기능)
- [시작하기](#toolbox-시작하기)
    * [사전 준비물](#bangbang-사전-준비물)
    * [설치](#gear-설치)
    * [설정](#key-설정-configpy)
    * [실행](#running-실행)
- [웹 UI에서 연결하기](#desktop_computer-웹-ui에서-연결하기)

## :star2: 프로젝트 소개

이 프로젝트는 Python과 `aiohttp`로 구축된 비동기 API 서버입니다. Chutes.ai의 대규모 언어 모델(LLM) 서비스로 요청을 전달하는 Ollama 호환 인터페이스를 제공하는 프록시 역할을 합니다. 이를 통해 사용자는 Ollama 클라이언트(WebUI)를 사용하여 Chutes.ai 모델과 상호 작용할 수 있습니다.

이 서버는 요청 변환, 매개변수 매핑, 시스템 프롬프트 주입, 메시지 기록 관리 등을 처리하고 Ollama 형식으로 클라이언트에 응답을 스트리밍합니다.

### :space_invader: 기술 스택

<ul>
  <li><a href="https://www.python.org/">Python (파이썬)</a></li>
  <li><a href="https://docs.aiohttp.org/en/stable/">aiohttp</a> (비동기 HTTP 클라이언트/서버용)</li>
  <li><a href="https://docs.python.org/3/library/asyncio.html">asyncio</a> (비동기 프로그래밍용)</li>
</ul>

### :dart: 주요 기능

- **Ollama 호환성:** 주요 Ollama API 엔드포인트 구현
- **Chutes.ai API 연동:** 설정된 Chutes.ai API로 요청을 원활하게 라우팅
- **`config.py`를 통한 설정:** API 토큰, 모델 이름, 서버 포트 및 기본 LLM 매개변수를 쉽게 설정
- **스트리밍 지원:** Chutes.ai의 스트리밍 응답을 클라이언트로 전달 처리

## :toolbox: 시작하기

다음 단계에 따라 로컬 머신에서 프록시 서버를 설정하고 실행하세요.

### :bangbang: 사전 준비물

- Python 3.8 이상이 설치되어 있는지 확인하십시오. 패키지 설치를 위해 `pip`도 필요합니다.
- Chutes.ai API 키를 발급받으세요: https://chutes.ai/app/api

### :gear: 설치

1.  저장소 복제 (아직 하지 않았다면):
    ```bash
    git clone https://github.com/2jang/ollama-chutesai-proxy.git
    cd ollama-chutesai-proxy
    ```

2.  필수 Python 패키지 설치:
    ```bash
    pip install aiohttp
    ```

### :key: 설정 (`config.py`)

서버를 실행하기 전에 설정을 해야 합니다.
`config.py`를 편집하여 필수 및 선택적 매개변수를 입력합니다. 최소한 `API_TOKEN`은 **반드시** 제공해야 합니다.

### :running: 실행

설정 및 종속성 설치가 완료되면 서버를 시작할 수 있습니다:

```bash
python main.py
```

### :desktop_computer: 웹 UI에서 연결하기

Ollama API 엔드포인트 연결을 지원하는 웹 UI를 사용하는 경우, 이 프록시 서버를 사용하도록 설정할 수 있습니다.

1.  웹 UI에서 **Settings (설정)** -> **Admin Settings (관리자 설정)** -> **Connections (연결)**으로 이동합니다.
2.  Ollama API URL을 추가하거나 수정합니다:
    * 이 프록시 서버가 **로컬 머신**(웹 UI와 동일한 머신이거나 로컬 네트워크에서 접근 가능)에서 실행 중인 경우 다음을 사용합니다:
      `http://localhost:11435`
      (`11435`가 `config.py`의 `SERVER_PORT`와 일치하는지 확인하십시오.)
    * 웹 UI가 **Docker 컨테이너** 내부에서 실행 중이고 이 프록시 서버가 호스트 머신에서 실행 중인 경우 다음을 사용합니다:
      `http://host.docker.internal:11435`
      (이 주소는 Docker 컨테이너가 호스트에서 실행 중인 서비스에 도달할 수 있도록 합니다. 다시 한번, 포트가 올바른지 확인하십시오.)

설정을 저장한 후, 모델 목록에서 사용자의 모델을 확인할 수 있습니다.

## :handshake: 감사의 말

* [Chutes.ai](https://chutes.ai/)
* [Ollama](https://ollama.com/)