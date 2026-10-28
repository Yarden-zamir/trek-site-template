import { defineApp } from "kitshn";

// kitshn 2 (https://kit.yarden-zamir.com) serves the built `site` folder as a static site.
// Limit: the uploader and the sign-in do not run, so the page cannot take uploads or edits.
// Revisit when a trek needs editing on the live page: deploy `compose.yml` as a kitshn 2 compose app.
export default defineApp({
  static: { output: "site" },
  deploy: [
    { on: "push", branch: "main", name: "prod", startsIn: "Everyone" },
    { on: "pull_request", name: "pr-{pr}", ephemeral: true },
  ],
});
