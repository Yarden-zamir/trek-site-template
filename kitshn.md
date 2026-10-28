# kitshn

This repository deploys with [kitshn 2](https://kit.yarden-zamir.com).

- `kitshn.config.ts` names the app and its deploys. kitshn serves the committed `site/` folder as a static site.
- `.github/workflows/kitshn.yml` calls `kitshn2-deploy.yml`. It signs in to kitshn with GitHub OIDC, so the repo needs no deploy secrets.
- A push to `main` deploys `prod`, open to everyone. Each pull request deploys a `pr-<number>` preview. kitshn removes the preview when the pull request closes.
- The first deploy of a new repo waits until the owner allows the repo in kitshn.
- Run `uv run src/build.py` and commit `site/` before you push. kitshn does not run the build.
- The uploader, the sign-in and `compose.yml` do not run on kitshn 2. The page cannot take uploads or edits.
