"""Сервис голосовых эффектов через ffmpeg.

Ответственность:
  - принять входной файл (OGG/MP3/WAV/M4A)
  - применить эффект через ffmpeg
  - вернуть результат в OGG Opus (формат Telegram voice messages)

ВСЁ выполняется через asyncio.create_subprocess_exec — без shell=True,
без subprocess.run (не блокируем event loop).

Доменные ошибки — VoiceEffectError.
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class VoiceEffectError(Exception):
    """Доменная ошибка сервиса голосовых эффектов."""


# лимит параллельных ffmpeg-обработок (голосовые маленькие, можно больше)
_effect_semaphore = asyncio.Semaphore(10)

# таймаут на ffmpeg (секунды) — голосовые обычно короткие
_FFMPEG_TIMEOUT = 120


# Словарь пресетов: имя эффекта → ffmpeg audio filter chain
EFFECTS: dict[str, str] = {
    # Бурундук — повышение высоты тона (pitch up)
    "chipmunk": "asetrate=44100*1.5,aresample=44100,atempo=0.75",

    # Бас — понижение высоты тона (pitch down)
    "bass": "asetrate=44100*0.7,aresample=44100,atempo=1.4",

    # Робот — эффект робота через phaser + tremolo
    "robot": "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75",

    # Шёпот — убрать тональную составляющую, усилить шумовую
    "whisper": "afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(0)*2-1)*2*3.14)':win_size=128:overlap=0.8",

    # Ускорение x1.5
    "speed_up": "atempo=1.5",

    # Замедление x0.7
    "slow_down": "atempo=0.7",

    # Радио — фильтр радиоприёмника (узкая полоса + лёгкие искажения)
    "radio": "highpass=f=500,lowpass=f=2500,volume=1.5,acompressor=threshold=-20dB:ratio=4",

    # Гелий — ультра-высокий тон (мультяшный)
    "helium": "asetrate=44100*1.8,aresample=44100,atempo=0.6",

    # Собор — длинная многоступенчатая реверберация
    "cathedral": "aecho=0.8:0.9:500|1000|1500|2000:0.5|0.4|0.3|0.2",

    # Призрак — реверс + эхо + реверс обратно (жуткий пре-эхо)
    "ghost": "areverse,aecho=0.8:0.9:200|400:0.5|0.3,areverse",

    # Винил — ретро-запись 1930-х: тёплый узкополосный, лёгкий wow, компрессия
    "vinyl": (
        "highpass=f=200,lowpass=f=4000,"
        "vibrato=f=0.5:d=0.02,"
        "acompressor=threshold=-18dB:ratio=2,"
        "volume=1.3"
    ),

    # Фазер — космическое плывущее мерцание, 80-е синти
    "phaser": (
        "aphaser=in_gain=0.5:out_gain=0.7:delay=3.5:decay=0.6:speed=0.5"
    ),

    # Мегафон — агрессивный рупор: узкая полоса + жёсткая компрессия + bitcrush
    "megaphone": (
        "highpass=f=500,lowpass=f=3500,"
        "acompressor=threshold=-25dB:ratio=10:attack=1:release=30,"
        "acrusher=level_in=2:level_out=3:bits=10:mode=lin:aa=1,"
        "volume=2"
    ),

    # Подкаст-интро — пресет "голос из трейлера": сильный низ, яркое присутствие, гарантовая компрессия
    "podcast": (
        "equalizer=f=100:t=q:w=1:g=6,"
        "equalizer=f=3500:t=q:w=1.5:g=6,"
        "acompressor=threshold=-30dB:ratio=8:attack=2:release=40,"
        "volume=1.5"
    ),

    # Дабстеп-воббл — LFO-модуляция громкости с басом, драм-н-бэйс вокал
    "dubstep": (
        "asetrate=44100*0.85,aresample=44100,atempo=1.18,"
        "apulsator=hz=2:amount=1:offset_l=0:offset_r=0.5,"
        "equalizer=f=100:t=q:w=0.5:g=6"
    ),

    # Студия — агрессивная красивая обработка: шумодав, глубокий тёплый низ,
    # срез мутных середин, сильное присутствие, яркий верх, плотная компрессия,
    # лёгкая интимная комната, эфирная нормализация
    "studio": (
        "highpass=f=100,"
        "afftdn=nf=-30,"
        "equalizer=f=120:t=q:w=1.2:g=4,"       # глубокий тёплый низ
        "equalizer=f=500:t=q:w=1:g=-3,"         # убираем мутную середину
        "equalizer=f=3000:t=q:w=1.5:g=5,"       # сильное присутствие
        "equalizer=f=9000:t=q:w=2:g=4,"         # яркий "воздушный" верх
        "acompressor=threshold=-22dB:ratio=5:attack=3:release=60,"
        "aecho=0.85:0.4:25:0.12,"               # лёгкая интимная комната
        "loudnorm=I=-14:TP=-1:LRA=8"
    ),
}


def get_effect_names() -> list[str]:
    """Возвращает список доступных эффектов."""
    return list(EFFECTS.keys())


async def get_audio_duration(path: Path) -> float:
    """Возвращает длительность аудио в секундах через ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1",
        str(path),
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise VoiceEffectError(f"ffprobe не найден: {exc}") from exc

    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=30,
        )
    except asyncio.TimeoutError:
        try:
            process.kill()
            await process.wait()
        except Exception:
            pass
        raise VoiceEffectError("ffprobe timeout")

    if process.returncode != 0:
        err = stderr.decode(errors="replace").strip()
        raise VoiceEffectError(f"ffprobe returncode={process.returncode}: {err}")

    raw = stdout.decode(errors="replace").strip()
    try:
        return float(raw)
    except ValueError:
        raise VoiceEffectError(f"ffprobe вернул невалидное значение: {raw!r}")


