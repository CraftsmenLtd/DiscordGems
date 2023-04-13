OWNER="CraftsmenLtd"
REPOSITORY="DiscordGems"

gh api repos/$OWNER/$REPOSITORY/actions/runs \
--paginate -q '.workflow_runs[] | "\(.id)"' | \
xargs -n1 -I % gh api repos/$OWNER/$REPOSITORY/actions/runs/% -X DELETE
