# Externalized Configuration

Extract all environment-specific configuration from the service binary into an external store.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Configuration (connection strings, feature flags, timeouts) is stored outside the service in a config store, environment variables, or a secrets manager. Services read configuration at startup or dynamically. The same binary runs in every environment.

**When to use**:
- The same service binary must run in development, staging, and production with different settings.
- Configuration must be changeable without rebuilding or redeploying the service.
- Secrets must not be committed to source control.

**Trade-offs**:
- The config store becomes a dependency — its availability affects service startup.
- Dynamic configuration changes can produce inconsistent state across running instances.
