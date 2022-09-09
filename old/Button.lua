--[[===============================
    The Menu Screen
=================================]]

local love = require "love"

function Button(text, func, func_param, width, height)
    return {
        width = width or 100,
        height = height or 100,
        func = func or function() print((text or "No text") .. " was clicked") end,
        func_param = func_param,
        text = text or "No text",
        button_x = 0,
        button_y = 0,
        text_x = 0,
        text_y = 0,

        checkPressed = function(self, mouse_x, mouse_y, cursor_radius)
            if (mouse_x + cursor_radius >= self.button_x) and
               (mouse_x - cursor_radius <= self.button_x + self.width) and
               (mouse_y + cursor_radius >= self.button_y) and
               (mouse_y - cursor_radius <= self.button_y + self.height) then
                if self.func_param then
                    self.func(self.func_param)
                else
                    self.func()
                end
                return true
            end
        end,

        draw = function(self, button_x, button_y, text_x, text_y)
            self.button_x = button_x or self.button_x
            self.button_y = button_y or self.button_y

            if text_x then
                self.text_x = text_x + self.button_x
            else
                self.text_x = self.button_x
            end

            if text_y then
                self.text_y = text_y + self.button_y
            else
                self.text_y = self.button_y
            end

            love.graphics.setColor(0.6, 0.6, 0.6)
            love.graphics.rectangle("fill", self.button_x, self.button_y, self.width, self.height, 5, 5, 2)

            love.graphics.setColor(0.1, 0.1, 0.1)
            love.graphics.print(self.text, self.text_x, self.text_y)

            love.graphics.setColor(1, 1, 1)
        end
    }
end

return Button