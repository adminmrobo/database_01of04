# 데이터베이스 설계 — 야간 연구실 교육 자료

일상 사례에서 출발해 표·키·제약을 갖춘 데이터베이스 설계까지 따라가는 웹 강의자료입니다.
모든 페이지는 **단일 HTML 파일**로 완결되며, 이미지·CSS·JS가 파일 안에 인라인으로 들어 있어
파일 하나만 열어도 그대로 동작합니다.

- **저자** 안상선 ((주)M-Robo 대표) · logix44@hanmail.net
- **교재 참고** 김연희, 『데이터베이스 개론』(3판)
- **라이선스** CC BY-NC 4.0 (비상업적 이용, 출처 표기 필수)

## 보기

GitHub Pages 주소에서 바로 열람합니다.

```
https://<계정>.github.io/db-lecture/          ← 전체 안내
https://<계정>.github.io/db-lecture/week1/    ← 1주차 표지
```

## 구성

```
docs/                        ← GitHub Pages 루트 (배포 대상)
├─ index.html                전체 안내
├─ week1/  6개               표지 + 세부 4 + 정답
├─ week2/  6개               표지 + 세부 4 + 정답
├─ week3/  7개               표지 + 세부 5 + 정답
└─ week4/  7개               표지 + 세부 5 + 정답

src/                         본문 소스 (섹션 단위 HTML 조각)
assets/                      디자인 시스템 · 이미지 자원
├─ base.css, base.js         야간 연구실 테마
├─ img.json                  히어로·일러스트·도식·스크린샷·아이콘 (base64)
└─ chars.json                캐릭터 22종 (투명 PNG, base64)

build2.py                    주차별 빌드 스크립트
talk.py                      캐릭터 대화 원고
```

각 주차는 독립적으로 읽도록 만들었습니다. 표지 → 세부 → 정답 순서로만 이동하며,
주차 사이에는 링크를 두지 않았습니다.

## 재빌드

```bash
python3 build2.py                 # docs/ 로 출력
OUT_DIR=build python3 build2.py   # 다른 폴더로 출력
```

`build2.py`는 `docs/`를 지우고 27개 파일을 다시 만듭니다. 수정은 `src/`와 `assets/base.css`에서 하고
다시 빌드하면 전체 페이지에 반영됩니다. `docs/`는 산출물이므로 직접 고치지 않습니다.

## 배포

`Settings → Pages → Source: Deploy from a branch → main / docs`.
순수 정적 파일이라 빌드 워크플로가 필요 없습니다. `.nojekyll`이 있으므로 Jekyll 처리를 건너뜁니다.

## 다른 언어로 번역할 때

번역본은 **언어별 디렉터리**로 나눕니다. 한국어가 기본(루트)이고, 번역본은 그 아래에 들어갑니다.

```
docs/index.html        한국어 (기본)
docs/week1/ …
docs/en/index.html     English
docs/en/week1/ …
docs/ja/index.html     日本語
```

이 구조를 쓰는 이유는 세 가지입니다.

1. **경로가 단순합니다.** `docs/en/week3/01_file_system.html`처럼 언어만 앞에 붙습니다.
2. **자산 공유 문제가 없습니다.** 이미지·CSS가 HTML 안에 인라인이라 언어별로 파일을 복제해도
   참조가 깨지지 않습니다. 언어당 약 8.6MB, 15주차까지 늘어도 30MB 안팎입니다.
3. **언어 전환 링크가 규칙적입니다.** 같은 경로에서 접두어만 바꾸면 됩니다.

번역 시 손대야 할 곳은 두 층입니다.

| 층 | 위치 | 비고 |
|---|---|---|
| 본문 | `src/*.body.html` | 섹션 단위 조각. 언어별로 `src/en/`처럼 복제해 번역 |
| 화면 문구 | `build2.py`, `talk.py` | 표지·정답·내비게이션 라벨과 캐릭터 대화. 문자열 표로 분리 필요 |

`<html lang="ko">`도 언어에 맞춰 바꿔야 합니다. 번역을 시작할 때 `build2.py`의 문자열을
`strings.py`(언어별 dict)로 분리하고 `LANG` 환경변수로 `docs/<lang>/`에 출력하도록 정리하는 것을 권합니다.
그 전까지 `build2.py`는 한국어 전용으로 동작합니다.

번역본을 추가하면 각 페이지 `<head>`에 상호 참조를 넣어 검색엔진이 언어판을 구분하게 합니다.

```html
<link rel="alternate" hreflang="ko" href="https://<계정>.github.io/db-lecture/week1/">
<link rel="alternate" hreflang="en" href="https://<계정>.github.io/db-lecture/en/week1/">
```

## 라이선스

CC BY-NC 4.0. 교육·연구 목적의 이용과 수정·재배포는 출처를 밝히면 허용됩니다.
상업적 이용은 별도 문의가 필요합니다.
