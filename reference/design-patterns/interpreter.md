# Interpreter

Define a grammar for a language and provide an interpreter to evaluate sentences in it.

**Applies to**: Object-Oriented Design

---

**What it is**: Given a language, defines a representation for its grammar along with an interpreter that uses the representation to interpret sentences.

**When to use**:
- A simple grammar needs to be interpreted (configuration DSLs, query languages, rule engines).
- The grammar is stable and simple — complex grammars require parser generators instead.

**Trade-offs**:
- Each grammar rule requires a class — complex grammars produce large class hierarchies.
- For complex languages, use a dedicated parser/compiler toolkit instead.
