--[[===============================
    Creating your first game in Love2D
=================================]]

local love = require "love" -- actually optional for running the game but VSCode might complain without it
local enemy = require "Enemy"
local button = require "Button"

math.randomseed(os.time())

local game = {
    difficulty = 1,
    state = {
        menu = true,
        paused = false,
        running = false,
        ended = false,
        settings = false
    },
    currLevel = 0,
    score = 0,
    --levels = {15, 30, 60, 120},
}

local fonts = {
    medium = {
        font = love.graphics.newFont(16),
        size = 16,
    },
    large = {
        font = love.graphics.newFont(24),
        size = 24,
    },
    massive = {
        font = love.graphics.newFont(60),
        size = 60,
    },
}

local player = {
    radius = 20,
    x = -100,
    y = -100
}

local buttons = {
    menu_state = {},
    ended_state = {}
}

local enemies = {}

local function changeGameState(state)
    game.state["menu"] = state == "menu"
    game.state["running"] = state == "running"
    game.state["paused"] = state == "paused"
    game.state["ended"] = state == "ended"
    game.state["settings"] = state == "settings"

    love.mouse.setGrabbed(state == "running")

    if (state == "paused") then
        player.paused_x, player.paused_y = player.x, player.y
    end
end

function love.load()
    changeGameState("menu")
    SetConfig()
    LoadButtons()
    --LoadEnemies()
end

_G.count = 0
function love.update(dt)
    print(count)
    _G.count = count + 1
    UpdatePlayerPos()
    UpdateEnemies(dt)
    UpdateScore(dt)
end

function love.draw()
    SetDefaultFont()
    DrawEnemies()
    DrawScore()
    DrawMenus()
    DrawFPSCounter()
    DrawPlayer()
end

--[[===============================
    Setup - functions
=================================]]

function SetConfig()
    love.window.setTitle("Save the Ball")
    love.mouse.setVisible(false)
end

function UpdatePlayerPos()
    player.x, player.y = love.mouse.getPosition()
end

function DrawPlayer()
    love.graphics.setColor(1, 1, 1)

    if game.state["paused"] then
        love.graphics.setColor(1, 1, 1, 0.5)
        love.graphics.circle("fill", player.paused_x, player.paused_y, player.radius)
        love.graphics.setColor(1, 1, 1)
    end

    if game.state["ended"] then
        love.graphics.setColor(1, 1, 1, 0.5)
        love.graphics.circle("fill", player.died_x, player.died_y, player.radius)
        love.graphics.setColor(1, 1, 1)
    end

    if game.state["running"] then
        love.graphics.circle("fill", player.x, player.y, player.radius)
    end

    if not game.state["running"] then
        love.graphics.circle("fill", player.x, player.y, player.radius / 2)
    end

    love.graphics.setColor(1, 1, 1)
end

function DrawFPSCounter()
    love.graphics.printf(
        "FPS: " .. love.timer.getFPS(),
        fonts.medium.font,
        10,
        love.graphics.getHeight() - 26,
        love.graphics.getWidth()
    )
end

--[[===============================
    Creating the Enemy - functions
=================================]]
function LoadEnemies()
    enemies = { enemy(1) }
end

