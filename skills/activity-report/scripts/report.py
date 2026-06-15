#!/usr/bin/env python3
"""
ActivityMonitor 로그 분석 리포트 생성기
사용법: python report.py [날짜(YYYY-MM-DD)] [--output 경로]
"""
import json, os, sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

LOG_DIR = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "activity-logs"

def load_logs(date_str: str | None = None) -> dict:
    """지정일(기본 오늘) 로그 로드"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"{date_str}.json"
    if not log_file.exists():
        return {"date": date_str, "entries": [], "error": f"{log_file} 없음"}
    with open(log_file, encoding="utf-8") as f:
        entries = json.load(f)
    return {"date": date_str, "entries": entries}

def analyze(entries: list) -> dict:
    """로그 분석 — 프로젝트별/시간대별 통계"""
    projects = defaultdict(lambda: {"total_sec": 0, "windows": set(), "entries": 0})
    hourly = defaultdict(lambda: defaultdict(int))
    timeline = []
    
    for e in entries:
        if isinstance(e, dict) and e.get("type") == "daily_summary":
            continue
        proj = e.get("project", "기타")
        sec = e.get("duration_sec", 0)
        projects[proj]["total_sec"] += sec
        projects[proj]["windows"].add(e.get("window", ""))
        projects[proj]["entries"] += 1
        hour = e.get("time", "00:00")[:2]
        hourly[hour][proj] += sec
        timeline.append({"time": e.get("time"), "project": proj, "duration": sec})
    
    return {
        "projects": dict(projects),
        "hourly": {h: dict(d) for h, d in sorted(hourly.items())},
        "timeline": timeline
    }

def format_report(date_str: str, analysis: dict) -> str:
    """마크다운 리포트 생성"""
    lines = []
    lines.append(f"# 📋 활동 리포트 — {date_str}\n")
    
    projs = analysis["projects"]
    if not projs:
        lines.append("_기록된 활동이 없습니다._\n")
        return "\n".join(lines)
    
    total_min = sum(p["total_sec"] for p in projs.values()) / 60
    
    # 프로젝트별 요약
    lines.append("## 📊 프로젝트별 소요 시간\n")
    lines.append("| 프로젝트 | 시간(분) | 비율 | 창 개수 |")
    lines.append("|----------|---------|------|--------|")
    for proj, data in sorted(projs.items(), key=lambda x: -x[1]["total_sec"]):
        mins = data["total_sec"] / 60
        pct = mins / total_min * 100 if total_min > 0 else 0
        lines.append(f"| {proj} | {mins:.0f}분 | {pct:.1f}% | {len(data['windows'])} |")
    lines.append(f"\n**총 관측 시간: {total_min:.0f}분 ({total_min/60:.1f}시간)**\n")
    
    # 시간대별 분포
    lines.append("## ⏰ 시간대별 활동\n")
    lines.append("```")
    for hour, projs_h in sorted(analysis["hourly"].items()):
        total_h = sum(projs_h.values()) / 60
        bar = "█" * max(1, int(total_h / 5))
        lines.append(f"{hour}:00 {bar} {total_h:.0f}분")
    lines.append("```\n")
    
    # 타임라인
    lines.append("## 📝 활동 타임라인\n")
    lines.append("```")
    for t in analysis["timeline"]:
        lines.append(f"  {t['time']}  [{t['project']:15}] {t['duration']}초")
    lines.append("```\n")
    
    return "\n".join(lines)

def main():
    args = sys.argv[1:]
    date_str = None
    output_path = None
    
    for a in args:
        if a.startswith("--output="):
            output_path = a.split("=", 1)[1]
        elif a.startswith("--"):
            continue
        else:
            date_str = a
    
    data = load_logs(date_str)
    if "error" in data:
        print(f"⚠️ {data['error']}")
        return
    
    analysis = analyze(data["entries"])
    report = format_report(data["date"], analysis)
    
    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")
        print(f"✅ 리포트 저장: {output_path}")
    else:
        print(report)

if __name__ == "__main__":
    main()