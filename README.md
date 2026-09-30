# Minion Decider

Minion Decider is a Windows-oriented Electron and React desktop application for browsing a locally maintained image collection and exploring its metadata. In the current codebase, an image is called a **minion**, while **cards** represent tags or reusable filters.

This repository is an in-progress application derived from Electron React Boilerplate. It requires an existing, schema-compatible SQLite database and image collection; neither is distributed with the repository.

## Current scope

The implemented UI can:

- browse images in pages of 12;
- open an individual image in screen, popup, side-panel, or tooltip contexts;
- filter images by image IDs, episodes, scenes, cards/tags, card relationships, or database views;
- browse searchable, hierarchical tag/card categories;
- browse episode and scene categories;
- inspect card details and JSON-defined compound filters; and
- view filter match counts and matching minions, edit and save existing filter conditions, and inspect a representative related minion;
- open a tag's details to see its subs, its direct image count, and the distinct image count of its whole subtree, and jump from any of those counts to the filtered image list;
- create, rename, and remove tags from the tag details screen;
- inspect a minion's season, episode, scene, related-card hierarchy, and source file; and
- reveal a source image in Explorer or copy it to an optional output directory configured in Settings; and
- load image and metadata records from a local SQLite database.

The application can save edits to a card's compound filter, add a sub tag, rename a tag, and remove a tag. Removal is refused for any tag that still has subs or image relations, so no relation is ever deleted implicitly. There is still no UI or database operation for assigning or unassigning tags on individual images.

## Architecture

The application has three runtime layers:

1. **Electron main process** — creates the window, registers custom image protocols, owns the SQLite connection, and handles database requests.
2. **Preload bridge** — exposes typed database and configuration methods through `contextBridge`.
3. **React renderer** — renders navigation, category lists, image grids, details, filters, pagination, popups, and side panels.

Renderer database requests use dedicated `ipcRenderer.invoke` methods for labels, categories, cards, minions, counts, related-card hierarchies, and card-filter updates. The main process registers matching `ipcMain.handle` endpoints, validates the caller and input, and returns either data or a structured error. Configuration and minion source/copy actions use separate allow-listed methods. No arbitrary IPC channel, SQL operation, or renderer-supplied filesystem path is exposed.

The project uses:

- Electron 35;
- React 19 and TypeScript 5;
- Material UI 7;
- `better-sqlite3`;
- Webpack through Electron React Boilerplate; and
- Jest, Testing Library, ESLint, and Prettier for validation.

## Runtime configuration and data prerequisites

On first start, the application displays native selectors for the SQLite database file, minion image root, card image root, and general file-system image root. Each path is validated for existence and expected file type before it is accepted.

The selected paths are saved as `runtime-config.json` in Electron's per-user application-data directory and validated again on later starts. The database is opened before the application window is created. Cancelling configuration or selecting an inaccessible resource exits without opening the renderer.

Launch the application with the `--configure` argument to replace an existing valid configuration. The previous configuration remains on disk until a complete replacement is selected and validated.

While the application is running, select **Settings** in the left navigation to review the active paths. Use **Choose…** beside a path to select a replacement with a native dialog; Cancel discards the draft. The minion copy output directory is optional. **Save and restart** validates the complete selection, probes a changed SQLite file read-only for essential tables and count views, saves the configuration atomically, and relaunches the application. If validation or saving fails, the current session and saved configuration remain unchanged. A restart is required so the database connection and all image protocol roots switch together. The `--configure` startup option remains available.

The SQLite database is expected to contain the tables, views, and columns referenced in `src/main/db.ts`, including `minions`, `cards`, `episodes`, `scenes`, relationship tables, and precomputed count views. The supplied version 1 baseline, a disposable test fixture, and image-path notes are in [data/README.md](data/README.md). The application does not run migrations or install fixtures; **never apply the baseline or fixture to an existing collection**. No production database, image corpus, or import workflow is included.

As a result, cloning and starting the repository on another machine is not enough to obtain a working application. The user must select an existing image collection and a database compatible with the queries. Compatibility with the version 1 baseline is not checked automatically.

## Development

### Requirements

- Node.js 22 is the version used by GitHub Actions. Package metadata currently advertises Node.js 14 or newer, but this has not been reconciled with CI or the current dependency set.
- npm 7 or newer.
- A supported native build toolchain for Electron and `better-sqlite3`.
- A schema-compatible database and its corresponding image directories.

### Install and start

```sh
npm install
npm start
```

`npm install` runs the repository's post-install tasks, installs Electron native dependencies, and builds the development DLL. The development server uses port `666` unless `PORT` is set.

### Useful commands

| Command               | Purpose                                                                      |
| --------------------- | ---------------------------------------------------------------------------- |
| `npm start`           | Build development bundles, run the renderer dev server, and launch Electron. |
| `npm test`            | Run the Jest test suite.                                                     |
| `npm run lint`        | Run ESLint over JavaScript and TypeScript sources.                           |
| `npm exec tsc`        | Run strict TypeScript checking without emitting output.                      |
| `npm run build`       | Build production main and renderer bundles.                                  |
| `npm run package`     | Build and package the app for the current platform.                          |
| `npm run rebuild`     | Rebuild native dependencies in `release/app`.                                |
| `npm run rebuild-sql` | Force-rebuild `better-sqlite3` for Electron.                                 |

