# Tasks

Classes used for tasks abstractions that use models.

---

## Task

Abstract subclass of the Executable and base class of the tasks. Use Models

---

## NERTask

Subclass of the Task. Abstraction for NER tasks.

---
---

# Objects

---

## Entity

- span: str

Text of the entity.

- start: int

Start postition in a text.

- end: int

End postition in a text.

---

## ClassifiedEntity

- span: str

Text of the entity.

- start: int

Start postition in a text.

- end: int

End postition in a text.

- entity: str

Class of the entity.