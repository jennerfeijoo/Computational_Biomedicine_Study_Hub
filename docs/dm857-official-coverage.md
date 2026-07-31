# DM857 official coverage audit

## Source boundary

This audit is based on the active SDU ODIN course description for **DM857 — Introduction to programming**:

- source: `https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=DM857&lang=en`
- approval date: 2025-04-11
- status: Approved - active
- audit date: 2026-07-31

ODIN defines the public learning outcomes, principal content, teaching language, workload, and examination form. It does not expose the detailed weekly syllabus, assigned literature, exercises, project brief, or grading rubric stored in itslearning. This matrix therefore audits public specification coverage only.

## Status rules

- **Covered:** current authored modules contain teaching, practice, and assessment evidence for the requirement.
- **Partial:** related activities or a preparation workflow exist, but equivalence with the complete official experience cannot yet be established.
- **Gap:** no equivalent learner workflow currently exists.

## Expected learning outcomes

| ID | Active SDU requirement | Authored evidence | Status |
|---|---|---|---|
| `dm857.sdu.lo01` | Design models for concrete problems. | M01 Foundations; M04 Functions; M11 ADTs; M12 OOP | Covered |
| `dm857.sdu.lo02` | Devise a program structure based on the model. | M04 Functions; M06 Sequences; M07 Mappings and sets; M11 ADTs; M12 OOP | Covered |
| `dm857.sdu.lo03` | Implement the planned program in the programming language used. | Python implementation, practice, and assessment across M01–M14 | Covered |
| `dm857.sdu.lo04` | Find and use adequate elements in the program library. | M05 Strings; M06 Sequences; M07 Mappings and sets; M08 Files and exceptions; M13 Scientific libraries | Covered |
| `dm857.sdu.lo05` | Plan and execute testing of the program. | M10 tree invariants and tests; M14 testing, debugging, and quality | Covered |
| `dm857.sdu.lo06` | Design and implement recursive solutions. | M09 Recursion; M10 Trees | Covered |
| `dm857.sdu.lo07` | Design and implement abstract data types. | M11 ADTs; M12 OOP | Covered |
| `dm857.sdu.lo08` | Use basic tree structures and algorithms. | M10 Trees | Covered |

## Official content topics

| ID | Active SDU topic | Authored evidence | Status |
|---|---|---|---|
| `dm857.sdu.ct01` | Sequence, repetition, conditional instruction, and subprogram. | M01–M04 | Covered |
| `dm857.sdu.ct02` | Lists, maps, and trees. | M06, M07, M10 | Covered |
| `dm857.sdu.ct03` | Structured programming techniques with examples and applications. | M01, M04, M08, M14 | Covered |
| `dm857.sdu.ct04` | Recursion and recursive data structures. | M09, M10 | Covered |
| `dm857.sdu.ct05` | Abstract data types and their realization. | M11, M12 | Covered |

## Examination alignment

The active examination consists of a group project and report of no more than ten pages, followed by a group presentation and a short individual oral examination.

| ID | Examination requirement | Current evidence | Status | Required increment |
|---|---|---|---|---|
| `dm857.sdu.exam01` | Group project and report, maximum ten pages. | A persistent five-milestone capstone now records group metadata, repository and commit evidence, testing evidence, report traceability, a ten-page internal outline, and a seven-criterion internal readiness rubric. | Partial | Import the official itslearning project brief and rubric when available; then add criterion-level artifact review and verified submission checks. |
| `dm857.sdu.exam02` | Group presentation. | No collaborative presentation rehearsal or assessment workflow. | Gap | Add role allocation, timing, slide checklist, rehearsal, and group rubric. |
| `dm857.sdu.exam03` | Short individual oral examination. | Oral-explanation items exist, but they are not a timed defense of the learner's own project. | Partial | Add a timed oral-defense simulator grounded in capstone artifacts and code decisions. |

## Capstone implementation boundary

The capstone workflow is an operational preparation scaffold, not a reconstruction of unpublished SDU assessment material. It provides:

- five evidence-bearing milestones from problem modelling through testing and report traceability;
- persistent project title, group members, repository URL, report reference, checklist state, evidence notes, and commit references;
- an internal weighted readiness rubric totaling 100 percent;
- an internal report outline budgeted to 9.5 pages, leaving margin under the publicly confirmed ten-page maximum;
- Spanish, English, and Danish interfaces with local atomic persistence.

The internal report outline and readiness rubric are explicitly labelled as preparation aids. The project/report row remains **Partial** because the official project brief and grading rubric are not exposed by ODIN and cannot yet be used to validate equivalence.

## Current conclusion

The public **learning outcomes and content topics are covered** by the current fourteen-module course. DM857 is **not yet examination-complete**. The project/report component now has an integrated preparation workflow but remains partial pending official brief-and-rubric validation; the group presentation remains a confirmed gap; and the individual oral defense remains partial.

The executable source of truth is `content/dm857/official_coverage.py`. Tests fail if the matrix references missing modules, changes the official row counts, duplicates requirement IDs, labels a requirement covered without practice and assessment evidence, or regresses the project row to the obsolete claim that no integrated capstone exists.
