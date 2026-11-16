# Set up your laptop for DevOps Pipeline from Zero

Everything is free. You add a tool only when a video needs it. Each step of the course is a git tag (`step-01` … `step-24`), so you can start from any video.

## Video 01: Git, Python, an editor, GitHub

| Tool | Mac | Windows | Linux (Ubuntu) | Check |
|---|---|---|---|---|
| Git | `xcode-select --install` | git-scm.com installer | `sudo apt install git` | `git --version` |
| Python 3.12 or newer | python.org installer | python.org installer (tick "Add to PATH") | `sudo apt install python3 python3-venv` (24.04 has 3.12) | `python3 --version` |
| An editor | any (VS Code, PyCharm, vim) | any | any | |
| GitHub account | github.com, free | | | |

Get the code:

```
git clone https://github.com/codewithgarry/devops-pipeline-from-zero.git
cd devops-pipeline-from-zero
git checkout step-01
```

To follow along in your own repo, fork it on GitHub (Fork, top right), then clone your fork instead.

## Video 03: a virtual environment and the tests

```
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

## Video 04: Docker

- Mac and Windows: Docker Desktop, free for personal use and education. On Windows, turn on WSL 2 when it asks.
- Linux: Docker Engine, from docs.docker.com/engine/install.
- Check: `docker run hello-world` prints "Hello from Docker!".

## Video 07 (optional): Podman

- podman.io. Check: `podman --version`.

## Video 08: a Docker Hub account and token

1. Sign up at hub.docker.com (free). Public images are free.
2. Account settings, Personal access tokens, Generate new token, access **Read & Write**. Copy it.
3. Log in once, and paste the token when it asks for a password:
   ```
   docker login -u <your-docker-hub-name>
   ```
4. Treat the token like a password. If it ever shows up in a screenshot, a chat or a commit: delete it on Docker Hub and make a new one.

## Video 09: GitHub Actions

Nothing to install: Actions are free for public repositories. Push the workflow, then open the Actions tab of your repo.

If GitHub says the account is locked because of billing, or you want CI on your own machine, add a self-hosted runner:

1. Your repo, Settings, Actions, Runners, New self-hosted runner. Pick your OS and run the commands it shows (they download the runner and register it with a one-time token).
2. Start it: `./run.sh` (or install it as a service with `sudo ./svc.sh install && sudo ./svc.sh start` on Linux).
3. Tell the workflow to use it: Settings, Secrets and variables, Actions, **Variables** tab, New repository variable: `RUNNER` = `self-hosted`.
   Delete the variable to go back to GitHub's runners. The workflow reads it as `runs-on: ${{ vars.RUNNER || 'ubuntu-latest' }}`.
4. The runner's machine needs Docker (video 04) for the build and scan jobs.

## Video 10: the GitHub CLI

- cli.github.com (Mac: `brew install gh`; Ubuntu: `sudo apt install gh`). Then `gh auth login`.
- Check: `gh run list` shows your workflow runs.

## Video 11: secrets for CI

Settings, Secrets and variables, Actions, **Secrets** tab, New repository secret, twice:

| Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | your Docker Hub name |
| `DOCKERHUB_TOKEN` | the token from video 08 |

Only their names are ever in git: `${{ secrets.DOCKERHUB_TOKEN }}`. `gh secret list` shows the names, never the values.

## Video 12: Trivy

Nothing to install: the workflow runs Trivy in CI. To scan on your laptop too (optional): trivy.dev, then `trivy image <image>`.

## Video 14: kubectl and a local Kubernetes cluster (kind)

- kubectl: kubernetes.io/docs/tasks/tools. Check: `kubectl version --client`.
- kind: kind.sigs.k8s.io. Check: `kind version`.
- The cluster file (1 control plane, 2 workers, the shop on localhost:8080) is in the repo from `step-14` on:

```
kind create cluster --name chai --config k8s/kind.yaml
kubectl get nodes
```

## Video 16: Argo CD

From the repo (the version is pinned in `k8s/argocd/install`):

```
kubectl apply -k k8s/argocd/install --server-side
kubectl apply -f k8s/argocd/application.yaml
kubectl get applications -n argocd
```

In your fork, change `repoURL` in `k8s/argocd/application.yaml` to your own repo first.

## Video 17: let CI write the new tag back

Your repo, Settings, Actions, General, Workflow permissions: **Read and write permissions**, Save.

## Video 20: Prometheus and Grafana (Helm), and jq

- Helm: helm.sh/docs/intro/install (Mac: `brew install helm`). jq: jqlang.org (Mac: `brew install jq`; Ubuntu: `sudo apt install jq`).
- Install the monitoring stack into the cluster:

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
kubectl get pods -n monitoring
```

## Video 21: the Grafana dashboard

```
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80 &
kubectl -n monitoring get secret monitoring-grafana -o jsonpath='{.data.admin-password}' | base64 -d; echo
```

Open localhost:3000, log in as `admin`, then Dashboards, New, Import, and upload `k8s/monitoring/chai-shop-dashboard.json` from the repo.

## Not enough memory?

The whole course runs in about 6 GB of free RAM (the monitoring stack is the biggest part). Close other apps before video 14. When you are done for the day: `kind delete cluster --name chai` removes everything, and the repo brings it all back.
