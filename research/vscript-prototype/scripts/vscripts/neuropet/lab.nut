// Explicitly invoked test harness. Never included by the playable mode.
IncludeScript("neuropet/model_tests", getroottable())
::NeuropetLab <- {
    startTime = 0.0,
    step = 0,
    timer = null,
    autoQuit = false,
    beforeShockCount = 0,
    previousDebug = false,
    function Start(quitAfter = false)
    {
        if (timer != null && timer.IsValid()) return
        ::NeuroPet.Start()
        previousDebug = ::NeuroPet.debug
        ::NeuropetRunModelTests()
        autoQuit = quitAfter
        startTime = Time()
        step = 0
        ::NeuroPet.frozen = true
        ::NeuroPet.Force("IDLE")
        ::NeuroPet.model.x = 450.0
        ::NeuroPet.Render()
        timer = SpawnEntityFromTable("info_target", { targetname = "neuropet_lab_clock" })
        timer.ValidateScriptScope()
        timer.GetScriptScope().NeuropetLabTick <- function()
        {
            try { return ::NeuropetLab.Tick() }
            catch (error)
            {
                printl("[neuropet-lab] FAIL: " + error)
                if (::NeuropetLab.timer != null && ::NeuropetLab.timer.IsValid()) ::NeuropetLab.timer.Kill()
                ::NeuropetLab.timer = null
                ::NeuroPet.Stop()
                if (::NeuropetLab.autoQuit) ::SendToConsole("quit")
                return 1.0
            }
        }
        AddThinkToEnt(timer, "NeuropetLabTick")
        printl("[neuropet-lab] started")
    },
    function Capture(name)
    {
        ::NeuroPet.Status()
        SendToConsole("jpeg neuropet_" + name + " 95")
    },
    function Tick()
    {
        local t = Time() - startTime
        if (step == 0 && t > 2) { ++step; Capture("idle") }
        else if (step == 1 && t > 3) { ++step; ::NeuroPet.SetDebug(true); ::NeuroPet.Force("WALK", "left") }
        else if (step == 2 && t > 4) { ++step; Capture("walk_a") }
        else if (step == 3 && t > 4.25) { ++step; Capture("walk_b") }
        else if (step == 4 && t > 5) { ++step; ::NeuroPet.Force("CLIMB", "left"); ::NeuroPet.model.y = 180; ::NeuroPet.Render() }
        else if (step == 5 && t > 6) { ++step; Capture("left") }
        else if (step == 6 && t > 7) { ++step; ::NeuroPet.Force("CLIMB", "right"); ::NeuroPet.model.y = 180; ::NeuroPet.Render() }
        else if (step == 7 && t > 8) { ++step; Capture("right") }
        else if (step == 8 && t > 9) { ++step; ::NeuroPet.Force("CEILING") }
        else if (step == 9 && t > 10) { ++step; Capture("ceiling") }
        else if (step == 10 && t > 11)
        {
            ++step
            ::NeuroPet.frozen = false
            beforeShockCount = ::NeuroPet.eventCount
            // This uses the actual event dispatcher, without injuring a player.
            FireGameEvent("player_incapacitated", { userid = 0, attacker = 0, type = 0 })
        }
        else if (step == 11 && t > 11.3) { ++step; Capture("fall") }
        else if (step == 12 && t > 12.3)
        {
            ++step
            Capture("landed")
            if (::NeuroPet.eventCount != beforeShockCount + 1) throw "Game event callback missing or duplicated"
            if (::NeuroPet.model.y != ::NeuroPet.model.Bottom()) throw "Clock-driven fall did not reach floor"
            ::NeuroPet.React("revive_success")
        }
        else if (step == 13 && t > 13) { ++step; Capture("cheer") }
        else if (step == 14 && t > 14) { ++step; ::NeuroPet.Force("SIT"); ::NeuroPet.frozen = true }
        else if (step == 15 && t > 15) { ++step; Capture("sit") }
        else if (step == 16 && t > 16) { ++step; ::NeuroPet.SetRenderer("text") }
        else if (step == 17 && t > 17) { ++step; Capture("text") }
        else if (step == 18 && t > 18) { ++step; ::NeuroPet.Stop() }
        else if (step == 19 && t > 19) { ++step; Capture("hidden"); printl("[neuropet-lab] PASS visual sequence and event dispatch") }
        else if (step == 20 && t > 20)
        {
            ++step
            timer.Kill()
            timer = null
            ::NeuroPet.frozen = false
            ::NeuroPet.SetRenderer("sprite")
            ::NeuroPet.SetDebug(previousDebug)
            if (autoQuit) SendToConsole("quit")
            else ::NeuroPet.Start()
        }
        return 0.03
    }
}
