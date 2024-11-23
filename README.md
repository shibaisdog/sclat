# Sclat

ASCII 아트 기능이 포함된 Python 기반 YouTube 비디오 플레이어입니다.

<p align="center">
    <img src="./asset/sclatLogo.png" width="248" alt="Sclat 로고">
</p>

## 🌐 언어 | Language

[한국어](README.md) | [English](README.en.md)

## ⚙️ 요구사항

> **중요**: 스트리밍 비디오 호환성을 위해 pytubefix는 반드시 7.1rc2 버전이어야 합니다

-   Python 3.8+
-   pygame
-   OpenCV (cv2)
-   moviepy == 1.0.3
-   chardet == 5.2.0
-   pytubefix == 7.1rc2
-   pyvidplayer2 == 0.9.24

## 🌟 주요 기능

-   YouTube 동영상 재생 및 다운로드 기능
-   실시간 ASCII 아트 변환 모드
-   직관적인 키보드 컨트롤
-   동영상 검색 기능
-   볼륨 및 재생 제어
-   GUI 및 CLI 인터페이스

## 🚀 실행 방법

### 설치

**Windows**

```batch
install.bat
```

**터미널**

```bash
install.sh
```

### 사용법

**Windows**

```batch
# GUI 모드
start.bat
```

**터미널**

```bash
# GUI 모드
start.sh

# CLI 모드
start.sh --nogui

# 단일 재생
start.sh --once

# 재생목록 모드
start.sh --play [URL1] [URL2]...
```

## 🎮 비디오 컨트롤

### 재생 제어

| 키  | 기능               |
| --- | ------------------ |
| `S` | 비디오 스킵         |
| `R` | 비디오 재시작      |
| `P` | 재생/일시정지      |
| `M` | 음소거/음소거 해제 |
| `L` | 반복 재생 전환     |
| `A` | ASCII 모드 전환    |

### 탐색

| 키  | 기능        |
| --- | ----------- |
| `↑` | 볼륨 증가   |
| `↓` | 볼륨 감소   |
| `←` | 15초 되감기 |
| `→` | 15초 앞으로 |

### 기능

|   키  | 기능                |
| ----- | ------------------- |
| `esc` | 검색화면으로 돌아가기 |
| `f11` | 전체화면             |

## 🔍 검색 인터페이스

-   비디오 URL 또는 검색어 입력
-   `Ctrl+V`로 URL 붙여넣기
-   방향키로 결과 탐색
-   Enter로 선택 재생
