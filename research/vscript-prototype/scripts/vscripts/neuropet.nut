// A separate co-op based mutation is the first-stage, reliable activation path.
MutationOptions <- {}
IncludeScript("neuropet/main", getroottable())
function SetupModeHUD() { ::NeuroPet.Start() }
function OnGameplayStart() { ::NeuroPet.Start() }
function OnShutdown() { ::NeuroPet.Stop() }
