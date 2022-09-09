--[[===============================
    Creating the Enemy
=================================]]

local love = require "love"

function Enemy(level, ai)
    ai = ai or 'chaser'

    local _radius =
        ai == 'roamer' and 10 or
        ai == 'switcher' and 15 or
        ai == 'grumpy' and 15 or
        20
    local shape =
        ai == 'roamer' and 'circle' or
        ai == 'switcher' and 'diamond2' or
        ai == 'grumpy' and 'spike' or
        ai == 'chaser' and 'diamond1'

    local randomOffset = function()
        return math.random() * 0.3 - 0.15
    end
    local roamColor =
        ai == 'roamer' and {0.5 + randomOffset(), 0.5 + randomOffset(), 0.5 + randomOffset()} or
        ai == 'switcher' and {0.5 + randomOffset(), 0.4 + randomOffset(), 1} or
        ai == 'grumpy' and {1, 0.6 + randomOffset(), 0.2 + randomOffset()} or
        ai == 'chaser' and nil
    local chaseColor =
        ai == 'roamer' and nil or
        ai == 'switcher' and {0.1 + randomOffset(), 0.1 + randomOffset(), 1} or
        ai == 'grumpy' and {1, 0.4 + randomOffset(), 0.3 + randomOffset()} or
        ai == 'chaser' and {1, 0.2 + randomOffset(), 0.1 + randomOffset()}

    local _x, _y
    local dice = math.random(1, 4)
    if dice == 1 then
        _x = math.random(0, love.graphics.getWidth())
        _y = -_radius * 4
    elseif dice == 2 then
        _x = love.graphics.getWidth() + _radius * 4
        _y = math.random(0, love.graphics.getHeight())
    elseif dice == 3 then
        _x = math.random(0, love.graphics.getWidth())
        _y = love.graphics.getHeight() + _radius * 4
    elseif dice == 4 then
        _x = -_radius * 4
        _y = math.random(0, love.graphics.getHeight())
    end

    return {
        level = level or 1,
        radius = _radius,
        x = _x,
        y = _y,
        ai = ai or 'chaser',
        target_x = -10,
        target_y = -10,
        mode = ai == 'chaser' and 'chase' or 'roam',
        modeTimer = 0,

        checkTouched = function(self, player_x, player_y, cursor_radius)
            if shape == "diamond1" or shape == 'diamond2' then
                local e_x = self.x + (player_x < self.x and -self.radius or self.radius)
                local e_y = self.y + (player_y < self.y and -self.radius or self.radius)
                local short_radius = self.radius / math.sqrt(2)
                
                local dx1, dy1 = player_x - e_x, player_y - self.y
                local dx2, dy2 = player_x - self.x, player_y - e_y
                local d1, d2 = math.sqrt(dx1^2 + dy1^2), math.sqrt(dx2^2 + dy2^2)
                return
                d1 <= cursor_radius or
                d2 <= cursor_radius or
                d1 + d2 <= 2 * short_radius * (1 + short_radius / cursor_radius)
            elseif shape == "circle" or shape == "spike" then
                local dx, dy = player_x - self.x, player_y - self.y
                local d = math.sqrt(dx^2 + dy^2)
                return d <= cursor_radius + self.radius
            end
        end,

        move = function(self, player_x, player_y, dt)
            local function newTargetX()
                local newTarget = self.x + math.random(-100, 100)

                if newTarget < 0 or newTarget > love.graphics.getWidth() then
                    return math.random(0, love.graphics.getWidth())
                else
                    return newTarget
                end
            end

            local function newTargetY()
                local newTarget = self.y + math.random(-100, 100)

                if newTarget < 0 or newTarget > love.graphics.getHeight() then
                    return math.random(0, love.graphics.getHeight())
                else
                    return newTarget
                end
            end

            local dx, dy
            if self.mode == 'chase' then
                dx = player_x - self.x
                dy = player_y - self.y
            elseif self.mode == 'roam' then
                if self.target_x < 0 then
                    self.target_x = newTargetX()
                end
                if self.target_y < 0 then
                    self.target_y = newTargetY()
                end
                dx = self.target_x - self.x
                dy = self.target_y - self.y
            end

            local dp = math.sqrt(dx * dx + dy * dy)
            local speed = 1 + (self.level - 1) * 0.1
            if self.mode == 'chase' or dp >= speed then
                self.x = self.x + speed * dx / dp
                self.y = self.y + speed * dy / dp
            elseif self.mode == 'roam' then
                self.target_x = newTargetX()
                self.target_y = newTargetY()
            end

            if self.ai == 'switcher' then
                self.modeTimer = self.modeTimer + dt
                if self.modeTimer > 15 then
                    self.modeTimer = 0
                    if self.mode == 'chase' then
                        self.mode = 'roam'
                        self.target_x = newTargetX()
                        self.target_y = newTargetY()
                    else
                        self.mode = 'chase'
                    end
                end
            end

            if self.ai == 'grumpy' then
                dx = player_x - self.x
                dy = player_y - self.y
                if math.sqrt(dx ^ 2 + dy ^ 2) > 150 then
                    if self.mode == 'chase' then
                        self.mode = 'roam'
                        self.target_x = newTargetX()
                        self.target_y = newTargetY()
                    end
                else
                    self.mode = 'chase'
                end
            end
        end,

        draw = function(self)
            if self.mode == 'roam' and roamColor then
                love.graphics.setColor(roamColor[1], roamColor[2], roamColor[3])
            elseif self.mode == 'chase' and chaseColor then
                love.graphics.setColor(chaseColor[1], chaseColor[2], chaseColor[3])
            end

            if shape == 'diamond1' then
                love.graphics.polygon("fill", --diamond shape
                    self.x, self.y - self.radius,
                    self.x + self.radius, self.y,
                    self.x, self.y + self.radius,
                    self.x - self.radius, self.y
                )
                love.graphics.setColor(0.1, 0.1, 0.1, 0.5)
                love.graphics.rectangle("fill", self.x - 8, self.y - 8, 16, 16, 5, 3)
            elseif shape == 'diamond2' then
                love.graphics.polygon("fill", --diamond shape
                    self.x, self.y - self.radius,
                    self.x + self.radius, self.y,
                    self.x, self.y + self.radius,
                    self.x - self.radius, self.y
                )
                love.graphics.setColor(0.1, 0.1, 0.1, 0.5)
                love.graphics.rectangle("fill", self.x - self.radius + 5, self.y - 3, 2 * self.radius - 10, 6, 5, 3)
            elseif shape == 'spike' then
                love.graphics.polygon("fill", --diamond shape
                    self.x, self.y - self.radius,
                    self.x + self.radius, self.y,
                    self.x, self.y + self.radius,
                    self.x - self.radius, self.y
                )
                local radius = self.radius / math.sqrt(2)
                love.graphics.polygon("fill", --smaller square
                    self.x - radius, self.y - radius,
                    self.x + radius, self.y - radius,
                    self.x + radius, self.y + radius,
                    self.x - radius, self.y + radius
                )
                love.graphics.setColor(0.1, 0.1, 0.1, 0.5)
                love.graphics.circle("fill", self.x, self.y, 7)
            elseif shape == 'circle' then
                love.graphics.circle("fill", self.x, self.y, self.radius)
                love.graphics.setColor(0.1, 0.1, 0.1, 0.5)
                love.graphics.circle("fill", self.x, self.y, self.radius / 2.5)
            end
            love.graphics.setColor(1, 1, 1)
        end,
    }
end

return Enemy