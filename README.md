# kibo-PRC

គម្រោងគ្រប់គ្រង និងបញ្ជា Robot សម្រាប់ការប្រកួតប្រជែង Robot Programming Competition (RPC)។
Robot Control and Autonomous Navigation System for the Robot Programming Competition (Kibo-RPC 7th - Int-Ball2).

[![GitHub](https://img.shields.io/badge/GitHub-korbsameth-blue?logo=github)](https://github.com/korbsameth)
[![Python](https://img.shields.io/badge/Python-2.7%20%7C%203.8%2B-brightgreen?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)

---

## សមាជិកក្រុម / Team Members (4 Members)

| No. | ឈ្មោះ (Name) | តួនាទី (Role) | ភារកិច្ចទទួលខុសត្រូវ (Responsibilities) | GitHub / Contact |
|:---:|---|---|---|:---:|
| 1 | Nou Srey Oun (នូ ស្រីអូន) | Team Leader & Project Manager | គ្រប់គ្រងគម្រោងទូទៅ សម្របសម្រួលក្រុម និងយុទ្ធសាស្ត្រប្រកួត | Team Leader |
| 2 | Korb Sameth (កប សាម៉េត) | Lead Programmer | សរសេរ main.py, រៀបចំ System Architecture និងសម្របសម្រួល Code | [@korbsameth](https://github.com/korbsameth) |
| 3 | Ly Ly Inh (លី លីអ៊ីញ) | Vision & AR Marker Dev | អភិវឌ្ឍន៍ marker_reader.py, ស្កេន និងចាប់ទិន្នន័យពី AR Marker | Member |
| 4 | Bunna Lida (ប៊ុនណា លីដា) | Motion & Hardware Controller | អភិវឌ្ឍន៍ movement.py, បញ្ជា Motor និង route_planner.py | Member |

---

## រចនាសម្ព័ន្ធ Folder / Project Structure

```text
kibo-PRC/
|
|-- code/
|   |-- main.py              # កម្មវិធីចម្បង (Main execution controller & loop)
|   |-- movement.py          # បញ្ជាចលនា Robot (Motor & attitude controls)
|   |-- marker_reader.py     # ស្កេន AR Marker (Camera & AR detection)
|   `-- route_planner.py     # រៀបចំផ្លូវ (Path planning & checkpoints)
|
|-- tests/
|   `-- test_mission.py      # Automated Unit Test Suite (Bug verification)
|
|-- Dockerfile               # Docker Container Definition
|-- docker-compose.yml       # Multi-service Docker Orchestration
|-- .dockerignore            # Docker build ignore rules
|-- requirements.txt         # Dependencies (numpy, opencv-python)
|-- .gitignore               # Git track rules
`-- README.md                # ឯកសារណែនាំគម្រោង និងសមាជិក
```

---

## របៀបដំណើរការជាមួយ Docker / Running with Docker

### ១. ដំណើរការ Mission តាមរយៈ Docker Compose:

```bash
docker compose up kibo-mission
```

### ២. ដំណើរការ Automated Unit Tests តាមរយៈ Docker Compose:

```bash
docker compose run --rm kibo-test
```

### ៣. Build និង Run ដោយផ្ទាល់ជាមួយ Docker CLI:

```bash
docker build -t kibo-prc:latest .
docker run --rm kibo-prc:latest
```

---

## របៀបដំណើរការ Local (Python Direct)

### ១. តម្រូវការដំឡើង (Dependencies):

```bash
pip install -r requirements.txt
```

### ២. ដំណើរការកម្មវិធីបញ្ជា Robot:

```bash
python code/main.py
```

### ៣. ដំណើរការ Automated Tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## លំហូរដំណើរការបេសកកម្ម (Execution Flow)

1. Docking Departure: ចេញដំណើរពី Docking Station
2. Sensor Initialization: បើក Camera និងរៀបចំ System Sensor
3. Checkpoint Navigation: ហោះទៅតាម Checkpoints នីមួយៗ (Joints, Hatch, Experimental Racks)
4. AR Detection & Attitude Alignment: ស្កេន AR Marker និងតម្រង់មុំកាមេរ៉ាឱ្យចំកណ្តាល
5. Goal Arrival & Complete Report: ទៅដល់ Goal Checkpoint និងបញ្ចប់បេសកកម្ម

---

## Git & Version Control

- Repository: https://github.com/korbsameth/kibo-PRC
- Lead Programmer: Korb Sameth ([@korbsameth](https://github.com/korbsameth))
- Team Leader: Nou Srey Oun
