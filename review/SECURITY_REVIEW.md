# Security Review Check Groups

> **Method**: Follow the review methodology in [REVIEW_METHOD.md](REVIEW_METHOD.md) before running these check groups.

Run against every PR that touches APIs, credentials, auth, or external service integrations.

---

## Step 0 — Trace the security model end-to-end

Before running any checklist, map how security actually works. No assumptions. Trace the code.

1. **Identify every landing point** — grep for all route handlers (`@Get`, `@Post`, `@Delete`, `@Patch`, `@Put`, API route files, tRPC procedures). List them all. No omissions.
2. **Trace the auth chain for each** — from HTTP request to data access. What guards/middleware run? What service methods? What DB queries? Full path, not just the first check.
3. **Understand the IAM layers** — the codebase may have multiple auth systems that look similar but are different:
   - **User authentication** — session, token, API key. Who is the caller?
   - **Org membership** — is the caller a member of the requested org?
   - **Project-level IAM** — does the caller have permission for this action on this project? (e.g., `evaluateAccess` with resource policies)
   - **Admin realm isolation** — is the org in the caller's admin realm?
   - **Service-to-service auth** — internal services calling each other. Trusted headers? Tokens? Nothing?
   - **Local policy evaluator vs remote IAM service** — they may use different action/resource formats. Verify the actual payloads reach the evaluator in the format it expects. Mock-based tests that never test real payloads prove nothing.
4. **Understand the user hierarchy** — check each level fully:
   - **System/service accounts** — full access, internal only
   - **Admin** — org-level management, realm-scoped
   - **Editor** — project-level write access
   - **Member** — project-level read access
   - **Anonymous/unauthenticated** — should have zero access
5. **For each landing point, verify every level applies**:
   - Is the caller authenticated?
   - Is org membership enforced?
   - Is project-level IAM enforced when projectId is set?
   - Is the IAM action correct for the operation (READ vs CREATE vs UPDATE vs DELETE)?
   - Do the IAM payloads use the format the evaluator actually accepts? (e.g., dotted permission strings, correct JRN format — verify against the evaluator code, not the type signature)
   - What happens when optional params are omitted? Does auth degrade silently?
   - What happens when the IAM service is unreachable? Fail-closed or fail-open?

---

## Authentication & Authorization

- [ ] Every endpoint requires caller identity — no silent fallback to system/anonymous
- [ ] Credential CRUD scoped by organizationId at the service layer, not just the proxy
- [ ] GET/UPDATE/DELETE by ID verify the record belongs to the caller's org before operating
- [ ] List endpoints require organizationId — omitting it never returns all orgs
- [ ] caller-supplied userId in request bodies cannot impersonate — always use callerContext.userId
- [ ] Admin proxy forwards caller identity to backend services (IAM headers, not just request ID)
- [ ] Backend rejects missing caller context with 401/403, not fallback to SYSTEM_USER
- [ ] Every credential mutating endpoint (create/update/delete) calls requireCallerContext or equivalent — no omissions after refactors
- [ ] Auth checks are centralized (guard/decorator), not per-method — prevents accidental omission

## Tenant Isolation

- [ ] Every route that accepts organizationId calls assertOrganizationInRealm (not just isOrganizationInScope)
- [ ] Every route that accepts/derives projectId calls assertProjectInRealm
- [ ] Org/project IDs from base64-encoded compound keys are validated, not trusted
- [ ] Cross-tenant tests exist: org A cannot list/read/update/delete org B's resources

## Runtime Credential Scoping

- [ ] Runtime credential resolution includes organizationId in the query — not just credentialId
- [ ] Credential lookup at runtime: `WHERE id = ? AND organizationId = ?` (or equivalent)
- [ ] providerName validated against expected adapter sourceType at resolution time
- [ ] credentialId in sourceMappings validated at entity upsert time (belongs to same org, correct provider)
- [ ] Cross-tenant credential test: entity in org A cannot use credential from org B
- [ ] Moving credential resolution to a new service preserves all scoping — audit after refactors

## Credential Exposure

