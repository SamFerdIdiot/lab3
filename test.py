#!/usr/bin/env python3
"""
Автотест для практического задания №6 (pipe + fifo).
Запуск:  python3 test.py
Требует, чтобы проект был собран в ./build
"""
import os
import re
import subprocess
import sys
import time

BUILD_DIR = "build"
FIFO_PATH = "myfifo"
TIME_RE = re.compile(r"\b(\d{2}):(\d{2}):(\d{2})\b")


def to_seconds(t):
    h, m, s = map(int, t)
    return h * 3600 + m * 60 + s


def seconds_between(t1, t2):
    """Разница с учётом перехода через полночь."""
    d = abs(to_seconds(t1) - to_seconds(t2))
    return min(d, 86400 - d)


def test_pipe():
    print("=== Тест 1: pipe ===")
    exe = os.path.join(BUILD_DIR, "mypipefifo")
    t0 = time.time()
    r = subprocess.run([exe], capture_output=True, text=True)
    elapsed = time.time() - t0
    print(r.stdout, end="")
    if r.stderr:
        print("[stderr]", r.stderr, end="")

    if r.returncode != 0:
        print(f"FAIL: код возврата {r.returncode}")
        return False

    times = TIME_RE.findall(r.stdout)
    if len(times) < 2:
        print(f"FAIL: ожидал 2 времени в выводе, нашёл {len(times)}")
        return False

    diff = seconds_between(times[0], times[1])
    print(f"Разница времён: {diff} сек (реально прошло {elapsed:.1f} сек)")
    if diff < 5:
        print("FAIL: разница меньше 5 секунд")
        return False
    print("OK\n")
    return True


def test_fifo():
    print("=== Тест 2: fifo ===")
    if os.path.exists(FIFO_PATH):
        os.remove(FIFO_PATH)
    os.mkfifo(FIFO_PATH)

    writer = os.path.join(BUILD_DIR, "mywriter")
    reader = os.path.join(BUILD_DIR, "myreader")

    # Reader стартует первым и блокируется на open(O_RDONLY)
    rp = subprocess.Popen([reader], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True)
    time.sleep(0.3)
    wp = subprocess.Popen([writer], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True)

    wp_out, wp_err = wp.communicate(timeout=30)
    rp_out, rp_err = rp.communicate(timeout=30)

    print("--- writer stdout ---"); print(wp_out, end="")
    if wp_err: print("[writer stderr]", wp_err, end="")
    print("--- reader stdout ---"); print(rp_out, end="")
    if rp_err: print("[reader stderr]", rp_err, end="")

    if wp.returncode != 0 or rp.returncode != 0:
        print(f"FAIL: коды возврата writer={wp.returncode}, reader={rp.returncode}")
        return False

    times = TIME_RE.findall(rp_out)
    if len(times) < 2:
        print(f"FAIL: reader вывел {len(times)} времён, ожидалось 2")
        return False

    diff = seconds_between(times[0], times[1])
    print(f"Разница времён в reader: {diff} сек")
    if diff < 10:
        print("FAIL: разница меньше 10 секунд")
        return False
    print("OK\n")
    return True


def main():
    if not os.path.isdir(BUILD_DIR):
        print("Сначала собери проект:")
        print("  cmake -S . -B build && cmake --build build")
        sys.exit(1)

    ok1 = test_pipe()
    ok2 = test_fifo()
    print("=" * 40)
    print("ИТОГ:", "ВСЁ ОК" if (ok1 and ok2) else "ЕСТЬ ОШИБКИ")
    sys.exit(0 if (ok1 and ok2) else 1)


if __name__ == "__main__":
    main()