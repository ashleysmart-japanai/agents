# Feature Toggle

Enable or disable features at runtime without deploying new code.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A conditional check in code determines whether a feature is active. The toggle state is read from configuration, a feature flag service, or a database. Toggles can be global, per-user, per-tenant, or percentage-based.

**When to use**:
- Deploying code before a feature is ready for all users (trunk-based development).
- A/B testing or gradual rollouts.
- Kill switches for risky features.

**Trade-offs**:
- Toggle checks accumulate and become technical debt if not removed after the feature is stable.
- Complex combinations of toggles produce hard-to-test code paths.
- The toggle store is a runtime dependency.
