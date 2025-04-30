# mattermost-gitea-connector
This is a personal project designed to merge pull requests using a [custom slash command](https://developers.mattermost.com/integrate/slash-commands/custom) in [mattermost](https://mattermost.com).

# My use case
I store my Docker Compose files in my personal [Gitea](https://about.gitea.com) instance, and I deploy them using [Komodo](https://komo.do). To keep my images up-to-date, I use the Renovate bot, which automatically creates a pull request when it detects a newer version of the corresponding Docker container.

If you're interested, I highly recommend reading this article by Nick Cunningham:

https://nickcunningh.am/blog/how-to-automate-version-updates-for-your-self-hosted-docker-containers-with-gitea-renovate-and-komodo

Whenever a new version is detected, renovate creates a pull request with the updated docker compose file. On merge, a webhook is triggered, which redeploys my stack.
Another webhook is triggered to send a message to my mattermost DevOps channel