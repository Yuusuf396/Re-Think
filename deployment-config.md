# Deployment Configuration Guide

This guide explains how to configure and deploy your GreenTrack Climatiqq application using the CI/CD pipeline.

## 🚀 Quick Start

### 1. Enable GitHub Actions
- Push the workflow files to your repository
- Go to Actions tab to see the pipelines
- Configure secrets (see below)

### 2. Set Up Environments
- Create `develop` branch for staging
- Protect `main` branch for production
- Set up branch protection rules

## 🔐 Required Secrets

### GitHub Repository Secrets

Navigate to: `Settings` → `Secrets and variables` → `Actions`

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
REACT_APP_API_URL=https://your-backend.onrender.com/api
```

## 🐳 Docker Hub Setup

### 1. Create Docker Hub Account
- Go to [Docker Hub](https://hub.docker.com/)
- Create account and verify email

### 2. Create Repository
- Create repository: `climatiqq-backend`
- Set visibility (public/private)

### 3. Generate Access Token
- Go to Account Settings → Security
- Create New Access Token
- Copy username and token

## 🌐 Render Setup

### 1. Get API Token
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Navigate to Account Settings → API Keys
3. Click "New API Key"
4. Copy the generated token

### 2. Get Service IDs
1. Go to your Render service
2. Copy service ID from URL: `https://dashboard.render.com/web/[SERVICE_ID]`
3. Note down both backend and frontend service IDs

### 3. Configure Services
- Ensure auto-deploy is enabled
- Set environment variables
- Configure build commands

## 🔄 Workflow Configuration

### Branch Strategy
```
main (production) ← develop (staging) ← feature branches
```

### Deployment Flow
1. **Feature Development**: Create feature branch from `develop`
2. **Staging**: Merge to `develop` → Auto-deploy to staging
3. **Production**: Merge `develop` to `main` → Auto-deploy to production

### Environment Variables

#### Backend (.env.production):
```bash
DEBUG=False
SECRET_KEY=your_production_secret_key
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

#### Frontend (.env.production):
```bash
REACT_APP_API_URL=https://your-backend-domain.com/api
REACT_APP_ENVIRONMENT=production
GENERATE_SOURCEMAP=false
```

## 📊 Monitoring and Notifications

### 1. GitHub Actions Status
- Check Actions tab for pipeline status
- Review logs for any failures
- Monitor deployment times

### 2. Render Dashboard
- Monitor service health
- Check deployment logs
- Review performance metrics

### 3. Custom Notifications
Add to your workflows:
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🚨 Troubleshooting

### Common Issues:

#### 1. Docker Build Fails
```bash
# Check Dockerfile syntax
docker build -t test .

# Verify requirements.txt
pip install -r requirements.txt
```

#### 2. Tests Fail
```bash
# Run tests locally
cd climatiqq-backend
python manage.py test

# Check database connection
python manage.py check --database default
```

#### 3. Deployment Fails
```bash
# Check Render service status
curl -H "Authorization: Bearer $RENDER_TOKEN" \
  "https://api.render.com/v1/services/$SERVICE_ID"

# Verify environment variables
echo $RENDER_TOKEN
echo $RENDER_SERVICE_ID
```

### Debug Commands:
```bash
# Check workflow runs
gh run list

# View specific run
gh run view [RUN_ID]

# Rerun failed workflow
gh run rerun [RUN_ID]

# Download artifacts
gh run download [RUN_ID]
```

## 🔒 Security Best Practices

### 1. Secrets Management
- Never commit secrets to code
- Use GitHub Secrets for sensitive data
- Rotate tokens regularly
- Use least privilege principle

### 2. Environment Isolation
- Separate staging and production
- Use different databases per environment
- Isolate API keys and tokens

### 3. Access Control
- Limit who can deploy to production
- Require PR reviews
- Use branch protection rules

## 📈 Performance Optimization

### 1. Build Optimization
- Use Docker layer caching
- Implement dependency caching
- Parallel job execution
- Optimize Docker images

### 2. Deployment Optimization
- Blue-green deployments
- Rolling updates
- Health checks
- Auto-scaling

### 3. Monitoring
- Application performance monitoring
- Infrastructure metrics
- Error tracking
- User analytics

## 🎯 Advanced Features

### 1. Multi-Environment Deployment
```yaml
environments:
  staging:
    url: https://staging.yourapp.com
  production:
    url: https://yourapp.com
    protection_rules:
      required_reviewers: 2
```

### 2. Canary Deployments
- Gradual rollout
- Traffic splitting
- Rollback capabilities
- A/B testing

### 3. Infrastructure as Code
- Terraform configurations
- CloudFormation templates
- Kubernetes manifests
- Docker Compose files

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render API Documentation](https://render.com/docs/api)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [React Production Build](https://create-react-app.dev/docs/production-build/)

## 🆘 Support

If you encounter issues:

1. Check the GitHub Actions logs
2. Review Render deployment logs
3. Verify all secrets are configured
4. Check environment variables
5. Review branch protection rules

For additional help, refer to the troubleshooting section above or create an issue in your repository.




