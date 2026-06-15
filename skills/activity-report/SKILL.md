---
name: activity-report
description: "ActivityMonitor 로그를 읽어 일간/주간 프로젝트별 작업 리포트 생성"
version: 1.0.0
author: go-seonsaeng
scripts:
  - scripts/report.py
---

# Activity Report

ActivityMonitor가 수집한 창 추적 로그를 분석하여 작업 리포트를 생성.

## 수동 리포트

```bash
# 오늘 리포트
python ~/hermes-skills/skills/activity-report/scripts/report.py

# 특정일
python ~/hermes-skills/skills/activity-report/scripts/report.py 2026-06-15

# 파일 저장
python ~/hermes-skills/skills/activity-report/scripts/report.py --output=~/report.md
```

## cronjob 자동 리포트 (매일 퇴근 시간)

```bash
hermes cron create \
  --schedule "0 18 * * 1-5" \
  --name "daily-activity-report" \
  --prompt "Load activity-report skill. Read today's ActivityMonitor log from /mnt/c/Users/thgo/activity-logs/ and generate a daily report. Format as markdown and deliver to me."
```

## 동작 원리

| 단계 | 설명 |
|------|------|
| 1. ActivityMonitor | 10초마다 활성 창 추적 → `activity-logs/{날짜}.json` |
| 2. report.py | JSON 로그 파싱 → 프로젝트별/시간대별 통계 |
| 3. Hermes + cron | 매일 정해진 시간에 실행 → 리포트 전달 |