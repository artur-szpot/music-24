# Minion Decider

Minion Decider is a Windows-oriented Electron and React desktop application for browsing a locally maintained image collection and exploring its metadata. In the current codebase, an image is called a **minion**, while **cards** represent tags or reusable filters.

This repository is an in-progress, machine-specific application derived from Electron React Boilerplate. It is not currently a portable or generally installable image manager.

## Current scope

The implemented UI can:

- browse images in pages of 12;
- open an individual image in screen, popup, side-panel, or tooltip contexts;
- filter images by image IDs, episodes, scenes, cards/tags, card relationships, or database views;
- browse searchable, hierarchical tag/card categories;
- browse episode and scene categories;
- inspect card details and JSON-defined compound filters; and
- load image and metadata records from a local SQLite database.

Despite the project's tagging purpose, the current source only exposes read operations. It does **not** provide UI or database operations for creating, editing, assigning, or deleting tags.

## Architecture

The application has three runtime layers:

1. **Electron main process** — creates the window, registers custom image protocols, owns the SQLite connection, and handles database requests.
2. **Preload bridge** — exposes a small `ipcRenderer` wrapper through `contextBridge`.
3. **React renderer** — renders navigation, category lists, image grids, details, filters, pagination, popups, and side panels.

Renderer requests are sent over one default IPC channel. Each request includes a private reply-channel name and a database operation. The main process executes the operation synchronously through `better-sqlite3` and replies on that private channel.

The project uses:

- Electron 35;
- React 19 and TypeScript 5;
- Material UI 7;
- `better-sqlite3`;
- Webpack through Electron React Boilerplate; and
- Jest, Testing Library, ESLint, and Prettier for validation.

## Current data prerequisites

The application currently depends on resources at hard-coded Windows paths:

- database: `E:\programming\ponypics\year45.db`;
- minion images: `E:\programming\ponypics\s\`;
- card images: `E:\programming\ponypics\cards\`; and
- general file-system images: `C:\Users\szpot\Downloads\`.

The SQLite database is expected to contain the tables, views, and columns referenced in `src/main/db.ts`, including `minions`, `cards`, `episodes`, `scenes`, relationship tables, and precomputed count views. No schema, migration, seed data, sample database, or import workflow is included.

As a result, cloning and starting the repository on another machine is not enough to obtain a working application. The paths must exist and the database must match the implicit schema expected by the queries.

## Development

### Requirements

- Node.js 22 is the version used by GitHub Actions. Package metadata currently advertises Node.js 14 or newer, but this has not been reconciled with CI or the current dependency set.
- npm 7 or newer.
- A supported native build toolchain for Electron and `better-sqlite3`.
- The machine-specific database and image directories listed above.

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

Packaging is configured for Windows NSIS, Linux AppImage, and macOS targets, but the hard-coded Windows paths make the current application effectively Windows- and machine-specific.

## Project structure

```text
.
├── .erb/                   Electron React Boilerplate build configuration
├── .github/workflows/      CI, publishing, and CodeQL workflows
├── assets/                 Application icons and platform assets
├── release/app/            Production runtime package and native dependency
├── src/
│   ├── __tests__/          Jest tests
│   ├── constants/          Shared IPC and pagination constants
│   ├── enums/              Database operations/tables and screen contexts
│   ├── main/               Electron main process, SQLite, menu, and preload
│   └── renderer/           React application, navigation, screens, and components
├── AGENTS.md               Contributor and coding-agent guidance
├── package.json            Scripts, dependencies, Jest, Prettier, and packaging
└── tsconfig.json           Strict TypeScript configuration
```

## Tests and automated checks

Only one automated test is currently present: a smoke test that renders `App` and checks that rendering returns a truthy result. There are no focused tests for:

- SQLite query construction or database operations;
- IPC request/reply behavior;
- custom protocol path handling;
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

- Database and asset locations are hard-coded to one workstation.
- The database schema and required image-directory layout are undocumented outside the source and are not versioned.
- Package name, description, product name, author, repository links, and portions of release configuration still identify Electron React Boilerplate.
- The single IPC endpoint accepts loosely typed operation objects, and several database paths interpolate values into SQL.
- The preload API permits arbitrary channel names rather than exposing a domain-specific API.
- Most renderer data subscriptions are registered during render instead of inside effects.
- Several production-facing values are placeholders or hard-coded, including navigation IDs and default detail content.
- Error handling is mostly console logging; the renderer has no consistent error state.
- There is no state-management or routing library in active use despite `react-router-dom` being installed.
- Accessibility is incomplete, including clickable images without equivalent button semantics or alternative text.
- Automated behavior coverage is minimal.

## Suggested cleanup — not implemented

The following items are recommendations only; they do not describe completed work:

1. **Externalize local configuration.** Select or configure the database and asset roots at runtime, validate them at startup, and store them in Electron's user-data directory.
2. **Version the data contract.** Add a schema, migrations, representative fixtures, and documentation for image naming and directory layout.
3. **Rename inherited metadata.** Update package, product, repository, author, release, badge, and changelog references to this application.
4. **Constrain the process boundary.** Replace the generic IPC pass-through with typed, allow-listed methods using `ipcMain.handle`/`ipcRenderer.invoke`, validate all inputs, and return structured errors.
5. **Harden database access.** Parameterize every value, allow-list table/view identifiers, separate query construction from execution, and add unit tests around both.
6. **Stabilize renderer effects.** Register and clean up IPC listeners in effects, avoid subscriptions during render, and handle loading, empty, and error states consistently.
7. **Clarify domain terminology.** Decide whether public UI and code should use image, minion, card, tag, and filter, then document and apply that vocabulary consistently.
8. **Expand tests.** Prioritize query builders, IPC handlers, category transforms, navigation, filters, pagination, and representative component interactions.
9. **Review dependencies and boilerplate.** Remove unused packages and inherited build/release files only after confirming they are unnecessary.
10. **Improve UX and accessibility.** Replace placeholder navigation, add semantic controls and image alternatives, and document supported workflows.

## License

This repository contains an MIT license. See `LICENSE` for its current terms and attribution.
