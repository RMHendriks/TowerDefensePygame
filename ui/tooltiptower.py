import pygame
from enemies.enemy import Enemy
from ui.tooltip import ToolTip
from towers.tower import Tower


class ToolTipTower(ToolTip):
    
    def __init__(self, entity: Tower, cell_size: int) -> None:
        super().__init__(entity, cell_size)
        
    def draw(self, window: pygame.surface.Surface) -> None:
        super().draw(window)
    
        if not self.hidden:
            entity_text = self.font.render(f"{self.entity}",
                                           True, self.entity.color)
            window.blit(entity_text, [self.pos_x + self.padding,
                                      self.pos_y + self.padding])
            object_text = self.font.render(f"Damage:   {round(self.entity.damage, 1)}",
                                           True, self.text_color)
            window.blit(object_text, [self.pos_x + self.padding,
                                      self.pos_y + self.padding * 6])
            speed_text = self.font.render(f"Speed:      {self.entity.speed} -> {self.entity.max_speed}",
                                           True, self.text_color)
            window.blit(speed_text, [self.pos_x + self.padding,
                                      self.pos_y + self.padding * 11])
            range_text = self.font.render(f"Range:      {self.entity.range}",
                                           True, self.text_color)
            window.blit(range_text, [self.pos_x + self.padding,
                                     self.pos_y + self.padding * 16])