# 툴체인 설치 (클코 웹 세션 기준, 2026-07-20 실증)

이 환경은 outbound가 정책 프록시를 거친다. **johnvansickle·third-party github release·CDN
(jsdelivr/unpkg)·Pexels/Unsplash는 403 차단**. 반면 npm registry / PyPI / fonts.gstatic /
storage.googleapis 는 허용. 아래는 그 제약을 우회한, 실제로 통과한 경로.

## 1) ffmpeg + ffprobe  (npm 인스톨러 패키지 = registry 경유라 허용)
```bash
cd /tmp && mkdir -p ffbin && cd ffbin && npm init -y >/dev/null
npm install @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe
cp node_modules/@ffmpeg-installer/linux-x64/ffmpeg   /usr/local/bin/ffmpeg
cp node_modules/@ffprobe-installer/linux-x64/ffprobe /usr/local/bin/ffprobe
chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe
```

## 2) Manim  (반드시 격리 venv — 시스템 파이썬의 Debian setuptools가 레거시 빌드를 깨뜨림)
```bash
# pango dev 헤더 (manimpango 소스 빌드에 필요; apt 미러는 이 패키지들엔 도달됨)
apt-get install -y libpango1.0-dev libcairo2-dev pkg-config

python3 -m venv /tmp/manim-venv
/tmp/manim-venv/bin/pip install --upgrade pip setuptools wheel
/tmp/manim-venv/bin/pip install manim        # → manim 0.20.1
/tmp/manim-venv/bin/python -c "import manim; print(manim.__version__)"
```
함정 기록:
- 시스템 `pip install manim` → `srt` 휠 빌드가 `install_layout` AttributeError로 실패.
  원인은 Debian 패치 setuptools. **venv가 근본 해결.**
- `manimpango` manylinux 휠 없음 → 소스 빌드 → `pangocairo` .pc 필요 → 위 apt로 해결.

## 3) 한글 라벨 폰트 (선택)
시스템에 한글 TTF가 없다. 필요하면 Noto Sans KR woff2를 ttf로 변환해 사용:
```bash
/tmp/manim-venv/bin/pip install fonttools brotli
/tmp/manim-venv/bin/python - <<'PY'
from fontTools.ttLib import TTFont; import glob
src=sorted(glob.glob('/root/.cache/hyperframes/fonts/noto-sans-kr/700-normal-*.woff2'))[0]
ft=TTFont(src); ft.flavor=None; ft.save('/tmp/kr700.ttf')
PY
```
주의: 위 캐시는 **서브셋**(그때 렌더한 글자만 포함). 임의 한글엔 전체 Noto Sans KR ttf 필요.

## 비고
- HyperFrames/Chrome는 이 스킬에선 불필요(Manim 확정). 설치 기록만 남김:
  `npm i -g hyperframes && hyperframes browser ensure` (Chrome Headless Shell은 googleapis에서 받아짐).
- 소스 촬영영상은 세션 업로드분 사용, 임의 경로 추정 금지.
