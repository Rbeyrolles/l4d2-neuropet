// Meaningful physics/state regression checks, executed in the actual game VM.
function NeuropetRunModelTests()
{
    local checks = 0
    local check = function(condition, message)
    {
        if (!condition) throw "[neuropet-test] FAIL: " + message
        checks++
    }
    local create = @() ::NeuropetModel(@() 0.6)
    local advance = function(model, seconds)
    {
        for (local tick = 0; tick < seconds * 60; ++tick) model.Step(1.0 / 60.0)
    }
    foreach (side in ["left", "right"])
    {
        local model = create()
        model.Force("WALK", side)
        model.x = side == "left" ? model.Left() + 0.1 : model.Right() - 0.1
        model.Step(1.0 / 60.0)
        check(model.state == "CLIMB", side + " walk attaches to wall")
        advance(model, 5)
        check(model.state == "CEILING", side + " climb reaches ceiling")
        check(model.direction == (side == "left" ? 1 : -1), "ceiling points inward")
        model.Shock("player_incapacitated", 3)
        check(model.state == "FALL" && model.vy > 0, "shock detaches from ceiling")
        advance(model, 1)
        check(model.state == "LAND" || model.state == "IDLE", "shock reaches floor")
        check(model.y == model.Bottom(), "landing clamps to floor")
    }
    local model = create()
    model.Force("CLIMB", "left")
    model.y = model.height * 0.4
    model.Shock("tank_spawn", 3)
    advance(model, 1)
    check(model.y == model.Bottom(), "wall shock must not reattach")
    model.Force("CEILING")
    model.lastShock = -100.0
    check(model.Shock("create_panic_event", 2), "first fright accepted")
    check(!model.Shock("witch_spawn", 1), "duplicate lower priority fright debounced")
    check(model.Shock("tank_spawn", 3), "higher priority fright interrupts")
    model.Celebrate("revive_success")
    advance(model, 1.5)
    check(model.state == "CHEER", "reward waits for landing")
    model.Force("IDLE")
    // Clear debounce from the preceding test so this specifically checks a hop.
    model.lastShock = -100.0
    model.Shock("player_incapacitated", 3)
    check(model.vy < 0, "ground fright hops upwards")
    advance(model, 1)
    check(model.y == model.Bottom(), "ground hop lands")
    advance(model, 600)
    check(model.x >= model.Left() && model.x <= model.Right(), "ten minute x bounds")
    check(model.y >= model.Top() && model.y <= model.Bottom(), "ten minute y bounds")
    local refused = false
    try { model.Step(5.0) } catch (error) { refused = true }
    check(refused, "long frame must be subdivided, not integrated in one step")
    printl("[neuropet-test] PASS " + checks + " model checks")
    return checks
}
