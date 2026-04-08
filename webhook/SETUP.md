# Strava Webhook → GitHub Action Relay

Triggers the Garmin sync GitHub Action instantly when you finish a ride.

## Flow

```
Finish ride → Garmin → Strava → This worker → GitHub Action → Site updates
```

## Setup Steps

### 1. Deploy the Cloudflare Worker

```bash
cd webhook
npx wrangler login
npx wrangler deploy
```

Note the worker URL (e.g. `https://strava-webhook-relay.<your-subdomain>.workers.dev`)

### 2. Set Worker Environment Variables

In the Cloudflare dashboard (Workers & Pages → strava-webhook-relay → Settings → Variables):

| Variable | Value |
|----------|-------|
| `STRAVA_VERIFY_TOKEN` | Any random string you choose (e.g. `my-cycling-webhook-2026`) |
| `GITHUB_TOKEN` | GitHub personal access token with `repo` scope ([create here](https://github.com/settings/tokens/new)) |
| `GITHUB_REPO` | `GeorgeChara/blog` |

Mark `GITHUB_TOKEN` as encrypted.

### 3. Register Strava Webhook Subscription

You already have Strava API credentials from the cycling-dashboard. Use them:

```bash
curl -X POST https://www.strava.com/api/v3/push_subscriptions \
  -F client_id=YOUR_STRAVA_CLIENT_ID \
  -F client_secret=YOUR_STRAVA_CLIENT_SECRET \
  -F callback_url=https://strava-webhook-relay.YOUR_SUBDOMAIN.workers.dev \
  -F verify_token=my-cycling-webhook-2026
```

Replace:
- `YOUR_STRAVA_CLIENT_ID` and `YOUR_STRAVA_CLIENT_SECRET` with your Strava API app credentials
- `YOUR_SUBDOMAIN` with your Cloudflare Workers subdomain
- `my-cycling-webhook-2026` with whatever you set as `STRAVA_VERIFY_TOKEN`

You should get back: `{"id": 12345, "resource_state": 2, ...}`

### 4. Verify

Go for a ride (or create a manual activity on Strava). Within a minute:
1. Strava POSTs to the worker
2. Worker triggers `garmin-activity` repository_dispatch
3. GitHub Action runs `garmin-sync.yml`
4. Site rebuilds with the new ride

### Troubleshooting

**Check worker logs:**
```bash
npx wrangler tail
```

**List existing subscriptions:**
```bash
curl -G https://www.strava.com/api/v3/push_subscriptions \
  -d client_id=YOUR_STRAVA_CLIENT_ID \
  -d client_secret=YOUR_STRAVA_CLIENT_SECRET
```

**Delete a subscription:**
```bash
curl -X DELETE "https://www.strava.com/api/v3/push_subscriptions/SUBSCRIPTION_ID" \
  -d client_id=YOUR_STRAVA_CLIENT_ID \
  -d client_secret=YOUR_STRAVA_CLIENT_SECRET
```
