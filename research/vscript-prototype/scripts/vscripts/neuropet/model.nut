// Independent, small state machine. Coordinates are virtual HUD units;
// y grows downwards. No entity or HUD calls belong in this file.
::NeuropetModel <- class
{
    width = 1000.0
    height = 562.5
    size = 72.0
    margin = 4.0
    bottomInset = 68.0
    walkSpeed = 90.0
    climbSpeed = 95.0
    ceilingSpeed = 65.0
    gravity = 1400.0
    drag = 1.2
    terminalSpeed = 900.0
    x = 0.0
    y = 0.0
    vx = 0.0
    vy = 0.0
    direction = 1
    wall = "right"
    state = "IDLE"
    age = 0.0
    duration = 2.0
    clock = 0.0
    lastShock = -100.0
    lastPriority = 0
    lastEvent = "spawn"
    pendingCheer = false
    random = null

    constructor(randomFunction)
    {
        random = randomFunction
        x = width * 0.45
        y = Bottom()
    }

    function Left() { return margin }
    function Right() { return width - size - margin }
    function Top() { return margin }
    function Bottom() { return height - size - margin - bottomInset }
    function Clamp(value, low, high) { return value < low ? low : (value > high ? high : value) }

    function Enter(next, seconds = 0.0)
    {
        state = next
        age = 0.0
        duration = seconds
        vx = 0.0
        vy = 0.0
    }

    function Fall(horizontal = 0.0, vertical = 30.0)
    {
        Enter("FALL")
        vx = horizontal
        vy = vertical
        // A fall detaches from its surface. In particular, touching the wall
        // must not count as a landing or reattach on the next physics tick.
        if (y >= Bottom() && vertical < 0.0) y = Bottom() - 0.01
    }

    function Shock(eventName, priority = 2)
    {
        if (clock - lastShock < 1.0 && priority <= lastPriority) return false
        lastShock = clock
        lastPriority = priority
        lastEvent = eventName
        pendingCheer = false
        local airborne = state == "CEILING" || state == "CLIMB" || state == "FALL"
        local push = x < width * 0.5 ? 140.0 : -140.0
        Fall(push, airborne ? 70.0 : -340.0)
        return true
    }

    function Celebrate(eventName)
    {
        lastEvent = eventName
        // Let an active fright/flight finish, then celebrate safely on the floor.
        pendingCheer = true
        if (state == "FALL" || state == "LAND") return
        if (state == "CLIMB" || state == "CEILING")
            Fall(0.0, 40.0)
        else
        {
            y = Bottom()
            pendingCheer = false
            Enter("CHEER", 2.0)
        }
    }

    function Force(next, side = "right")
    {
        local valid = ["IDLE", "WALK", "CLIMB", "CEILING", "FALL", "LAND", "SIT", "CHEER"]
        if (valid.find(next) == null) throw "Unknown state: " + next
        direction = side == "left" ? -1 : 1
        pendingCheer = false
        if (next == "CLIMB")
        {
            wall = side
            x = side == "left" ? Left() : Right()
            y = Bottom()
        }
        else if (next == "CEILING" || next == "FALL")
        {
            x = width * 0.5
            y = Top()
        }
        else y = Bottom()
        Enter(next, next == "CEILING" ? 12.0 : 3.0)
        if (next == "FALL") vy = 30.0
    }

    function Step(dt)
    {
        if (dt <= 0.0 || dt > 0.05) throw "Step requires a fixed dt in (0, 0.05]"
        age += dt
        clock += dt
        switch (state)
        {
            case "IDLE":
            case "SIT":
                if (age >= duration)
                {
                    if (random() < 0.20) direction = -direction
                    Enter("WALK", 3.0 + random() * 5.0)
                }
                break
            case "WALK":
                vx = direction * walkSpeed
                x += vx * dt
                y = Bottom()
                if (x <= Left() || x >= Right())
                {
                    wall = x <= Left() ? "left" : "right"
                    x = wall == "left" ? Left() : Right()
                    Enter("CLIMB")
                }
                else if (age >= duration)
                    Enter(random() < 0.5 ? "IDLE" : "SIT", 1.0 + random() * 2.0)
                break
            case "CLIMB":
                x = wall == "left" ? Left() : Right()
                vy = -climbSpeed
                y += vy * dt
                if (y <= Top())
                {
                    y = Top()
                    direction = wall == "left" ? 1 : -1
                    Enter("CEILING", 8.0 + random() * 8.0)
                }
                break
            case "CEILING":
                y = Top()
                vx = direction * ceilingSpeed
                x += vx * dt
                if (x <= Left() || x >= Right() || age >= duration)
                {
                    x = Clamp(x, Left(), Right())
                    Fall(-direction * 90.0, 30.0)
                }
                break
            case "FALL":
                vx /= 1.0 + drag * dt
                vy = Clamp(vy + gravity * dt, -terminalSpeed, terminalSpeed)
                x += vx * dt
                y += vy * dt
                if (x < Left() || x > Right())
                {
                    x = Clamp(x, Left(), Right())
                    vx = 0.0
                }
                if (y < Top())
                {
                    y = Top()
                    vy = 0.0
                }
                if (y >= Bottom() && vy >= 0.0)
                {
                    y = Bottom()
                    Enter("LAND", 0.35)
                }
                break
            case "LAND":
                if (age >= duration)
                {
                    if (pendingCheer)
                    {
                        pendingCheer = false
                        Enter("CHEER", 2.0)
                    }
                    else Enter("IDLE", 1.0 + random() * 2.0)
                }
                break
            case "CHEER":
                if (age >= duration) Enter("IDLE", 1.5)
                break
        }
        x = Clamp(x, Left(), Right())
        y = Clamp(y, Top(), Bottom())
    }

    function PoseSlot()
    {
        local right = direction > 0
        switch (state)
        {
            case "IDLE": return right ? 1 : 0
            case "WALK": return right ? 3 : 2
            case "CLIMB": return wall == "right" ? 5 : 4
            case "CEILING": return right ? 7 : 6
            case "FALL": return right ? 9 : 8
            case "LAND": return right ? 11 : 10
            case "SIT": return 12
            case "CHEER": return 13
        }
        return 0
    }
}
