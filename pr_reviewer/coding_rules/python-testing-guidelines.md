Follow these instructions for optimal tests suites:

### Test Suite Design

- Create unit tests for all Domain functions and public methods.
- Create unit tests for all Infrastructure functions and public methods.
- Create integration tests for all Services (these should use Fake Infrastructure objects).
- Create E2E tests for all API code (these should use the Services objects with Fake Infrastructure objects).
- Coverage should be of 100% of the codebase, except for "# pragma: no cover" directives.
- If something is too complex to test and is not too critical, you may use a "# pragma: no cover" directive.

### Test Best Practices

- Use pytest.
- Use normal functions for tests, DO NOT use classes.
- Use one or more asserts in the same test only if they handle the same case (that is, they will most likely fail or pass altogether).
- Write tests mirroring the package structure adding a directory for happy paths and error cases (e.g. "package/app.py" - "tests/app/happy_paths.py" and "tests/app/error_cases.py).
- Use fixtures for values and objects setup.
- Keep fixtures in a conftest.py file close to where they're used, ideally in the same directory.
- If a fixture is used by multiple tests throughout the suite, put it in a conftest.py in a higher-level directory.
- Prefer fewer tests that cover the critical happy paths and edge cases (1-2 happy paths per entrypoint, that is per function/method).
- Prefer short and simpler tests.

- Do not use Mocks/Stubs/Patches anywhere except in Infrastructure real objects.
- Do not write multiple tests with different asserts if they will pass or fail in the same scenario, group those asserts in the same test to avoid redundancy.
- Do not test ABC classes.

### Test Template (tests should look similar to this)

def test_func_x(fixture_a: str, fixture_b: SomeObject) -> None:
    result = func_x(fixture_a, fixture_b)

    assert isinstance(result, ResultObject)
    assert result.success
