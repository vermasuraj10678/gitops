# GitOps Demo with ArgoCD and Kustomize

This repository demonstrates a complete GitOps workflow using:
- **Spring Boot** application
- **ArgoCD** for continuous deployment
- **Kustomize** for environment-specific configurations
- **Kubernetes** namespaces for environment isolation

## 🏗️ Project Structure

```
├── app/                              # Spring Boot application
│   ├── src/main/java/...            # Java source code
│   ├── src/main/resources/          # Configuration files
│   └── pom.xml                      # Maven dependencies
├── k8s/                             # Kubernetes manifests
│   ├── base/                        # Base Kustomize configuration
│   │   ├── deployment.yaml          # Base deployment
│   │   ├── service.yaml             # Base service
│   │   └── kustomization.yaml       # Base kustomization
│   └── overlays/                    # Environment-specific overrides
│       ├── dev/                     # Development environment
│       │   ├── kustomization.yaml   # Dev kustomization
│       │   └── deployment-patch.yaml # Dev-specific patches
│       └── staging/                 # Staging environment
│           ├── kustomization.yaml   # Staging kustomization
│           └── deployment-patch.yaml # Staging-specific patches
├── Dockerfile                       # Container build definition
└── README.md                        # This file
```

## 🚀 Features

### Application Features
- REST API with health checks
- Environment-aware configuration
- Spring Boot Actuator for monitoring
- Dockerized for containerization

### GitOps Features
- **Environment Isolation**: Separate namespaces for `dev` and `staging`
- **Kustomize Management**: Base manifests with environment-specific overlays
- **ArgoCD Integration**: Automatic deployment on Git changes
- **Progressive Delivery**: Different resource allocation per environment

## 🌍 Environment Configurations

| Environment | Namespace | Replicas | CPU Request | Memory Request | 
|-------------|-----------|----------|-------------|----------------|
| Development | `gitops-dev` | 1 | 100m | 128Mi |
| Staging | `gitops-staging` | 3 | 250m | 256Mi |

## 🔧 Local Development

### Prerequisites
- Java 17+
- Maven 3.6+
- Docker
- kubectl
- k3d (for local Kubernetes)

### Build and Run Locally
```bash
# Build the application
cd app
./mvnw clean package

# Run locally
./mvnw spring-boot:run

# Build Docker image
docker build -t gitops-demo:latest .
```

## ☸️ Kubernetes Deployment

### Create Namespaces
```bash
kubectl create namespace gitops-dev
kubectl create namespace gitops-staging
```

### Deploy with Kustomize
```bash
# Deploy to development
kubectl apply -k k8s/overlays/dev

# Deploy to staging  
kubectl apply -k k8s/overlays/staging
```

### Verify Deployments
```bash
# Check dev environment
kubectl get all -n gitops-dev

# Check staging environment
kubectl get all -n gitops-staging
```

## 🔄 GitOps Workflow

1. **Developer pushes code** to this GitHub repository
2. **ArgoCD detects changes** and syncs automatically
3. **Kustomize applies** environment-specific configurations
4. **Applications deploy** to respective namespaces
5. **Monitoring** ensures applications are healthy

## 📋 ArgoCD Applications

This repository will be monitored by two ArgoCD applications:
- `gitops-demo-dev` → Monitors `k8s/overlays/dev`
- `gitops-demo-staging` → Monitors `k8s/overlays/staging`

## 🔍 Testing the Application

### Access the Application
```bash
# Port forward to access locally
kubectl port-forward -n gitops-dev service/dev-gitops-demo-service 8080:80
kubectl port-forward -n gitops-staging service/staging-gitops-demo-service 8081:80
```

### Test Endpoints
```bash
# Health check
curl http://localhost:8080/health

# Application info
curl http://localhost:8080/

# Actuator endpoints
curl http://localhost:8080/actuator/health
```

## 🔐 Security Best Practices

- Non-root user in container
- Resource limits defined
- Health checks configured
- Minimal base image used

## 📈 Next Steps

1. Set up ArgoCD in your cluster
2. Create ArgoCD applications pointing to this repository
3. Configure webhooks for immediate sync (optional)
4. Add monitoring and alerting
5. Implement blue-green or canary deployments

---

**Happy GitOps-ing!** 🎉