# Remnaware tg notification tool

## Description
  This bot use telegram and remna webhooks for notification user
  of end subscription.

## Instalation
  For install this project make .env vars:
  ```
  TELEGRAM_BOT_TOKEN=<bot tocken>
  RAILWAY_PUBLIC_DOMAIN=<bot webhook domain>
  REMNA_TOKEN="<remna api tocken>"
  REMNA_PUBLIC_DOMAIN=https://<remna panel domain>
  REMNA_SECRET_KEY="<remna webhook secret>"
  ```

  For bot you need webhook domain for this bot via https.
  Installation docker compose for install with remna panel:
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

## Remna settings
   ```
   ### WEBHOOK ###
   WEBHOOK_ENABLED=true
   ### Only https:// is allowed
   WEBHOOK_URL=https://<bot webhook domain>/remnahook
   ### This secret is used to sign the webhook payload, must be exact 64 characters. Only a-z, 0-9, A-Z are allowed.
   WEBHOOK_SECRET_HEADER="<remna webhook secret>"
   ```