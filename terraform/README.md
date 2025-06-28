# FastAPI Cloud Run Deployment

This repo deploys a service on **Cloud Run** to showcase a **FastAPI** backend used to generate texts and images.

## Features

- **Text Generation**: Responds like a pirate would. ☠️  
- **Image Generation**: Only generates **anime-style** images. 🎌

## Resources Deployed

- **Artifact Registry**
- **Cloud Run Service**
- **Secret in Secret Manager**

## Deployment Instructions

1. Navigate to the `terraform` folder:

   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply 
    ```

## Required inputs
    - TF_VAR_api-key