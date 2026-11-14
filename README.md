---
project: root
---

# diagram-software-architecture

> draw.io software-architecture diagrams, and the work of improving the diagram skill that draws them.

## What it is

A repo that does two things together:

- **Diagram creation.** Software-architecture diagrams drawn as draw.io (`.drawio`) files. A diagram is one file, one picture, and it is kept in the library named for what it shows (four libraries, below).
- **Diagram-skill improvement.** The diagram skill (how these diagrams are built, checked and rendered) is improved here by drawing real diagrams with it: what a diagram shows the skill gets wrong or lacks is what gets fixed in the skill.

## Where it fits

The workspace root of this repo; it has no parent. Its four libraries: [architecture-frontend](./architecture-frontend/README.md) · [architecture-backend](./architecture-backend/README.md) · [architecture-cloud](./architecture-cloud/README.md) · [architecture-overall](./architecture-overall/README.md).

## What only this level knows

A diagram is written into the library its name says: a frontend diagram into `architecture-frontend`, a backend one into `architecture-backend`, a cloud one into `architecture-cloud`, and one of the system as a whole into `architecture-overall`. Each diagram is one storage folder of its library, `<NNN>-<name>`, holding its `.drawio`.

## Working with it

**To draw a diagram,** say which one you want and name its library in the request; the root routes by the library's name (`## Topic Routing`), or set one with `focus <library>`. Throwaway generator scripts start with `🚫` and are git-ignored.

**To improve the skill,** draw with it here and note what the result gets wrong or lacks; the fix goes into the skill, and the diagram is redrawn with the fixed skill.

## Children

| Name | Type | Path |
|------|------|------|
| architecture-frontend | library | ./architecture-frontend |
| architecture-backend | library | ./architecture-backend |
| architecture-cloud | library | ./architecture-cloud |
| architecture-overall | library | ./architecture-overall |

## Topic Routing

| Field | Value |
|-------|-------|
| Mode | dynamic |

| Topic | Path | Signals |
|-------|------|---------|
| architecture-frontend | ./architecture-frontend | frontend · front end · ui |
| architecture-backend | ./architecture-backend | backend · back end · server side · microservices |
| architecture-cloud | ./architecture-cloud | cloud · aws · azure · gcp · vpc |
| architecture-overall | ./architecture-overall | overall · whole system · end to end · system context |
