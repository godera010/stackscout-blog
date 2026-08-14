---
title: "Running Linux Containers on Windows with WSL 2"
description: "A practical guide to understanding how Windows, WSL 2, Docker, and Linux containers work together in a modern development environment."
slug: "running-linux-containers-on-windows-with-wsl-2"
tags: ["Windows", "WSL 2", "Docker", "Containers", "Linux", "DevOps"]
draft: true
---

# Running Linux Containers on Windows with WSL 2

Windows is still one of the most common desktop operating systems for developers, but a large part of modern development tooling is built around Linux. Docker, Bash, Linux package managers, server environments, and many deployment workflows naturally fit together in a Linux-based environment.

This is where **Windows Subsystem for Linux 2 (WSL 2)** becomes useful.

With WSL 2, you can keep Windows as your main desktop environment while running a real Linux kernel and using Linux development tools alongside Windows applications. Docker Desktop can then use WSL 2 as its backend for Linux containers.

The result is a development setup that looks roughly like this:

```text
┌──────────────────────────────────────────────┐
│                 Windows                      │
│                                              │
│  VS Code   Browser   PowerShell   Git       │
│                    │                         │
│                    ▼                         │
│              ┌──────────────┐                │
│              │    WSL 2     │                │
│              │              │                │
│              │ Ubuntu/Linux │                │
│              │ Linux Kernel │                │
│              └──────┬───────┘                │
│                     │                        │
│                     ▼                        │
│               Docker Engine                 │
│                     │                        │
│          ┌──────────┼──────────┐             │
│          ▼          ▼          ▼             │
│       Nginx       Node.js    PostgreSQL      │
│      container    container    container     │
└──────────────────────────────────────────────┘
```

> **Note:** WSL 2 is not itself a Docker container runtime. WSL 2 provides the Linux environment and kernel; Docker uses that environment/backend to run Linux containers.

## Why run containers on Windows?

A developer may prefer Windows for everyday work but still need Linux-based tooling for application development.

For example, a project might require:

- Linux shell commands
- Node.js or Python tooling
- PostgreSQL and Redis
- Docker Compose
- Linux command-line utilities
- Development environments that closely resemble production Linux servers

Without WSL 2, developers often end up choosing between a traditional virtual machine, dual booting, or a more fragmented setup.

WSL 2 provides another option: **use Windows for the desktop and Linux where the development workflow needs it.**

## What is WSL 2?

Windows Subsystem for Linux allows developers to run Linux distributions and Linux command-line tools directly from Windows.

WSL 2 is the newer architecture and uses a real Linux kernel. Microsoft describes WSL as a way to run a GNU/Linux environment directly on Windows without the traditional overhead of setting up a conventional virtual machine or dual-boot arrangement.

Official documentation:

