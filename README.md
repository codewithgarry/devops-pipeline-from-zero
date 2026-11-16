# DevOps Pipeline from Zero

A free beginner course on YouTube by Code With Garry: one small Python app, the **chai shop**, taken from "it works on my machine" to a full pipeline that tests, builds, scans, deploys with GitOps, heals itself, rolls back with git, and pages you when it breaks. All of it on your own laptop.

```
git push → tests → image → vulnerability scan → Docker Hub → new tag in git → Argo CD → Kubernetes → Prometheus, Grafana, alerts
```

Every command and its output in the videos is real, and every step of the course is a git tag in this repo.

## Start

```
git clone https://github.com/codewithgarry/devops-pipeline-from-zero.git
cd devops-pipeline-from-zero
git checkout step-01        # or the step of the video you are watching
```

What to install, video by video: [docs/SETUP.md](docs/SETUP.md). Nothing costs money.

## The app

A small Flask API (`app.py`):

| Endpoint | What it does |
|---|---|
| `GET /` | the shop is open, and its menu |
| `GET /menu` | prices |
| `POST /order` `{"item": "chai", "qty": 2}` | a bill with 5 % GST |
| `GET /health` | `ok`, and the running version |
| `GET /metrics` | the order counter, for Prometheus (from step 20) |

## The course, step by step

| Video | Tag | What you build |
|---|---|---|
| 01 It works on my machine | `step-01` | the app runs on one machine and fails on another |
| 02 What a pipeline is | | the journey from a push to production |
| 03 Run the tests yourself | `step-01` | a venv and `pytest` |
| Checkpoint 1 | | |
| 04 Your first Dockerfile | `step-04` | the app in a container |
| 05 Smaller and safer images | `step-05` | gunicorn, a non-root user, `.dockerignore` |
| 06 Settings and health | `step-06` | settings from the environment, a healthcheck |
| 07 Podman | `step-06` | the same image, no daemon |
| 08 Push to Docker Hub | `step-06` | your image on Docker Hub |
| Checkpoint 2 | | |
| 09 GitHub Actions from zero | `step-09` | the first workflow |
| 10 Tests on every push | `step-10` | a red check blocks a bad pull request |
| 11 Build the image in CI | `step-11` | CI builds and pushes the image |
| 12 Scan for vulnerabilities | `step-12` | Trivy fails the build on a critical CVE |
| 13 Faster with caching | `step-13` | cached CI, measured before and after |
| Checkpoint 3 | | |
| 14 Kubernetes with kind | `step-14` | a 3-node cluster on your laptop |
| 15 Deploy by hand | `step-14` | `kubectl apply -k k8s/app` |
| 16 Argo CD | `step-16` | GitOps: the cluster follows git |
| 17 The full loop | `step-17` | a push goes live by itself |
| 18 Self-healing | `step-17` | delete pods, they come back |
| 19 Roll back with git | `step-19` | `git revert` undoes a bad release |
| Checkpoint 4 | | |
| 20 Metrics with Prometheus | `step-20` | `/metrics` and a ServiceMonitor |
| 21 A Grafana dashboard | `step-21` | the shop, live |
| 22 An alert that pages | `step-22` | a PrometheusRule fires in Alertmanager |
| 23 Secrets out of git | `step-22` | GitHub secrets and Kubernetes Secrets |
| 24 Audit your pipeline | `step-24` | [PIPELINE-CHECKLIST.md](PIPELINE-CHECKLIST.md) for your own projects |
| Final exam | | |

## Layout

```
app.py, test_app.py          the shop and its tests
Dockerfile, .dockerignore    the image
.github/workflows/ci.yml     test → build → scan → push → write the new tag to k8s/app
k8s/kind.yaml                the local cluster
k8s/app/                     Deployment, Service, kustomization (Argo CD watches this folder)
k8s/argocd/                  Argo CD, pinned, and the Application
k8s/monitoring/              ServiceMonitor, alert rule, Grafana dashboard
```

## Using your own fork

Change these to your names: `k8s/app/kustomization.yaml` (the image), `k8s/argocd/application.yaml` (`repoURL`), and the two repository secrets from video 11. Everything else works as it is.
