# **Native WSL Containers on Windows: Comprehensive Guide & Architectural Deep Dive**

For years, running Linux containers on Windows required setting up third-party tooling suites like Docker Desktop or managing standalone Podman machines. With the release of **WSL Containers** (powered by wslc.exe in WSL 2.9.3+), Microsoft has embedded native container management directly into the Windows Subsystem for Linux (WSL) ecosystem.

This document serves as an exhaustive reference and draft material for blogging, covering the technical architecture, Docker comparison, CLI usage, and programmatic management via C\# / .NET.

## **1\. Overview & Core Value Proposition**

---

WSL Containers is an open-source subsystem feature that allows developers and administrators to pull standard OCI container images (such as those from Docker Hub or private registries), build images from Dockerfiles/Containerfiles, and run isolated Linux containers natively on Windows without a dedicated Docker daemon service.

### **Key Highlights**

* **Zero Extra Daemon Overhead:** Directly leverages the existing WSL 2 Linux kernel microVM instead of running an extra daemon layer.  
* **Open Source & Free:** Completely built into WSL under standard open-source licensing, avoiding licensing hurdles for enterprise developer teams.  
* **Direct Hardware & GPU Passthrough:** Seamless DXCore / CUDA acceleration for AI/ML workloads (PyTorch, TensorFlow, Ollama, vLLM).  
* **Dual-Interface Support:** Managed via the command-line interface (wslc) or programmatically via the Microsoft.WSL.Containers NuGet package for C\#/C++.  
* **Enterprise Governance:** Compatible with Microsoft Intune policy enforcement and Microsoft Defender for Endpoint (MDE).

## **2\. Architectural Deep Dive: How It Works**

---

WSL Containers eliminates the translation and virtualization layers commonly required by legacy desktop container setups by leveraging Linux primitives directly inside the existing WSL 2 lightweight utility VM.

### **Underlying Mechanisms**

1. **Kernel Namespace & cgroup Isolation:** Containers run as native Linux processes sharing the managed WSL 2 kernel. Process isolation, mount points, and resource quotas (CPU/Memory limits) are enforced using standard Linux cgroups v2 and kernel namespaces.  
2. **Storage & Image Layering:** WSL Containers pulls standard OCI-compliant image manifests and layers. Storage is managed directly inside the native ext4 virtual disk format (VHDX) or via VirtioFS for near-native I/O throughput.  
3. **Networking Bridge:** Ports published using \-p \<host\_port\>:\<container\_port\> are mapped directly to localhost on the Windows host machine via the WSL 2 mirrored/NAT network stack.  
4. **GPU Direct Access:** Utilizes WSL's paravirtualized GPU driver (/dev/dxg) to pass compute tasks directly to host NVIDIA/AMD GPUs.

## **3\. Comprehensive Comparison: WSL Containers vs. Docker Desktop**

---

| Feature / Dimension | Native WSL Containers (wslc) | Docker Desktop on Windows   |
| :---- | :---- | :---- |
| **Installation Model** | Built directly into WSL (enabled via wsl \--update \--pre-release) | Standalone installer, daemon services, and desktop GUI client |
| **Licensing & Cost** | 100% Free and Open Source (Apache 2.0 / WSL open-source license) | Free for personal/small business; paid subscription required for large enterprise use |
| **Resource Consumption** | Minimal idle overhead; shares standard WSL VM memory pool and dynamic memory reclaim | Heavier baseline footprint due to background Electron UI and daemon management processes |
| **CLI Syntax & Ergonomics** | Mirrors Docker CLI syntax (wslc run, wslc ps, wslc build, \-it, \--rm, \-d) | Standard Docker CLI (docker run, docker ps, docker build) |
| **Image Compatibility** | Standard OCI images (Docker Hub, GitHub Container Registry, Azure ACR) | Standard OCI images and Docker Hub integration |
| **Ecosystem & Multi-container Tooling** | Direct CLI and C\#/.NET SDK integration; Docker Engine API socket emulation in progress | Mature support for Docker Compose, Docker Swarm, Kubernetes (k8s), and IDE plugins |
| **Programmatic Application Embedding** | Native .NET / C++ NuGet package (Microsoft.WSL.Containers) to run containers within Windows apps | Managed over Docker Engine REST API socket or CLI wrappers |

## **4\. Step-by-Step Hands-On Guide**

### ---

**Prerequisites & Setup**

Ensure that WSL is updated to the pre-release track (version 2.9.3 or higher):

