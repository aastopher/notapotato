# Not a Potato
A web app for image generation using **Potato_GAN**.

## Quick Start Guide

### Prerequisites
Ensure you have the following tools installed before proceeding:
* [`kubectl`](https://kubernetes.io/docs/tasks/tools/)
* [`minikube`](https://minikube.sigs.k8s.io/docs/start/)
* [`devspace`](https://devspace.sh/docs/getting-started/installation)

### 1. Start Minikube
Start the local Kubernetes cluster using Minikube:
```bash
minikube start
```

Launch the Minikube dashboard to manage the cluster visually:
```bash
minikube dashboard
```

### 2. Create Namespace
Specify a Kubernetes namespace for the project to isolate your resources:
```bash
devspace use namespace notapotato
```

### 3. Start Application in Development Mode
Deploy the application into the Minikube cluster and start development mode:
```bash
devspace dev
```
This command deploys the app, synchronizes code changes, and automatically reloads the UI.

**Note:** For easier management, open the Devspace UI to access logs and the running application:
```bash
devspace ui
```
From the Devspace UI, you can:
- View real-time logs
- Exec into pods
- Access the application directly by selecting the **UI pod** and clicking "Open"

### 4. Access the Application
Once the application is running, you can interact with it through your browser. To open the app:
1. Go to the Devspace UI.
2. Select the **UI pod** and click **Open** to launch the web application.

### 5. Access the Swagger doc page
Once the application is running, you can interact directly with the existing api endpoint(s) through your browser.
1. Go to the Devspace UI.
2. Select the **FastAPI pod** and click **Open** to launch the web application.
3. Append `/docs` to the url

```
http://<minikube-ip>:<port>/docs
```

### 6. Stop the Application
To stop the development environment and clean up:

* Stop the Devspace sync by killing the process:
  ```bash
  Ctrl + C
  ```

* Stop the Minikube cluster:
  ```bash
  minikube stop
  ```

### 7. Clean Up
Once you're done, clean up resources and images to free up space:

* Purge the Kubernetes resources created by Devspace:
  ```bash
  devspace purge
  ```

* Clean up unused Docker container images:
  ```bash
  devspace clean images
  ```

---

## Next Steps
After following the quick start instructions, your **Not a Potato** web app should be running on Minikube. You can access the application and swagger page through the Devspace UI.

For further configuration and troubleshooting, refer to the following documentation:
- [Kubectl Docs](https://kubernetes.io/docs/reference/kubectl/)
- [Minikube Docs](https://minikube.sigs.k8s.io/docs/)
- [Devspace Docs](https://devspace.sh/docs/)

This guide provides a straightforward setup with easy access to the application and logs through the Devspace UI and Minikube dashboard.