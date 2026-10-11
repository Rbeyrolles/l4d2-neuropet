IncludeScript("neuropet/model", getroottable())

if ("NeuroPet" in getroottable()) ::NeuroPet.Stop()

::NeuroPet <- {
    model = null,
    timer = null,
    hud = null,
    enabled = false,
    debug = false,
    frozen = false,
    renderer = "sprite",
    previousTime = 0.0,
    accumulator = 0.0,
    nextHudTime = 0.0,
    selectedSlot = -1,
    lastState = "",
    eventCount = 0,
    droppedTime = 0.0,
    fixedStep = 1.0 / 60.0,
    hudPeriod = 0.05,
    flags = { hidden = 16384, noBackground = 64, left = 256, survivors = 1024 },

    function Start()
    {
        if (enabled && timer != null && timer.IsValid()) return
        // Native engine bindings require the root table as their receiver,
        // even when this closure is called as an instance member.
        model = ::NeuropetModel(@() ::RandomFloat(0.0, 1.0))
        hud = { Fields = {} }
        for (local slot = 0; slot < 14; ++slot)
            hud.Fields["pose" + slot] <- {
                slot = slot,
                dataval = " ", // Nonempty text keeps the engine field active.
                flags = flags.left | flags.survivors | flags.hidden
            }
        hud.Fields.status <- {
            slot = 14, dataval = " ",
            flags = flags.left | flags.survivors | flags.noBackground | flags.hidden
        }
        HUDSetLayout(hud)
        timer = SpawnEntityFromTable("info_target", { targetname = "neuropet_clock" })
        if (timer == null) throw "Neuropet could not create its clock entity"
        timer.ValidateScriptScope()
        timer.GetScriptScope().NeuropetTick <- function()
        {
            try { return ::NeuroPet.Tick() }
            catch (error)
            {
                ::NeuroPet.Stop()
                printl("[neuropet] clock stopped after error: " + error)
                throw error
            }
        }
        previousTime = Time()
        accumulator = 0.0
        droppedTime = 0.0
        eventCount = 0
        selectedSlot = -1
        lastState = ""
        nextHudTime = 0.0
        enabled = true
        AddThinkToEnt(timer, "NeuropetTick")
        Render()
        printl("[neuropet] started; renderer=" + renderer + "; shared survivor HUD")
    },

    function Stop()
    {
        enabled = false
        if (timer != null && timer.IsValid()) timer.Kill()
        timer = null
        if (hud != null)
        {
            foreach (field in hud.Fields) field.flags = field.flags | flags.hidden
            HUDSetLayout(hud)
        }
        selectedSlot = -1
    },

    function Tick()
    {
        local owner = ::NeuroPet;
        if (!owner.enabled) return 1.0;
        local now = ::Time();
        local elapsed = now - owner.previousTime;
        owner.previousTime = now;
        if (elapsed < 0.0) elapsed = 0.0;
        if (elapsed > 0.25)
        {
            owner.droppedTime = owner.droppedTime + elapsed - 0.25;
            elapsed = 0.25;
        }
        if (!owner.frozen)
        {
            // Keep the loop operands local and the owner explicit; do not rely
            // on implicit table-member resolution across instance calls.
            local pending = owner.accumulator + elapsed;
            local dt = owner.fixedStep;
            local pet = owner.model;
            local steps = 0;
            while (pending >= dt && steps < 12)
            {
                pet.Step(dt);
                pending = pending - dt;
                steps = steps + 1;
            }
            if (pending >= dt)
            {
                owner.droppedTime = owner.droppedTime + pending;
                pending = 0.0;
            }
            owner.accumulator = pending;
        }
        else owner.accumulator = 0.0;
        if (now >= owner.nextHudTime)
        {
            owner.Render();
            owner.nextHudTime = now + owner.hudPeriod;
        }
        return 0.03;
    },

    function Render()
    {
        if (!enabled) return
        local slot = renderer == "text" ? 14 : model.PoseSlot()
        local changed = slot != selectedSlot
        for (local pose = 0; pose < 14; ++pose)
        {
            local field = hud.Fields["pose" + pose]
            field.flags = flags.left | flags.survivors | (pose == slot ? 0 : flags.hidden)
        }
        local status = hud.Fields.status
        status.flags = flags.left | flags.survivors | flags.noBackground
        if (!debug && renderer != "text") status.flags = status.flags | flags.hidden
        local nx = model.x / model.width
        local ny = model.y / model.height
        local nw = model.size / model.width
        local nh = model.size / model.height
        if (renderer == "text")
        {
            status.dataval = "(o_o) " + model.state
            HUDPlace(14, model.Clamp(nx, 0.0, 0.80), ny, 0.20, 0.055)
        }
        else
        {
            HUDPlace(slot, nx, ny, nw, nh)
            status.dataval = format("NP %s | %s | events:%d", model.state, model.lastEvent, eventCount)
            HUDPlace(14, 0.30, 0.015, 0.65, 0.045)
        }
        // Explicitly submit visibility changes. Do not depend on the native
        // update callback noticing changed flags in all loading contexts.
        if (changed) HUDSetLayout(hud)
        selectedSlot = slot
        if (model.state != lastState)
        {
            lastState = model.state
            if (debug) printl("[neuropet] state=" + lastState + "; slot=" + model.PoseSlot())
        }
    },

    function Force(state, side = "right")
    {
        if (!enabled) Start()
        model.Force(state, side)
        Render()
    },

    function React(eventName)
    {
        if (!enabled) return
        ++eventCount
        switch (eventName)
        {
            case "player_incapacitated":
            case "tank_spawn": model.Shock(eventName, 3); break
            case "witch_harasser_set":
            case "create_panic_event": model.Shock(eventName, 2); break
            case "witch_spawn": model.Shock(eventName, 1); break
            case "revive_success":
            case "survivor_rescued":
            case "player_entered_checkpoint": model.Celebrate(eventName); break
            default: throw "Unknown reaction event: " + eventName
        }
        printl("[neuropet] reaction=" + eventName + "; count=" + eventCount)
        Render()
    },

    function SetDebug(show)
    {
        debug = show
        if (enabled) { Render(); HUDSetLayout(hud) }
    },

    function SetRenderer(name)
    {
        if (name != "sprite" && name != "text") throw "Renderer must be sprite or text"
        renderer = name
        selectedSlot = -1
        if (enabled) Render()
    },

    function SetAspect(aspect)
    {
        if (aspect < 1.0 || aspect > 4.0) throw "Aspect must be in [1,4]"
        if (!enabled) Start()
        local yFraction = model.y / model.height
        model.height = model.width / aspect
        model.y = model.Clamp(yFraction * model.height, model.Top(), model.Bottom())
        if (model.state == "IDLE" || model.state == "WALK" || model.state == "SIT" ||
            model.state == "LAND" || model.state == "CHEER") model.y = model.Bottom()
        Render()
    },

    function Status()
    {
        if (!enabled) { printl("[neuropet] stopped"); return }
        printl(format("[neuropet] %s x=%.2f y=%.2f vx=%.2f vy=%.2f slot=%d events=%d dropped=%.3f",
            model.state, model.x, model.y, model.vx, model.vy, model.PoseSlot(), eventCount, droppedTime))
    }
}

