/**
 * Cloudflare Worker: Strava Webhook → GitHub Action trigger
 *
 * Strava sends a POST when a new activity is created.
 * This worker validates it and fires a repository_dispatch
 * event on the blog repo to trigger the Garmin sync.
 *
 * Environment variables (set in Cloudflare dashboard):
 *   STRAVA_VERIFY_TOKEN  - random string you choose, used during subscription setup
 *   GITHUB_TOKEN         - GitHub personal access token (repo scope)
 *   GITHUB_REPO          - e.g. "GeorgeChara/blog"
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // --- GET: Strava webhook validation (subscription setup) ---
    if (request.method === "GET") {
      const mode = url.searchParams.get("hub.mode");
      const token = url.searchParams.get("hub.verify_token");
      const challenge = url.searchParams.get("hub.challenge");

      if (mode === "subscribe" && token === env.STRAVA_VERIFY_TOKEN) {
        return new Response(JSON.stringify({ "hub.challenge": challenge }), {
          headers: { "Content-Type": "application/json" },
        });
      }
      return new Response("Forbidden", { status: 403 });
    }

    // --- POST: Strava event notification ---
    if (request.method === "POST") {
      const event = await request.json();

      // Only trigger on new activities (not updates/deletes)
      if (event.object_type === "activity" && event.aspect_type === "create") {
        const resp = await fetch(
          `https://api.github.com/repos/${env.GITHUB_REPO}/dispatches`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${env.GITHUB_TOKEN}`,
              Accept: "application/vnd.github+json",
              "User-Agent": "strava-webhook-relay",
            },
            body: JSON.stringify({
              event_type: "garmin-activity",
              client_payload: {
                strava_activity_id: event.object_id,
                owner_id: event.owner_id,
              },
            }),
          }
        );

        if (resp.ok) {
          return new Response("Triggered", { status: 200 });
        }
        return new Response(`GitHub API error: ${resp.status}`, { status: 502 });
      }

      // Acknowledge other events without triggering
      return new Response("OK", { status: 200 });
    }

    return new Response("Method not allowed", { status: 405 });
  },
};
