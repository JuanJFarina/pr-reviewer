### Beautiful is better than ugly.

- Code should be elegant, easy, simple, sophisticated, refined, and smart. Beautiful
  python code is code that follows all the next rules.

### Explicit is better than implicit.

- Use type annotations extensively. Nested types (e.g.,
  "dict[str, list[dict[str, Any]]]") should be avoided completely, either using pydantic
  models, classes, or using TypedDict or TypeAlias.
- Prefer functions and composition over classes and inheritance whenever possible.
- Classes should be used for defining data structures, contracts or encapsulating behavior.
- Inheritance should mostly be used for reusing data structures in more specific ones, or
  for Dependency Inversion Principle (by leveraging polymorphism).
- Prefer pure functions (without side effects) whenever possible.
- Your code should be completely explicit about what it does, not hiding anything.

### Simple is better than complex.

- Prefer simpler constructs, that is, do not use language features that make things
  either implicit or too hard to track the implementation details.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Avoid overusing inheritance or Protocols.

### Complex is better than complicated.

- When a simple solution is not possible, prefer a complex one (by leveraging more
  sophisticated design patterns or language features) over an overly complicated
  solution.
- Some problems are better solved by leveraging well known design patterns, if there is
  no pythonic way of solving it in a more simple fashion.
- Writing more code to solve a problem is always a bad idea, so never write complicated
  designs that require an extensive amount of code, if a more succinct option is
  available, be it simple (preferable) or at least complex (but still succinct).

### Flat is better than nested.

- Avoid nesting, the more levels of indentation the worst the code is.
- Do not go out of your way to avoid nesting, 3 levels is good, 4 is not desirable but is
  acceptable. 5 levels of indentation should not happen.

### Sparse is better than dense.

- Avoid having too many lines of code in one simple file, unless the logic only makes
  sense there. Most of the time, having some logic extracted in a nearby file and using a
  good descriptive name with type annotations should be good.
- Similarly, avoid having more than six python files in a single directory, either merge
  the code of some files, or put one or more files in folders accordingly.

### Readability counts.

- Code should be understandable as if reading plain english. Do not use comments to
  explain code.
- Be very descriptive with names.
- You can have longer functions and methods names for the sake of readability (up to 50
  chars if truly needed), but try to keep variables, arguments, and attributes names not
  too long (less than 30 chars).
- A shorter but descriptive name is always better than a longer and equally descriptive
  one.
