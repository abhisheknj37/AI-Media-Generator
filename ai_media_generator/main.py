import os
import uuid
import time
import wave
import random
import re
import requests
import numpy as np
from dotenv import load_dotenv
from gtts import gTTS
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from urllib.parse import quote

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
os.makedirs("assets", exist_ok=True)


# ══════════════════════════════════════════════════════
#  AI CALL
# ══════════════════════════════════════════════════════
def call_ai(prompt: str, max_tokens: int = 1800) -> str:
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "meta-llama/llama-3-8b-instruct",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        res = requests.post(url, headers=headers, json=data, timeout=45)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"AI ERROR: {e}")
    return ""


# ══════════════════════════════════════════════════════
#  STORY
# ══════════════════════════════════════════════════════
def generate_story(prompt: str) -> str:
    result = call_ai(
        f"Write a fun 4-sentence children story about: {prompt}.\n"
        f"Rules:\n"
        f"- Exactly 4 sentences, each on its own line.\n"
        f"- Simple words a child understands.\n"
        f"- Include a character name, a challenge, and a happy ending.\n"
        f"- Do NOT include titles, numbers, or headings.\n"
        f"Output only the 4 story sentences, nothing else."
    )
    lines = [l.strip() for l in result.splitlines() if l.strip()]
    if len(lines) < 2:
        lines = [
            f"Once upon a time, a brave little {prompt} set off on a big adventure.",
            f"Along the way, the {prompt} faced a tricky challenge but never gave up.",
            f"With a clever idea and a kind heart, the {prompt} solved everything!",
            f"Everyone cheered and they all lived happily ever after. The End!"
        ]
    return "\n".join(lines[:4])


# ══════════════════════════════════════════════════════
#  IMAGE FETCH  — rate-limit aware, session reuse
# ══════════════════════════════════════════════════════
_session = requests.Session()
_session.headers.update({"User-Agent": "Mozilla/5.0 KidsAIWorld/1.0"})

_last_request_time = 0.0
_MIN_REQUEST_GAP   = 8.0   # seconds minimum between Pollinations requests


def _rate_limit_wait():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _MIN_REQUEST_GAP:
        wait = _MIN_REQUEST_GAP - elapsed
        print(f"  ⏳ Rate-limit pause: {wait:.1f}s…")
        time.sleep(wait)
    _last_request_time = time.time()


