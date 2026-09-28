# AGENTS.md

## Purpose

This file is operational guidance for contributors and coding agents working in this repository. It describes the codebase as it exists now. It does not authorize the cleanup recommendations below to be treated as already implemented.

## Repository scope

Minion Decider is a desktop viewer for a local, metadata-rich image collection. The domain language used by the source is:

- **minion** — an image record;
- **card** — a tag or a reusable/compound filter definition;
- **episode** and **scene** — image metadata and filter dimensions;
- **relation** — the relationship between a minion and a card; and
- **view** — a database view or JSON-defined compound filter, depending on context.

The present application browses and filters data. No write path for assigning or editing tags is implemented.

## Source-of-truth map

| Area                                                 | Location                                    | Notes                                                                                                  |
| ---------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| npm scripts, dependencies, Jest, Prettier, packaging | `package.json`                              | Still contains inherited Electron React Boilerplate identity.                                          |
| Production native dependency                         | `release/app/package.json`                  | Contains `better-sqlite3`, rebuilt for Electron.                                                       |
| Build system                                         | `.erb/`                                     | Inherited Webpack/Electron build and packaging support. Avoid editing without a build-specific reason. |
| Electron lifecycle and IPC                           | `src/main/main.ts`                          | Loads configuration, creates the window, handles IPC, and registers asset protocols.                   |
| Runtime configuration                                | `src/main/runtimeConfig.ts`                 | Validates and persists paths and confines asset requests to configured roots.                          |
| Database operations                                  | `src/main/db.ts`                            | Initializes configured SQLite and contains all current SQL/query construction.                         |
| Data contract                                        | `data/`                                     | Version 1 SQLite baseline, disposable fixture, and image-path notes.                                   |
| Renderer bridge                                      | `src/main/preload.ts`                       | Exposes existing IPC methods and dedicated configuration methods.                                      |
| Shared process constants                             | `src/constants/`, `src/enums/`              | IPC channel, page size, DB operations/tables, and screen contexts.                                     |
| Renderer composition                                 | `src/renderer/App.tsx`                      | Loads global labels and selects exactly one primary screen.                                            |
| Navigation descriptors                               | `src/renderer/interfaces/setScreenProps.ts` | Builds screen-state objects; the app does not currently use URL routing.                               |
| Screens                                              | `src/renderer/screens/`                     | Lists and details for minions, cards, and categories.                                                  |
| Reusable UI                                          | `src/renderer/components/`                  | Categories, filters, minion images, chips, and loaders.                                                |
| Styling                                              | `src/renderer/App.css`                      | A single global stylesheet.                                                                            |
| Tests                                                | `src/__tests__/`                            | Currently contains one renderer smoke test.                                                            |
| Automation                                           | `.github/workflows/`                        | Test/package checks, publishing, and CodeQL.                                                           |

Do not infer the database schema from TypeScript interfaces alone. `data/migrations/001_initial.sql` captures the supplied version 1 schema; compare it with queries in `src/main/db.ts` and the actual database before claiming compatibility.

## Runtime flow

1. After Electron is ready, the main process loads and validates `runtime-config.json` from Electron's `userData` directory.
2. Missing or invalid configuration, or the `--configure` argument, starts native file/directory selection. A complete valid selection is persisted; cancellation exits the app.
3. The main process initializes SQLite with the configured database before creating a window.
4. Electron registers `minion`, `card`, and `file-system` protocol handlers rooted in the configured directories. Resolved paths are confined to those roots.
5. The preload script exposes `window.electron.ipcRenderer` through `contextBridge`.
6. The renderer sends an object on `default-channel`. The object includes an operation and usually a private reply channel.
7. The main process calls `dbOperation()` and replies on the requested private channel.
8. `App` first requests card, scene, and episode labels, then renders one screen selected through a `SetScreenProps` object.
9. List screens request rows and counts separately; minion lists paginate with 12 records per page.
10. Settings reads the active paths through dedicated preload methods. The main process validates a complete replacement, saves it atomically, then relaunches so SQLite and asset protocols use the new roots together.

This request/reply mechanism is current behavior, not a preferred template for new APIs. If a task changes this boundary, account for the main process, preload declaration, renderer callers, and tests together.

## Runtime data assumptions

Runtime paths are selected by the user and stored outside the repository in Electron's per-user `userData` directory. The source no longer assumes one developer's paths. Settings can review paths and use native selectors for replacement; cancelling keeps the existing resources, and applying changes restarts the app. A version 1 schema and disposable fixture are in `data/`; the application has no migration runner or import process. Image naming beyond the minion URL construction is not established. Never apply the baseline migration or fixture to an existing collection.

Never commit a personal runtime configuration, database, image corpus, credentials, or other local-only data. Configuration tests must use temporary files and directories.

## Coding conventions

Follow repository configuration rather than introducing a new style:

- Use TypeScript for application code and keep strict type checking enabled.
- Use two spaces, LF line endings, UTF-8, a final newline, and no trailing whitespace as defined by `.editorconfig`.
- Use single quotes as configured by Prettier.
- Follow the existing semicolon and trailing-comma style.
- Use function components and hooks for React UI.
- Use PascalCase for components and component files, camelCase for functions and local values, and uppercase underscore names for enum members and shared constant keys.
- Keep imports grouped at the top and use relative imports consistent with surrounding files.
- Prefer explicit domain types over `any`; existing `any` is technical debt, not a pattern to copy.
- Keep renderer-only UI in `src/renderer`; code with Electron, filesystem, protocol, or database privileges belongs in the main process or a carefully constrained preload API.
- Keep cross-process constants and enums in `src/constants` or `src/enums` when both layers need them.
- Preserve naming in the touched area unless a task explicitly includes a coordinated terminology migration.

Some prop-only modules use `.tsx` despite containing no JSX, and prop types are split inconsistently between component files and adjacent `*Props` files. Match the local pattern for focused changes; treat normalization as separate cleanup.

## Security and data rules

- Treat renderer input and database content as untrusted at the process boundary.
- Do not add renderer access to Node.js, Electron primitives, arbitrary filesystem paths, or raw database handles.
- Do not expand the generic IPC API without validation and an explicit allow-list.
- Parameterize SQL values. Table and view identifiers cannot be parameterized in SQLite, so allow-list them before interpolation.
- Preserve `contextBridge` isolation and avoid enabling `nodeIntegration`.
- Validate custom-protocol paths before resolving or fetching them; path traversal and escaping an asset root must not be possible.
- Do not log image metadata or local paths unless needed for diagnosis.
- Database mutations require an explicit task, transaction/error behavior, and tests. There are no mutations today.

## Testing and validation

The renderer baseline is one smoke test in `src/__tests__/App.test.tsx`. It only verifies that rendering `App` returns a truthy result. `src/__tests__/runtimeConfig.test.ts` adds focused path validation, atomic persistence, asset resolution, and traversal coverage; `src/__tests__/Settings.test.tsx` covers settings interactions. Do not claim broad application coverage from these tests.

Use the checks relevant to a change:

```sh
npm test
npm run lint
npm exec tsc
npm run build
```

`npm run package` is the broadest repository check and is run in CI, but it is slower and invokes platform packaging. Native dependency changes may also require `npm run rebuild` or `npm run rebuild-sql`.

When behavior changes, add focused tests where practical:

- pure query/transform logic: unit tests;
- renderer components: Testing Library interaction tests;
- IPC: handler tests with validated requests and structured failures;
- database behavior: fixture-backed integration tests using a temporary database; and
- custom protocols: tests for valid paths, malformed URLs, traversal, and missing files.

Tests must not depend on a developer's saved runtime configuration, database, or personal image directories.

## Change discipline

Before changing code:

1. Identify whether the change crosses Electron main, preload, and renderer boundaries.
2. Inspect the adjacent interfaces, enums, and navigation descriptors.
3. Distinguish current behavior from desired cleanup; do not combine unrelated refactors with a feature or fix.
4. Check whether inherited `.erb` behavior already solves the build concern.

While changing code:

- Keep diffs focused and avoid formatting unrelated files.
- Update types and tests with behavior.
- Keep loading, empty, and error states explicit.
- Clean up subscriptions created by React effects.
- Avoid hard-coded record IDs, paths, channels, and placeholder UI.
- Preserve the current read-only data behavior unless mutations are specifically requested.

Before completion:

- Run TypeScript, lint, and relevant tests.
- Run a build when process boundaries, bundling, assets, or dependencies change.
- Report checks not run and machine-specific behavior that could not be verified.
- Update `README.md` when setup, scope, architecture, scripts, or limitations change.

## Known test and design gaps

No focused automated coverage currently exists for SQL construction, operation dispatch, IPC, Electron protocol registration, category-tree transforms, navigation, filters, pagination, loading/error states, or accessibility. High-risk implementation details include dynamic SQL, arbitrary IPC channel names, listeners registered during React rendering, and database compatibility with the version 1 baseline.

## Suggested cleanup backlog — not implemented

Keep cleanup work incremental and separately reviewable. Suggested order:

1. Capture representative behavior with tests before structural changes.
2. Verify compatibility with the version 1 baseline and image layout; add separately numbered migrations for later changes.
3. Extend configuration management with deeper schema and image availability checks if needed; in-app path selection and a controlled restart exist.
4. Define typed request/response contracts and replace generic IPC forwarding with allow-listed handlers.
5. Extract and test query builders; parameterize values and allow-list identifiers.
6. Move renderer listener registration into effects with cleanup and structured error handling.
7. Replace placeholder IDs/content and settle public domain terminology.
8. Add semantic controls, alt text, keyboard behavior, and accessibility tests.
9. Audit unused dependencies, stale boilerplate files, package metadata, release settings, and CI versions.
10. Add a supported tagging/mutation workflow only after the data and process contracts are explicit.

These are recommendations, not standing permission to perform broad refactors during unrelated tasks.