\# Update WSL in PowerShell  
wsl \--update \--pre-release

\# Verify installed version  
wsl \--version

### **Building and Running a Custom Container**

Below is a sample Python web service setup to test container building and deployment.

**1\. Project Code (server.py):**

from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):  
    def do\_GET(self):  
        self.send\_response(200)  
        self.send\_header('Content-type', 'text/html')  
        self.end\_headers()  
        self.wfile.write(b"\<h1\>Serving from Native WSL Container (wslc)\</h1\>")

if \_\_name\_\_ \== '\_\_main\_\_':  
    server \= HTTPServer(('0.0.0.0', 8080), Handler)  
    print("Server listening on port 8080...")  
    server.serve\_forever()

**2\. Container Definition (Dockerfile):**

FROM python:3.11-slim  
WORKDIR /app  
COPY server.py .  
EXPOSE 8080  
CMD \["python", "server.py"\]

**3\. CLI Execution Sequence:**

\# Build the container image  
wslc build \-t wslc-demo-app .

\# Verify the image list  
wslc image ls

\# Run the container in detached mode with port forwarding  
wslc run \-d \--rm \-p 8080:8080 \--name demo-service wslc-demo-app

\# Inspect running containers  
wslc container ps

\# View live container logs  
wslc container logs demo-service

\# Stop the container  
wslc container stop demo-service

## **5\. Programmatic Container Management with C\# / .NET**

---

One of the distinguishing features of WSL Containers is first-class support for native Windows applications via the Microsoft.WSL.Containers NuGet package.

### **Package Installation**

dotnet add package Microsoft.WSL.Containers \--prerelease

### **C\# Implementation Example**

using System;  
using System.Threading.Tasks;  
using Microsoft.WSL.Containers;

namespace WslContainersBlogDemo;

internal class Program  
{  
    static async Task Main(string\[\] args)  
    {  
        Console.WriteLine("Initializing WSL Container Session...");

        // Establish session connected to underlying WSL instance  
        using var session \= new WslContainerSession();

        string targetImage \= "python:3.11-slim";

        // Pull OCI image with progress tracking  
        Console.WriteLine($"Pulling {targetImage}...");  
        await session.PullImageAsync(targetImage, new ImagePullProgress(progress \=\>  
        {  
            Console.WriteLine($"Progress: {progress.Percentage}% \- {progress.Status}");  
        }));

        // Configure container specifications  
        var options \= new ContainerCreateOptions  
        {  
            Image \= targetImage,  
            Name \= "embedded-wsl-runner",  
            EnableGpu \= true, // GPU Passthrough for CUDA/DirectX  
            EnvironmentVariables \=  
            {  
                { "RUNTIME\_ENV", "Production" }  
            },  
            PortMappings \=  
            {  
                new PortMapping(HostPort: 8080, ContainerPort: 80\)  
            }  
        };

        // Create and start container  
        using var container \= await session.CreateContainerAsync(options);  
        await container.StartAsync();  
        Console.WriteLine($"Container started successfully (ID: {container.Id})");

        // Execute commands and stream output  
        var execOptions \= new ProcessExecutionOptions  
        {  
            Command \= "python3",  
            Arguments \= new\[\] { "-c", "import platform; print(f'Kernel: {platform.uname()}')" },  
            RedirectStandardOutput \= true,  
            RedirectStandardError \= true  
        };

        using var process \= await container.ExecuteProcessAsync(execOptions);  
        process.OutputDataReceived \+= (s, line) \=\> Console.WriteLine($"\[stdout\]: {line}");  
        process.ErrorDataReceived \+= (s, err) \=\> Console.Error.WriteLine($"\[stderr\]: {err}");

        int exitCode \= await process.WaitForExitAsync();  
        Console.WriteLine($"Process finished with code: {exitCode}");

        // Stop container instance  
        await container.StopAsync();  
        Console.WriteLine("Container stopped and cleaned up.");  
    }  
}

## **6\. Summary & Key Takeaways for Blog Readers**

* ---

  **Target Audience:** Developers who want a frictionless Linux container experience directly on Windows without heavy desktop client overhead or enterprise subscription concerns.  
* **Seamless Transition:** The command syntax directly mirrors Docker commands, meaning muscle memory is 100% transferable.  
* **Application Extensibility:** Native Windows applications (WPF, WinUI, WinForms, CLI tools) can now bundle, spin up, and manage isolated Linux micro-services locally via .NET.