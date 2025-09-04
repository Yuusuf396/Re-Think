# CI/CD Pipeline Setup Guide

This repository includes comprehensive CI/CD pipelines for both the Django backend and React frontend using GitHub Actions.

## 🚀 What's Included

### 1. Backend CI/CD Pipeline (`backend-ci-cd.yml`)
- **Testing**: Runs Django tests with PostgreSQL database
- **Code Quality**: Linting with flake8, black, and isort
- **Security**: Security checks with bandit and safety
- **Docker**: Builds and pushes Docker images to Docker Hub
- **Deployment**: Staging and production deployment triggers

### 2. Frontend CI/CD Pipeline (`frontend-ci-cd.yml`)
- **Testing**: Runs React tests and generates coverage reports
- **Code Quality**: ESLint and Prettier checks
- **Build**: Creates production-ready build artifacts
- **Deployment**: Staging and production deployment

### 3. Render Deployment (`render-deploy.yml`)
- **Automatic Deployment**: Triggers Render deployments via API
- **Smart Triggers**: Only deploys changed services
- **Notifications**: Deployment status updates

## 🔧 Setup Instructions

### Step 1: GitHub Secrets Configuration

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add these secrets:

#### Backend Secrets:
```
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password
```

#### Render Secrets:
```
RENDER_TOKEN=your_render_api_token
RENDER_BACKEND_SERVICE_ID=your_backend_service_id
RENDER_FRONTEND_SERVICE_ID=your_frontend_service_id
```

#### Frontend Secrets:
```
REACT_APP_API_URL=your_backend_api_url
```

### Step 2: Get Render API Token

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Navigate to Account Settings → API Keys
3. Create a new API key
4. Copy the token to your GitHub secrets

### Step 3: Get Render Service IDs

1. Go to your Render service
2. Copy the service ID from the URL: `https://dashboard.render.com/web/[SERVICE_ID]`
3. Add to GitHub secrets

### Step 4: Branch Protection (Recommended)

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Select the CI checks you want to require

## 📋 Workflow Triggers

### Backend Pipeline:
- **Triggers on**: Changes to `climatiqq-backend/` directory
- **Branches**: `main`, `develop`
- **Pull Requests**: All PRs to `main` and `develop`

### Frontend Pipeline:
- **Triggers on**: Changes to `climatiqq-frontend/` directory
- **Branches**: `main`, `develop`
- **Pull Requests**: All PRs to `main` and `develop`

### Render Deployment:
- **Triggers on**: Push to `main` branch
- **Smart Detection**: Only deploys services with changes

## 🔄 Workflow Stages

### 1. Test Stage
- Code checkout
- Dependency installation
- Linting and code quality checks
- Security scanning
- Unit and integration tests
- Test coverage reporting

### 2. Build Stage
- Docker image building (Backend)
- Frontend build artifacts
- Artifact upload for deployment

### 3. Deploy Stage
- **Staging**: Automatic deployment on `develop` branch
- **Production**: Manual approval deployment on `main` branch
- **Render**: API-triggered deployments

## 🐳 Docker Integration

The backend pipeline automatically:
- Builds Docker images
- Pushes to Docker Hub
- Tags with `latest` and commit SHA
- Uses GitHub Actions cache for faster builds

## 📊 Monitoring and Notifications

### Artifacts Generated:
- Test results and coverage reports
- Security scan reports
- Build artifacts
- Docker images

### Notifications:
- GitHub Actions status checks
- Deployment status updates
- Custom notification hooks (Slack, Discord, etc.)

## 🚨 Troubleshooting

### Common Issues:

1. **Docker Build Fails**:
   - Check Docker Hub credentials
   - Verify Dockerfile syntax
   - Check resource limits

2. **Tests Fail**:
   - Review test output in Actions tab
   - Check database configuration
   - Verify dependencies

3. **Deployment Fails**:
   - Check Render API token
   - Verify service IDs
   - Check Render service status

### Debug Commands:

```bash
# Check workflow runs
gh run list

# View specific run logs
gh run view [RUN_ID]

# Rerun failed workflow
gh run rerun [RUN_ID]
```

## 🔒 Security Best Practices

1. **Secrets Management**:
   - Never commit secrets to code
   - Use GitHub Secrets for sensitive data
   - Rotate tokens regularly

2. **Branch Protection**:
   - Require PR reviews
   - Enforce status checks
   - Protect main branch

3. **Dependency Scanning**:
   - Regular security updates
   - Automated vulnerability scanning
   - Pin dependency versions

## 📈 Performance Optimization

1. **Caching**:
   - pip cache for Python dependencies
   - npm cache for Node.js
   - Docker layer caching

2. **Parallel Jobs**:
   - Independent test and build stages
   - Concurrent frontend/backend processing
   - Smart dependency management

3. **Resource Management**:
   - Use Ubuntu runners for cost efficiency
   - Optimize Docker image sizes
   - Clean up artifacts regularly

## 🎯 Next Steps

1. **Customize Workflows**: Adapt to your specific deployment needs
2. **Add Notifications**: Integrate with Slack, Discord, or email
3. **Performance Monitoring**: Add deployment metrics and monitoring
4. **Security Scanning**: Integrate additional security tools
5. **Multi-Environment**: Add development and testing environments

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render API Documentation](https://render.com/docs/api)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [React Build Optimization](https://create-react-app.dev/docs/production-build/)