async def apply_effect(
    input_path: Path,
    output_path: Path,
    effect_name: str,
) -> None:
    """Применяет голосовой эффект к аудиофайлу.

    Вход: любой аудиоформат (OGG, MP3, WAV, M4A и т.д.)
    Выход: OGG Opus (формат Telegram voice messages)

    Бросает VoiceEffectError при ошибке ffmpeg.
    """
    inp = Path(input_path)
    out = Path(output_path)

    if not inp.exists():
        raise VoiceEffectError(f"входной файл не найден: {inp}")

    if effect_name not in EFFECTS:
        raise VoiceEffectError(f"неизвестный эффект: {effect_name!r}")

    # гарантируем что родительская директория для output существует
    out.parent.mkdir(parents=True, exist_ok=True)

    audio_filter = EFFECTS[effect_name]

    # конвертируем в OGG Opus с применением фильтра
    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "error",
        "-i", str(inp),
        "-af", audio_filter,
        "-c:a", "libopus",
        "-b:a", "64k",
        "-vn",  # убираем видео (если вдруг есть)
        "-application", "voip",  # оптимизация для голоса
        str(out),
    ]

    async with _effect_semaphore:
        logger.info(
            "ffmpeg: эффект '%s' на %s → %s",
            effect_name, inp.name, out.name,
        )
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise VoiceEffectError(f"ffmpeg не найден: {exc}") from exc
        except Exception as exc:
            raise VoiceEffectError(f"ffmpeg: ошибка запуска: {exc}") from exc

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=_FFMPEG_TIMEOUT,
            )
        except asyncio.TimeoutError:
            # процесс завис — убиваем и чистим частичный output
            try:
                process.kill()
            except ProcessLookupError:
                pass
            try:
                await process.wait()
            except Exception:
                pass
            try:
                if out.exists():
                    out.unlink()
            except OSError:
                pass
            logger.error(
                "ffmpeg: таймаут %s сек на файле %s", _FFMPEG_TIMEOUT, inp,
            )
            raise VoiceEffectError("ffmpeg timeout")

        if process.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            logger.error(
                "ffmpeg returncode=%s, stderr=%s", process.returncode, err,
            )
            # не оставляем битый output
            try:
                if out.exists():
                    out.unlink()
            except OSError:
                pass
            raise VoiceEffectError(
                f"ffmpeg returncode={process.returncode}: {err[:500]}"
            )

    if not out.exists() or out.stat().st_size == 0:
        raise VoiceEffectError("ffmpeg отработал, но выходной файл пуст")


def classify_error(exc: BaseException) -> str:
    """Классифицирует исключение для выбора i18n-сообщения.

    Категории:
      - file_too_large
      - unsupported_format
      - ffmpeg_error
      - network
      - unknown
    """
    if isinstance(exc, VoiceEffectError):
        msg = str(exc).lower()
        if "timeout" in msg:
            return "ffmpeg_error"
        if "too large" in msg or "file too large" in msg:
            return "file_too_large"
        if "invalid data" in msg or "no such" in msg or "not found" in msg:
            return "unsupported_format"
        return "ffmpeg_error"
    if isinstance(exc, asyncio.TimeoutError):
        return "network"
    name = type(exc).__name__.lower()
    if "timeout" in name or "network" in name or "connection" in name:
        return "network"
    return "unknown"
