# Setup

1. Create a **public** repository named exactly `Gowtham07-learn`.
2. Put `README.md` in the repository root.
3. Put `assets/profile.svg` in `assets/`.
4. Put `scripts/generate_profile.py` in `scripts/`.
5. Put `.github/workflows/update-profile.yml` in `.github/workflows/`.
6. Push everything to GitHub.
7. Open **Actions → Update GitHub Profile → Run workflow** once.
8. The graphic will then refresh automatically every day.

The workflow uses GitHub's built-in `GITHUB_TOKEN`; no personal access token is required.

Replace the LinkedIn URL in `README.md` with your actual profile.