- [Microsoft: Install WSL](https://learn.microsoft.com/windows/wsl/install)
- [Microsoft: WSL documentation](https://learn.microsoft.com/windows/wsl/)
- [Microsoft: Compare WSL 1 and WSL 2](https://learn.microsoft.com/windows/wsl/compare-versions)

## Installing WSL 2

On a modern Windows installation, the basic installation command is:

```powershell
wsl --install
```

After installation, you can inspect your installed distributions with:

```powershell
wsl --list --verbose
```

You should see information similar to:

```text
NAME      STATE           VERSION
Ubuntu    Running         2
```

The important part is the `VERSION` column. For this workflow, you generally want the distribution running under **WSL 2**.

For the complete and current installation process, use Microsoft's documentation rather than relying on an old tutorial:

[Install WSL](https://learn.microsoft.com/windows/wsl/install)

## Where does Docker fit in?

This is the part that often causes confusion.

Installing WSL 2 does not automatically mean that Docker is installed. WSL provides the Linux environment. Docker provides the container tooling and engine.

A simplified view is:

```text
Windows
   │
   ▼
WSL 2
   │
   ▼
Linux environment
   │
   ▼
Docker Engine
   │
   ▼
Linux containers
```

Docker Desktop for Windows can use a **WSL 2 based engine**. Docker also provides WSL integration so that Docker commands can be used from supported WSL distributions.

Official Docker documentation:

- [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/)
- [Docker Desktop with WSL](https://docs.docker.com/desktop/features/wsl/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

## Installing Docker Desktop

Download Docker Desktop from Docker's official website:

[Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

During configuration, make sure the installation is configured to use the **WSL 2 based engine**.

Docker's documentation may change as the product evolves, so use the current installation guide for the exact options shown by your version.

After installation, open Docker Desktop and check the WSL integration settings. Your Linux distribution should be enabled for integration.

## Test the installation

From your WSL terminal, run:

```bash
docker --version
```

Then test the Docker engine with:

```bash
docker run --rm hello-world
```

If the setup is working, Docker will download the `hello-world` image and run the container.

This is a useful first test because it confirms that the Docker client can communicate with the Docker engine and that the engine can create and run a container.

## Run your first web container

Let's try something more visible.

Run Nginx with:

```bash
docker run -d -p 8080:80 nginx
```

Now open:

```text
http://localhost:8080
```

You should see the default Nginx page.

The important idea here is that you are accessing a service running inside a Linux container while using Windows as your desktop environment.

The flow looks like this:

```text
Browser on Windows
        │
        ▼
http://localhost:8080
        │
        ▼
Port 8080
        │
        ▼
Nginx container
        │
        ▼
Port 80 inside container
```

## Windows applications and Linux development tools can work together

One of the best parts of this setup is that you do not have to choose between Windows and Linux for every task.

For example, you might use:

```text
Windows
├── VS Code
├── Chrome / Edge
├── Microsoft Teams
└── File Explorer

WSL 2
├── Ubuntu
├── Bash
├── Git
├── Node.js
├── Python
└── Linux CLI tools

Docker
├── PostgreSQL
├── Redis
├── Nginx
└── Application containers
```

VS Code can connect directly into WSL, allowing the editor running on Windows to work with files and development tools inside the Linux environment.

Microsoft's guidance for setting up a development environment with WSL is here:

[Microsoft: Set up your development environment on WSL](https://learn.microsoft.com/windows/wsl/setup/environment)

## Where should your project files live?

This is one of the most important practical details.

For Linux-heavy development workloads, it is generally better to keep your project inside the WSL filesystem rather than treating WSL as a Linux shell sitting on top of a Windows project directory.

For example:

```bash
mkdir -p ~/projects
cd ~/projects
```

A project might then live at:

```text
/home/your-user/projects/my-app
```

You can still access your Windows drives from WSL through paths such as:

```text
/mnt/c/Users/YourName/
```

But Microsoft recommends keeping Linux-oriented project files inside the WSL filesystem for better performance, especially when tools perform large numbers of file operations.

This matters for workflows involving package installation, builds, Git operations, file watching, and containers.

Microsoft's Dev Containers guidance discusses this issue directly:

[Microsoft: Improve performance when using Dev Containers with WSL](https://learn.microsoft.com/windows/dev-environment/docker/dev-containers)

## Windows filesystem vs WSL filesystem

A simplified comparison is:

```text
Windows filesystem
C:\Users\YourName\projects\app
        │
        └── accessed from WSL as:
            /mnt/c/Users/YourName/projects/app

WSL filesystem
/home/your-user/projects/app
```

For projects that are primarily Linux-based, keeping the repository under `/home/...` can make the development experience smoother.

## WSL 2 is not the same thing as a virtual machine

This comparison needs some nuance.

WSL 2 uses virtualization technology under the hood and runs a Linux kernel, so it is not accurate to describe it as “no virtualization.” However, Microsoft designed WSL to integrate Linux closely with Windows rather than behaving like a traditional desktop virtual machine that you manage as a separate computer.

That distinction matters because the developer experience is different.

With a traditional VM you might think in terms of:

```text
Windows
   │
   ▼
Virtual Machine
   │
   └── Linux guest
```

With WSL you generally think in terms of:

```text
Windows
   │
   ├── Windows apps
   │
   └── WSL Linux environment
```

Microsoft's architecture documentation explains the relationship between WSL 2, the Linux kernel, and its lightweight virtual machine architecture.

Useful reference:

[Microsoft: WSL 2 architecture](https://learn.microsoft.com/windows/wsl/compare-versions)

## Linux containers vs Windows containers

Another common source of confusion is the phrase “Docker on Windows.”

Docker can work with both Linux containers and Windows containers, but they are not the same thing.

For many developer workflows using Docker Desktop with WSL 2, the containers are **Linux containers**.

Conceptually:

```text
Docker Desktop on Windows
│
├── Linux container workflow
│      └── WSL 2 backend
│
└── Windows container workflow
       └── Windows container technology
```

Docker and Microsoft both document how Windows users can switch between Linux and Windows container modes.

References:

- [Docker: Switch between Linux and Windows containers](https://docs.docker.com/desktop/features/wsl/)
- [Microsoft: Windows containers](https://learn.microsoft.com/virtualization/windowscontainers/)

## What about Docker Compose?

Once Docker is working, a major advantage is that you can run an entire development stack with Docker Compose.

For example:

```yaml
services:
  app:
    image: node:22
    working_dir: /app
    volumes:
      - .:/app
    command: npm run dev

  db:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: example
```

Then:

```bash
docker compose up
```

Instead of installing PostgreSQL directly into Windows, your database can live in a container alongside the rest of the development environment.

For more information:

[Docker Compose documentation](https://docs.docker.com/compose/)

## A practical developer workflow

A typical workflow might look like this:

```text
1. Open Windows
       ↓
2. Start VS Code
       ↓
3. Connect VS Code to WSL
       ↓
4. Open ~/projects/my-app
       ↓
5. Start Docker containers
       ↓
6. Develop using Linux tools
       ↓
7. Open the application from Windows browser
```

The user experience feels surprisingly unified even though several layers are involved underneath.

## Common problems

### `docker: command not found`

If Docker is unavailable inside WSL, check that Docker Desktop is running and that your WSL distribution is enabled under Docker Desktop's WSL integration settings.

### Docker engine is unavailable

Try:

```bash
docker info
```

If the client exists but cannot reach the engine, the issue may be Docker Desktop not running or the WSL integration configuration.

### Projects feel slow

Check where your repository lives.

A Linux-heavy project stored under:

```text
/mnt/c/Users/...
```

may not perform as well as a project stored under:

```text
/home/your-user/projects/...
```

especially for workloads with lots of filesystem operations.

### WSL is using the wrong version

Check:

```powershell
wsl --list --verbose
```

To convert a distribution to WSL 2, Microsoft documents the following command pattern:

```powershell
wsl --set-version <DistroName> 2
```

Use the exact distro name shown by `wsl --list --verbose`.

## WSL 2 vs a traditional Linux virtual machine

| Feature | WSL 2 | Traditional VM | Dual Boot |
|---|---|---|---|
| Keep Windows running normally | Yes | Yes | No |
| Linux kernel | Yes | Yes | Yes |
| Separate Linux desktop required | No | Usually | No |
| Easy Windows/Linux workflow | Excellent | Good | Poor |
| Reboot required to switch OS | No | No | Yes |
| Good for container development | Excellent | Good | Good |
| Setup complexity | Low | Medium | High |

This is not a universal performance ranking. The right choice depends on workload, hardware, filesystem access patterns, and whether you need a full Linux desktop.

## When WSL 2 makes sense

WSL 2 is especially useful when you:

- develop on Windows but target Linux servers
- use Docker extensively
- work with Linux-first tooling
- need Bash and Linux command-line utilities
- want to use Docker Compose locally
- want to avoid dual booting
- want a tighter Windows/Linux workflow than a traditional VM provides

It is less compelling when you need a complete Linux desktop environment, specialized VM features, or a workload that is better isolated in a dedicated virtual machine.

## Final thoughts

The biggest benefit of WSL 2 is not simply that it lets Windows run Linux commands.

It gives developers a way to combine two ecosystems:

```text
Windows
+ Linux
+ Docker
+ Containers
+ VS Code
= A flexible development workstation
```

For developers building APIs, web applications, databases, microservices, and containerized systems, this can provide a practical local environment without abandoning Windows.

The important thing is to understand the layers rather than treating WSL and Docker as the same thing:

```text
Windows
   ↓
WSL 2
   ↓
Linux kernel / Linux environment
   ↓
Docker Engine
   ↓
Linux containers
   ↓
Your application
```

Once that model makes sense, the rest of the setup becomes much easier to understand and troubleshoot.

---

## Official documentation and source links

Use these as the primary references for the article:

1. Microsoft — Install WSL  
   https://learn.microsoft.com/windows/wsl/install

2. Microsoft — Windows Subsystem for Linux documentation  
   https://learn.microsoft.com/windows/wsl/

3. Microsoft — Set up your development environment on WSL  
   https://learn.microsoft.com/windows/wsl/setup/environment

4. Microsoft — WSL versions and architecture  
   https://learn.microsoft.com/windows/wsl/compare-versions

5. Microsoft — WSL and Dev Containers  
   https://learn.microsoft.com/windows/dev-environment/docker/dev-containers

6. Docker — WSL 2 backend  
   https://docs.docker.com/desktop/features/wsl/

7. Docker — Install Docker Desktop on Windows  
   https://docs.docker.com/desktop/setup/install/windows-install/

8. Docker — Docker Compose  
   https://docs.docker.com/compose/

9. Microsoft — Windows containers documentation  
   https://learn.microsoft.com/virtualization/windowscontainers/

10. Docker — Docker Desktop  
    https://www.docker.com/products/docker-desktop/

## Suggested image sources

For a technical blog, prefer official screenshots, diagrams you create yourself, or openly licensed images.

### Official screenshots / product visuals

Docker Desktop media and product pages:  
https://www.docker.com/products/docker-desktop/

Microsoft WSL documentation:  
https://learn.microsoft.com/windows/wsl/

Microsoft Windows Developer documentation:  
https://learn.microsoft.com/windows/dev-environment/

### Image search / inspiration

Wikimedia Commons — WSL-related media search:  
https://commons.wikimedia.org/w/index.php?search=Windows+Subsystem+for+Linux&title=Special:MediaSearch&type=image

Wikimedia Commons — Docker-related media search:  
https://commons.wikimedia.org/w/index.php?search=Docker+container&title=Special:MediaSearch&type=image

### Recommended original diagrams to create for this article

Instead of using random stock images, create these yourself:

1. **Architecture diagram** — Windows → WSL 2 → Docker → Containers.
2. **Filesystem diagram** — `C:\Users\...` vs `/home/...`.
3. **Request flow diagram** — Windows browser → localhost → container → application.
4. **Development workflow diagram** — VS Code → WSL → Docker Compose → services.
5. **Comparison graphic** — WSL 2 vs VM vs dual boot.

## Image caption ideas

- *How Windows, WSL 2, and Docker work together to run Linux containers.*
- *A typical Windows development workflow using WSL 2 and Docker.*
- *Why Linux-heavy projects are often better stored inside the WSL filesystem.*
- *Windows browser accessing an application running inside a Linux container.*

## Editorial note

Technology changes quickly. Before publishing, re-check the Docker Desktop and Microsoft documentation linked above and update screenshots or UI instructions to match the versions you are actually demonstrating.