def _fetch_image(prompt: str, width: int = 512, height: int = 512,
                 timeout: int = 90) -> "str | None":
    _rate_limit_wait()
    safe = quote(prompt[:200])
    seed = random.randint(1, 99999)
    url  = (
        f"https://image.pollinations.ai/prompt/{safe}"
        f"?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
    )
    try:
        r = _session.get(url, timeout=timeout)
        if r.status_code == 200 and len(r.content) > 5_000:
            path = f"assets/{uuid.uuid4()}.jpg"
            with open(path, "wb") as f:
                f.write(r.content)
            img = Image.open(path).convert("RGB")
            img.save(path, quality=90)
            print(f"  ✅ Image saved: {path}")
            return path
        elif r.status_code == 429:
            print(f"  ⚠️  429 Rate limited — backing off 20s")
            time.sleep(20)
        else:
            print(f"  ⚠️  HTTP {r.status_code}, size={len(r.content)}")
    except requests.exceptions.Timeout:
        print(f"  ⏱  Timeout: {prompt[:50]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    return None


def _fetch_image_with_retry(prompt: str, width: int = 512, height: int = 512,
                             attempts: int = 3) -> "str | None":
    extra_delays = [0, 15, 30]
    for i in range(attempts):
        if extra_delays[i] > 0:
            print(f"  💤 Extra wait {extra_delays[i]}s before retry {i+1}…")
            time.sleep(extra_delays[i])
        print(f"  🔄 Attempt {i+1}/{attempts}: {prompt[:55]}…")
        path = _fetch_image(prompt, width=width, height=height, timeout=90)
        if path:
            return path
    return None


# ══════════════════════════════════════════════════════
#  BEAUTIFUL ILLUSTRATED FALLBACK (scene-aware)
# ══════════════════════════════════════════════════════
def _make_beautiful_fallback(text: str, width: int = 640, height: int = 360,
                              scene_idx: int = 0) -> str:
    path = f"assets/{uuid.uuid4()}.png"
    img  = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    palettes = [
        {"sky_top": (255, 180, 100), "sky_bot": (255, 130,  80),
         "ground":  ( 80, 140,  60), "sun": (255, 240,  50)},
        {"sky_top": ( 80, 160, 255), "sky_bot": (160, 210, 255),
         "ground":  ( 60, 130,  50), "sun": (255, 230,   0)},
        {"sky_top": (255, 100,  50), "sky_bot": (255, 200, 100),
         "ground":  (100,  80,  40), "sun": (255, 220,   0)},
        {"sky_top": ( 10,  10,  60), "sky_bot": ( 30,  30, 100),
         "ground":  ( 20,  60,  30), "sun": (240, 240, 200)},
    ]
    pal = palettes[scene_idx % len(palettes)]

    for y in range(height):
        t = y / height
        r = int(pal["sky_top"][0] * (1-t) + pal["sky_bot"][0] * t)
        g = int(pal["sky_top"][1] * (1-t) + pal["sky_bot"][1] * t)
        b = int(pal["sky_top"][2] * (1-t) + pal["sky_bot"][2] * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    ground_y = int(height * 0.68)
    draw.rectangle([0, ground_y, width, height], fill=pal["ground"])

    sx, sy, sr = int(width * 0.82), int(height * 0.18), 38
    draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=pal["sun"])

    for cx, cy in [(110, 55), (340, 42), (510, 70)]:
        for dx, dy, cr in [(-20,0,22),(0,-10,28),(20,0,22),(40,5,18)]:
            draw.ellipse([cx+dx-cr, cy+dy-cr, cx+dx+cr, cy+dy+cr],
                         fill=(255, 255, 255))

    for tx in [50, 155, width-55, width-175, width//2 - 35]:
        th = random.randint(55, 90)
        ty = ground_y - th
        draw.rectangle([tx-7, ty, tx+7, ground_y], fill=(100, 60, 30))
        for oy, rr, shade in [(0,44,0),(-28,36,15),(-52,26,25)]:
            g_val = 110 + shade
            draw.ellipse([tx-rr, ty+oy-rr, tx+rr, ty+oy+rr],
                         fill=(30, g_val, 30))

    for _ in range(22):
        fx = random.randint(15, width-15)
        fy = random.randint(ground_y+8, height-8)
        fc = random.choice([(255,80,120),(255,200,50),(150,80,255),(50,200,255)])
        draw.ellipse([fx-6, fy-6, fx+6, fy+6], fill=fc)
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=(255,255,200))

    if scene_idx % 4 == 3:
        for _ in range(40):
            sx2 = random.randint(0, width)
            sy2 = random.randint(0, ground_y-20)
            draw.ellipse([sx2-2, sy2-2, sx2+2, sy2+2], fill=(255,255,255))

    label = text[:48] if len(text) <= 48 else text[:45]+"..."
    draw.rectangle([0, height-42, width, height], fill=(0, 0, 0))
    draw.rectangle([0, height-42, width, height-40], fill=(255, 215, 0))
    draw.text((14, height-30), f">> {label}", fill=(255, 220, 80))

    img.save(path, quality=95)
    return path


def generate_image(prompt: str) -> str:
    """Fetch main illustration (512x512)."""
    path = _fetch_image_with_retry(prompt, width=512, height=512, attempts=3)
    if path:
        return path
    return _make_beautiful_fallback(prompt, width=512, height=512, scene_idx=1)


# ══════════════════════════════════════════════════════
#  AUDIO
# ══════════════════════════════════════════════════════
def generate_audio(text: str) -> str:
    path = f"assets/{uuid.uuid4()}.mp3"
    try:
        gTTS(text=text, lang="en", slow=False).save(path)
        return path
    except Exception as e:
        print(f"Audio error: {e}")
    wav_path = f"assets/{uuid.uuid4()}.wav"
    with wave.open(wav_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        wf.writeframes(b"\x00" * 22050 * 2)
    return wav_path


# ══════════════════════════════════════════════════════
#  MUSIC
# ══════════════════════════════════════════════════════
def _chord_music(duration: float) -> str:
    path = f"assets/{uuid.uuid4()}.wav"
    fr   = 44100
    t    = np.linspace(0, duration, int(fr * duration), endpoint=False)
    wave_data = (
        0.18 * np.sin(2 * np.pi * 261.63 * t) +
        0.12 * np.sin(2 * np.pi * 329.63 * t) +
        0.10 * np.sin(2 * np.pi * 392.00 * t) +
        0.06 * np.sin(2 * np.pi * 523.25 * t) +
        0.04 * np.sin(2 * np.pi * 130.81 * t)
    ).astype(np.float32)
    fade = min(int(fr * 0.5), len(wave_data) // 4)
    wave_data[:fade]  *= np.linspace(0, 1, fade)
    wave_data[-fade:] *= np.linspace(1, 0, fade)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fr)
        wf.writeframes((wave_data * 32767).astype(np.int16).tobytes())
    return path


# ══════════════════════════════════════════════════════
#  VIDEO FRAME HELPERS  (pure PIL — no MoviePy lambdas)
# ══════════════════════════════════════════════════════

def _color_grade(img: Image.Image, scene_idx: int) -> Image.Image:
    grades = [
        (1.05, 1.10, 1.00),
        (1.00, 1.05, 1.15),
        (1.10, 0.95, 0.90),
        (0.90, 0.95, 1.20),
    ]
    r_f, g_f, b_f = grades[scene_idx % len(grades)]
    r, g, b = img.split()
    r = r.point(lambda p: min(255, int(p * r_f)))
    g = g.point(lambda p: min(255, int(p * g_f)))
    b = b.point(lambda p: min(255, int(p * b_f)))
    return Image.merge("RGB", (r, g, b))


def _add_scene_overlay(img: Image.Image, scene_idx: int,
                       width: int, height: int) -> Image.Image:
    labels = [
        "* Once upon a time...",
        "* The adventure begins!",
        "* A magical discovery!",
        "* Happily ever after!",
    ]
    label   = labels[scene_idx % len(labels)]
    overlay = img.copy()
    draw    = ImageDraw.Draw(overlay)
    bx, by  = 10, height - 38
    draw.rectangle([bx, by, bx + 270, by + 28], fill=(0, 0, 0))
    draw.text((bx + 6, by + 6), label, fill=(255, 215, 0))
    return Image.blend(img, overlay, alpha=0.85)


def _make_zoom_frames(img_path: str, out_w: int, out_h: int,
                      fps: int, duration: float, scene_idx: int = 0,
                      zoom_start: float = 1.0,
                      zoom_end:   float = 1.10) -> list:
    src     = Image.open(img_path).convert("RGB").resize((out_w, out_h), Image.LANCZOS)
    src     = _color_grade(src, scene_idx)
    src_w, src_h = src.size
    n_frames = max(2, int(fps * duration))
    frames   = []
    for i in range(n_frames):
        progress = i / max(n_frames - 1, 1)
        zoom     = zoom_start + (zoom_end - zoom_start) * progress
        crop_w   = int(src_w / zoom)
        crop_h   = int(src_h / zoom)
        left     = (src_w - crop_w) // 2
        top      = (src_h - crop_h) // 2
        cropped  = src.crop((left, top, left + crop_w, top + crop_h))
        frame    = cropped.resize((out_w, out_h), Image.LANCZOS)
        if i < 18 or i > n_frames - 10:
            frame = _add_scene_overlay(frame, scene_idx, out_w, out_h)
        frames.append(np.array(frame, dtype=np.uint8))
    return frames


def _make_fade_frames(frame_a: np.ndarray, frame_b: np.ndarray,
                      n_frames: int) -> list:
    frames = []
    for i in range(n_frames):
        alpha   = i / max(n_frames - 1, 1)
        blended = (frame_a * (1.0 - alpha) + frame_b * alpha).astype(np.uint8)
        frames.append(blended)
    return frames


# ══════════════════════════════════════════════════════
#  4 SCENE PROMPTS  — always different angles/moments
# ══════════════════════════════════════════════════════
def _build_scene_prompts(prompt: str) -> list[str]:
    """
    Returns 4 semantically distinct prompts for the same topic
    so each scene looks genuinely different.
    """
    return [
        f"{prompt}, colorful cartoon children book illustration, bright daytime, wide establishing shot",
        f"{prompt}, exciting adventure moment, kids animated style, close-up action scene, vibrant colors",
        f"{prompt}, magical discovery, whimsical children illustration, golden hour lighting, medium shot",
        f"{prompt}, happy celebration ending, cheerful cartoon, confetti and stars, sunny background",
    ]


# ══════════════════════════════════════════════════════
#  VIDEO  — always 4 REAL images, smart fallback
# ══════════════════════════════════════════════════════
def generate_video(prompt: str, main_image_path: str = None) -> str:
    """
    4-scene animated video with ALWAYS 4 distinct images.
    Strategy:
      Scene 1 → reuse main_image_path if available (saves 1 API call)
      Scene 2 → fetch new image (different angle/moment)
      Scene 3 → fetch new image (different angle/moment)
      Scene 4 → fetch new image (different angle/moment)
    If any fetch fails → PIL-generated fallback with unique palette (NOT a repeat).
    """
    try:
        from moviepy.editor import ImageSequenceClip, AudioFileClip
    except ImportError:
        print("moviepy not installed — pip install moviepy")
        return ""

    os.makedirs("assets", exist_ok=True)

    OUT_W, OUT_H = 640, 360
    FPS          = 24
    SCENE_SEC    = 4.0
    FADE_SEC     = 0.5
    fade_n       = max(2, int(FPS * FADE_SEC))

    scene_prompts = _build_scene_prompts(prompt)
    scene_imgs: list[str] = []

    # ── Scene 1: reuse main image if available ──────────────
    if main_image_path and os.path.exists(main_image_path):
        src = Image.open(main_image_path).convert("RGB").resize(
            (OUT_W, OUT_H), Image.LANCZOS)
        p = f"assets/{uuid.uuid4()}.jpg"
        src.save(p, quality=92)
        scene_imgs.append(p)
        print(f"  🖼️  Scene 1: reusing main image (no API call) ✅")
    else:
        print(f"  📸 Scene 1: fetching…")
        p = _fetch_image_with_retry(scene_prompts[0], width=OUT_W, height=OUT_H, attempts=3)
        scene_imgs.append(p or _make_beautiful_fallback(scene_prompts[0], OUT_W, OUT_H, 0))

    # ── Scenes 2, 3, 4: always fetch distinct images ───────
    for idx in range(1, 4):
        print(f"  📸 Scene {idx+1}: fetching distinct image…")
        p = _fetch_image_with_retry(scene_prompts[idx], width=OUT_W, height=OUT_H, attempts=3)
        if p:
            scene_imgs.append(p)
        else:
            # PIL fallback — unique palette per scene, NOT a repeat of scene 1
            print(f"  🎨 Scene {idx+1}: using unique PIL fallback (palette {idx})…")
            scene_imgs.append(
                _make_beautiful_fallback(scene_prompts[idx], OUT_W, OUT_H, scene_idx=idx)
            )

    # Safety check — should never happen, but guarantee exactly 4
    while len(scene_imgs) < 4:
        scene_imgs.append(
            _make_beautiful_fallback(prompt, OUT_W, OUT_H, scene_idx=len(scene_imgs))
        )

    print(f"\n🎬 Rendering {len(scene_imgs)} scenes into frames…")

    # ── Render all frames ──────────────────────────────────
    all_frames: list[np.ndarray] = []

    zoom_configs = [
        (1.00, 1.10),   # Scene 1: slow zoom in
        (1.10, 1.00),   # Scene 2: slow zoom out
        (1.00, 1.08),   # Scene 3: gentle zoom in
        (1.05, 1.00),   # Scene 4: pull back
    ]

    for idx, img_path in enumerate(scene_imgs):
        z_start, z_end = zoom_configs[idx % len(zoom_configs)]
        zoom_frames = _make_zoom_frames(
            img_path, OUT_W, OUT_H,
            fps=FPS, duration=SCENE_SEC,
            scene_idx=idx,
            zoom_start=z_start,
            zoom_end=z_end,
        )
        if idx == 0:
            black = np.zeros((OUT_H, OUT_W, 3), dtype=np.uint8)
            all_frames += _make_fade_frames(black, zoom_frames[0], fade_n)
            all_frames += zoom_frames
        else:
            all_frames += _make_fade_frames(all_frames[-1], zoom_frames[0], fade_n)
            all_frames += zoom_frames

    # Fade out to black
    black = np.zeros((OUT_H, OUT_W, 3), dtype=np.uint8)
    all_frames += _make_fade_frames(all_frames[-1], black, fade_n)

    total_sec = len(all_frames) / FPS
    print(f"  📊 {len(all_frames)} frames  ({total_sec:.1f}s)")

    # ── Encode ─────────────────────────────────────────────
    try:
        music_path = _chord_music(total_sec)
        clip       = ImageSequenceClip(all_frames, fps=FPS)
        audio      = AudioFileClip(music_path)
        if audio.duration > clip.duration:
            audio = audio.subclip(0, clip.duration)
        clip = clip.set_audio(audio)

        output = f"assets/{uuid.uuid4()}.mp4"
        clip.write_videofile(
            output,
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
            bitrate="1800k",
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            logger=None,
        )
        clip.close()
        audio.close()
        time.sleep(0.5)

        abs_path = os.path.abspath(output)
        print(f"  ✅ Video saved: {abs_path}")
        return abs_path

    except Exception as e:
        print(f"  ❌ Video export error: {e}")
        return ""


# ══════════════════════════════════════════════════════
#  QUIZ
# ══════════════════════════════════════════════════════
def _parse_quiz_blocks(raw: str) -> list[dict]:
    quiz   = []
    blocks = re.split(r'\n-{2,}\n?', raw.strip())
    for block in blocks:
        if not block.strip():
            continue
        try:
            lines  = [l.strip() for l in block.splitlines() if l.strip()]
            q_line = None
            for l in lines:
                if re.match(r'^Q\d+[\s:\.]+', l, re.IGNORECASE):
                    q_line = re.sub(r'^Q\d+[\s:\.]+', '', l).strip()
                    break
            if not q_line:
                for l in lines:
                    if not re.match(r'^[A-D][)\.]\s', l) and "ANSWER" not in l.upper():
                        q_line = l
                        break
            if not q_line:
                continue

            opts = {}
            for l in lines:
                m = re.match(r'^([A-D])[)\.]\s*(.+)', l)
                if m:
                    opts[m.group(1).upper()] = m.group(2).strip()

            ans_letter = None
            for l in lines:
                m = re.match(r'^ANSWER\s*:?\s*([A-D])', l, re.IGNORECASE)
                if m:
                    ans_letter = m.group(1).upper()
                    break

            if len(opts) < 4 or ans_letter not in opts:
                continue
            ans_text  = opts[ans_letter]
            opts_list = list(opts.values())
            if len(opts_list) != 4:
                continue
            quiz.append({"q": q_line, "options": opts_list, "answer": ans_text})
        except Exception:
            continue
    return quiz


def _fill_in_blank(story: str, prompt: str) -> list[dict]:
    sentences = [s.strip() for s in re.split(r'[.\n]', story) if len(s.strip()) > 12]
    random.shuffle(sentences)
    stop = {'that','this','with','have','from','they','were','been',
            'will','would','could','their','there','about','once','upon'}
    word_pool = list(set(
        w for w in re.findall(r'\b[a-zA-Z]{4,}\b', story.lower()) if w not in stop
    ))
    qs, used = [], set()
    for sentence in sentences:
        if len(qs) >= 4:
            break
        words = [w for w in sentence.split()
                 if len(w) > 3 and w.isalpha() and w.lower() not in used]
        if not words:
            continue
        key    = random.choice(words)
        used.add(key.lower())
        blank_q = sentence.replace(key, "_____", 1)
        wrongs  = [w for w in word_pool
                   if w.lower() != key.lower() and w.isalpha() and len(w) > 2]
        random.shuffle(wrongs)
        options = [key] + wrongs[:3]
        while len(options) < 4:
            options.append(random.choice(["happy", "blue", "tree", "fast"]))
        random.shuffle(options)
        qs.append({"q": f"Fill in the blank: {blank_q}",
                   "options": options[:4], "answer": key})
    return qs


def generate_quiz(prompt: str, story: str) -> list[dict]:
    ai_prompt = f"""You are a fun quiz master for children aged 6-12.

TOPIC: "{prompt}"

STORY:
{story}

Create EXACTLY 8 multiple-choice questions. Mix these types:
- 3 questions about what happened in the story (comprehension)
- 2 questions about the topic "{prompt}" (fun facts a child would know)
- 2 fill-in-the-blank from story sentences
- 1 creative/imagination question about the topic

RULES:
1. All 8 questions must be COMPLETELY DIFFERENT from each other.
2. Each has exactly 4 choices: A, B, C, D.
3. Only ONE choice is correct.
4. Vary which letter (A/B/C/D) is correct — do NOT make A always correct.
5. Wrong answers should be funny but clearly wrong for kids.
6. Keep language very simple.

USE THIS FORMAT EXACTLY (no extra text outside this format):
Q1: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q2: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q3: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q4: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q5: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q6: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q7: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
---
Q8: <question>
A) <choice>
B) <choice>
C) <choice>
D) <choice>
ANSWER: <letter>
"""
    raw  = call_ai(ai_prompt, max_tokens=2000)
    quiz = _parse_quiz_blocks(raw)

    if len(quiz) < 8:
        extras = _fill_in_blank(story, prompt)
        for q in extras:
            if len(quiz) >= 8:
                break
            quiz.append(q)

    fallbacks = [
        {"q": "What is this story mainly about?",
         "options": [prompt.title(), "The Moon", "A Bicycle", "The Ocean"],
         "answer": prompt.title()},
        {"q": "What makes a good story?",
         "options": ["Fun characters", "Blank pages", "No words", "Only numbers"],
         "answer": "Fun characters"},
        {"q": f"Which word describes {prompt} best?",
         "options": ["Amazing", "Boring", "Invisible", "Broken"],
         "answer": "Amazing"},
    ]
    random.shuffle(fallbacks)
    for fb in fallbacks:
        if len(quiz) >= 8:
            break
        quiz.append(fb)

    for q in quiz:
        ans = q["answer"]
        random.shuffle(q["options"])
        q["answer"] = ans

    random.shuffle(quiz)
    return quiz[:8]


# ══════════════════════════════════════════════════════
#  GAME DATA
# ══════════════════════════════════════════════════════
def generate_game_data(prompt: str, story: str) -> dict:
    all_text  = (story + " " + prompt).lower()
    raw_words = list(set(re.findall(r'\b[a-zA-Z]{4,10}\b', all_text)))
    ai_raw    = call_ai(
        f"List exactly 15 simple English words (4 to 8 letters each) related to '{prompt}' "
        f"for a children's word game. One word per line. No numbers, no punctuation."
    )
    ai_words = [
        w.strip().lower()
        for w in ai_raw.splitlines()
        if 4 <= len(w.strip()) <= 8 and w.strip().isalpha()
    ]
    word_pool = list(set(raw_words + ai_words))
    padding   = ["adventure","rainbow","dragon","magic","forest",
                 "castle","friend","happy","river","bridge",
                 "cloud","light","music","smile","brave"]
    while len(word_pool) < 15:
        word_pool.append(random.choice(padding))
    random.shuffle(word_pool)
    return {"words": word_pool[:15], "prompt": prompt, "story": story}


# ══════════════════════════════════════════════════════
#  IMAGE PIECES
# ══════════════════════════════════════════════════════
def slice_image(image_path: str, rows: int = 2, cols: int = 3) -> list[str]:
    os.makedirs("assets", exist_ok=True)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    img    = Image.open(image_path).convert("RGB")
    w, h   = img.size
    pw, ph = w // cols, h // rows
    pieces = []
    for r in range(rows):
        for c in range(cols):
            box   = (c*pw, r*ph, (c+1)*pw, (r+1)*ph)
            piece = img.crop(box)
            path  = f"assets/{uuid.uuid4()}.png"
            piece.save(path)
            pieces.append(path)
    indices = list(range(len(pieces)))
    random.shuffle(indices)
    return [pieces[i] for i in indices]


# ══════════════════════════════════════════════════════
#  MAIN ENTRY
# ══════════════════════════════════════════════════════
def run(prompt: str):
    print(f"\n{'='*55}")
    print(f"  Generating learning world for: '{prompt}'")
    print(f"{'='*55}\n")

    print("📖 Generating story…")
    story = generate_story(prompt)
    print(f"  Done.\n")

    print("🖼️  Generating main illustration…")
    image = generate_image(prompt)
    print(f"  Done: {image}\n")

    print("🎧 Generating audio narration…")
    audio = generate_audio(story)
    print(f"  Done: {audio}\n")

    print("🎬 Generating story animation video (4 unique images)…")
    video = generate_video(prompt, main_image_path=image)
    print(f"  Done: {video}\n")

    print("🧠 Generating quiz…")
    quiz = generate_quiz(prompt, story)
    print(f"  Done. {len(quiz)} questions.\n")

    print("🎮 Generating game data…")
    game_data = generate_game_data(prompt, story)
    print(f"  Done.\n")

    print("🧩 Slicing image for puzzle…")
    pieces = slice_image(image)
    print(f"  Done. {len(pieces)} pieces.\n")

    print(f"{'='*55}")
    print(f"  ✅ All content ready for: '{prompt}'")
    print(f"{'='*55}\n")

    return story, image, audio, video, quiz, game_data, pieces