Packaging is configured for Windows NSIS, Linux AppImage, and macOS targets. Runtime path selection is cross-platform, but packaged behavior has not been verified on every target.

## Project structure

```text
.
├── .erb/                   Electron React Boilerplate build configuration
├── .github/workflows/      CI, publishing, and CodeQL workflows
├── assets/                 Application icons and platform assets
├── data/                   SQLite baseline, disposable fixture, and data-contract notes
├── release/app/            Production runtime package and native dependency
├── src/
│   ├── __tests__/          Jest tests
│   ├── constants/          Shared IPC and pagination constants
│   ├── enums/              Database operations/tables and screen contexts
│   ├── main/               Electron main process, runtime config, SQLite, menu, and preload
│   └── renderer/           React application, navigation, screens, and components
├── AGENTS.md               Contributor and coding-agent guidance
├── package.json            Scripts, dependencies, Jest, Prettier, and packaging
└── tsconfig.json           Strict TypeScript configuration
```

## Tests and automated checks

The suite contains a renderer smoke test, settings interaction tests, database IPC validation tests, and focused runtime-configuration tests covering path validation, atomic replacement failure, persistence/loading, in-root asset resolution, and traversal rejection. There are no focused tests for:

- SQLite query construction or database operations;
- Electron-backed IPC registration or end-to-end transport;
- Electron custom protocol registration and responses;
- category tree construction and filtering;
- navigation and screen selection;
- pagination; or
- failure and empty-data states.

GitHub Actions runs packaging, linting, TypeScript checking, and Jest on pushes and pull requests. The broad CI commands are more comprehensive than the current behavioral test coverage.

## Coding standards observed in the repository

- TypeScript is configured with strict mode and the React JSX transform.
- EditorConfig requires UTF-8, LF line endings, two-space indentation, trimmed trailing whitespace, and a final newline.
- Prettier uses single quotes; existing TypeScript follows semicolon and trailing-comma conventions from the inherited tooling.
- ESLint extends the Electron React Boilerplate configuration with TypeScript support and several relaxed import and shadowing rules.
- React code uses function components and hooks.
- Shared constants and enums live outside the renderer when they are used across process boundaries.
- Component and screen prop types are generally kept in adjacent files, although naming and file extensions are not fully consistent.

See `AGENTS.md` for contributor-focused constraints and validation guidance.

## Known limitations

- Initial runtime configuration uses sequential native dialogs; in-app settings require a restart and do not verify full database schema compatibility or the presence of image files.
- A version 1 SQLite baseline is documented, but there is no migration runner or automatic compatibility check for existing databases. Image naming beyond the renderer's minion URL construction is not established.
- Package name, description, product name, author, repository links, and portions of release configuration still identify Electron React Boilerplate.
- Database query construction is separated from execution, dynamic values are parameterized, and dynamic view identifiers are checked against existing database views. Fixture-backed coverage for representative query behavior is still missing.
- Other renderer data/effect behavior needs additional validation and consistent error-state coverage.
- Several production-facing values are placeholders or hard-coded, including navigation IDs and default detail content.
- Error handling is mostly console logging; the renderer has no consistent error state.
- There is no state-management or routing library in active use despite `react-router-dom` being installed.
- Accessibility is incomplete, including clickable images without equivalent button semantics or alternative text.
- Automated behavior coverage is minimal.

## Suggested cleanup — not implemented

The following items are recommendations only; they do not describe completed work:

1. **Extend the data contract.** Verify existing-database compatibility, document remaining image naming conventions, and add new numbered migrations as the contract evolves. A version 1 baseline and disposable fixture are already in `data/`.
2. **Extend configuration management.** The Settings screen now reviews and replaces paths with a controlled restart; consider richer validation of database compatibility and image availability.
3. **Rename inherited metadata.** Update package, product, repository, author, release, badge, and changelog references to this application.
4. **Extend process-boundary coverage.** Typed, allow-listed database and configuration methods replace the generic pass-through; add Electron-backed integration tests and review response validation.
5. **Extend database query coverage.** Add fixture-backed integration tests for schema compatibility and representative SQL behavior.
6. **Stabilize renderer effects.** Register and clean up IPC listeners in effects, avoid subscriptions during render, and handle loading, empty, and error states consistently.
7. **Clarify domain terminology.** Decide whether public UI and code should use image, minion, card, tag, and filter, then document and apply that vocabulary consistently.
8. **Expand tests.** Prioritize query builders, IPC handlers, category transforms, navigation, filters, pagination, and representative component interactions.
9. **Review dependencies and boilerplate.** Remove unused packages and inherited build/release files only after confirming they are unnecessary.
10. **Improve UX and accessibility.** Replace placeholder navigation, add semantic controls and image alternatives, and document supported workflows.

## License

This repository contains an MIT license. See `LICENSE` for its current terms and attribution.
