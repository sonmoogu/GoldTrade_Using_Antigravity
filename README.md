# KRX 금 현물 자동매매 시스템: 가이드 (Walkthrough)

제공해주신 Gemini의 리서치 내용을 바탕으로 Python FastAPI와 순수 웹 기술(Vanilla Web)을 활용한 **KRX 금 현물 자동매매 시스템** 웹 애플리케이션 구축을 완료했습니다.

## 1. 시스템 아키텍처 (구조)

이 애플리케이션은 크게 두 가지 요소로 나뉘어져 있으며, `C:\Users\moogon2\.gemini\antigravity\scratch\krx_gold_trading`에 구성되어 있습니다:

### 백엔드 (Python FastAPI)
*   **`main.py`**: 중심이 되는 메인 서버 애플리케이션입니다. 매 2초마다 시장 상황을 체크하고 알고리즘에 맞을 경우 주문을 실행하는 비동기 이벤트 루프를 백그라운드에서 실행합니다. 프론트엔드 UI를 띄워주고 REST API(`/api/status`, `/api/toggle`)를 제공합니다.
*   **`trading_engine.py`**: 매매 전략을 담당합니다. 20-이동평균선(SMA)을 계산하며, **골든크로스(현재가 > 20 SMA)**가 발생하고 **매수 호가 잔량이 매도 호가 잔량보다 1.5배 많을 때** 매수 신호를 발생시킵니다.
*   **`risk_management.py`**: 안전장치 역할을 합니다. 투자할 수 있는 **최대 자산을 15%로 제한**하며, **+4.5% 도달 시 익절**, **-2.0% 도달 시 손절**을 강제 집행합니다.
*   **`broker_api.py`**: 삼성증권(mPOP) API 인페이스를 흉내낸 Mock(모의) 파일입니다. 안전한 테스트를 위해 임의의 가격 변화와 매매 체결 동작을 시뮬레이션합니다.

### 프론트엔드
*   **`index.html` & `styles.css`**: 데스크톱과 모바일 모두에서 최적화된 고급스러운 다크 모드 및 글래스모피즘(Glassmorphism)이 적용된 대시보드 웹 페이지입니다.
*   **`app.js`**: 백엔드의 상태를 불러와 실시간 가격, 20 SMA, 계좌 잔고, 그리고 현재 보유 포지션을 화면에 실시간으로 나타내줍니다. 가격 변화 시 미세한 애니메이션 효과도 포함되어 있습니다.

## 2. 실행 가이드 (Walkthrough & Execution)

> [!CAUTION]
> 현재 시스템(Windows)에 Python이 설치되어 있지 않거나 경로(PATH) 설정이 안 되어 있는 것으로 파악됩니다. 로컬에서 실행해보시려면 먼저 Python 설치가 완료되어야 합니다.

Python을 설치하신 후 아래 단계를 따라주세요:

1. **프로젝트 폴더로 이동**
   터미널을 열고 다음 명령어를 입력합니다:
   ```cmd
   cd C:\Users\moogon2\.gemini\antigravity\scratch\krx_gold_trading
   ```
2. **가상환경 설정 및 패키지 설치**
   ```cmd
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. **서버 실행**
   ```cmd
   uvicorn backend.main:app --reload
   ```
4. **웹 대시보드 접속**
   웹 브라우저를 열고 [http://localhost:8000](http://localhost:8000)으로 접속합니다. 다크 모드 기반의 프리미엄 UI를 보실 수 있습니다. **"Start Trading"** 버튼을 누르면 설정해 둔 규칙에 따라 매매가 시뮬레이션되는 모습을 실시간으로 확인하실 수 있습니다.

## 3. 다음 단계 (실전 적용)
모의 환경(Mock) 테스트를 마치고 실전 매매로 넘어가실 때는:
1. 삼성증권(또는 연동할 증권사)에 문의하여 실전/모의 API 키를 발급받습니다.
2. `broker_api.py`의 `MockBrokerAPI`를 실제 증권사에서 제공하는 HTTP/WebSocket 통신 코드로 교체하여 실제 KRX 금 현물 호가 데이터를 받아오게 셋팅합니다.
