---
title: git-serious
description: Visualize, track, and secure your CI/CD system — for humans and agents.
headline: CI/CD configuration is impossible to see all at once. That’s what the grid is for.
lede: Visualize, track, and secure your CI/CD system — for humans and agents.

status:
  label: pre-alpha
  text: git-serious is being built in the open, first against our own CI/CD system. Nothing here is installable yet.
  milestones:
    - self
    - friends
    - public alpha
  now: self


slides:
  - src: images/shots/tap-lanes.png
    title: One repository, as machinery.
    text: The tap repository's CI/CD drawn as lanes. The PR gate every change rolls through, publish, scheduled, fleet, baseline. Each workflow card carries zizmor's verdict. Open PRs and the security findings sit beneath.
    alt: The tap repository's workflows drawn as a machinery graph in lanes, with a table of open pull requests below.
  - src: images/shots/landing.png
    title: What moved in the last 24 hours.
    text: Every repository with something to review, and what it is. The open PRs, their checks, and the plugins they touch. The ones with nothing to do say so.
    alt: A triage page listing repositories with open pull requests to review, grouped by product and plugin.
  - src: images/shots/secrets.png
    title: Every secret the estate holds.
    text: Names only, since GitHub never returns a value. Where each one is held, where it can reach, who actually names it, and the names workflows use that no scope defines.
    alt: A secrets overview page with a summary strip, a list of secret names defined nowhere, and one card per secret.
  - src: images/shots/secret-openai.png
    title: One secret, in full.
    text: Held by the organisation, reachable from an exposed trigger. Every workflow that names it, what starts each one, and how far the secret reaches beyond where it is used.
    alt: A single organisation secret's page with holder and visibility, a reach section, and a row per consuming workflow.
  - src: images/shots/secret-phantom.png
    title: Named everywhere, defined nowhere.
    text: A secret that does not exist does not fail. GitHub hands the step an empty string and the job goes green. The grid says cannot find. Whether that is a defect is for the reader to know.
    alt: A page for a secret name used by many workflows but defined at no scope, with an explanation and a row per workflow naming it.
  - src: images/shots/zizmor.png
    title: Findings across the organisation.
    text: zizmor runs offline over the workflow YAML already on the grid. Every finding lands attached to its workflow, and the workflows the scanner could not read are listed as unknown, not clean.
    alt: A table of zizmor security findings across repositories, with a coverage summary below it.
  - src: images/shots/zizmor-workflow.png
    title: A workflow file, findings in the margin.
    text: One workflow file with every finding marked on the source and called out alongside it, Tufte-style. The workflow's anatomy is drawn beneath.
    alt: A workflow YAML file with a security finding highlighted on a line and explained in the right margin.
  - src: images/shots/zizmor-finding.png
    title: One finding, in context.
    text: Title and verdict, the workflow's anatomy, what to change, and whether it matters here, given what the grid knows about the repository.
    alt: A single security finding page with the workflow's anatomy graph and guidance on what to change.
  - src: images/shots/github-workflow.png
    title: Anatomy of a workflow.
    text: Jobs ranked over what they need, steps inside each, artifacts to the side, and the recent runs beneath with elapsed time against the usual.
    alt: A workflow anatomy graph of jobs and steps, with a table of recent runs below.
  - src: images/shots/cares.png
    title: The plumbing.
    text: Collectors and their schedules. What reads GitHub, how often, when it last ran, and what it brought back.
    alt: A table of collectors and schedules with run state and last-run summaries.

why_heading: Answering “What the hell is going on and is it even remotely secure?”

does_heading: Your CI/CD system, on the grid.
does:
  - title: Pulls your running CI/CD system onto the grid
    text: Repos, pipelines, runs, rules, apps, credentials, and the relationships between them, as one connected graph.
  - title: Exactly the pages, views, and affordances you need
    text: Built to be read by people, and by the agents working alongside them. Extensible, configurable, and built to be tailored to your needs.
  - title: Tracks how configuration and operations change over time
    text: So “what changed?” is a question with an answer. Which you’d think would have already been dealt with, but turns out…
  - title: Enables automated, agent-driven security review
    text: Native agent access to the grid enables your agents to find issues and help fix them.
  - title: Does all of it with down-scoped, read-only access
    text: Blast radius bounded by design, based on credentials you control. It can never be the thing that breaks it.

running_heading: Three steps, when it’s ready.
steps:
  - Clone the repo.
  - Run the install / configure skill.
  - Tailor it to your liking.
running_note: Nothing here is installable yet. The roadmap lives in the repo’s milestones.

concepts_heading: Understand your CI/CD, sleep easier at night.
concepts:
  - title: Master complexity
    text: git-serious tracks and distills what you actually need to know across multiple dimensions. All information can be accessed by humans and agents.
  - title: Software as a sophisticated beanbag
    text: Adjust it yourself. Build your own plugins to add pages, views, collectors, whatever you need to understand *your* system. git-serious ships with GitHub.com, which you can remove, extend, or replace with your own forge. It’s your software, make it do what you want.
  - title: The grid
    text: Underneath it all is the data model at the center of [The Analogy Platform](https://github.com/unified-systems-com/tap). Graph representations, history tracking, field-level information provenance, plugin management (uv), and multi-user RBAC right out of the box.

---

Building, maintaining, and securing a modern CI/CD system is complicated, and the
complexity is the bad kind: it isn’t in one place. It’s strewn across workflow files,
branch rulesets, environments, org settings, the bots and apps wired into your repos,
the third-party services they talk to — and don’t get me started on PATs.

No single screen shows you all of it, so nobody actually knows what it is. That’s the
worst of all worlds, and it sits on the most critical of critical paths: the one that
ships your software.
