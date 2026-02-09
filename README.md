# Bonus Assignment 2: Code Generator

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=2AA4-Vash-Team-Assignments_BonusAssignment2&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=2AA4-Vash-Team-Assignments_BonusAssignment2)

**Course:** SFWRENG 2AA4 — Software Design I (Winter 2026)

## Overview

A proof-of-concept code generator that translates draw.io Class Diagram-like models (XML) into Java source code.

## Repository Structure

```
.
├── codegen.py                          # Code generator (Python)
├── examples/
│   ├── default/
│   │   ├── model/
│   │   │   ├── car.drawio              # Default model (XML source)
│   │   │   └── car.png                 # Default model (figure)
│   │   └── src-gen/                    # Generated Java code + Main.java
│   └── new/
│       ├── model/
│       │   ├── university.drawio       # New model (XML source)
│       │   └── university.png          # New model (figure)
│       └── src-gen/                    # Generated Java code + Main.java
```

## Usage

```bash
python3 codegen.py <input.drawio> <output_directory>
```

**Default example (Car):**
```bash
python3 codegen.py examples/default/model/car.drawio examples/default/src-gen
```

**New example (University):**
```bash
python3 codegen.py examples/new/model/university.drawio examples/new/src-gen
```
