# Deployment Guide

This guide covers different options for deploying the Inclusive Job Ad Analyzer web application.

## Quick Start

### Local Development
```bash
# Run on default port (7860)
python -m inclusive_job_ad_analyser

# Or with custom settings
python run_app.py --port 8080 --share
```

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access the app at: http://localhost:7860

### Manual Docker Build

```bash
# Build image
docker build -t job-ad-analyzer .

# Run container
docker run -p 7860:7860 job-ad-analyzer
```

---

## Cloud Platform Deployment

### Hugging Face Spaces (Free)

1. Create account at https://huggingface.co
2. Create new Space (Gradio app)
3. Clone this repository or upload files
4. Add `app.py` in root:
   ```python
   from inclusive_job_ad_analyser.webapp import create_interface
   
   if __name__ == "__main__":
       demo = create_interface()
       demo.launch()
   ```
5. Space will auto-deploy

**Pros**: Free, automatic HTTPS, shareable URL
**Cons**: Public by default (can upgrade for private)

### Railway

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway auto-detects Python and installs dependencies
5. Set environment variables:
   - `PORT=7860`
6. Deploy!

**Pros**: Free tier available, automatic deployments
**Cons**: Requires credit card for free tier

### Render

1. Create account at https://render.com
2. Click "New" → "Web Service"
3. Connect repository
4. Settings:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - Start Command: `python -m inclusive_job_ad_analyser`
5. Deploy

**Pros**: Free tier, custom domains
**Cons**: Slower cold starts on free tier

### AWS / GCP / Azure

Use Docker deployment method with:
- **AWS**: Elastic Container Service (ECS) or App Runner
- **GCP**: Cloud Run
- **Azure**: Container Instances

Example for AWS App Runner:
```bash
# Build and push to ECR
aws ecr create-repository --repository-name job-ad-analyzer
docker tag job-ad-analyzer:latest <account>.dkr.ecr.<region>.amazonaws.com/job-ad-analyzer:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/job-ad-analyzer:latest

# Create App Runner service from ECR image
```

---

## Self-Hosting on Server

### Using systemd (Linux)

Create `/etc/systemd/system/job-analyzer.service`:
```ini
[Unit]
Description=Inclusive Job Ad Analyzer
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/job-ad-analyzer
Environment="PATH=/opt/job-ad-analyzer/.venv/bin"
ExecStart=/opt/job-ad-analyzer/.venv/bin/python -m inclusive_job_ad_analyser
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable job-analyzer
sudo systemctl start job-analyzer
sudo systemctl status job-analyzer
```

### Using Nginx as Reverse Proxy

```nginx
server {
    listen 80;
    server_name jobanalyzer.example.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Environment Variables

Configure the app using environment variables:

```bash
# Server settings
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860

# Optional: Authentication
GRADIO_USERNAME=admin
GRADIO_PASSWORD=secure_password

# Optional: Analytics
GRADIO_ANALYTICS_ENABLED=false
```

---

## Security Considerations

### Authentication

Add to `webapp.py`:
```python
interface.launch(
    auth=("username", "password"),
    # Or use auth callback
    auth_message="Welcome to Job Ad Analyzer"
)
```

### HTTPS

For production, always use HTTPS:
- Cloud platforms handle this automatically
- Self-hosted: Use Let's Encrypt with Nginx/Caddy
- Or use Cloudflare in front

### Rate Limiting

For public deployments, consider adding rate limiting to prevent abuse:
```python
interface.launch(
    max_threads=10,  # Limit concurrent requests
)
```

---

## Monitoring

### Health Checks

The Docker Compose file includes a health check. For custom monitoring:

```python
# Add health endpoint
@app.route("/health")
def health():
    return {"status": "healthy"}
```

### Logs

```bash
# Docker logs
docker-compose logs -f

# Systemd logs
journalctl -u job-analyzer -f

# Application logs
# Add logging to webapp.py as needed
```

---

## Scaling

### Horizontal Scaling

For high traffic:
1. Deploy multiple instances
2. Use load balancer (AWS ALB, GCP Load Balancer, Nginx)
3. Share config/data via volume mounts or object storage

### Performance Optimization

- Use Redis for caching analysis results
- Implement request queuing for job searches
- Add CDN for static assets
- Pre-load spaCy model on startup

---

## Troubleshooting

### Port Already in Use
```bash
# Use different port
python run_app.py --port 8080
```

### spaCy Model Missing
```bash
python -m spacy download en_core_web_sm
```

### Gradio Not Installed
```bash
pip install gradio
```

### Web Scraping Fails
```bash
# Install optional dependencies
pip install requests beautifulsoup4
```

---

## Updates and Maintenance

### Pulling Updates
```bash
git pull origin main
pip install -r requirements.txt --upgrade
docker-compose down && docker-compose up -d --build
```

### Backup Configuration
Always backup:
- `config/settings.yaml` (custom scoring weights)
- `data/bias_terms.csv` (custom terms)

---

For more help, see the [main README](../README.md) or open an issue on GitHub.
