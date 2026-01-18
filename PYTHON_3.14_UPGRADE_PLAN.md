# Python 3.14 Upgrade Plan for pytraccar

**Current State:** Python 3.13 minimum version
**Target State:** Python 3.14 minimum version
**Date:** 2026-01-18

## Executive Summary

This document outlines the plan to upgrade pytraccar to Python 3.14 as the minimum supported version. The upgrade primarily involves configuration updates, dependency verification, code quality improvements, and comprehensive testing to ensure compatibility with Python 3.14.

**Note:** This is a conservative upgrade focused on version bumps and compatibility verification. The codebase already uses modern Python patterns and does not require significant refactoring.

---

## Phase 1: Configuration & Metadata Updates

### 1.1 Update pyproject.toml
**Files:** `pyproject.toml`

**Changes Required:**
- Update `requires-python = ">=3.13"` → `">=3.14"` (line 18)
- Update `python = "^3.13"` → `"^3.14"` (line 32)
- Update `python_version = "3.13"` → `"3.14"` (line 59, mypy config)

**Rationale:** Set the minimum version constraint for the project and ensure tooling uses the correct Python version for type checking.

### 1.2 Update GitHub Actions Workflow
**Files:** `.github/workflows/actions.yml`

**Changes Required:**
- Update all Python version references from `"3.13"` to `"3.14"` (lines 21, 24, 42, 76, 79)
- Update test matrix to include `"3.14"` (line 42)

**Rationale:** Ensure CI/CD pipeline tests against Python 3.14.

### 1.3 Update README Badge
**Files:** `README.md`

**Changes Required:**
- Update badge from `Python-3.13-indigo.svg` → `Python-3.14-indigo.svg` (line 4)

**Rationale:** Reflect the minimum supported Python version in documentation.

### 1.4 Update Dependencies
**Files:** `pyproject.toml`, `poetry.lock`

**Changes Required:**
- Run `poetry update` to update all dependencies to Python 3.14-compatible versions
- Review and update pinned dependency versions in `[tool.poetry.group.dev.dependencies]`
- Verify all dependencies support Python 3.14

**Rationale:** Ensure all dependencies are compatible with Python 3.14.

---

## Phase 2: Verify Python 3.14 Compatibility

### 2.1 Review Exception Handling Syntax
**Files:** All Python files with multiple exception types

**Changes Required:**
- Review exception handling clauses to take advantage of simplified syntax
- Where multiple exceptions are caught without an `as` clause, parentheses can now be omitted
- Example: `except (Exception1, Exception2):` can become `except Exception1, Exception2:`

**Current Status:**
- `pytraccar/client.py:129` - `except (TraccarAuthenticationException, TraccarResponseException):`
- `pytraccar/client.py:135` - `except (aiohttp.ClientError, asyncio.CancelledError) as exception:`
- `pytraccar/client.py:280-285` - Multiple WSMsgType checks

**Decision:** Keep existing syntax for readability. The new syntax is optional and the current parenthesized form remains valid and more explicit.

---

## Phase 3: Review Python 3.14 Features (Information Only)

### 3.1 Review pathlib Usage
**Files:** Entire codebase

**Current Status:**
- The project does not appear to use pathlib extensively
- No file operations that would benefit from the new pathlib.Path.copy_recursive() or pathlib.Path.move() methods

**Changes Required:**
- No immediate changes needed
- Document for future reference that Python 3.14 pathlib enhancements are available

**Rationale:** Python 3.14 adds recursive copying and moving to pathlib, but this library doesn't perform filesystem operations.

### 3.2 Compression Module Reorganization (Future Consideration)
**Current Status:**
- The project does not use any compression modules (zlib, gzip, bz2, lzma, or zstd)

**Changes Required:**
- None at this time
- Document for future reference

**Rationale:** Python 3.14 reorganizes compression modules under `compression.*` namespace, but this doesn't affect the current codebase.

### 3.3 asyncio Changes Verification
**Files:** `pytraccar/client.py`

**Critical Change:** `asyncio.get_event_loop()` now raises RuntimeError if no event loop exists

**Current Status:**
- The project does not call `asyncio.get_event_loop()` anywhere
- Uses modern async/await patterns with `aiohttp.ClientSession`
- No implicit event loop creation

**Changes Required:**
- None - the codebase is already compliant

**Rationale:** Verify compliance with asyncio behavioral changes in Python 3.14.

---

## Phase 4: Code Quality & Modern Python Patterns

### 4.1 Type Hints Enhancement
**Files:** All model files using TypedDict

**Current Pattern:**
```python
class DeviceModel(TypedDict):
    """Model for the devices response."""
    id: int
    name: str
    # ...
```

**Opportunity:**
- Python 3.14's deferred annotation evaluation improves performance for type-heavy code
- Consider using `typing.TypedDict` with `total=False` for optional fields more explicitly
- Review use of `dict[str, Any]` vs more specific types

**Changes Required:**
- Review model definitions in `pytraccar/models/` directory
- Consider splitting required and optional fields using TypedDict inheritance
- This improves type safety with minimal runtime overhead

