# AWS EC2 Node.js + Nginx + Docker Setup
#===========================================

This repository documents how to deploy a Node.js application on an Amazon EC2 instance with Nginx and Docker.

---

## EC2 Setup

- Amazon Linux 2023
- Security group allows:
  - SSH (22)
  - HTTP (80)

---

## Installed Software

- Docker
- Node.js 20
- Nginx

---

## Deployment Steps

### Connect to EC2
```bash
ssh -i "jabulaniInstance01.pem" ec2-user@<PUBLIC-IP>