- [ ] GET endpoints never return decrypted secrets (passwords, tokens, API keys)
- [ ] Display fields (email, subdomain, instance_url) are masked or returned as booleans
- [ ] Credential field names (keys) can be returned; values cannot
- [ ] Encrypted blobs are never forwarded to the client — decrypt server-side, mask, return

## OAuth Flows

- [ ] State parameter is cryptographically signed — not plain base64
- [ ] Callback validates state signature before processing
- [ ] Authorization URL domain is whitelisted — no caller-controlled redirect targets
- [ ] Token exchange URL is whitelisted — no caller-controlled SSRF via state.loginDomain
- [ ] OAuth client secrets never appear in client-visible code or responses
- [ ] PKCE (code_challenge/code_verifier) used where supported
- [ ] Secrets stored between authorize and callback survive multi-instance deployments — no in-process Map/cache that breaks when authorize and callback land on different instances
- [ ] If using cookies to carry secrets: encrypted (AES-256-GCM or equivalent), HttpOnly, Secure, SameSite=Lax
- [ ] If using server-side cache: shared across all instances (Redis/DB), not per-process

## SSRF / Egress Control

- [ ] URLs constructed from stored credentials (instance_url, api_domain, subdomain, host) are validated against domain whitelists
- [ ] No user-controlled input flows into fetch/HTTP client URLs without validation
- [ ] Internal service URLs (metadata servers, localhost, RFC1918) are explicitly blocked
- [ ] Every shared client lib has a domain validation regex (not just `z.string().min(1)`)
- [ ] Credential-controlled base URLs (e.g., Raclear baseUrl) are either whitelisted or configured server-side, not arbitrary
- [ ] OAuth token refresh URLs are derived from validated domains, not raw credential fields
- [ ] Subdomain fields validated with strict regex — no dots, slashes, control chars, protocol prefixes

## Injection

- [ ] User input in KQL/SOQL/SQL queries is escaped or parameterized
- [ ] Field names from user input are validated against known schemas before query construction
- [ ] No string interpolation of user input into query strings without escaping
- [ ] Record IDs are escaped before embedding in query strings (KQL `$id = "..."`, SOQL `Id IN ('...')`)
- [ ] Resource/object names in queries are validated or quoted — not raw string interpolation
- [ ] Escaping covers ALL query paths — both keyword search (_q) AND findByRecordIds

## Batch / DoS Protection

- [ ] findByRecordIds enforces a max batch size before dispatching to adapters
- [ ] Per-ID sequential fetch loops (no bulk API) have a hard cap and bounded concurrency
- [ ] Pagination loops have a max-page safety limit to prevent runaway requests
- [ ] Caller-supplied arrays (recordIds, linkIds, etc.) are length-validated at the API boundary

## Input Validation

- [ ] sourceType/providerName validated against registered adapters — arbitrary strings rejected
- [ ] Zod validation on all create/update request bodies at the API boundary
- [ ] Pagination limits enforced (max limit, max offset)
- [ ] Resource identifiers (appId, collection name, recordId) validated before external API calls

## DI / Framework Safety

- [ ] NestJS provider patterns use supported semantics — no Angular-style `multi: true` (not supported in NestJS)
- [ ] Multi-provider injection uses useFactory pattern: `useFactory: (...adapters) => adapters, inject: [Class1, Class2, ...]`
- [ ] Registry/module tests assert all expected providers are registered at runtime
- [ ] Refactors that move auth checks between files are verified — grep for requireCallerContext coverage on all mutating endpoints

## Error Exposure

- [ ] Stack traces never serialized into HTTP response bodies — internal file paths, function names, and package structure enable targeted attacks
- [ ] Error `details` / `cause` objects stripped of stack traces before client-facing serialization
- [ ] Internal error messages reviewed for information leakage (class names, DB table names, query fragments)
- [ ] Wrap-and-rethrow patterns do not forward `error.stack` into client-visible fields (e.g. `details`, `meta`, `context`)
- [ ] Error responses use generic messages for 5xx; detailed messages only for 4xx input validation

## Logging

- [ ] Credentials, tokens, passwords, API keys never appear in logs
- [ ] Only credential IDs logged, not values
- [ ] Error messages from external services sanitized before logging (no token leakage)