**Example Enhancement:**
```python
class DeviceModelRequired(TypedDict):
    id: int
    name: str
    uniqueId: str
    status: str
    disabled: bool

class DeviceModel(DeviceModelRequired, total=False):
    lastUpdate: str | None
    phone: str | None
    model: str | None
    contact: str | None
    category: str | None
    attributes: dict[str, Any]
```

**Rationale:** Improved type safety and better IDE support.

### 4.2 Review Enum Usage
**Files:** `pytraccar/models/subscription.py`

**Current Pattern:**
```python
class SubscriptionStatus(StrEnum):
    CONNECTED = "connected"
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    ERROR = "error"
```

**Status:**
- Already using `StrEnum` (introduced in Python 3.11)
- No changes needed - this is modern best practice

**Rationale:** Verify enum usage is optimal for Python 3.14.

### 4.3 Modern datetime Patterns
**Files:** `pytraccar/client.py`

**Current Pattern:**
```python
from datetime import UTC, datetime, timedelta
# ...
datetime_now = datetime.now(tz=UTC).replace(tzinfo=None)
```

**Status:**
- Already using `datetime.UTC` (Python 3.11+)
- Pattern is intentionally removing timezone for API compatibility

**Changes Required:**
- None - already using modern datetime patterns

**Rationale:** Verify datetime usage aligns with Python 3.14 best practices.

---

## Phase 5: Testing & Validation

### 5.1 Update Test Suite
**Files:** All test files in `tests/` directory

**Changes Required:**
- Run full test suite with Python 3.14
- Verify 100% code coverage is maintained (current requirement)
- Update any Python version-specific tests if present
- Check for deprecation warnings

**Commands:**
```bash
poetry install
poetry run pytest --cov --cov-report=term-missing
poetry run mypy pytraccar
poetry run ruff check pytraccar
```

**Success Criteria:**
- All tests pass
- Coverage remains at 100%
- No mypy errors
- No ruff violations
- No deprecation warnings

### 5.2 Update pre-commit Hooks
**Files:** `.pre-commit-config.yaml`

**Current Status:**
- Already using poetry run commands
- System language hooks will use the poetry environment

**Changes Required:**
- Verify all pre-commit hooks work with Python 3.14
- Test the complete pre-commit workflow

**Commands:**
```bash
poetry run pre-commit run --all-files
```

---

## Phase 6: Documentation Updates

### 6.1 Update Contribution Guide
**Files:** `README.md`

**Changes Required:**
- Update any Python version references in contribution instructions
- Verify example code works with Python 3.14
- Update development environment setup instructions if needed

### 6.2 Update Example Code
**Files:** `example.py`

**Current Status:**
```python
async with aiohttp.ClientSession(
    cookie_jar=aiohttp.CookieJar(unsafe=True)
) as client_session:
```

**Changes Required:**
- Verify example code runs correctly with Python 3.14
- Test with actual Traccar server or mocked environment
- Ensure all imports and patterns are Python 3.14 compatible

### 6.3 Add Migration Notes
**Files:** Create `CHANGELOG.md` or update existing changelog

**Changes Required:**
- Document the Python version requirement change
- Note any breaking changes for users
- Provide migration guidance

**Example Entry:**
```markdown
## [Next Version] - YYYY-MM-DD

### Breaking Changes
- **Minimum Python version increased to 3.14**
  - Users must upgrade to Python 3.14 or later
  - All dependencies have been updated to support Python 3.14
  - See PYTHON_3.14_UPGRADE_PLAN.md for technical details

### Improvements
- Verified compatibility with Python 3.14
- Updated dependencies to Python 3.14-compatible versions
- Enhanced type hints for better type safety
```

---

## Implementation Order

The phases should be executed in the following order:

1. **Phase 1** - Update configuration and metadata
2. **Phase 2** - Verify Python 3.14 compatibility (review only)
3. **Phase 3** - Review new features (information only, no changes required)
4. **Phase 4** - Code quality improvements (optional enhancements)
5. **Phase 5** - Testing and validation
6. **Phase 6** - Documentation updates

---

## Risk Assessment

### Low Risk
- Configuration updates (Phase 1)
- Documentation updates (Phase 6)
- Code quality improvements (Phase 4) - optional enhancements

### Medium Risk
- Dependency updates - some dependencies may not support Python 3.14 yet
- Test suite validation - may reveal unexpected compatibility issues

### High Risk
- None identified - the project already uses modern Python patterns and no breaking code changes are planned

---

## Timeline Considerations

**Prerequisites:**
- Python 3.14 must be released (Released: October 7, 2025 ✓)
- All dependencies must support Python 3.14
- CI/CD infrastructure must support Python 3.14

**Estimated Effort:**
- Phase 1: 1-2 hours (configuration updates and dependency verification)
- Phase 2: 30 minutes (compatibility review - no changes expected)
- Phase 3: 15 minutes (information only - documentation review)
- Phase 4: 2-3 hours (optional code quality improvements)
- Phase 5: 2-4 hours (testing and validation)
- Phase 6: 1-2 hours (documentation updates)

