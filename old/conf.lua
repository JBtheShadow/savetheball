local love = require "love"

function love.conf(t)
    t.console = true
    t.window.msaa = 4
end