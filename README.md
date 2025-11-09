# Remnaware tg notification tool

## Description
  This bot use telegram and remna webhooks for notification user
  of end subscription.

## Instalation
  ```
  mkdir /opt/notificator
  ```
  For install this project make /opt/notificator/.env vars:
  ```
  TELEGRAM_BOT_TOKEN=<bot tocken>
  RAILWAY_PUBLIC_DOMAIN=<bot webhook domain>
  REMNA_TOKEN="<remna api token>"
  REMNA_PUBLIC_DOMAIN=https://<remna panel domain>
  REMNA_SECRET_KEY="<remna webhook secret>"
  ```
  - TELEGRAM_BOT_TOKEN - you may get this token from bot father
  - RAILWAY_PUBLIC_DOMAIN - you domain where bot is work need https
  - REMNA_TOKEN - you remnaware token get from remna settings
  - REMNA_PUBLIC_DOMAIN - you remnaware panel domain
  - REMNA_SECRET_KEY - This secret is used to sign the webhook payload, must be exact 64 characters. Only a-z, 0-9, A-Z are allowed.

  For bot you need webhook domain for this bot via https.
  Installation /opt/notificator/docker-compose.yaml for install with remna panel:
  ```
  services:
    remna-notificator:
        image: iphizic/remna-notificator:latest
        restart: unless-stopped
        container_name: remna-notificator
        env_file:
            - .env
        hostname: remna-notificator
        networks:
          - remnawave-network

networks:
  remnawave-network:
      driver: bridge
      external: true
      name: remnawave-network
  ```

## Remna /opt/remnawave/env file settings
   ```
   ### WEBHOOK ###
   WEBHOOK_ENABLED=true
   ### Only https:// is allowed
   WEBHOOK_URL=https://<bot webhook domain>/remnahook
   ### This secret is used to sign the webhook payload, must be exact 64 characters. Only a-z, 0-9, A-Z are allowed.
   WEBHOOK_SECRET_HEADER="<remna webhook secret>"
   ```