**Total Estimated Effort:** 7-12 hours

**Note:** The majority of effort is in testing/validation (Phase 5) and optional code quality improvements (Phase 4). The core upgrade (Phases 1-3, 6) is estimated at 3-5 hours.

---

## Rollback Plan

If issues are encountered:

1. **Git Branch:** All changes should be on the feature branch `claude/plan-python-3.14-upgrade-uMTFH`
2. **Dependency Lock:** Keep a backup of `poetry.lock` before updates
3. **Version Pin:** If specific dependencies fail, pin to working versions
4. **Gradual Migration:** Can support both 3.13 and 3.14 temporarily using `requires-python = ">=3.13"`

---

## Success Criteria

The upgrade will be considered successful when:

- ✅ All configuration files reference Python 3.14
- ✅ All tests pass on Python 3.14
- ✅ 100% code coverage maintained
- ✅ No mypy type checking errors
- ✅ No ruff linting violations
- ✅ All pre-commit hooks pass
- ✅ CI/CD pipeline succeeds
- ✅ Example code runs successfully
- ✅ Documentation is updated
- ✅ No deprecation warnings from Python 3.14

---

## Post-Upgrade Monitoring

After deployment:

1. Monitor PyPI download statistics for Python version distribution
2. Watch for bug reports related to Python 3.14 compatibility
3. Track potential performance improvements from Python 3.14 optimizations:
   - Incremental garbage collection (automatic benefit)
   - Improved free-threaded mode (if applicable to workload)
   - General runtime improvements

---

## References

- [Python 3.14 Release Notes](https://docs.python.org/3/whatsnew/3.14.html)
- [PEP 749: Deferred Evaluation of Annotations](https://peps.python.org/pep-0749/)
- [Better Stack: Python 3.14 New Features](https://betterstack.com/community/guides/scaling-python/python-3-14-new-features/)
- [Cloudsmith: Python 3.14 Release Guide](https://cloudsmith.com/blog/python-3-14-what-you-need-to-know)
- [Real Python: Python 3.14 Released](https://realpython.com/python-news-november-2025/)

---

## Questions & Considerations

1. **Dependency Compatibility:** Have all dependencies (especially aiohttp) released Python 3.14-compatible versions?
2. **Breaking Changes:** Are there any user-facing API changes required? (Expected: None)
3. **Performance Testing:** Should we benchmark before/after to quantify improvements?
4. **User Impact:** What percentage of current users are on Python 3.13 vs earlier versions?
5. **Support Timeline:** How long should we maintain Python 3.13 support in a separate branch?

---

## Appendix A: Files Requiring Changes

### Configuration Files (Required)
- `pyproject.toml` - Update Python version constraints
- `.github/workflows/actions.yml` - Update CI/CD Python version
- `README.md` - Update version badge

### Documentation Files (Required)
- `README.md` - Update contribution guidelines if needed
- `example.py` - Verify compatibility (no changes expected)
- Changelog - Document version requirement change

### Python Source Files (Optional - Code Quality Improvements)
- `pytraccar/models/*.py` - Consider TypedDict enhancements
- All source files - Review and enhance type hints as needed

### Test Files (Validation)
- All files in `tests/` directory - Verify tests pass on Python 3.14

---

## Appendix B: Dependency Checklist

Dependencies to verify for Python 3.14 compatibility:

**Runtime Dependencies:**
- [ ] aiohttp ^3.13

**Development Dependencies:**
- [ ] codespell 2.4.1
- [ ] coverage 7.13.1
- [ ] mypy 1.19.1
- [ ] pre-commit 4.5.1
- [ ] pre-commit-hooks 6.0.0
- [ ] pytest 9.0.2
- [ ] pytest-asyncio 1.3.0
- [ ] pytest-cov 7.0.0
- [ ] ruff 0.14.13
- [ ] safety 3.7.0

**Build Dependencies:**
- [ ] poetry-core >=1.0.0

---

## Appendix C: Python 3.14 Features Summary

**Features Applicable to This Project:**
1. ✅ Deferred annotation evaluation (PEP 749) - Already using `from __future__ import annotations` which remains compatible
2. ✅ Improved asyncio behavior - Already compliant, not using deprecated patterns
3. ✅ Performance improvements - Automatic benefits (incremental GC, runtime optimizations)
4. ❌ Template string literals - Not adopting at this time
5. ❌ pathlib enhancements - Not applicable (no filesystem operations)
6. ❌ Compression module reorganization - Not applicable (no compression used)
7. ❌ Subinterpreters - Not applicable to this library's use case

**Breaking Changes Verified:**
1. ✅ `asyncio.get_event_loop()` behavior change - Not used in this project (compliant)
2. ✅ Exception syntax changes - Optional enhancement, keeping current syntax for clarity
3. ✅ No other breaking changes affect this codebase

---

*End of Python 3.14 Upgrade Plan*
