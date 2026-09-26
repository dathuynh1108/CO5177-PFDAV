# CO5177 · PFDAV

Course project website for **Programming Foundations for Data Analysis and Visualization**.

**[Visit the website](https://dathuynh1108.github.io/CO5177-PFDAV/)**

## Course

| Field | Details |
| --- | --- |
| University | Ho Chi Minh City University of Technology, VNU-HCM |
| Faculty | Computer Science and Engineering |
| Course code | CO5177 |
| Instructor | Lê Thành Sách |
| Semester | 261 · Academic year 2026–2027 |

## Team

| Student ID | Name |
| --- | --- |
| 2570161 | Huỳnh Thành Đạt |
| 2570083 | Lương Minh Duy |

## Selected assignments

| Assignment | Data type | Track | Overview |
| --- | --- | --- | --- |
| 01 | [Tabular](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/tabular.html) | Required | Structured-data exploration, preprocessing and modeling. |
| 02 | [Text](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/text.html) | Required | Corpus exploration, text representations and analysis. |
| 03 | [Image](https://dathuynh1108.github.io/CO5177-PFDAV/assignments/image.html) | Selected elective | Visual exploration, feature extraction and model evaluation. |

The website currently introduces the course, team and assignment requirements. Specific datasets, experiments, notebooks, reports and presentation videos will be added as the projects develop.

## Technology

Static HTML5, CSS3 and vanilla JavaScript. No backend, package installation or build step is required. The interface and documentation are in English; member names retain their Vietnamese spelling.

## Repository structure

```text
.
├── index.html                 # Course and team landing page
├── requirements.html          # Assignment brief summary
├── assignments/
│   ├── tabular.html           # Assignment 01
│   ├── text.html              # Assignment 02
│   └── image.html             # Assignment 03
├── assets/
│   ├── styles.css             # Design system and responsive styles
│   ├── site-config.js         # Team settings and resource links
│   ├── app.js                 # Navigation and configuration handling
│   └── favicon.svg
├── .gitignore
└── .nojekyll
```

## Run locally

```bash
git clone https://github.com/dathuynh1108/CO5177-PFDAV.git
cd CO5177-PFDAV
python3 -m http.server 8000
```

Open **http://localhost:8000**. Core page content is also readable by opening `index.html` directly.

## Deploy to GitHub Pages

In **Settings → Pages → Build and deployment**, select:

```text
Source: Deploy from a branch
Branch: main
Folder: / (root)
```

Save the settings. GitHub Pages publishes the files from `main`. No custom GitHub Actions workflow is needed. Internal assets and links use relative paths compatible with the `/CO5177-PFDAV/` project URL. The `.nojekyll` file disables Jekyll processing.

## Update content

Edit `assets/site-config.js` to set the registered group name, member contributions, GitHub profiles and assignment resource links. For example, after a report is available:

```js
report: 'reports/tabular.pdf'
```

Use HTTPS URLs for external resources and project-relative paths for repository files. Leave unavailable resources empty; the page displays their publication status without creating broken links. Do not put credentials or private information in this public configuration file.

Main page copy and requirement summaries live in the corresponding HTML files. Keep these in sync with the configuration when updating published content so that the no-JavaScript view remains accurate.

## Accessibility and presentation

The site includes responsive layouts, keyboard-accessible navigation, a skip link, visible focus states, reduced-motion support and print styles. Core content is available without JavaScript. Fonts are loaded from Google Fonts with local system fallbacks; font files are not stored in the repository.

## Assignment reference

Requirements are summarized from **Course Assignment v4.0, dated 14 September 2026**, for Semester 261. The official assignment brief and course LMS announcements determine final requirements and deadlines.
