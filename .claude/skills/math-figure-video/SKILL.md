---
name: math-figure-video
description: >
  교재의 수학 도형(정육면체·직육면체·각뿔·각기둥·원뿔·원기둥 등)을 지정하면 Manim으로
  전개도 접기 / 회전 / 단면 / 라벨 애니메이션을 만들어, 촬영 소스 영상 위에 깔끔하게(검은 카드 없이)
  오버레이한다. "이 도형 띄워", "전개도 접기", "도형 영상", "매쓰빌더 도형", "교재 47쪽 삼각기둥"
  같은 요청에 사용. 렌더는 Manim(정확한 기하) 고정 — HyperFrames는 쓰지 않는다.
status: draft   # 나중에 완성 (2026-07-20): prism/단면/라벨 미완, 데스크탑 로그인 후 이어서
---

# math-figure-video

교재 도형을 **지정 → 애니메이션 → 소스 영상 위 오버레이**하는 스킬. 도형 정확도가 핵심이라
렌더는 **Manim**으로 고정한다. (HyperFrames/CSS 3D는 비교 끝에 탈락 — 기하 정확도 부족.)

## 워크플로

1. **지정 (designate)**  — 사용자가 도형을 알려주는 단계
   - 최우선: 교재 페이지를 **사진/스캔으로 세션에 업로드** → 어떤 입체인지 인식.
   - 교재 도형은 유한 집합(각뿔/각기둥/정다면체/회전체)이라 인식이 안정적.
   - 말로 지정도 가능: "밑면 정삼각형 삼각뿔, 좀 낮게".
   - 인식 결과를 파라미터로 매핑: `SIDES`(밑면 변수), `HEIGHT`(높이), 동작.

2. **애니메이션 (animate)**  — Manim 씬
   - **3D 입체** `scripts/solid_anim.py`: n각뿔 전개도 접기 + 회전 (n=3,4,5,6…), 투명 배경.
     ```bash
     SIDES=4 HEIGHT=1.25 ACTIONS=fold,rotate \
       /tmp/manim-venv/bin/manim -qm -t --format=mov --fps 30 -r 1000,1000 \
       scripts/solid_anim.py SolidAnim
     # 산출: media/videos/solid_anim/1000p30/SolidAnim.mov (영상 위 합성용)
     ```
   - **2D 증명/작도** `scripts/pythagoras_proof.py`: 유클리드 피타고라스 증명(전단 이동).
     흰 배경 교재풍, 4단계(도형→왼쪽세트→오른쪽세트→색칠), 한글 캡션 포함.
     ```bash
     /tmp/manim-venv/bin/manim -r 1920,1080 --fps 30 --format mp4 \
       scripts/pythagoras_proof.py Pyth
     ```
     좌표 매핑 함수 `P()` 하나로 모든 요소를 그리는 패턴 — 다른 평면 기하 증명의 템플릿으로 재사용.

3. **오버레이 (overlay)**  — `scripts/overlay.sh`, **검은 카드 없이 도형만**
   ```bash
   scripts/overlay.sh SRC.MOV SolidAnim.mov out.mp4 1260 70 600
   # 라벨을 넣으려면 7번째 인자로 (KR_FONT에 한글 TTF 필요):
   # scripts/overlay.sh SRC.MOV SolidAnim.mov out.mp4 1260 70 600 "정사각뿔 전개도 → 입체"
   ```

4. **육안 확인 필수** — 프레임 스냅샷으로 접힘·회전·정합을 눈으로 검증한 뒤 완료 보고.
   ```bash
   ffmpeg -y -ss 6.5 -i out.mp4 -frames:v 1 check.png   # Read로 확인
   ```

## 설치
`SETUP.md` 참조. 요약: Manim은 격리 venv(`/tmp/manim-venv`), ffmpeg/ffprobe는 npm 인스톨러
패키지로 확보(정적 다운로드 호스트는 프록시 차단됨).

## 남은 작업 (나중에 완성)
- 각기둥(prism): 밑면을 apex로 모으는 대신 높이로 압출.
- 단면(cross-section): 평면 교차 단면 강조.
- 라벨: 꼭짓점/모서리/치수 `MathTex` 표기.
- 밝은 구간 가독성: 검은 카드 없이 **얇은 외곽선/그림자** 옵션.
- 소스 영상 무음(나레이션 후반 삽입 전제) — 오디오 트랙 미처리 정상.
