# Forefather

Skills for studying and publishing standalone HTML with Codex. Each skill is a folder containing a `SKILL.md` file and display metadata. There is no build step or package installation for this repo.

| Skill | What it does |
| --- | --- |
| [quizzer](quizzer/SKILL.md) | Analyzes labs and past assessments, creates practice quizzes when requested, and identifies knowledge gaps from results. |
| [question-helper](question-helper/SKILL.md) | Answers academic and technical questions in Like a Baby, University, or Answer Now mode. |
| [html-daemon](html-daemon/SKILL.md) | Saves and manages standalone HTML pages at 111416.xyz, with a Python helper for verified uploads. |

## Install with Codex

Paste this into Codex:

```text
$skill-installer Install quizzer, question-helper, and html-daemon from https://github.com/Revanth15/forefather, branch main, into ~/.agents/skills. The skill directories are quizzer, question-helper, and html-daemon.
```

This installs all three skills for your user account. To install just one, name only that skill and its directory.

On your next turn, try one of the examples below. If the skill does not appear, restart Codex. In the CLI or IDE extension, use `/skills` to check the list.

If the installer reports that a skill already exists, use the update instructions below.

## Install manually

These commands use Git and a shell such as bash or zsh. Clone the repo, or open your existing checkout:

```sh
git clone https://github.com/Revanth15/forefather.git
cd forefather
```

Choose one installation scope. Cloning alone leaves the skills outside Codex's discovery directories.

### For all your projects

Run from the forefather checkout:

```sh
mkdir -p ~/.agents/skills
cp -R quizzer question-helper html-daemon ~/.agents/skills/
```

To install only quizzer, for example:

```sh
cp -R quizzer ~/.agents/skills/
```

### For one project

Replace `/path/to/your-project` with the project's actual path. Run from the forefather checkout:

```sh
mkdir -p "/path/to/your-project/.agents/skills"
cp -R quizzer question-helper html-daemon "/path/to/your-project/.agents/skills/"
```

Open Codex in that project. You can commit its `.agents/skills/` directory if you want teammates to use the same copies.

Copy the whole skill folder, including `agents/openai.yaml`. A user installation should look like this:

```text
~/.agents/skills/
├── quizzer/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── question-helper/
│   ├── SKILL.md
│   └── agents/openai.yaml
└── html-daemon/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/api.md
    └── scripts/html_daemon.py
```

Codex's [skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) describes discovery locations and project scope.

## Use the skills

Mention a skill explicitly with `$quizzer`, `$question-helper`, or `$html-daemon`. Codex can also select a skill when your request matches its description.

### Quizzer

Attach your source material or point Codex to files it can read. For an analysis of existing assessments:

```text
$quizzer Analyze these lab sheets and past papers. Identify recurring question types and what I should review.
```

To generate a quiz:

```text
$quizzer Create a practice quiz from these materials. Match the style and time restrictions of the past quizzes.
```

Quizzer defaults to analysis until you ask for new questions. Generated interactive quizzes default to one HTML file with CSS and JavaScript included. Open it in a browser to take the quiz. It starts in dark mode and has a theme toggle at the top.

When past examples specify time restrictions, the generated quiz uses them by default. The final results break down performance by topic and question type, with review suggestions based on recurring mistakes. Copy or download the results and share them with Codex for follow-up analysis.

You can request chat delivery, a worksheet, or a question bank instead. Specify a question count, difficulty, or time limit when you want to override the defaults.

### Question helper

Choose how much explanation you want:

```text
$question-helper Like a Baby: explain Python variable scope from first principles.
```

```text
$question-helper University: explain why this function raises UnboundLocalError.
```

```text
$question-helper Answer now: fix this function and show the corrected code.
```

University is the default. You can switch modes during a conversation.

### HTML Daemon

Use Python 3 and the HTML Daemon skill to save a self-contained HTML file and get its viewing URL:

```text
$html-daemon Upload /absolute/path/to/page.html with the title "My page" and return its viewing URL.
```

The service uses https://admin.111416.xyz for its API and https://111416.xyz for saved pages. Include CSS and JavaScript inline; files must be UTF-8 and at most 1 MiB. The bundled helper verifies uploaded bytes and also supports listing, downloading, replacing, renaming, and deleting documents. It has no Python package dependencies.

The service currently has no authentication, so uploaded documents are publicly accessible. The skill explains viewer restrictions, browser storage, and version checks for updates. Use the returned `viewUrl` to open a page; `downloadUrl` deliberately downloads the original file.

## Update installed skills

Installed copies do not track changes in this repo. Back up any edits you made to those copies before updating.

From your forefather checkout, pull the latest version and copy the folders to the same location you used during installation:

```sh
git pull --ff-only
cp -R quizzer question-helper html-daemon ~/.agents/skills/
```

For a project installation, replace `~/.agents/skills/` with that project's `.agents/skills/` directory. If an earlier installer used `~/.codex/skills/` or a custom destination, copy there instead. Keep one installed copy per skill to avoid duplicate entries.

Codex detects skill changes automatically. Restart it if an update does not appear.

## Troubleshooting

- If a skill is missing, check that its `SKILL.md` sits directly inside the skill folder, such as `~/.agents/skills/quizzer/SKILL.md`.
- If you installed for one project, open Codex inside that project's repository.
- If you see duplicate entries, check your user and project skill directories for copies with the same name.
- If Quizzer only analyzes your material, explicitly ask it to create a quiz. Analysis is its default mode.
