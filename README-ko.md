# Ollama-Chutes.ai 프록시 서버 ↔️☁️</h1>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)]([https://www.python.org/](https://www.python.org/))

<p>:earth_americas: <a href="https://github.com/2jang/ollama-chutesai-proxy/blob/main/README-ko.md">한국어</a> | <a href="https://github.com/2jang/ollama-chutesai-proxy">English</a></p>

Chutes.ai의 LLM 서비스와 연동되는 Ollama 호환 API 프록시 서버입니다.  

이 프로젝트는 Python과 `aiohttp`로 구축된 비동기 API 서버입니다. 프록시 역할을 하여 Chutes.ai의 대규모 언어 모델(LLM) 서비스로 요청을 전달하는 Ollama 호환 인터페이스를 제공합니다.
이를 통해 사용자들은 Ollama용으로 설계된 클라이언트(예: WebUI)를 사용하여 Chutes.ai 모델과 상호작용할 수 있습니다. 🚀

이 서버는 요청 변환, 매개변수 매핑, 시스템 프롬프트 주입, 메시지 기록 관리 등을 처리하며, Ollama 형식으로 클라이언트에 응답을 스트리밍합니다.

## ✨ 주요 기능

- ⚙️ **쉬운 설정**: `config.py`를 통해 API 토큰, 모델 이름, 서버 포트 및 기본 LLM 매개변수를 쉽게 설정할 수 있습니다.
- 💨 **스트리밍 지원**: Chutes.ai로부터 스트리밍 응답을 처리하고 클라이언트에 전달합니다.

## ❓ Chutes.ai란?

Chutes.ai는 API 요청을 통해 다양한 LLM(대규모 언어 모델)을 사용할 수 있게 해주는 서비스입니다. 많은 모델이 무료로 제공됩니다. 자유롭게 Chutes.ai의 모델들을 탐색해 보세요!

## 🚀 시작하기

### 📋 사전 준비물

-   **Python**: Python 3.8 이상이 설치되어 있는지 확인하세요.
-   **pip**: Python 패키지 설치 프로그램으로, 보통 Python과 함께 설치됩니다.
-   **Chutes.ai API 키**: [Chutes.ai](https://chutes.ai/app/api)에서 API 키를 발급받으세요. **필수** 항목입니다.

### 🛠️ 설치 단계

1.  **저장소 복제 (Clone the repository)**:
    ```bash
    git clone [https://github.com/2jang/ollama-chutesai-proxy.git](https://github.com/2jang/ollama-chutesai-proxy.git)
    cd ollama-chutesai-proxy
    ```

2.  **필요한 Python 패키지 설치 (Install required Python packages)**:
    ```bash
    pip install aiohttp
    ```

### 🔑 설정 (`config.py`)

서버를 실행하기 전에 **반드시** 설정을 해야 합니다.
`config.py` 파일을 편집하여 필수 및 선택적 매개변수를 입력하세요.

**필수 항목:**
* `API_TOKEN`: 여러분의 Chutes.ai API 토큰.

설정 및 종속성 설치가 완료되면 다음 명령으로 서버를 시작할 수 있습니다:

```bash
python main.py
```

## 🖥️ WebUI에서 연결하기

Ollama API 엔드포인트에 연결을 지원하는 WebUI(예: Ollama WebUI, Open WebUI 등)를 사용하는 경우, 이 프록시 서버를 사용하도록 설정할 수 있습니다.

1.  WebUI에서 **설정** -> **관리자 설정** -> **연결**로 이동합니다.
2.  Ollama API URL을 추가하거나 수정합니다:
    * 프록시 서버가 **로컬 머신**(WebUI와 동일한 머신이거나 로컬 네트워크에서 접근 가능)에서 실행 중인 경우:
      `http://localhost:11435`
      (`11435`가 `config.py`의 `SERVER_PORT`와 일치하는지 확인하세요.)
    * WebUI가 **Docker 컨테이너** 내에서 실행 중이고 프록시 서버가 호스트 머신에서 실행 중인 경우:
      `http://host.docker.internal:11435`
      (이 주소는 Docker 컨테이너가 호스트에서 실행 중인 서비스에 도달할 수 있도록 합니다. 다시 한 번, 포트가 올바른지 확인하세요.)

설정을 저장한 후에는 여러분의 모델을 선택할 수 있게 됩니다.

## 🧩 사용된 기술 스택

-   **코어**:
    -   [Python](https://www.python.org/) (3.8 이상)
-   **비동기 HTTP**:
    -   [aiohttp](https://docs.aiohttp.org/en/stable/) (비동기 HTTP 클라이언트/서버용)
-   **동시성**:
    -   [asyncio](https://docs.python.org/3/library/asyncio.html) (비동기 프로그래밍용, Python 내장)

## 🤝 기여하기

버그 리포트, 기능 제안 또는 풀 리퀘스트(Pull Request)는 언제나 환영합니다! 기여하고 싶으시다면 다음 단계를 따라주세요:

1.  이 저장소를 포크(Fork)하세요.
2.  기능 브랜치를 만드세요 (`git checkout -b feature/AmazingFeature`).
3.  변경 사항을 커밋하세요 (`git commit -m 'Add some AmazingFeature'`).
4.  브랜치에 푸시하세요 (`git push origin feature/AmazingFeature`).
5.  풀 리퀘스트를 열어주세요.

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

* [Chutes.ai](https://chutes.ai/) - LLM 서비스를 제공해 주셔서 감사합니다.
* [Ollama](https://ollama.com/) - 이 프록시가 호환성을 목표로 하는 API 사양을 제공해 주셔서 감사합니다.

---

⭐ 이 프로젝트가 유용하다고 생각되시면 Star를 눌러주세요! ⭐
