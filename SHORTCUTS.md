# Log shortcut

One iOS Shortcut called "Log" that ticks off a move, weights, run or ride sync
by dispatching a GitHub Actions workflow. The deploy runs after each one.

## Token

GitHub > Settings > Developer settings > Fine-grained tokens > Generate new token.

- Repository access: only `GeorgeChara/blog`
- Permissions: Actions, Read and write

## Shortcut

1. **Text**: paste the token.
2. **Choose from Menu** with four items. Each sets a **Text** action to the workflow file:

   | Menu item  | Workflow          |
   |------------|-------------------|
   | Move       | `log-move.yml`    |
   | Weights    | `log-gym.yml`     |
   | Run        | `log-run.yml`     |
   | Sync rides | `garmin-sync.yml` |

3. **Get Contents of URL**
   - URL: `https://api.github.com/repos/GeorgeChara/blog/actions/workflows/<file>/dispatches`
     (insert the menu result in place of `<file>`)
   - Method: POST
   - Headers:
     - `Authorization`: `Bearer <token>`
     - `Accept`: `application/vnd.github+json`
     - `X-GitHub-Api-Version`: `2022-11-28`
   - Request Body: JSON, `ref` = `main`
4. **Show Notification**: "Logged".

## Responses

- 204: success
- 401: bad token
- 403: token is missing Actions write
- 404: typo in the URL or workflow file name

## Optional

- Runs: add **Ask for Input** (number) and send `{"ref":"main","inputs":{"km":"<km>"}}`.
- Undo: send `{"ref":"main","inputs":{"remove":"true"}}`. Add `"date":"YYYY-MM-DD"` for a day other than today.

## Zwift

Zwift > Settings > Connections > Garmin Connect, so indoor rides sync with the rest.