function UpdateEnemies(dt)
    if game.state["running"] then
        for i = 1, #enemies do
            if not enemies[i]:checkTouched(player.x, player.y, player.radius) then
                enemies[i]:move(player.x, player.y, dt)

                if math.floor(game.score) ~= game.currLevel then
                    game.currLevel = math.floor(game.score)

                    if game.currLevel % 10 == 0 then
                        if game.currLevel % 60 == 0 then
                            table.insert(enemies, 1, enemy(game.difficulty * #enemies + 1, 'chaser'))
                        elseif game.currLevel % 40 == 0 then
                            table.insert(enemies, 1, enemy(game.difficulty * #enemies + 1, 'grumpy'))
                        elseif game.currLevel % 20 == 0 then
                            table.insert(enemies, 1, enemy(game.difficulty * #enemies + 1, 'switcher'))
                        else
                            table.insert(enemies, 1, enemy(game.difficulty * #enemies + 1, 'roamer'))
                        end
                    end
                end
            else
                player.died_x, player.died_y = player.x, player.y
                changeGameState("ended")
            end
        end
    end
end

function DrawEnemies()
    if game.state["running"] or game.state["paused"] or game.state["ended"] then
        for i = 1, #enemies do
            enemies[i]:draw()
        end
    end
end
--[[===============================
    The Menu Screen - functions
=================================]]

local function startNewGame()
    changeGameState("running")

    game.score = 0
    game.currLevel = 0

    LoadEnemies()
end

function LoadButtons()
    buttons.menu_state.play_game = Button("Play Game", startNewGame, nil, 150, 45)
    buttons.menu_state.settings = Button("Settings", nil, nil, 150, 45)
    buttons.menu_state.exit_game = Button("Exit Game", love.event.quit, nil, 150, 45)

    buttons.ended_state.replay_game = Button("Replay", startNewGame, nil, 100, 45)
    buttons.ended_state.menu = Button("Menu", changeGameState, "menu", 100, 45)
    buttons.ended_state.exit_game = Button("Quit", love.event.quit, nil, 100, 45)
end

function DrawMenus()
    if game.state["menu"] then
        love.graphics.printf("Save the Ball", fonts.massive.font, 0, 20,
            love.graphics.getWidth(), "center"
        )
        love.graphics.printf("Move the ball using your mouse cursor and avoid touching the enemies for as long as you can!",
            fonts.medium.font, 0, 50 + fonts.massive.size, love.graphics.getWidth(), "center"
        )

        buttons.menu_state.play_game:draw(love.graphics.getWidth() / 2 - 75, love.graphics.getHeight() / 2, 10, 15)
        --buttons.menu_state.settings:draw(love.graphics.getWidth() / 2 - 75, love.graphics.getHeight() / 2 + 55, 10, 15)
        --buttons.menu_state.exit_game:draw(love.graphics.getWidth() / 2 - 75, love.graphics.getHeight() / 2 + 110, 10, 15)
        buttons.menu_state.exit_game:draw(love.graphics.getWidth() / 2 - 75, love.graphics.getHeight() / 2 + 55, 10, 15)

    elseif game.state["ended"] then
        love.graphics.setColor(0, 0, 0, 0.5)
        love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())

        love.graphics.setColor(1, 1, 1)

        love.graphics.setFont(fonts.large.font)

        buttons.ended_state.replay_game:draw(love.graphics.getWidth() / 2 - 50, love.graphics.getHeight() / 1.8, 10, 10)
        buttons.ended_state.menu:draw(love.graphics.getWidth() / 2 - 50, love.graphics.getHeight() / 1.53, 10, 10)
        buttons.ended_state.exit_game:draw(love.graphics.getWidth() / 2 - 50, love.graphics.getHeight() / 1.33, 10, 10)

        love.graphics.printf("Game Over", fonts.massive.font, 0, love.graphics.getHeight() / 3 - fonts.massive.size,
            love.graphics.getWidth(), "center"
        )
        love.graphics.printf("Score: " .. math.floor(game.score), fonts.large.font, 0, love.graphics.getHeight() / 3,
            love.graphics.getWidth(), "center"
        )
    elseif game.state["paused"] then
        love.graphics.setColor(0, 0, 0, 0.5)
        love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())

        love.graphics.setColor(1, 1, 1)
        love.graphics.printf("Game Paused", fonts.massive.font, 0, love.graphics.getHeight() / 2 - fonts.massive.size,
            love.graphics.getWidth(), "center"
        )
        love.graphics.printf("Click on the center of the player ball to resume", fonts.medium.font, 0, love.graphics.getHeight() / 2 + fonts.massive.size,
            love.graphics.getWidth(), "center"
        )
    end
end

function love.mousepressed(x, y, buttonPressed, isTouch, presses)
    if not game.state["running"] then
        if buttonPressed == 1 then
            if game.state["menu"] then
                for index in pairs(buttons.menu_state) do
                    if buttons.menu_state[index]:checkPressed(x, y, player.radius / 2) then
                        break
                    end
                end
            elseif game.state["ended"] then
                for index in pairs(buttons.ended_state) do
                    if buttons.ended_state[index]:checkPressed(x, y, player.radius / 2) then
                        break
                    end
                end
            elseif game.state["paused"] then
                local dx, dy = x - player.paused_x, y - player.paused_y
                local d = math.sqrt(dx^2 + dy^2)
                if d <= player.radius / 2 then
                    changeGameState("running")
                end
            end
        end
    end
end

--[[===============================
    Adding a Point System - functions
=================================]]
function UpdateScore(dt)
    if game.state["running"] then
        game.score = game.score + dt
    end
end

function DrawScore()
    if game.state["running"] or game.state["paused"] then
        love.graphics.printf(
            "Score: " .. math.floor(game.score),
            fonts.large.font,
            0,
            10,
            love.graphics.getWidth(),
            "center"
        )
    end
end
--[[===============================
    Game Over Screen - functions
=================================]]
function SetDefaultFont()
    love.graphics.setFont(fonts.medium.font)
end

--[[===============================
    Extra - functions
=================================]]
function love.focus(f)
    if not f and game.state["running"] then
        changeGameState("paused")
    end
end