// Default reactions are to any survivor, because Scripted HUD is shared through
// GameRules. These callbacks do not identify the local viewing client.
::NeuropetEvents <- {
    function OnGameEvent_player_incapacitated(params) { ::NeuroPet.React("player_incapacitated") },
    function OnGameEvent_tank_spawn(params) { ::NeuroPet.React("tank_spawn") },
    function OnGameEvent_witch_spawn(params) { ::NeuroPet.React("witch_spawn") },
    function OnGameEvent_witch_harasser_set(params) { ::NeuroPet.React("witch_harasser_set") },
    function OnGameEvent_create_panic_event(params) { ::NeuroPet.React("create_panic_event") },
    function OnGameEvent_revive_success(params) { ::NeuroPet.React("revive_success") },
    function OnGameEvent_survivor_rescued(params) { ::NeuroPet.React("survivor_rescued") },
    function OnGameEvent_player_entered_checkpoint(params) { ::NeuroPet.React("player_entered_checkpoint") }
}
// EMS can include a mode during initialization and activation. Register once
// per g_RoundState identity, so the same event cannot be delivered twice.
local callbackRound = "g_RoundState" in getroottable() ? ::g_RoundState : null
if (!("NeuropetCallbackRound" in getroottable()) || ::NeuropetCallbackRound != callbackRound)
{
    ::NeuropetCallbackRound <- callbackRound
    __CollectEventCallbacks(::NeuropetEvents, "OnGameEvent_", "GameEventCallbacks", RegisterScriptGameEventListener)
}
