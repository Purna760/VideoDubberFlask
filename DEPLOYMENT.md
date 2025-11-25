# Deployment Guide for Render

This guide will help you deploy the Video Dubbing & Translation App to Render.

## Prerequisites

- GitHub account (to host your repository)
- Render account (free tier available at https://render.com)

## Step 1: Push Code to GitHub

1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit - Video dubbing app"
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Step 2: Create Web Service on Render

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:

### Basic Settings
- **Name**: `video-dubbing-app` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

### Build Settings
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 600
  ```

### Advanced Settings

#### Add Build Command for FFmpeg
Since FFmpeg is required as a system dependency, you need to add it:

1. Go to "Environment" tab
2. Add this to **Build Command** (before pip install):
   ```
   apt-get update && apt-get install -y ffmpeg pkg-config
   ```

Final Build Command should be:
```
apt-get update && apt-get install -y ffmpeg pkg-config && pip install -r requirements.txt
```

#### Environment Variables
- **PYTHON_VERSION**: `3.11.0`
- Add `SESSION_SECRET` (generate a random string)

#### Instance Type
- **Free**: Works for testing (limited resources)
- **Starter ($7/month)**: Recommended for production (better performance, no sleep)

## Step 3: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Monitor the deployment logs for any errors
4. Once deployed, you'll get a URL like: `https://video-dubbing-app.onrender.com`

## Step 4: Test Your Deployment

1. Visit your deployment URL
2. Upload a short test video (30 seconds)
3. Select a target language
4. Verify the dubbing process completes successfully
5. Download and check the dubbed video

## Important Notes

### Performance Considerations

- **Free Tier**: Apps sleep after 15 minutes of inactivity, causing cold starts
- **Processing Time**: Video dubbing is CPU-intensive. Expect:
  - 30-second video: ~2-3 minutes
  - 5-minute video: ~10-15 minutes
- **Timeout**: Gunicorn is configured with 600-second (10-minute) timeout
- **Memory**: Large videos (>100MB) may require more RAM (upgrade plan if needed)

### Storage Limitations

- Render's free tier has limited storage
- Temporary files are cleaned up automatically after processing
- Consider external storage (S3, Cloudinary) for production at scale

### Troubleshooting

**Build Fails**
- Check that FFmpeg installation succeeded in logs
- Verify all dependencies in requirements.txt are compatible

**App Crashes During Processing**
- Check memory usage (may need to upgrade plan)
- Verify video file size is under 500MB
- Check logs for specific error messages

**Slow Processing**
- Free tier has limited CPU - upgrade to Starter or higher
- Consider using smaller Whisper model for faster transcription
- Optimize by processing audio in chunks

### Monitoring

- Enable logging in Render dashboard
- Monitor resource usage (CPU, memory)
- Set up alerts for failures

### Cost Optimization

1. **Free Tier**: Good for testing and demos
2. **Starter Plan ($7/month)**: Recommended for light production use
3. **Standard Plan**: For high traffic or faster processing

### Security

- Keep `SESSION_SECRET` environment variable secure
- Add rate limiting for production (prevent abuse)
- Consider authentication for commercial use

## Alternative: Using render.yaml

You can also deploy using the `render.yaml` file included in this repository:

1. Push code to GitHub
2. In Render dashboard, select "New" → "Blueprint"
3. Connect repository
4. Render will automatically read `render.yaml` configuration
5. Review and deploy

## Support

For issues:
1. Check Render deployment logs
2. Review error messages in browser console
3. Test locally first to isolate deployment vs. code issues

## Next Steps After Deployment

1. Add custom domain (available on paid plans)
2. Enable HTTPS (automatic on Render)
3. Set up monitoring and alerts
4. Consider adding:
   - User authentication
   - Video processing queue
   - Database for job history
   - Cloud storage integration
